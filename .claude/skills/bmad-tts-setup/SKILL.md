---
name: bmad-tts-setup
description: 'Installs or reconfigures the TTS Shared Bmad module — registers help entries, writes config, surfaces module metadata, and refreshes shared project rules into .claude/rules. Use when the user says "setup tts module", "install tts", "configure tts", "/bmad-tts-setup", or — for the focused rules-only refresh — "update rule", "cập nhật rule", or "/bmad-tts-setup --update-rules".'
---

# TTS Module Setup

## Overview

Installs or reconfigures the TTS Shared Bmad module into a project. This is the entry point for first-run installation and any subsequent reconfiguration — the module's capability skills (`/bmad-tts-design-story`, `/bmad-tts-design-story-pr`, `/bmad-tts-check-review`) depend on the config and help-CSV entries this skill writes. After module registration, the skill offers Bitbucket connection and (optional) Figma token + Sonar credentials paste so the user finishes first-time auth in a single flow.

Module identity (code, name, version) lives in `assets/module.yaml`. Capability registry lives in `assets/module-help.csv`. The full registration flow is described in `assets/module-setup.md`.

**Args:**
- `--update-rules` — **focused rules-only refresh.** Skip full setup; only sync `assets/templates/` from git and copy `.claude/rules/*` into the project (overwriting stale rules). Also triggered by the natural-language phrases `update rule` / `cập nhật rule`. See "Update Rules Mode" below.
- `--headless` / `-H` — non-interactive setup using sensible defaults.
- `--skip-bitbucket` — suppress the post-setup Bitbucket prompt.
- `--skip-figma` — suppress the post-setup Figma token prompt.
- `--skip-sonar` — suppress the post-setup Sonar credentials prompt.
- `--skip-template-sync` — suppress the pre-step that refreshes `assets/templates/` from the git source of truth (e.g. when offline).
- `--skip-templates` — suppress copying bundled templates (`.claude/...` files) into the project.
- `--overwrite-templates` — replace existing template files at the destination (otherwise existing files are skipped, never silently clobbered).
- `--template-sync-branch <name>` — pull templates from a non-default git branch (default `master`).

## Conventions

- Bare paths (e.g. `assets/module.yaml`) resolve from this skill's root.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{project-root}` written into config files is a **literal token** — never substitute it on disk.

## On Activation

### Mode Detection

Before anything else, decide which flow to run:

- **Update Rules mode** — the invocation contains `--update-rules`, OR the user's request is a rules-refresh phrase such as `update rule`, `cập nhật rule`, `update rules`, `refresh rules`, `cập nhật quy tắc`. Run the "Update Rules Mode" section below and HALT — do NOT run Steps 1–4.
- **Full setup mode** — anything else (`setup`, `install`, `configure`, a bare invocation, `--headless`). Run Steps 1–4 below.

## Update Rules Mode

A focused refresh that updates ONLY the shared project rules in `{project-root}/.claude/rules/` from the git source of truth. It does NOT touch config, help-CSV entries, starter files (`.claude/claude.md`), or Bitbucket — use full setup for those.

Honors `--skip-template-sync` and `--template-sync-branch <name>` (same semantics as full setup). `--headless` makes it non-interactive; it never blocks on input either way.

### Step R1: Sync templates from git

Same as full-setup Step 2 — refresh the skill's `assets/templates/` from the authoritative repo so the rules are current. Skip if `--skip-template-sync` was passed.

```bash
python3 scripts/sync-templates-from-git.py \
  --config-user "{project-root}/_bmad/config.user.yaml" \
  [--branch <name>]   # default master; override with --template-sync-branch
```

The script reads the bitbucket bearer token from `_bmad/config.user.yaml` (`tts.bitbucket.token`). If no token is found it exits non-zero. In that case:
- Surface the error in one line (e.g. `Không sync được rule từ git (chưa có bitbucket token). Chạy /bmad-tts-bitbucket-connect rồi thử lại.`).
- Continue to Step R2 anyway — it will copy whatever rules are already in `assets/templates/.claude/rules/`. If that directory is also empty, report that nothing was updated and HALT.

