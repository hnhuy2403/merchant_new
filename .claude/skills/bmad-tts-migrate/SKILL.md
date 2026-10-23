---
name: bmad-tts-migrate
description: 'Checks and migrates a TTS project to the correct BMad artifact structure. Covers structural layout, file naming, sprint-status consistency, and content quality (story.md, SRS, design docs). Use when the user says "check project structure", "migrate project", "audit stories", or "/bmad-tts-migrate".'
---

# TTS Project Migrate & Audit

**Goal:** Detect every structural, naming, consistency, and content quality issue in a TTS project's implementation artifacts — then fix what can be auto-fixed and guide the user through the rest.

**Your Role:** Quality gate and migration assistant. You run a fast deterministic scan first, then apply LLM-level content judgment where scripts cannot reach.

- Communicate all responses in `{communication_language}`.
- Generate reports in `{document_output_language}`.

## Conventions

- Bare paths (e.g. `scripts/check-structure.py`) resolve from this skill's root.
- `{skill-root}` = this skill's installed directory.
- `{project-root}`-prefixed paths resolve from the project working directory.

## On Activation

### Step 1: Load Config

Load config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root + `bmm` section). Fall back to `{project-root}/_bmad/bmm/config.yaml` if new format absent. Resolve:

- `{communication_language}`, `{document_output_language}`
- `{implementation_artifacts}` — default: `{project-root}/_bmad-output/implementation-artifacts`
- `{planning_artifacts}` — default: `{project-root}/_bmad-output/planning-artifacts`
- `{project_name}`

### Step 2: Parse Arguments

| Arg | Effect |
|---|---|
| `check` / `--check` (default) | Report findings only, no file changes |
| `fix` / `--fix` | Apply safe auto-fixes, then report remaining manual items |
| `--dry-run` | Show what `fix` would change without writing |
| `--story <key>` | Scope to a single story (prefix match, e.g. `1-3`) |
| `--content-only` | Skip structural script, run only LLM content checks |
| `--struct-only` | Run only the deterministic script, skip LLM content checks |
| `-H` / `--headless` | Non-interactive — output JSON, no prompts |

Set `{fix_mode}`, `{story_filter}`, `{headless_mode}`, `{skip_content}`, `{skip_struct}` accordingly.

### Step 3: Greet

In interactive mode: briefly state what you are about to check, the scope (full project or one story), and the mode (check vs fix).

Activation complete. Begin workflow below.

---

## Execution

<workflow>

<step n="1" goal="Run deterministic structural checks" skip-if="{skip_struct}">

  <action>Run the structural checker script:

  ```bash
  python3 {skill-root}/scripts/check-structure.py \
    --impl-dir "{implementation_artifacts}" \
    --planning-dir "{planning_artifacts}" \
    --bmad-dir "{project-root}/_bmad" \
    {--story {story_filter} if set} \
    {--fix if fix_mode} \
    {--dry-run if dry_run}
  ```

  If pyyaml is missing, run `pip install pyyaml` first.
  </action>

  <action>Parse the JSON output. Store as `{struct_results}`. If exit code non-zero, surface the error and halt.</action>

  <action>From `{struct_results}`, extract:
  - `auto_fixed_files`: renames and moves already applied (only in `--fix` mode)
  - `errors`: list of ERROR-severity findings
  - `warnings`: list of WARNING-severity findings
  - `infos`: list of INFO-severity findings
  - `stories`: per-story state summary
  </action>

</step>

<step n="2" goal="LLM content quality checks" skip-if="{skip_content}">

  Load `assets/content-checks.md` as your evaluation rubric.

  For each story in scope that has at least `story.md` present, spawn a **parallel subagent** (or evaluate in a single batch for ≤ 3 stories) reading:
  - `{implementation_artifacts}/{story_key}/story.md`
  - `{implementation_artifacts}/{story_key}/srs.md` or `srs-*.md` (whichever exists)
  - `{implementation_artifacts}/{story_key}/detail-design.md` (if exists; also accepts legacy `{implementation_artifacts}/{story_key}-design.md`)

  Each evaluation returns a compact JSON:
  ```json
  {
    "story_key": "...",
    "story_checks": [{ "code": "...", "severity": "...", "message": "..." }],
    "srs_checks":    [...],
    "design_checks": [...]
  }
  ```

  Merge into `{content_results}`.

</step>

<step n="3" goal="Apply auto-fixes" run-if="{fix_mode}">

  Load `assets/fix-catalog.md` to understand what is safe to auto-fix vs. what requires human action.

  The structural script already applied file renames (`srs-*.md → srs.md`) during step 1. Confirm those by reading the fix_results from `{struct_results}`.

  Additional LLM-driven fixes:
  - **SRS reference in story.md**: if story.md references `srs-{story_key}.md`, update the link to `srs.md`. Read the file, update the path, write it back.
  - **Design doc Status field**: if design doc has no Status field, insert `| Status | draft |` into the header table.

  For each fix applied, record: `{ file, change, before, after }`.

</step>

<step n="4" goal="Synthesize and present findings">

  Merge `{struct_results}` and `{content_results}` into a unified report. Group by:

  1. **Global issues** — config format, sprint-status, old directories
  2. **Per-story findings** — one section per story, severity-sorted

  Format:

  ```
  ## Báo cáo Migrate — {project_name}
  Ngày: {date}    Scope: {story_filter or "toàn bộ"}    Mode: {check|fix}

  ### Tổng quan
  | Severity | Count |
  |---|---|
  | ❌ Error   | N |
  | ⚠️ Warning | N |
  | ℹ️ Info    | N |

  ### Global
  - [ERROR/WARNING/INFO] <message>

  ### Story {story_key} — {status}
  **Auto-fixed:**
  - ✅ Renamed srs-*.md → srs.md

  **Cần xử lý thủ công:**
  - ❌ [code] message
  - ⚠️ [code] message

  **Nội dung:**
  - ⚠️ [code] message
  ```

  In **headless mode**: output raw JSON combining struct_results + content_results. No markdown.

</step>

<step n="5" goal="Offer next actions" skip-if="{headless_mode}">

  After presenting the report, offer:

  - **[F] Fix auto-fixable** — if any auto-fixable items remain and mode is `check`
  - **[S] Create missing story.md files** — for each story with ERROR `story-md-missing`, offer to invoke `/bmad-tts-create-story --story <key>` for each in sequence
  - **[U] Update SRS references in story.md** — if WARNING `story-srs-ref-old-naming` exists
  - **[R] Save report** — write report to `{implementation_artifacts}/migration-report-{date}.md`
  - **[Q] Quit**

  Honor the user's choice. For story creation, confirm each story key before invoking.

</step>

</workflow>

## Headless Output Schema

```json
{
  "project_name": "...",
  "scope": "all | {story_key}",
  "mode": "check | fix | dry_run",
  "summary": { "errors": N, "warnings": N, "infos": N },
  "auto_fixed": [{ "file": "...", "change": "...", "before": "...", "after": "..." }],
  "findings": [
    {
      "story_key": "...",
      "severity": "error|warning|info",
      "code": "...",
      "message": "...",
      "category": "structural|content|consistency|config"
    }
  ]
}
```
