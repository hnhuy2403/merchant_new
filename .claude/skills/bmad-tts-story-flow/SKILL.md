---
name: bmad-tts-story-flow
description: 'Full story pipeline orchestrator for TTS team. Detects current pipeline stage and chains create-srs → design-story → design-story-pr → check-review → dev-story in order for a single story. Use when the user says "chạy full flow", "run story pipeline", "pipeline story [key]", or "/bmad-tts-story-flow".'
---

# Story Pipeline Orchestrator (TTS)

**Goal:** Detect where a story is in the TTS development pipeline and drive it forward — either one step at a time (interactive) or fully automated (headless). The pipeline is:

```
[BA]  create-srs        → SRS / BDD scenarios
[Dev] design-story      → Detail design document
[Dev] design-story-pr   → Bitbucket PR cho tech lead review
[Dev] check-review      → Address review comments / wait for approval
[Dev] dev-story         → Implementation & coding
```

**Your Role:** Pipeline coordinator. You inspect filesystem state to determine current stage, display a clear dashboard, then load and execute the appropriate next skill. You do not implement steps yourself — you delegate to the skill responsible for each step.

- Communicate in `{communication_language}`.
- Do not modify story.md, srs.md, or design docs directly — leave that to each delegated skill.

## Conventions

- Bare paths resolve from this skill root.
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to `bmad-tts-story-flow`.

## On Activation

### Step 1: Load Config

Load config from `{project-root}/_bmad/config.yaml` and `{project-root}/_bmad/config.user.yaml` (root level, then `tts` section). Fall back to `{project-root}/_bmad/bmm/config.yaml` if TOML missing. Resolve:

- `project_name`, `user_name`
- `communication_language`, `document_output_language`
- `implementation_artifacts`
- `planning_artifacts`

If config missing, inform the user to run `/bmad-tts-setup` first, then HALT.

### Step 2: Parse Args & Detect Headless

Supported args:
- `--story-key <key>` — story key like `1-2-user-auth`; sets `{{story_key}}` directly.
- `--story <path>` — explicit story.md path; derive `{{story_key}}` from folder basename.
- `--step <name>` — force-run a specific step (`srs`, `design`, `pr`, `review`, `dev`), skipping auto-detection.
- `--headless` / `-H` — non-interactive; auto-chain all remaining steps.
- `--next-only` — run only the next pending step, then stop.

Set `{headless_mode}` accordingly.

### Step 3: Discover Story

If `--story-key` or `--story` provided, use directly.

Otherwise auto-discover from `{implementation_artifacts}/sprint-status.yaml`: find the first story (top-to-bottom) with status `ready-for-dev`, `in-progress`, or `designed`. If multiple candidates, ask the user to choose. If none, ask the user to provide a story-key.

Verify `{implementation_artifacts}/{{story_key}}/story.md` exists. If not, HALT with: "story.md không tồn tại. Chạy /bmad-tts-create-story trước."

### Step 4: Greet

Greet `{user_name}` and announce: "Đang kiểm tra pipeline cho story **{{story_key}}**..." — skip if headless.

Activation complete. Begin the workflow below.

## Execution

<workflow>

<step n="1" goal="Detect pipeline stage">

Inspect the filesystem and story.md to determine which steps are done. Set boolean flags:

**`srs_done`** — true when:
- `{implementation_artifacts}/{{story_key}}/srs.md` exists AND
- File contains at least one BDD scenario marker (`H1`, `E1`, or `R1` as a standalone token)

**`design_done`** — true when any of the following:
- `{implementation_artifacts}/{{story_key}}/detail-design.md` exists AND contains a `| Status |` metadata row (injected by `design-story`; not present in the `create-story` skeleton)
- story.md Dev Notes contains a `**Design Doc:**` line pointing to an existing file

**`pr_done`** — true when:
- story.md Dev Notes contains a `**Design PR:**` line with a Bitbucket URL, OR
- `{implementation_artifacts}/{{story_key}}/` directory contains a file matching `*-pr-*.md` or `*-design-pr*.md`

**`review_done`** — true when:
- story.md Dev Notes contains `**Design PR Status:** approved` or `merged`, OR
- `sprint-status.yaml` shows story status as `approved` or `design-approved`

**`dev_done`** — true when:
- story.md Status field equals `review` or `done`, OR
- `sprint-status.yaml` shows story status as `review` or `done`

</step>

<step n="2" goal="Display pipeline dashboard">

Print a clear pipeline status table in `{communication_language}`:

```
╔══════════════════════════════════════════════════════╗
║     TTS Story Pipeline — {{story_key}}               ║
╠══════════════════════════════════════════════════════╣
║  Step              Role   Status                     ║
╠══════════════════════════════════════════════════════╣
║  1. create-srs     [BA]   ✅ Done / ⏳ Pending       ║
║  2. design-story   [Dev]  ✅ Done / ⏳ Pending       ║
║  3. design-pr      [Dev]  ✅ Done / ⏳ Pending       ║
║  4. check-review   [Dev]  ✅ Done / ⏳ Pending       ║
║  5. dev-story      [Dev]  ✅ Done / ⏳ Pending       ║
╠══════════════════════════════════════════════════════╣
║  Next step: <next pending step name>                  ║
╚══════════════════════════════════════════════════════╝
```