On success, log `files_synced_count`.

### Step R2: Copy rules into the project

Copy ONLY `.claude/rules/*`, always overwriting (rules are authoritative and track git). `--only-glob` restricts the copy to just the rules subtree, so no other template file is created or modified.

```bash
python3 scripts/copy-templates.py \
  --source assets/templates \
  --target {project-root} \
  --only-glob '.claude/rules/*' \
  --overwrite-glob '.claude/rules/*' \
  [--dry-run]   # only if --dry-run-templates was passed
```

Parse the JSON output and report to the user:
- `copied_count` rule files refreshed (list their destination paths so the user sees exactly which rules changed).
- `error_count` (surface each per-file error).

If `copied_count` is 0 and there were no errors, tell the user there were no rules to update (the synced `.claude/rules/` was empty). HALT cleanly after reporting — Update Rules mode does nothing else.

### Step 1: Module Registration

Load `assets/module-setup.md` and follow its registration flow end-to-end. That document covers: checking existing config, collecting user preferences (or applying defaults in headless mode), writing `{project-root}/_bmad/config.yaml`, `{project-root}/_bmad/config.user.yaml`, and merging entries into `{project-root}/_bmad/module-help.csv` via the helper scripts in `scripts/`.

After registration completes, display the `module_greeting` from `assets/module.yaml`. Then proceed to Step 2.

### Step 2: Sync Templates from Git (source of truth)

Refresh the skill's own `assets/templates/` directory from the authoritative git repo at `http://bitbucket.digital.vn/scm/vss/tts-shared-bmad.git` BEFORE Step 3 copies templates into the project. This guards against installer drift — `npx bmad-method install` has been observed to skip the `assets/templates/` subtree, leaving it empty at the skill destination.

The sync OVERWRITES the local `assets/templates/` (git is source of truth). Skip this step if `--skip-template-sync` was passed.

```bash
python3 scripts/sync-templates-from-git.py \
  --config-user "{project-root}/_bmad/config.user.yaml" \
  [--branch <name>]   # default master; override with --template-sync-branch
```

The script reads the bitbucket bearer token from `_bmad/config.user.yaml` (`tts.bitbucket.token`). If no token is found, the script exits non-zero. In that case:
- Surface the error in one line.
- Do NOT halt the whole flow — continue to Step 3. The user may be offline, on first-time setup without bitbucket credentials, or running before `/bmad-tts-bitbucket-connect`. Step 3 will copy whatever is already in `assets/templates/`.

On success, log `files_synced_count` from the JSON output.

### Step 3: Copy Bundled Templates

Mirror the `assets/templates/` tree into `{project-root}/`. Two policies apply:

- **Authoritative paths** (`.claude/rules/*`): ALWAYS overwritten from the freshly-synced templates — these encode shared project rules and must track the git source of truth (see Step 2). Local edits to `.claude/rules/*.md` will be replaced.
- **Starter paths** (everything else, e.g. `.claude/claude.md`): PRESERVED if they already exist — these are seed files that each project customizes (e.g. adding project-specific sections). The script never silently clobbers them.

Skip this step if `--skip-templates` was passed.

```bash
python3 scripts/copy-templates.py \
  --source assets/templates \
  --target {project-root} \
  --overwrite-glob '.claude/rules/*' \
  [--overwrite]   # only if --overwrite-templates was passed — forces EVERY file (incl. claude.md)
  [--dry-run]     # only in headless mode if --dry-run-templates was passed
```

The `--overwrite-glob` patterns are fnmatch globs against the source-relative path. Pass multiple `--overwrite-glob` to add more authoritative subtrees.

Parse the JSON output. Report to the user:
- `copied_count` files newly placed
- `skipped_count` files preserved (these existed already; show their paths so the user knows nothing was overwritten)
- `error_count` (per-file errors — surface each)

