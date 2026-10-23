---
name: bmad-tts-design-story
description: 'Generates a detailed implementation-ready design document for a story before development. Use when the user says "design story [story file]", "create detail design for [story]", or "/bmad-tts-design-story".'
---

# Detail Design Story Workflow

**Goal:** Produce an implementation-ready detail design document for a single story so the dev agent can implement it without ambiguity, rework, or guessing.

**Your Role:** Senior design engineer who turns story-level intent into concrete component, data, API, and file-level decisions — the guardrail that prevents costly mid-dev pivots.

- Communicate in `{communication_language}` and tailor explanations to `{user_skill_level}`.
- Generate the design doc in `{document_output_language}`.
- Treat the story file as authoritative for **what** to build; your job is to specify **how**.
- Do not write production code; the deliverable is a design doc only.
- Do not modify the story file beyond appending a `Design Doc:` reference and a status update.

## Conventions

- Bare paths (e.g. `references/template.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## On Activation

### Pre-flight: Module Config Check

Check `{project-root}/_bmad/config.yaml` for a `tts` section.

- **If `tts` section is missing:** halt with this message and do NOT continue:
  `TTS module is not registered. Run /bmad-tts-setup first to install module config and help entries, then re-run this skill.`
- **If `tts` section exists:** proceed to Step 1 below.

If the user passed `setup`, `configure`, or `install` as an argument to THIS skill, redirect them: `Module setup lives in /bmad-tts-setup — please call that skill instead.` Then halt.

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

Treat every entry in `{workflow.persistent_facts}` as foundational context for the whole run. Entries prefixed `file:` are paths or globs under `{project-root}` — load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Config

Load config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level and `bmm` section). Fall back to `{project-root}/_bmad/bmm/config.yaml` if the new format is not present. If config is missing, inform the user that `bmm-setup` (or `bmad-bmb-setup`) can configure the module, and continue with sensible defaults.

Resolve:

- `project_name`, `user_name`, `user_skill_level`
- `communication_language`, `document_output_language`
- `planning_artifacts`, `implementation_artifacts`
- `date` as system-generated current datetime

### Step 5: Greet the User

Greet `{user_name}` in `{communication_language}`. State that this workflow produces a detail design doc for a story, mention whether headless mode is active, and confirm the auto-discovered story (Step 1 of execution) before generating.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Headless Mode

If invoked with `--headless` or `-H`:

- Do not pause for confirmation between steps.
- Skip the user-approval gate (Step 6) — apply the self-review and adversarial findings automatically and save.
- If the story cannot be auto-discovered or the design fails its self-check, halt with a clear error. Never silently produce a low-quality artifact.

## Paths

- `story_file` = explicit story path if user-provided; otherwise auto-discovered from `sprint_status`
- `sprint_status` = `{implementation_artifacts}/sprint-status.yaml`
- `design_template` = `{workflow.design_template}` (default: `references/template.md`)
- `design_checklist` = `{workflow.design_checklist}` (default: `references/checklist.md`)
- `design_output_path` = `{workflow.design_output_path}` (default: `{implementation_artifacts}/{{story_key}}/detail-design.md`)

## Execution

<workflow>

<step n="1" goal="Find target story" tag="sprint-status">
  <check if="{{story_path}} provided by user">
    <action>Use {{story_path}} directly. Read the COMPLETE story file. Extract `story_key`, `epic_num`, `story_num`, `story_title` from the filename pattern `{{epic_num}}-{{story_num}}-{{story_title}}.md` and from the file's metadata.</action>
    <action>Verify story Status is `ready-for-dev`. If `designed` already, ASK the user whether to redesign (overwrite existing design doc) or halt.</action>
    <goto anchor="loaded" />
  </check>

  <action>Read the FULL `{sprint_status}` file from start to end, preserving order.</action>
  <action>Find the FIRST entry under `development_status` whose key matches the pattern `number-number-name` (not an `epic-X` or retrospective key) AND whose value equals `ready-for-dev`.</action>

  <check if="no `ready-for-dev` story found">
    <output>📋 No `ready-for-dev` stories found in sprint-status.yaml.

      Options:
      1. Run `create-story` first to produce a story ready for design
      2. Provide an explicit story file path
      3. Quit
    </output>
    <ask>Choose [1], [2] (provide path), or [q]:</ask>
    <action>Honor the user's choice. For [1] or [q], HALT.</action>
  </check>

  <action>Extract `epic_num`, `story_num`, `story_title` from the matched key. Set `story_key`. Resolve the matching story file in `{implementation_artifacts}` — try in this order, use the first that exists:
    1. `{implementation_artifacts}/{{story_key}}/story.md` (folder layout from `bmad-tts-create-story`)
    2. `{implementation_artifacts}/{{story_key}}.md` (legacy flat layout from upstream `bmad-create-story`)
    If neither exists, HALT with: "Story file not found for key {{story_key}}".
    Read the resolved story file COMPLETELY.
  </action>

  <anchor id="loaded" />
  <action>Parse the story file's sections: Story, Acceptance Criteria, Tasks/Subtasks, Dev Notes, Status. Do not modify yet.</action>
</step>

<step n="2" goal="Load supporting context selectively">
  <action>The story's Dev Notes already contains architecture, file structure, and technical requirements distilled by `bmad-create-story`. Treat that as your primary reference.</action>
  <action>Only load additional artifacts (`{planning_artifacts}/architecture*.md`, `{planning_artifacts}/prd*.md`, `{planning_artifacts}/*ux*.md`) if the story's Dev Notes leaves a specific question unanswered for design (e.g. an external API contract not described, a state machine you cannot infer). Load the smallest slice that answers the gap.</action>
  <action>If files being modified are listed in the story's Dev Notes File List, READ those existing files in `{project-root}` to ground the design in current code reality — surprise mismatches at design time prevent dev rework.</action>
</step>

<step n="3" goal="Draft the detail design document">
  <action>Initialize the output file from `{design_template}` at `{design_output_path}`. Substitute story metadata into the header.</action>
  <action>Fill every section the template defines. Each section must be implementation-ready: a competent dev should be able to read it and write code without further clarification.</action>
  <critical>Specificity rules:
    - Component Breakdown: name each new/modified module, class, or function with its signature and single-sentence responsibility. No placeholder names.
    - Data Model & Flow: include a Mermaid sequence diagram for the primary happy path; describe state transitions explicitly.
    - API Contracts: full request/response schema, validation rules, status codes, error shapes — not just endpoint names.
    - File Changes: a table where every row is `path | NEW or UPDATE | precise change` (e.g. "extract X into helper Y", not "refactor").
    - Edge Cases & Error Handling: enumerate inputs that break naive implementations, concurrency concerns, partial-failure scenarios — and the chosen handling for each.
    - Test Plan: list concrete test names for unit/integration/e2e, mapped to acceptance criteria.
    - Open Questions / Risks: anything you could not resolve from inputs. Better to surface than guess.
  </critical>
  <action>Set the design doc Status to `draft`. Save the file.</action>
</step>

<step n="4" goal="Self-review against the design checklist">
  <action>Validate the draft against `{design_checklist}`. For any item that fails, fix the design doc directly. Iterate until the checklist passes or until the only remaining failures are `Open Questions` that genuinely require user input.</action>
  <action>Update the design doc Status to `self-reviewed` once the checklist passes.</action>
</step>

<step n="5" goal="Adversarial review (configurable)">
  <check if="{workflow.skip_adversarial_review} is true">
    <action>Skip this step. Note in the design doc's "Adversarial Review Findings" section: `Skipped per configuration.`</action>
    <goto step="6" />
  </check>

  <action>Invoke `{workflow.adversarial_review_skill}` (default: `bmad-review-edge-case-hunter`) on the draft design doc. Pass the design doc path and the story file path as context. The reviewer's job is to find unhandled edge cases, missing failure modes, and ambiguous specifications — not stylistic feedback.</action>
  <action>Incorporate the reviewer's findings:
    - High-severity items: address in the design doc directly (update the relevant section).
    - Medium/Low items: add to the "Adversarial Review Findings" section with a chosen disposition (addressed / accepted / deferred-to-dev) and one-line rationale.
  </action>
  <action>Update the design doc Status to `reviewed`.</action>
</step>

<step n="6" goal="User approval gate">
  <check if="headless mode">
    <action>Skip this step. Set design doc Status to `approved` automatically.</action>
    <goto step="7" />
  </check>

  <action>Present a concise summary to {user_name}: design doc path, sections covered, count of edge cases identified, count of open questions. Do NOT dump the full doc — point them to the file.</action>
  <ask>Approve, request changes, or abort? [a/c/x]</ask>

  <check if="user requests changes">
    <action>Capture the change requests. Apply them to the design doc. Re-run the relevant portion of self-review (Step 4) for the changed sections. Re-present.</action>
  </check>

  <check if="user aborts">
    <action>Leave the design doc on disk with Status `draft` so the user can resume manually. HALT.</action>
  </check>

  <action>Set design doc Status to `approved`.</action>
</step>

<step n="7" goal="Finalize and update sprint status" tag="sprint-status">
  <action>Save the final design doc.</action>

  <action>Update the story file: append a single line near the top of the Dev Notes section: `**Design Doc:** {{design_output_path}}` (path relative to project root). Do not modify any other story content.</action>

  <check if="{sprint_status} file exists">
    <action>Load the FULL `{sprint_status}` file. Find `development_status[{{story_key}}]`.</action>
    <action>Verify current value is `ready-for-dev`. Update to `designed`. Update `last_updated` to today.</action>
    <action>Save the file, preserving ALL comments and STATUS DEFINITIONS.</action>
    <action>If the STATUS DEFINITIONS block does not list `designed`, append `designed: Design doc complete and approved; ready for dev` to it (preserve formatting).</action>
  </check>

  <output>✅ Detail design ready, {user_name}.

    - Story: {{story_key}}
    - Design Doc: {{design_output_path}}
    - Status: designed

    Next step: run `/bmad-dev-story` to implement.
  </output>

  <action>Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow.on_complete` — if non-empty, follow it as the final terminal instruction before exiting.</action>
</step>

</workflow>
