---
name: bmad-tts-check-review
description: 'Checks merge/review status of Bitbucket PRs for stories awaiting review (design or code), then transitions sprint-status states accordingly. Use when the user says "check review", "check pr status", "transition merged stories", or "/bmad-tts-check-review".'
---

# Check Review & Transition Workflow (Bitbucket)

**Goal:** Look up the Bitbucket PR status for each story in a "PR-pending" state, surface reviewer comments (and help the dev address them), then automatically advance sprint-status when the PR is approved and merged. Generic across review phases — currently configured for **detail-design review** (`design-pr-open` → `design-approved`); extend with additional phases by adding entries to `{workflow.transitions}`.

**Your Role:** Pipeline gatekeeper that closes the loop between Bitbucket PR lifecycle and the project's sprint-status state machine — so dev/QA always see an accurate "what's ready to pick up" picture without hand-editing YAML.

- Communicate in `{communication_language}`.
- Read-only on Bitbucket (`bb-cli pr-list`); write-only on `sprint-status.yaml`.
- Never auto-revert a story's state to an earlier state without surfacing it to the user — closed-unmerged PRs are usually a real signal worth a confirmation.
- Bitbucket auth comes from `{project-root}/_bmad/config.user.yaml` (`tts.bitbucket.*`). Pass everything to `bb-cli.py` via env vars — NEVER as CLI args:
  `BB_API_BASE_URL`, `BB_API_FLAVOR`, `BB_AUTH_METHOD`, `BB_USERNAME`, `BB_APP_PASSWORD`, `BB_TOKEN`, `BB_WORKSPACE`, `BB_REPOSITORY`.
  Supports both Cloud and Server/DC flavors transparently — `bb-cli` auto-detects from the URL.

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

Load config from `{project-root}/_bmad/config.yaml`/`config.user.yaml` (root level and `bmm` section). Halt with `TTS module is not registered. Run /bmad-tts-setup first.` if the `tts` section is missing.

Resolve: `project_name`, `user_name`, `communication_language`, `implementation_artifacts`, `date` (system-current).

### Step 5: Greet the User

Greet `{user_name}` in `{communication_language}`. Briefly state what this skill does (check PR merge/review state for stories awaiting review; transition states accordingly), mention headless mode if active, and indicate the candidate stories you'll inspect (preview from Step 1 of execution).

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Headless Mode

If invoked with `--headless` or `-H`:

- Do not pause for confirmation between steps.
- Apply all transitions where the PR is unambiguously merged.
- For closed-unmerged PRs, apply the configured `on_closed_unmerged` action ONLY if it equals `revert` AND the transition entry has `auto_revert_in_headless = true`. Otherwise, leave the state unchanged and emit a warning in the report.
- For open PRs, never modify state — just record the review status.
- Output a structured report (table) at the end; non-zero exit if any story had a hard error (PR-not-found for a candidate story, or Bitbucket API failure).

## Args

- `--story <key>` — restrict to a single story (key like `3-2-add-voice-cloning`). Skips auto-discovery.
- `--transition <id>` — restrict to one transition entry by `id` (e.g. `design-review`). Useful when you only want to check one phase.
- `--dry-run` — report what would change without writing to `sprint-status.yaml`.
- `-H` / `--headless` — non-interactive mode (see above).

## Paths

- `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`
- `bb_cli` = `{workflow.bb_cli_path}` (default: `{project-root}/skills/bmad-tts-bitbucket-connect/scripts/bb-cli.py`)
- `bitbucket_creds` = `tts.bitbucket` block in `{project-root}/_bmad/config.user.yaml`

## Execution

<workflow>

<step n="1" goal="Discover candidate stories" tag="sprint-status">
  <action>Load Bitbucket credentials from `{bitbucket_creds}` (the `tts.bitbucket` block in config.user.yaml). Required: `api_base_url`, `api_flavor`, `auth_method`, `workspace`, `repository`, plus secrets per auth method. If missing, halt with: `Bitbucket connection not configured. Run /bmad-tts-bitbucket-connect first.`
    Build the env-var bundle for `bb-cli`: `BB_API_BASE_URL`, `BB_API_FLAVOR`, `BB_AUTH_METHOD`, `BB_WORKSPACE`, `BB_REPOSITORY`, plus `BB_USERNAME`+`BB_APP_PASSWORD` (cloud app-password) OR `BB_TOKEN` (cloud access-token OR server bearer). Use this bundle for every `bb-cli` call below — never echo secrets.
  </action>

  <action>Read the FULL `{sprint_status}` file from start to end, preserving order.</action>

  <action>Build the candidate list: iterate `development_status` entries whose key matches `number-number-name` (skip `epic-X` and retrospectives) AND whose value matches some `from_state` in `{workflow.transitions}`. Each candidate carries: `story_key`, current `state`, and the matched `transition` entry.</action>

  <check if="--story arg provided">
    <action>Filter the candidate list to just that `story_key`. If it has no matching transition, halt with `Story <key> is in state <state>; no configured transition matches.`</action>
  </check>

  <check if="--transition arg provided">
    <action>Filter the candidate list to entries matching only that transition `id`.</action>
  </check>

  <check if="candidate list is empty">
    <output>Không có story nào ở state cần kiểm tra (`{from_states}`). Sprint-status đã sạch.</output>
    <action>HALT cleanly with exit 0.</action>
  </check>

  <action>Run `git fetch --all --prune` once to ensure remote state is current.</action>