If `error_count > 0`, do NOT halt the whole flow — templates are nice-to-have, not blocking. Continue to Step 4.

In interactive mode, if any files were skipped, briefly mention `--overwrite-templates` as the way to force replacement.

### Step 4: Offer Bitbucket Connection

Inspect `{project-root}/_bmad/config.user.yaml` for an existing `tts.bitbucket` block.

- **If `tts.bitbucket` already configured:** confirm briefly (`Bitbucket already connected: workspace=<ws>, ****<last4>`). HALT cleanly — no further action.
- **If `tts.bitbucket` missing AND `--skip-bitbucket` was passed:** print a one-line reminder (`Bitbucket chưa setup. Chạy /bmad-tts-bitbucket-connect khi sẵn sàng paste token.`) and HALT.
- **If `tts.bitbucket` missing AND headless mode:** print the same reminder. Do NOT auto-invoke `/bmad-tts-bitbucket-connect` in headless — that skill needs `--auth-method` and a token, which CI won't have on the same invocation. HALT cleanly.
- **If `tts.bitbucket` missing AND interactive:** ASK the user:

  > Bitbucket credentials chưa setup. Các skill PR-related (`/bmad-tts-design-story-pr`, `/bmad-tts-check-review`) cần creds này.
  > Setup Bitbucket connection ngay bây giờ? `[y]es / [n]o (làm sau)`

  - `y` → invoke `/bmad-tts-bitbucket-connect` directly. The connect skill will run interactively and return — once it completes, the combined setup is done. HALT.
  - `n` → print the reminder and HALT cleanly.

In both branches, proceed to Step 5 once Bitbucket gate completes.

### Step 5: Offer Figma Token (optional)

Inspect `{project-root}/_bmad/config.user.yaml` for an existing `tts.figma.token` (any non-empty value).

