---
name: bmad-tts-bitbucket-connect
description: 'Connects this project to Bitbucket (Cloud or Server/Data Center) — prompts for the host URL and a token, validates it via the Bitbucket REST API, and saves credentials to config.user.yaml (gitignored). Use when the user says "connect bitbucket", "setup bitbucket", "configure bitbucket auth", or "/bmad-tts-bitbucket-connect".'
---

# Bitbucket Connection

**Goal:** Make the project usable with Bitbucket by storing valid credentials in a gitignored config file. The downstream tts skills (`bmad-tts-design-story-pr`, `bmad-tts-check-review`) read these credentials to call the Bitbucket REST API.

Supports BOTH flavors:
- **Cloud** (`api.bitbucket.org/2.0`) — auth via App Password or Workspace/Repository/Project Access Token
- **Server / Data Center** (self-hosted, e.g. `bitbucket.example.com`) — auth via HTTP Access Token (Bearer)

Flavor is auto-detected from the API base URL the user provides; explicit override is available.

**Your Role:** Auth onboarding helper. The job is narrow: collect a token safely, prove it works, write it to the right place. Treat the token as a secret end-to-end — never echo it back, never log it in plaintext, never write it to `config.yaml` (which is committed).

- Communicate in `{communication_language}`.
- Token is written ONLY to `{project-root}/_bmad/config.user.yaml` (the gitignored personal-config file).
- When displaying the token (preview, confirmation), MASK to last 4 characters: `bb-token: ****abcd`.
- Never include the raw token in tool-call output, error messages, or the conversation transcript.

## Conventions

- Bare paths (e.g. `scripts/bb-cli.py`) resolve from the skill root.
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

Treat every entry in `{workflow.persistent_facts}` as foundational context for the run.

### Step 4: Load Config

Load `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml`. Halt with `TTS module is not registered. Run /bmad-tts-setup first.` if the `tts` section is missing from `config.yaml`. Note any existing `tts.bitbucket` section in `config.user.yaml` — used in Step 1 of execution to detect reconfiguration.

### Step 5: Greet the User

Greet `{user_name}` in `{communication_language}`. State that this skill collects + validates Bitbucket credentials. Indicate whether existing creds were found (reconfiguration) or this is a first-time setup.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Headless Mode

If invoked with `--headless` or `-H`:

- Do not prompt for any value. All required inputs MUST come from CLI args (or env vars listed below).
- Halt with a clear error if mandatory inputs are missing.
- `--no-validate` is honored, but the default in headless is still to validate (CI should fail loudly on bad creds).

## Args

- `--api-base-url <url>` — Bitbucket API base. Cloud default: `https://api.bitbucket.org/2.0`. For Server: just the host root, e.g. `https://bitbucket.example.com` (the `/rest/api/1.0` suffix is added by `bb-cli`).
- `--api-flavor <cloud|server>` — explicit flavor override. By default auto-detected from URL (`api.bitbucket.org` → cloud, else server).
- `--auth-method <app-password|access-token|bearer>` — auth scheme. Cloud uses `app-password` or `access-token`; Server uses `bearer`.
- `--username <handle>` — Bitbucket nickname (Cloud app-password mode only).
- `--app-password <secret>` — Cloud app password. **Never log.**
- `--token <secret>` — token value. Cloud access-token OR Server HTTP Access Token. **Never log.**
- `--workspace <slug>` — Cloud workspace slug, OR Server project key (e.g. `VSS`). Required for downstream skills.
- `--repository <slug>` — repository slug (recommended; downstream skills need it).
- `--no-validate` — skip API validation call after writing.
- `--overwrite` — overwrite existing creds without prompting.
- `-H` / `--headless` — non-interactive mode.

Equivalent env vars: `BB_API_BASE_URL`, `BB_API_FLAVOR`, `BB_AUTH_METHOD`, `BB_USERNAME`, `BB_APP_PASSWORD`, `BB_TOKEN`, `BB_WORKSPACE`, `BB_REPOSITORY`.

## Paths

- `bb_cli` = `scripts/bb-cli.py`
- `user_config` = `{project-root}/_bmad/config.user.yaml`

## Execution

<workflow>

