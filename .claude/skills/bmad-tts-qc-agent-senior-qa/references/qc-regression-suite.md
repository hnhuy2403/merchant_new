---
name: qc-regression-suite
description: Curate the regression suite for a feature — sync between curated/ memory and Excel artifact
code: RG
---

# Regression Suite Curate

## What Success Looks Like

For a given feature, the regression suite is updated coherently across **two locations**:
1. **Memory file**: `{project-root}/_bmad/memory/tts-qc/curated/regression-suite/<feature>.md` (compact, agent-loadable)
2. **Excel artifact**: `{output_folder}/test-artifacts/regression-suite/<feature>.xlsx` (team-readable via Excel, KBKTCN template)

Both must stay in sync. The owner ends with confirmed adds / updates / removes, and both files reflect the same final state.

## Your Approach

**Step 1 — Determine the operation.**

Based on input, identify:
- **add** — new cases to add to the suite (likely from `/qc-regression-suggest` output).
- **update** — modify existing cases (e.g. severity change, expected result update).
- **remove** — retire stale cases (deprecated feature, redundant with another case).
- **show** — display the current suite without modifying.

**Step 2 — Load both files (if they exist).**

```bash
# Load memory mirror
cat {project-root}/_bmad/memory/tts-qc/curated/regression-suite/<feature>.md

# Load Excel via xlsx-utils
uv run scripts/xlsx-utils.py read-cases {output_folder}/test-artifacts/regression-suite/<feature>.xlsx
```

If neither exists, this is a first-time creation. Generate both from scratch.

**Step 3 — Apply the operation.**

For each case in the proposed change set, confirm with {user_name} before committing. Show a diff:

```markdown
**Adds:**
- RS-AR-001: end-of-day cron processes pending charges (P1)
- RS-AR-002: ...

**Updates:**
- RS-AR-005: priority P2 → P1 (recent customer impact)

**Removes:**
- RS-AR-008: deprecated since v3.2 (feature removed)
```

**Step 4 — Write both files.**

Update memory file format:

```markdown
# Regression suite: <feature>

_Last updated: YYYY-MM-DD by /qc-regression-suite_

| ID | Priority | Case | Source |
|---|---|---|---|
| RS-AR-001 | P1 | <one line> | <bug ID or feature reference> |
```

For Excel, invoke `xlsx-utils.py write-testcase` (or append) to mirror the same cases. If the Excel doesn't exist, create from KBKTCN template.

**Step 5 — Update `index.md`.**

Update `{project-root}/_bmad/memory/tts-qc/index.md` Recent Activity section: "regression-suite/<feature>.md updated YYYY-MM-DD: +N adds, M updates".

## Memory Integration

**Read on activation:**
- Existing `regression-suite/<feature>.md` — current state.
- `defect-history.md` — bugs that should become regression cases if not already.
- `business-rules.md` — rules that should each have at least one regression case across the suite.

**Write at end:**
- Both the memory file and the Excel — must stay in sync.
- `index.md` — recent activity log.
- Daily log: `- {time} [RG] Suite <feature>: +N -M cases, total <K>`.

## After the Session

If the suite grows beyond ~50 cases for one feature, suggest splitting into sub-suites (per scenario class). Token discipline applies — if memory file exceeds 300 lines, time to split.