- **If `tts.figma.token` already set:** confirm briefly (`Figma token already set: ****<last4>`). HALT cleanly — no further action.
- **If missing AND `--skip-figma` was passed:** print a one-line reminder (`Figma token chưa setup. Paste vào _bmad/config.user.yaml (key tts.figma.token) hoặc chạy /bmad-tts-setup lại khi sẵn sàng.`) and HALT.
- **If missing AND headless mode:** print the same reminder. HALT cleanly.
- **If missing AND interactive:** ASK the user:

  > Figma token chưa setup. **Optional** — chỉ cần khi muốn dùng skill `tts-figma-api` (list/get/export screens). Skip an toàn nếu workflow hiện tại không động đến Figma.
  > Setup Figma token ngay? `[y]es / [n]o (làm sau)`

  - `n` → print the reminder and HALT cleanly.
  - `y` → ASK user to paste the personal access token (must start with `figd_` — lấy tại https://www.figma.com/settings → *Personal access tokens*). Treat as **secret**: never echo the raw value back; only ever show `****<last4>`.

    Validate by hitting `GET https://api.figma.com/v1/files/I3jxlZZi9hUlSAC2YBis8j?depth=1` with header `X-Figma-Token: <pasted>`. Pass the token via env var, NOT inline curl arg (avoid shell-history exposure):

    ```bash
    FIGMA_KEY=<pasted> bash -c 'curl -s -o /dev/null -w "%{http_code}" -H "X-Figma-Token: $FIGMA_KEY" "https://api.figma.com/v1/files/I3jxlZZi9hUlSAC2YBis8j?depth=1"'
    ```

    Branch on the status code:
    - **200** — validated. Write entry to `config.user.yaml` (merge under `tts.figma.token`, preserve all other top-level keys). Confirm: `✅ Figma token saved: ****<last4>`.
    - **401 / 403** — token rejected (bad value, expired, or wrong scope). ASK `[r]etry / [a]bort`. On retry, loop back to paste step. On abort, HALT without writing.
    - **404** — default `file_key` not accessible by this token. Token may still be valid for a different file the user owns. ASK `[s]ave anyway (set tts.figma.file_key manually later) / [a]bort`.
    - **network error** — surface error, ASK `[r]etry / [s]ave without validation / [a]bort`.

### Step 6: Offer Sonar Credentials (optional)

Inspect `{project-root}/_bmad/config.user.yaml` for an existing `tts.sonar` block (with a non-empty `token`).

- **If `tts.sonar.token` already set:** confirm briefly (`Sonar already connected: <host_url>, project=<project_key>, ****<last4>`). HALT cleanly — no further action.
- **If missing AND `--skip-sonar` was passed:** print a one-line reminder (`Sonar chưa setup. Thêm block tts.sonar vào _bmad/config.user.yaml hoặc chạy /bmad-tts-setup lại khi sẵn sàng.`) and HALT.
- **If missing AND headless mode:** print the same reminder. HALT cleanly.
- **If missing AND interactive:** ASK the user:

  > Sonar credentials chưa setup. **Optional** — chỉ cần khi muốn dùng skill `vds-tts-fix-sonar` (pull + fix lỗi SonarQube). Skip an toàn nếu chưa cần.
  > Setup Sonar ngay? `[y]es / [n]o (làm sau)`

  - `n` → print the reminder and HALT cleanly.
  - `y` → collect the four `tts.sonar` fields (show defaults in brackets, ask together):
    - `host_url` [`http://sonar-10.digital.vn`]
    - `token` — Sonar **User Token** (lấy tại Sonar UI → *My Account › Security › Generate Tokens*; prefix `squ_` trên SonarQube 9.x+). Treat as **secret**: never echo the raw value; only ever show `****<last4>`.
    - `project_key` — the `componentKeys` value on the Sonar dashboard.
    - `default_branch` [`staging`].

    Validate the token against the host. Pass the token via env var, NOT inline curl arg (avoid shell-history exposure):

    ```bash
    SONAR_TOKEN=<pasted> bash -c 'curl -s -o /dev/null -w "%{http_code}" -u "$SONAR_TOKEN:" "<host_url>/api/authentication/validate"'
    ```

    Branch on the status code (the endpoint returns 200 with `{"valid":true|false}`; capture the body too if you need to distinguish):
    - **200 + `valid:true`** — validated. Write the `tts.sonar` block to `config.user.yaml` (merge under `tts.sonar`, preserve all other top-level keys). Confirm: `✅ Sonar saved: <host_url>, project=<project_key>, ****<last4>`.
    - **200 + `valid:false` / 401** — token rejected (bad value, expired, or revoked). ASK `[r]etry / [a]bort`. On retry, loop back to the collect step. On abort, HALT without writing.
    - **404 / connection refused** — `host_url` likely wrong or unreachable. ASK `[e]dit host / [s]ave anyway / [a]bort`.
    - **network error** — surface error, ASK `[r]etry / [s]ave without validation / [a]bort`.

This skill's job is done after Step 6. Do NOT auto-invoke design or PR workflows — the user calls them explicitly when ready.

## Headless Mode

If invoked with `--headless` or `-H`:

- Apply all defaults from `assets/module.yaml` (no interactive prompts).
- Display the confirmation summary and module greeting.
- Step 2 (template sync): run non-interactively. If no token is available, surface the error and continue — do NOT block headless installs on missing bitbucket creds. Honor `--skip-template-sync` and `--template-sync-branch`.
- Step 3 (templates): copy without prompting; skip-existing default still protects user content. Honor `--overwrite-templates` and `--skip-templates`.
- Step 4 (Bitbucket): skip the interactive prompt — print the reminder line if creds are missing.
- Step 5 (Figma): skip the interactive prompt — print the reminder line if token is missing.
- Step 6 (Sonar): skip the interactive prompt — print the reminder line if creds are missing.
- Exit cleanly — never block on user input.
