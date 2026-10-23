---
name: qc-regression-suggest
description: Suggest regression test cases for a code change — pulls from curated suite and adds new cases for changed area
code: RS
---

# Regression Suggestions

## What Success Looks Like

Given a code change description (or git diff), the owner ends with a prioritized list of regression cases to run before shipping. The list combines (a) existing cases from `regression-suite/<feature>.md` that are touched by the change, and (b) new cases proposed for the changed area. Output is concrete enough to execute or pass to `qc-testcase`.

## Your Approach

**Step 1 — Identify affected areas.**

From the change description (or diff scope), determine:
- Which features / modules are directly touched.
- Which features / modules share dependencies (DB tables, shared services, common UI components).
- Which past bugs in `defect-history.md` were in this area.

**Step 2 — Pull existing regression cases.**

For each affected feature, load `{project-root}/_bmad/memory/tts-qc/curated/regression-suite/<feature>.md` if it exists. List cases with:

```markdown
### From regression suite (must run)
| Source | Case | Reason it's selected |
|---|---|---|
| `regression-suite/auto-recharge.md` | RS-AR-001: end-of-day cron processes pending charges | Change touches recharge cron path |
```

**Step 3 — Propose new cases for the changed area.**

For code paths NOT covered by existing regression suite, propose new cases:

```markdown
### New cases proposed (gaps in suite)
| # | Case | Why needed |
|---|---|---|
| 1 | <case> | New code path: <reason> |
```

**Step 4 — Risk-tier the combined list.**

```markdown
### Run order (priority)
1. **Must run** (P0): N cases
2. **Should run** (P1): M cases
3. **Optional spot-check** (P2): K cases
```

**Heuristics:**

- If change touches **money / auth / personal data**, must-run regression set is doubled.
- If change is in a **shared service**, expand to all features depending on it.
- If `defect-history.md` shows a past bug in the same code area, add that bug's repro as a regression case.

**Output:** the suggestion list. If {user_name} accepts new cases, route them to `qc-regression-suite` to formalize into the curated suite.

## Memory Integration

**Read on activation:**
- `regression-suite/*.md` — curated cases, pull cases from each affected feature.
- `defect-history.md` — past bugs in change area become regression bait.
- `legacy-logic/<topic>.md` — domain knowledge of feature interactions.

**Write at end:**
- If new gaps surface that should become permanent regression cases, hand off to `/qc-regression-suite` to add them.
- Daily log: `- {time} [RS] Regression for change <X>: M cases from suite + K new`.

## After the Session

Track which proposed cases {user_name} accepted vs ran ad-hoc — calibration on which categories they trust to be regression-worthy.