Use ✅ for done, ⏳ for pending (next step), ⬜ for not-yet-reachable.

If all steps done → print "🎉 Pipeline hoàn tất! Story {{story_key}} sẵn sàng cho code review." and HALT.

</step>

<step n="3" goal="Confirm execution scope (interactive only)">

<check if="headless_mode OR --next-only">
  Skip this step — proceed directly to Step 4.
</check>

<check if="--step arg provided">
  Skip this step — force-run the specified step.
</check>

Determine `{{next_step}}` = first step where flag is false (srs → design → pr → review → dev).

Count remaining steps (how many flags are false). If more than 1 remaining:

Ask the user:

> Pipeline còn **{{remaining_count}} bước** chưa hoàn thành.
> Bạn muốn:
> - **[N]** Chỉ chạy bước tiếp theo (`{{next_step}}`)
> - **[A]** Tự động chạy toàn bộ các bước còn lại
> - **[Q]** Thoát, tự chạy thủ công

Map response:
- `N` / `next` → set `run_all = false`
- `A` / `all`  → set `run_all = true`
- `Q` / `quit` → HALT cleanly

</step>

<step n="4" goal="Execute next step">

Determine which step to run:
- If `--step` provided: map arg to step name → `srs`→create-srs, `design`→design-story, `pr`→design-story-pr, `review`→check-review, `dev`→dev-story
- Otherwise: first step with flag = false

<check if="no pending steps">
  Print "✅ Tất cả bước đã hoàn tất." and HALT.
</check>

<check if="next pending step = create-srs">
  <action>Load `{skill-root}/../bmad-tts-create-srs/SKILL.md` into context.</action>
  <action>Follow all instructions in that SKILL.md. Pass `--story-key {{story_key}}` as argument. Pass `--headless` if `{headless_mode}` is true.</action>
  <action>On completion, re-evaluate `srs_done` flag from filesystem.</action>
</check>

<check if="next pending step = design-story">
  <action>Load `{skill-root}/../bmad-tts-design-story/SKILL.md` into context.</action>
  <action>Follow all instructions in that SKILL.md. Pass `--story-key {{story_key}}` as argument. Pass `--headless` if `{headless_mode}` is true.</action>
  <action>On completion, re-evaluate `design_done` flag from filesystem.</action>
</check>

<check if="next pending step = design-story-pr">
  <action>Load `{skill-root}/../bmad-tts-design-story-pr/SKILL.md` into context.</action>
  <action>Follow all instructions in that SKILL.md. Pass `--story-key {{story_key}}` as argument. Pass `--headless` if `{headless_mode}` is true.</action>
  <action>On completion, re-evaluate `pr_done` flag from filesystem.</action>
</check>

<check if="next pending step = check-review">
  <action>Load `{skill-root}/../bmad-tts-check-review/SKILL.md` into context.</action>
  <action>Follow all instructions in that SKILL.md. Pass `--story-key {{story_key}}` as argument. Pass `--headless` if `{headless_mode}` is true.</action>
  <action>On completion, re-evaluate `review_done` flag from filesystem.</action>
</check>

<check if="next pending step = dev-story">
  <action>Load `{skill-root}/../bmad-tts-dev-story/SKILL.md` into context.</action>
  <action>Follow all instructions in that SKILL.md. Pass `--story {{implementation_artifacts}}/{{story_key}}/story.md` as argument. Pass `--headless` if `{headless_mode}` is true.</action>
  <action>On completion, re-evaluate `dev_done` flag from filesystem.</action>
</check>

</step>

<step n="5" goal="Chain or stop after step completion">

<check if="--next-only OR (not run_all AND not headless_mode)">
  Print a brief summary of what was completed. Then print the updated pipeline dashboard (re-run Step 2 logic). HALT — user controls when to run the next step.
</check>

<check if="run_all OR headless_mode">
  <check if="any flags still false">
    <action>Goto Step 4 and run the next pending step.</action>
  </check>
  <check if="all flags now true">
    Print:
    > 🎉 **Pipeline hoàn tất!** Story **{{story_key}}** đã trải qua toàn bộ:
    > create-srs → design-story → design-story-pr → check-review → dev-story
    >
    > Status hiện tại: **review** — sẵn sàng cho code review.
    > Gợi ý: chạy `/code-review` để review implementation.
    HALT.
  </check>
</check>

</step>

</workflow>

## Notes

- This orchestrator does **not** replicate skill logic — it delegates. If a skill's behavior needs to change, update that skill's SKILL.md directly.
- The `check-review` step may be long-running (waiting for Bitbucket approval). In headless mode, the skill should poll or return immediately — see `bmad-tts-check-review` docs.
- If a step is unexpectedly incomplete after execution (flag still false), print a warning and HALT rather than looping — avoids infinite retry on broken states.
- BA-owned steps (`create-srs`) can be skipped by a dev if the BA has already run them externally; the pipeline detects this automatically via file existence.