<step n="1" goal="Detect existing config + decide flow">
  <action>Inspect the loaded `tts.bitbucket` block (if any) from `{user_config}`. Capture: existing `auth_method`, `workspace`, `repository`, and presence (not value) of `token` / `app_password`.</action>

  <check if="existing config present AND not --overwrite AND not headless">
    <action>Show user the existing config (mask any secret to `****<last4>`). ASK: `[k]eep existing / [o]verwrite / [a]bort`.</action>
    <check if="user chose [k]"><action>Skip to Step 5 (validate existing).</action></check>
    <check if="user chose [a]"><action>HALT cleanly.</action></check>
  </check>

  <check if="existing config present AND headless AND not --overwrite">
    <action>HALT with `Bitbucket creds already configured. Pass --overwrite to replace.`</action>
  </check>
</step>

<step n="2" goal="Resolve API host + flavor (try git auto-detect first)">
  <action>Try to auto-detect connection params from the project's git remote:
    ```bash
    python3 {bb_cli} detect-from-git --cwd {project-root}
    ```
    Parse the JSON output. If `found == true`, the response carries `host`, `flavor`, `workspace`, `repository`, `api_base_url` — already normalized (Server project keys uppercased; SSH remotes default to https for API).
  </action>

  <check if="found AND interactive AND not --overwrite">
    <action>Show the user the detected values clearly:
      ```
      🔎 Detected from git remote (origin):
         api_base_url:  {{api_base_url}}
         flavor:        {{flavor}}
         workspace:     {{workspace}}     (project key for Server)
         repository:    {{repository}}
      ```
      ASK: `[u]se as defaults / [m]anually enter / [a]bort`.
    </action>
    <check if="user chose [u]"><action>Pre-fill `api_base_url`, `flavor`, `workspace`, `repository`. Skip the manual prompts in this step and Step 4 for those fields. Still need credentials → continue to Step 3.</action></check>
    <check if="user chose [m]"><action>Discard detected values and fall through to manual entry below.</action></check>
    <check if="user chose [a]"><action>HALT cleanly with no changes.</action></check>
  </check>

  <check if="found AND headless">
    <action>Pre-fill all four fields automatically (CLI args still override individually). Continue to Step 3 without prompting.</action>
  </check>

  <check if="not found OR user chose manual">
    <action>Resolve `api_base_url` (arg/env/prompt):
      - Cloud users: press enter to accept default `https://api.bitbucket.org/2.0`.
      - Server users: paste the host root, e.g. `https://bitbucket.example.com` (do NOT include `/rest/api/1.0` — the helper adds it).
    </action>
    <action>Auto-detect `flavor`: `api.bitbucket.org` in the URL → `cloud`, else → `server`. Show the detected value to the user. If the user passes `--api-flavor`, that wins.</action>
  </check>
</step>