</step>

<step n="2" goal="Look up PR state for each candidate (Bitbucket)">
  <action>For each candidate, substitute `{{story_key}}` into the transition's `head_pattern` and `base_pattern` to get `head` and `base`.</action>

  <action>Query Bitbucket for the most relevant PR via `bb-cli` (creds in env, never CLI args):
    ```bash
    BB_API_BASE_URL=... BB_API_FLAVOR=... BB_AUTH_METHOD=... [creds env] BB_WORKSPACE=... BB_REPOSITORY=... \
      python3 {bb_cli} pr-list --source <head> --dest <base> --state all --limit 5
    ```
    Parse JSON `prs[]`. Each entry already carries the normalized `state` (`open`/`merged`/`closed_unmerged`), `merged_at`, `url`, and `review_summary` (`approvals`, `changes_requested`, `pending_reviewers`).
    Selection rule: prefer `state == merged` (most recent `merged_at`); else prefer `open` (most recent); else most recent `closed_unmerged`. If `prs[]` is empty, mark `not_found`.
  </action>

  <action>Record per candidate:
    - `pr_id`, `pr_url`
    - `pr_state` ∈ `{merged, open, closed_unmerged, not_found}`
    - `review_summary` (for open PRs): `approvals`/`changes_requested`/`pending_reviewers` counts
    - `review_status` (derived for display): `APPROVED` if `approvals > 0` and `changes_requested == 0`; `CHANGES_REQUESTED` if `changes_requested > 0`; `REVIEW_PENDING` otherwise.
    - `merged_at` (ISO timestamp, if merged)
    - `target_state` (computed from the matched transition's `on_merged` / `on_closed_unmerged`)
  </action>

  <check if="pr_state is not_found">
    <action>Mark this candidate as `error` with reason `No PR found for {{head}} → {{base}} on workspace/repo {{workspace}}/{{repository}}`. Do NOT halt the whole run — continue with other candidates and surface this in the final report.</action>
  </check>
</step>

<step n="2b" goal="Fetch and display review comments for open PRs">

  <check if="any candidate has pr_state == open AND review_summary.changes_requested > 0">
    <action>For each such candidate, fetch comments via bb-cli (creds in env):
      ```bash
      BB_... python3 {bb_cli} pr-comments --pr-id <pr_id> --unresolved-only
      ```
      Parse `comments[]`. Each comment has: `id`, `author`, `body`, `inline` (path + line, or null), `resolved`.
    </action>

    <action>Display a comment list for each story, grouped by file (inline comments first, then general):

      **📋 Review comments — {{story_key}} (PR #{{pr_id}})**

      **[Inline — `src/foo/Bar.java:42`]**
      > @techlead: "Thiếu null check ở đây — nếu input null sẽ NPE."

      **[General]**
      > @sa_reviewer: "Cần bổ sung sequence diagram cho luồng retry."

      For each comment, also show:
      - Comment ID (for tracking)
      - Author + timestamp
    </action>

    <action>Ask the dev — skip in headless mode:
      > Có **{{unresolved_count}}** comment chưa resolve. Bạn muốn:
      > - **[R]** Review từng comment (tôi sẽ giúp bạn address)
      > - **[S]** Bỏ qua, chỉ xem trạng thái PR
    </action>
  </check>

  <check if="any candidate has pr_state == open AND review_summary.changes_requested == 0 AND review_summary.approvals == 0">
    <action>Display brief note: "PR đang chờ reviewer — chưa có comment nào. Quay lại sau khi reviewer feedback." No comment fetch needed.</action>
  </check>

</step>

<step n="2c" goal="Help dev address comments interactively">

  <check if="dev chose [S] OR headless_mode OR no unresolved comments">
    <goto step="3" />
  </check>

  <action>For each unresolved comment in order (inline first, general after):

    Print the comment clearly:
    ```
    ─── Comment #{{id}} — @{{author}} ───────────────────────────────
    File: {{inline.path}}:{{inline.line}}   (or "General comment")
    "{{body}}"
    ─────────────────────────────────────────────────────────────────
    ```

    Ask the dev:
    > Bạn muốn làm gì với comment này?
    > - **[F]** Tôi đã fix — đánh dấu resolved
    > - **[D]** Thảo luận / cần giải thích thêm
    > - **[I]** Bỏ qua comment này
    > - **[Q]** Dừng review comments, chuyển sang check PR status
  </action>

  <check if="dev chose [F]">
    <action>Mark comment as addressed in local tracking list `{{resolved_comments}}`.</action>
    <action>Print: "✅ Comment #{{id}} đã được đánh dấu resolved."</action>
    <action>Continue to next comment.</action>
  </check>

  <check if="dev chose [D]">
    <action>Ask the dev what they need clarified. Answer based on the comment context and the story's design doc / srs.</action>
    <action>After discussion, ask: "Bạn đã sẵn sàng fix chưa? [F] để đánh dấu resolved, [I] để bỏ qua."</action>
  </check>

  <check if="dev chose [I]">
    <action>Skip this comment. Continue to next.</action>
  </check>

  <check if="dev chose [Q]">
    <action>Stop iterating comments. Goto step 3.</action>
  </check>

  <action>After all comments processed, print summary:
    > **Comment resolution summary — {{story_key}}**
    > ✅ Đã address: {{resolved_count}} / {{total_count}}
    > ⏭️ Bỏ qua: {{skipped_count}}
    >
    > Nhớ push commit fix lên branch `{{head_branch}}` trước khi PR được approve.
  </action>

</step>

<step n="3" goal="Plan transitions and confirm">
  <action>For each candidate, decide the action:
    - `pr_state == merged` → action = `transition`, new state = transition's `on_merged`
    - `pr_state == open` → action = `report-only` (include `review_status` + counts in report)
    - `pr_state == closed_unmerged`:
      - If transition's `on_closed_unmerged` is set: action = `revert`, new state = that value
      - Else: action = `report-only` (warn user)
    - `pr_state == not_found` → action = `error`
  </action>

  <check if="any planned action is `transition` or `revert`, and not headless mode, and not --dry-run">
    <action>Present the planned changes as a table:
      | Story | PR | PR state | Action | Current → New |
      |-------|----|----------|--------|---------------|
      Then ASK: `[a]pply / [d]ry-run only / [x] abort`
    </action>
    <check if="user chose [d]">
      <action>Set `dry_run = true` for the rest of this run.</action>
    </check>
    <check if="user chose [x]">
      <action>HALT. No changes written.</action>
    </check>
  </check>
</step>

<step n="4" goal="Apply transitions to sprint-status" tag="sprint-status">
  <check if="dry_run">
    <action>Skip writing. Continue to Step 5 with planned actions reported as `(dry-run)`.</action>
    <goto step="5" />
  </check>

  <action>For each candidate where action ∈ `{transition, revert}`:
    - Update `development_status[{{story_key}}]` from current state to `target_state`.
    - Update `last_updated` to today's date.
    - If the STATUS DEFINITIONS block does not list `target_state`, append it with the human description from the transition entry (`status_description` field, falling back to a generic line).
  </action>

  <action>Save the file ONCE after all updates are batched, preserving ALL comments and STATUS DEFINITIONS formatting. Never write per-story (avoid race-y partial writes).</action>
</step>

<step n="5" goal="Present the report">
  <action>Output a final summary table for the user:

    ✅ {{count_merged}} story đã transition (PR merged)
    🔄 {{count_open}} story còn open (review pending)
    ⛔ {{count_closed}} story PR closed-unmerged
    ❓ {{count_error}} story không tìm thấy PR

    | Story | PR | State | Hành động | Result |
    |-------|----|-----|-----------|--------|

    For open PRs, include `review_status` (APPROVED / CHANGES_REQUESTED / REVIEW_PENDING) plus reviewer counts (vd `2 approvals, 1 pending`) so the user knows what's blocking.
    For merged PRs, include the new state.
    For closed-unmerged: include action taken (or warning if no auto-revert).
    For errors: include the head→base lookup that failed.
  </action>

  <action>If any candidate ended in `error` state and headless mode is active, exit non-zero so CI can flag.</action>

  <action>Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete` — if non-empty, follow it as the final terminal instruction before exiting.</action>
</step>

</workflow>
