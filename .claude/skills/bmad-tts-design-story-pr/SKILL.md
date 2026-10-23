---
name: bmad-tts-design-story-pr
description: 'Creates a Bitbucket PR from features/{story}-dev into features/{story} for techlead/SA review of a story''s detail design. Use when the user says "create design PR", "design story PR", or "/bmad-tts-design-story-pr".'
---

# Detail Design PR Workflow (Bitbucket)

**Goal:** After a story's detail design is approved, open a Bitbucket PR from `features/{story_key}-dev` into the story's integration branch `features/{story_key}` with the right techlead/SA reviewers, so the design gets a human gate before any deeper implementation work continues.

**Your Role:** Release engineer turning approved design into a clean review-ready PR — title, body, head/base branches, reviewers all derived from project conventions, no manual fiddling.

- Communicate in `{communication_language}`.
- The PR body uses `{document_output_language}` (matches the design doc's language).
- Treat the design doc and story file as authoritative; do not modify them.
- Never push directly to the story's integration branch (`features/{story_key}`), `staging`, `release`, or `master`. Always via PR.
- Never use `--no-verify`, `--force`, or skip pre-commit hooks. If a hook fails, halt and surface the error.
- Bitbucket auth comes from `{project-root}/_bmad/config.user.yaml` (`tts.bitbucket.*`). Pass everything to `bb-cli.py` via env vars — NEVER as CLI args (avoids shell-history exposure):
  `BB_API_BASE_URL`, `BB_API_FLAVOR`, `BB_AUTH_METHOD`, `BB_USERNAME`, `BB_APP_PASSWORD`, `BB_TOKEN`, `BB_WORKSPACE`, `BB_REPOSITORY`.
  Supports both **Bitbucket Cloud** (reviewers as UUIDs) and **Bitbucket Server/DC** (reviewers as usernames). The bb-cli helper auto-detects flavor from the API URL. Mask any token in user-visible output.

## Conventions

- Bare paths (e.g. `references/template.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`

If the script fails, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying structural merge rules:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code`/`id` replace matching entries and append new ones, all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context for the run. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Config

Load config from `{project-root}/_bmad/config.yaml`/`config.user.yaml` (root level and `bmm` section) — fall back to `{project-root}/_bmad/bmm/config.yaml` if present. If the `tts` section is missing, halt with: `TTS module is not registered. Run /bmad-tts-setup first to install module config and help entries.` If only the `bmm` section is missing (but `tts` is present), continue with sensible defaults.

Resolve: `project_name`, `user_name`, `communication_language`, `document_output_language`, `implementation_artifacts`, `planning_artifacts`, `date` (system-current).

### Step 5: Greet the User

Greet `{user_name}` in `{communication_language}`. State that this workflow opens a design-review PR for techlead/SA, mention whether headless mode is active, and confirm the auto-discovered story (Step 1 of execution) before proceeding.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Headless Mode

If invoked with `--headless` or `-H`:

- Do not pause for confirmation between steps.
- `--team <team-code>` MUST be provided as an arg (or in `{workflow.headless_defaults}`). Halt with a clear error if missing — never guess team.
- Skip the user-approval gate (Step 6). Apply preflight findings automatically; abort hard if any blocking precondition fails (including missing base branch — no interactive fallback in headless).

## Args

- `--story <path>` — explicit story file path (skips auto-discovery).
- `--team <code>` — team code. Determines reviewers via `{workflow.reviewers_by_team}`.
- `--base <branch>` — override the auto-derived base branch (default: `features/{{story_key}}`). Useful when team uses a non-standard integration branch name for a story.
- `--update` — if a PR already exists from the head branch, push the new commit and refresh PR body instead of failing.
- `-H` / `--headless` — non-interactive mode (see above).

## Paths

- `story_file` = explicit `--story` value if user-provided; otherwise auto-discovered from `sprint_status`
- `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`
- `pr_body_template` = `{workflow.pr_body_template}` (default: `references/pr-body-template.md`)
- `pr_body_output` = `{implementation_artifacts}/{{story_key}}-design-pr-body.md` (transient, used as `--body-file` then deleted)
- `bb_cli` = `{workflow.bb_cli_path}` (default: `{project-root}/skills/bmad-tts-bitbucket-connect/scripts/bb-cli.py`)
- `bitbucket_creds` = `tts.bitbucket` block in `{project-root}/_bmad/config.user.yaml`

## Execution

<workflow>

<step n="1" goal="Find target story + design doc" tag="sprint-status">
  <check if="{{story_path}} provided by user">
    <action>Read the story file directly. Extract `story_key`, `epic_num`, `story_num`, `story_title` from filename `{{epic_num}}-{{story_num}}-{{story_title}}.md` and metadata.</action>
    <goto anchor="loaded" />
  </check>

  <action>Read the FULL `{sprint_status}` file from start to end, preserving order.</action>
  <action>Find the FIRST `development_status` entry whose key matches `number-number-name` (not `epic-X` or retrospective) AND value equals `designed`.</action>

  <check if="no `designed` story found">
    <output>📋 Không tìm thấy story nào ở trạng thái `designed` trong sprint-status.yaml.

      Lựa chọn:
      1. Chạy `/bmad-tts-design-story` trước để có design doc đã được approve
      2. Cung cấp đường dẫn story bằng `--story <path>`
      3. Thoát
    </output>
    <ask>Chọn [1], [2] (cung cấp path), hoặc [q]:</ask>
    <action>Honor the user's choice. For [1] or [q], HALT.</action>
  </check>

  <action>Extract `epic_num`, `story_num`, `story_title`. Set `story_key`. Locate the matching story file in `{implementation_artifacts}` and read it COMPLETELY.</action>

  <anchor id="loaded" />
  <action>Verify story Status is `designed`. If not, warn the user (`Story is in state X, expected 'designed'`) and ASK whether to proceed anyway or abort.</action>
  <action>Locate the `**Design Doc:**` line in Dev Notes. Extract its path. If missing, halt with `Story has no Design Doc reference — run /bmad-tts-design-story first.`</action>
  <action>Read the design doc completely. Identify: AC summary, file changes table, breaking-changes section (if present), test plan section, open questions.</action>
</step>

<step n="2" goal="Resolve branches and validate environment (git + Bitbucket)">
  <action>Verify the project is a git repository. Halt with a clear error if not.</action>

  <action>Load Bitbucket credentials from `{bitbucket_creds}` (the `tts.bitbucket` block in config.user.yaml). Required fields: `api_base_url`, `api_flavor`, `auth_method`, `workspace`, `repository`. Plus secrets: `username`+`app_password` (cloud/app-password) OR `token` (cloud/access-token OR server/bearer).
    If missing or incomplete, halt with: `Bitbucket connection not configured. Run /bmad-tts-bitbucket-connect first.`
    Build the env-var bundle for `bb-cli`:
      `BB_API_BASE_URL=<url>`, `BB_API_FLAVOR=<cloud|server>`,
      `BB_AUTH_METHOD=<auth_method>`, `BB_WORKSPACE=<ws or projectKey>`, `BB_REPOSITORY=<repo>`,
      plus `BB_USERNAME`+`BB_APP_PASSWORD` (cloud app-password) OR `BB_TOKEN` (cloud access-token OR server bearer).
    Pass via env in EVERY `bb-cli` invocation in this workflow. Never echo secrets in tool output.
  </action>

  <action>Resolve branch names by substituting `{{story_key}}` into:
    - `head_branch` = `{workflow.head_branch_pattern}` (default `features/{{story_key}}-dev`)
    - `base_branch` = `--base` arg if provided, else `{workflow.base_branch_pattern}` (default `features/{{story_key}}`)
  </action>

  <action>Inspect git working tree. Allowed dirty paths: the design doc and the story file (the two artifacts produced by the design workflow). Anything else dirty:
    - In headless mode: HALT with `Working tree dirty outside design artifacts: <files>`.
    - Interactive: present the dirty file list and ASK whether to abort or proceed (user accepts responsibility).
  </action>

  <action>Run `git fetch --all --prune` to ensure remote branch info is current.</action>

  <action>Verify the **base branch** exists on the remote (`git ls-remote --exit-code --heads origin {{base_branch}}`). If missing:
    - **Headless**: HALT with `Base branch {{base_branch}} not found on origin. Team-lead must create it before this PR can be opened.`
    - **Interactive**: present the situation clearly and offer:
      `[1] Cung cấp base branch khác (nhập tên thủ công)`
      `[2] Abort — chờ team-lead tạo nhánh {{base_branch}}`
      For [1], capture the new value, re-verify it exists on remote, and proceed (or loop on missing). For [2], HALT cleanly with no git side effects.
    Do NOT auto-create the base branch — it is a team-shared integration branch and must be created intentionally.
  </action>

  <action>Check whether a PR already exists from `{{head_branch}}` into `{{base_branch}}` by running `bb-cli` with credentials in env:
    ```bash
    BB_API_BASE_URL=... BB_API_FLAVOR=... BB_AUTH_METHOD=... BB_WORKSPACE=... BB_REPOSITORY=... [BB_TOKEN=... | BB_USERNAME=... BB_APP_PASSWORD=...] \
      python3 {bb_cli} pr-list --source {{head_branch}} --dest {{base_branch}} --state OPEN
    ```
    Note: for Server flavor, `pr-list` filters by `dest` server-side and `source` client-side — both work transparently. The returned `prs[].id` is the Bitbucket PR ID needed for `pr-edit` later.
    Parse the JSON output. If `count > 0`, capture the first PR's `id` and `url` — handled in Step 6 (existing-PR branch).
  </action>
</step>

<step n="3" goal="Gather team + breaking changes">
  <action>Resolve `team`:
    - If provided via `--team` arg, use it.
    - Otherwise (interactive only) ask the user, presenting `{workflow.teams}` as choices. If the list is empty, accept free-form input and warn if the team has no entry in `{workflow.reviewers_by_team}`.
    - Headless without `--team` (and no `headless_defaults.team`): HALT with `--team is required in headless mode.`
  </action>

  <action>Confirm breaking changes:
    - Read the design doc's "Breaking Changes" section if present.
    - Present the summary to the user and ASK to confirm or amend (interactive). In headless: take the design doc content as-is.
    - If no breaking-changes section exists, ASK (interactive) whether this PR introduces breaking changes; if yes, capture a 1-3 line summary. Headless: assume `none`.
  </action>

  <action>Look up reviewers via `{workflow.reviewers_by_team}[team]`. Fall back to `reviewers_by_team.default` if the team has no explicit entry. If both missing, halt with the team code and a hint to update customize.toml.</action>

  <action>Resolve each reviewer entry to the right ID format for the active flavor:
    - **Cloud** expects UUID. Entries already shaped as `{a1b2c3d4-...}` (curly-brace UUIDs) are used as-is. Otherwise treat as nickname and look up via:
      ```bash
      BB_API_BASE_URL=... BB_API_FLAVOR=... BB_AUTH_METHOD=... [creds env] BB_WORKSPACE=... \
        python3 {bb_cli} user-lookup --query <nickname>
      ```
      Use `matches[0].id` (the UUID).
    - **Server** expects username (`name`). Entries pass through verbatim — no lookup needed unless you want to verify existence (optional). For verification, run `bb-cli user-lookup --query <name>` and check `matches[]` is non-empty.
    - If lookup returns zero matches: halt with `Reviewer '<entry>' not found in workspace '<ws>'. Update reviewers_by_team in customize.toml.`. If multiple ambiguous matches in Cloud, prefer exact `nickname` then ask user to disambiguate.
    - Cache resolution in memory for this run; do NOT persist (workspace memberships change).
  </action>

  <action>Set `pr_title` from `{workflow.pr_title_template}` (default `[Design] {{story_key}} — {{story_title}}`).</action>
  <action>Set `commit_message` from `{workflow.commit_message_template}` (default `design({{story_key}}): {{story_title}}`).</action>
</step>

<step n="4" goal="Compose PR body">
  <action>Load the PR body template from `{pr_body_template}`. Substitute every placeholder using values gathered so far:
    - `{{story_key}}`, `{{story_title}}`, `{{epic_num}}`, `{{story_num}}`
    - `{{design_doc_path}}` — repo-relative path to the design doc
    - `{{ac_summary}}` — bullet list distilled from the story's Acceptance Criteria
    - `{{breaking_changes}}` — the confirmed summary, or the literal `Không có` / `None` if none
    - `{{test_plan_summary}}` — short paragraph from design doc's Test Plan section
    - `{{open_questions}}` — bullet list from design doc's Open Questions; literal `Không có` if empty
    - `{{base_branch}}`, `{{head_branch}}`, `{{team}}`, `{{reviewers}}` (comma-separated Bitbucket nicknames — display form, NOT UUIDs)
  </action>
  <action>Write the rendered body to `{pr_body_output}`. This file is transient — it'll be removed in Step 6 after `bb-cli pr-create` consumes it.</action>
</step>

<step n="5" goal="Confirmation gate">
  <check if="headless mode">
    <action>Skip this step.</action>
    <goto step="6" />
  </check>

  <action>Present a concise summary to {user_name}:
    - `{{head_branch}}` → `{{base_branch}}`
    - Reviewers (with `@`)
    - PR title
    - First ~10 lines of the rendered PR body + `(see {pr_body_output} for full body)`
    - Whether an existing PR will be updated or a new one created
  </action>
  <ask>[c]reate / [e]dit body / [r]e-pick team / [a]bort</ask>

  <check if="user chose [e]">
    <action>Open `{pr_body_output}` and let the user dictate edits (or accept inline edits via the conversation). Re-render and re-present.</action>
  </check>

  <check if="user chose [r]">
    <action>Re-enter Step 3 (Gather team + breaking changes), keep the rest.</action>
  </check>

  <check if="user chose [a]">
    <action>Delete `{pr_body_output}`. Leave git state untouched. HALT.</action>
  </check>
</step>

<step n="6" goal="Execute git + Bitbucket API operations">
  <action>Switch to head branch:
    - If `{{head_branch}}` exists locally: `git switch {{head_branch}}`.
    - Else if it exists on remote: `git switch --track origin/{{head_branch}}`.
    - Otherwise: create it FROM the base branch — `git switch -c {{head_branch}} origin/{{base_branch}}`. This ensures the dev branch starts cleanly off the integration branch, not off whatever the user happened to have checked out.
  </action>

  <action>Stage ONLY the design doc and the story file (paths captured in Step 1). Run `git commit -m "{{commit_message}}"`. If the commit produces no changes (e.g. design doc was already committed on this branch), proceed without erroring.</action>
  <action>If a pre-commit hook fails: HALT, surface the failure to the user, and instruct them to fix the issue and re-run. Never use `--no-verify`.</action>

  <action>Push: `git push -u origin {{head_branch}}`. If the remote has diverged, halt with the conflict and instruct the user to reconcile manually — do not force-push.</action>

  <check if="existing PR detected in Step 2">
    <check if="--update flag passed (or interactive user chose update)">
      <action>Edit the existing PR via `bb-cli` (creds in env, repeat `--reviewer <UUID>` for each resolved reviewer):
        ```bash
        BB_API_BASE_URL=... BB_API_FLAVOR=... BB_AUTH_METHOD=... [creds env] BB_WORKSPACE=... BB_REPOSITORY=... \
          python3 {bb_cli} pr-edit --pr-id <existing_pr_id> \
            --body-file {pr_body_output} \
            --reviewer <uuid-1> --reviewer <uuid-2> ...
        ```
        Parse the JSON `url` field. The push above already updated the PR's commits — this call refreshes body + reviewer list.
      </action>
    </check>
    <check if="not updating">
      <action>HALT with the existing PR URL and `Pass --update to refresh, or decline the existing PR first.`</action>
    </check>
  </check>

  <check if="no existing PR">
    <action>Create the PR via `bb-cli` (creds in env, repeat `--reviewer <UUID>` for each resolved reviewer):
      ```bash
      BB_API_BASE_URL=... BB_API_FLAVOR=... BB_AUTH_METHOD=... [creds env] BB_WORKSPACE=... BB_REPOSITORY=... \
        python3 {bb_cli} pr-create \
          --source {{head_branch}} --dest {{base_branch}} \
          --title "{{pr_title}}" --body-file {pr_body_output} \
          --reviewer <uuid-1> --reviewer <uuid-2> ...
      ```
      Parse the JSON `id` and `url` fields. If status != ok, surface the upstream error (HTTP status + Bitbucket message) clearly — common: 401 (bad creds — re-run /bmad-tts-bitbucket-connect), 400 (branch mismatch), 403 (token lacks repo write scope).
    </action>
  </check>

  <action>Delete `{pr_body_output}` (transient).</action>
</step>

<step n="7" goal="Update sprint status and finalize" tag="sprint-status">
  <check if="{sprint_status} file exists">
    <action>Load the FULL `{sprint_status}` file. Find `development_status[{{story_key}}]`. Verify current value is `designed`. Update to `design-pr-open`. Update `last_updated` to today.</action>
    <action>If the STATUS DEFINITIONS block does not list `design-pr-open`, append: `design-pr-open: Detail design PR opened for techlead/SA review` (preserve formatting).</action>
    <action>If the STATUS DEFINITIONS block does not list `design-approved`, also append: `design-approved: Detail design PR merged by techlead/SA; story is ready for implementation` (preserve formatting). This pre-registers the next state so the post-merge transition feels native.</action>
    <action>Save the file, preserving ALL comments and STATUS DEFINITIONS.</action>
  </check>

  <output>✅ PR design đã được tạo, {user_name}.

    - Story: {{story_key}}
    - PR: {{pr_url}}
    - {{head_branch}} → {{base_branch}}
    - Team: {{team}} · Reviewers: {{reviewers}}
    - Sprint status: design-pr-open

    Vòng đời tiếp theo:
      1. Techlead/SA review PR. Nếu yêu cầu chỉnh sửa, dev push thêm commit lên `{{head_branch}}` — PR auto-update.
      2. Khi PR được MERGE vào `{{base_branch}}`, chạy `/bmad-tts-check-review` để auto-transition
         sprint-status: design-pr-open → design-approved. (Hoặc sửa thủ công sprint-status.yaml.)
      3. Chạy `/bmad-dev-story` để bắt đầu implementation. dev-story chỉ pick up khi status = `design-approved`.
  </output>

  <action>Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete` — if non-empty, follow it as the final terminal instruction before exiting.</action>
</step>

</workflow>