<step n="3" goal="Choose auth method">
  <action>Resolve `auth_method` from `--auth-method`, env, or interactive prompt — choices depend on flavor:
    - **Cloud** → `app-password` (legacy, username + app password issued at https://bitbucket.org/account/settings/app-passwords/) OR `access-token` (modern Workspace/Repository/Project Access Token).
    - **Server / DC** → `bearer` (HTTP Access Token issued in repo/project/personal settings → Personal access tokens).
    Default for Server is `bearer` (only option); skip the prompt if flavor=server.
  </action>

  <check if="headless AND auth_method missing AND flavor==cloud">
    <action>HALT with `--auth-method required for cloud in headless mode.`</action>
  </check>
</step>

<step n="4" goal="Collect credentials">
  <check if="flavor == cloud AND auth_method == app-password">
    <action>Resolve `username` (arg/env/prompt). Bitbucket nickname (NOT email).</action>
    <action>Resolve `app_password` (arg/env/prompt). Instruct user to paste — do NOT echo. Confirm with masked preview: `Got app-password ****<last4> for user @<nick>`.</action>
  </check>

  <check if="flavor == cloud AND auth_method == access-token">
    <action>Resolve `token` (arg/env/prompt). Instruct paste — do NOT echo. Masked preview: `Got cloud access-token ****<last4>`.</action>
  </check>

  <check if="flavor == server">
    <action>Resolve `token` (arg/env/prompt). Instruct paste of the HTTP Access Token (Server tokens often start with `BBDC-...` or similar prefix). Masked preview: `Got server bearer-token ****<last4>`.</action>
  </check>

  <action>Resolve `workspace` (skip if already pre-filled from git auto-detect in Step 2):
    - Cloud: workspace slug (visible in Bitbucket URL: `bitbucket.org/<workspace>/...`).
    - Server: project key (uppercase, e.g. `VSS` — visible in the URL `bitbucket.example.com/projects/<KEY>/...`).
  </action>
  <action>Resolve `repository` (skip if already pre-filled from git auto-detect). Repo slug (visible after `/repos/` for Server, after workspace for Cloud). Recommended; downstream skills need it.</action>
</step>

<step n="5" goal="Validate credentials against Bitbucket API">
  <check if="--no-validate flag passed">
    <action>Skip validation. Note in confirmation that credentials were stored unverified.</action>
    <goto step="7" />
  </check>

  <action>Run validation by invoking `{bb_cli}` with the gathered credentials. Pass everything via env vars (NOT CLI args) to avoid shell-history exposure:
    ```bash
    BB_API_BASE_URL=<api_base_url> \
    BB_API_FLAVOR=<flavor> \
    BB_AUTH_METHOD=<auth_method> \
    BB_USERNAME=<username if cloud/app-password> \
    BB_APP_PASSWORD=<app_password if cloud/app-password> \
    BB_TOKEN=<token if cloud/access-token OR server/bearer> \
    BB_WORKSPACE=<workspace or project_key> \
    BB_REPOSITORY=<repository slug, optional> \
    python3 {bb_cli} validate
    ```
    Capture stdout (success JSON includes `flavor` and `identity`) or stderr (error JSON). Do NOT print env-var values back to the user — only the script's output.
  </action>

  <check if="validation status != ok">
    <action>Surface the upstream error (HTTP status + Bitbucket message) clearly. Common causes: 401 = bad creds, 403 = token lacks scope, 404 = workspace/project not found.</action>
    <check if="not headless">
      <ask>`[r]etry credentials / [s]ave anyway (skip validation) / [a]bort`</ask>
      <check if="user chose [r]"><action>Return to Step 2.</action></check>
      <check if="user chose [a]"><action>HALT.</action></check>
    </check>
    <check if="headless">
      <action>HALT with non-zero exit. Never write invalid creds in headless mode.</action>
    </check>
  </check>
</step>

<step n="6" goal="Validate existing config (only if user chose [k]eep in Step 1)">
  <action>Run validation on the existing config (same env-var pattern as Step 5). If it fails, warn the user and offer re-collection (loop back to Step 2). If it passes, jump to Step 8.</action>
</step>

<step n="7" goal="Write credentials to config.user.yaml">
  <action>Read `{user_config}` (create empty `{}` if missing). Locate or create the `tts:` section, then the `bitbucket:` subsection. Write a unified shape; only the fields relevant to the chosen flavor + auth method are populated, others omitted:
    ```yaml
    tts:
      bitbucket:
        api_base_url: <url>             # always
        api_flavor: <cloud or server>   # always
        auth_method: <app-password | access-token | bearer>
        workspace: <slug or project_key>
        repository: <slug or null>      # only if user provided
        # cloud/app-password only:
        username: <nick>
        app_password: <secret>
        # cloud/access-token OR server/bearer:
        token: <secret>
    ```
    Set keys based on flavor + `auth_method`; do NOT carry over fields from another mode. Preserve all other unrelated content in the file.
  </action>

  <action>If `{project-root}/.gitignore` exists, verify it includes the path `{project-root}/_bmad/config.user.yaml` (or a glob pattern that covers it). If not, ASK the user (interactive) whether to add it — never silently modify gitignore.</action>
</step>

<step n="8" goal="Confirm and report">
  <output>✅ Bitbucket connection lưu thành công, {user_name}.

    - Flavor: {{flavor}}  ({{api_base_url}})
    - Auth method: {{auth_method}}
    - Workspace/Project: {{workspace}}
    - Repository: {{repository or "(chưa set — phải truyền args khi gọi skill khác)"}}
    - Credential: ****{{last4}}
    - Validation: {{validation_result}} (identity: {{identity}})
    - Lưu tại: {project-root}/_bmad/config.user.yaml (gitignored)

    Bước tiếp:
      - `/bmad-tts-design-story-pr` — sẽ tự đọc tts.bitbucket từ config.user.yaml để tạo PR
      - `/bmad-tts-check-review` — sẽ tự đọc cùng config để check PR state
  </output>

  <action>Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete` — if non-empty, follow as final terminal instruction.</action>
</step>

</workflow>
