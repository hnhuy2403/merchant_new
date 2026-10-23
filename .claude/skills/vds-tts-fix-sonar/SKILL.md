---
name: vds-tts-fix-sonar
description: Query SonarQube findings for the current project + walk the agent through fixing them in priority order (BLOCKER → CRITICAL → MAJOR → MINOR → INFO). Reads credentials from `_bmad/config.user.yaml` (gitignored, never committed). Use when the user says "fix sonar", "sửa lỗi sonar", "scan sonar", or "/vds-tts-fix-sonar".
---

# Fix Sonar Workflow

**Goal:** Pull open issues from SonarQube for `{project_key}@{branch}`, group them by severity + rule, then implement fixes in the codebase one batch at a time. Each fix references the exact Sonar rule + file:line so the dev can trace back.

**Your Role:** Code-quality remediator. Read each issue, understand the rule, apply the smallest possible fix that satisfies the rule without breaking behavior. Surface design-level concerns (e.g. "Sonar wants this method split but it would hurt readability") for user judgment rather than silently doing them.

## Conventions

- Bare paths (e.g. `scripts/sonar-cli.py`) resolve from this skill's root.
- `{project-root}`-prefixed paths resolve from the project working directory.
- All Sonar API calls go through `scripts/sonar-cli.py` — never embed token inline in bash, never echo it. Pass credentials via env vars only.

## Pre-flight

Read `{project-root}/_bmad/config.user.yaml` and verify the `tts.sonar` block exists with:
- `host_url` (e.g. `http://sonar-10.digital.vn`)
- `token` (Sonar user token, prefix `squ_` for SonarQube 9.x+)
- `project_key` (the Sonar componentKeys value — usually the artifact / repo slug)
- `default_branch` (e.g. `staging`)

**If `tts.sonar` is missing,** halt with:
```
Sonar credentials chưa setup. Thêm block `tts.sonar` vào _bmad/config.user.yaml (file gitignored):

tts:
  sonar:
    host_url: http://sonar-10.digital.vn
    token: <Sonar User Token — User Account > Security > Generate Tokens>
    project_key: <componentKeys trên Sonar dashboard>
    default_branch: staging

Sau đó re-run /vds-tts-fix-sonar.
```

**If `tts.sonar.token` does NOT start with `squ_` and is NOT a valid base64-like string,** warn the user but continue (let API call surface the actual auth error).

## Args

- `--severity <list>` — comma-separated, restrict to severities. Default: `BLOCKER,CRITICAL,MAJOR`. Other values: `MINOR`, `INFO`. Use `--severity all` to include everything.
- `--rule <ruleKey>` — restrict to one Sonar rule key (e.g. `java:S1192`).
- `--file <substring>` — restrict to files whose path contains substring (vd `LabelService`).
- `--branch <name>` — override `default_branch` from config.
- `--max <n>` — cap the number of issues to fetch (default 200).
- `--dry-run` — list what would change without writing.
- `--no-fix` — only fetch + display, do not propose fixes (useful for a first triage pass).
- `-H` / `--headless` — non-interactive: apply fixes for all `safe` rules (those listed in `references/safe-rules.txt`) without confirmation; skip rules that require judgment.

## Workflow

### Step 1: Validate auth + project access

Run:
```bash
SONAR_HOST_URL=... SONAR_TOKEN=... python3 scripts/sonar-cli.py validate
```

Expect `{"status":"ok","valid":true}`. If `valid:false`, halt with the API error message.

### Step 2: Fetch issues

Run:
```bash
SONAR_HOST_URL=... SONAR_TOKEN=... SONAR_PROJECT_KEY=... python3 scripts/sonar-cli.py issues \
  --branch <branch> \
  --severities <severities> \
  [--rule <ruleKey>] \
  [--file <substring>] \
  --max <max>
```

Parse JSON. Each issue carries: `key`, `rule`, `severity`, `type` (BUG/VULNERABILITY/CODE_SMELL/SECURITY_HOTSPOT), `component` (file path), `line`, `message`, `effort`, `debt`, `tags`.

### Step 3: Group + present summary

Group issues by `(severity, rule, component)`. Present a table:

```
| Severity | Type | Rule | Count | Files (top 3) |
|----------|------|------|-------|---------------|
| BLOCKER  | BUG  | java:S2189 | 1 | LabelService.java |
| MAJOR    | CODE_SMELL | java:S1192 | 5 | CategoryService.java, LabelService.java, ... |
```

Show total count + estimated effort (sum of `debt` minutes, format as `Xh Ym`).

### Step 4: Fix in priority order

For each group (BLOCKER first, then CRITICAL, MAJOR, MINOR), for each issue:

1. Fetch the rule description: `python3 scripts/sonar-cli.py rule --key <ruleKey>` — returns title + description.
2. Read the file at `{component}` around `{line}` (±15 lines).
3. Decide fix strategy:
   - **Safe auto-fix** (rule listed in `references/safe-rules.txt`): apply directly.
   - **Judgment required** (e.g. `java:S3776` cognitive complexity, `java:S138` long method): show user the issue + proposed fix, ask `[a]pply / [s]kip / [m]odify`.
   - **False positive / won't-fix**: ask user, if confirmed, mark on Sonar via `/api/issues/do_transition` (out of scope of this skill — note for manual action).
4. Apply the fix via the standard Edit tool. KEEP behavior; do NOT refactor beyond what the rule requires.
5. Track per-issue outcome: `fixed`, `skipped`, `flagged-judgment`, `error`.

**Critical guardrails:**
- KHÔNG sửa file ngoài `code/vss-catalog-service/src/`. Test files only if Sonar issue specifically targets them.
- KHÔNG bỏ business logic để "đạt" rule. Nếu rule conflict với product behavior, surface to user.
- KHÔNG generate test file mới (Architecture Rule #19 — test do QC owner đảm nhiệm).
- KHÔNG đụng vào migration đã apply (V2/V3/...) — chỉ touch migration MỚI nếu Sonar có rule SQL.

### Step 5: Compile + validate

After all fixes (or after each batch of 10 in headless mode):
1. Run `./mvnw -q -DskipTests compile` to verify Java code still compiles.
2. If compile fails: revert the last batch, mark those issues as `error`, halt.
3. Run quick smoke if available (Spring Boot start? skip if too slow).

### Step 6: Report

Output final summary:
```
✅ Fixed: N issues
⏭️ Skipped (user choice): M
⚠️ Flagged for judgment: K
❌ Errors (compile fail): E

Files modified: <list>

Next step: trigger Sonar re-scan via CI to confirm issues closed.
```

If `E > 0`, exit non-zero in headless.

## Headless Mode

If invoked with `--headless`:
- Apply fixes for all safe rules without confirmation.
- Skip rules requiring judgment (don't ask, just flag for later).
- Exit non-zero if any compile fail.
- Never block on user input.

## Notes on token security

- Token lưu trong `_bmad/config.user.yaml` — file đã được `.gitignore` cover (`**/config.user.yaml`).
- Script `sonar-cli.py` nhận token qua env var `SONAR_TOKEN`, KHÔNG truyền qua CLI args (tránh leak vào `ps`/process list).
- Khi user rotate token: chỉ cần update field `token` trong config.user.yaml, không cần re-setup gì khác.
- Nếu nghi ngờ token bị leak: revoke trên SonarQube UI (User > Security > Tokens) + rotate ngay.
