---
name: qc-estimate
description: Effort estimate for testing a feature — hours/days, with reasoning model
code: ES
---

# Test Effort Estimate

## What Success Looks Like

The owner ends with an estimate range (low / mid / high) for testing effort, broken down by activity (analysis, case authoring, execution, retest, regression, reporting), with a **visible model** behind every number. No "vibes-based" estimates — every figure is `count × rate + buffer`.

## Your Approach

Output structure:

```markdown
## Test effort: <feature>

**Range**: <low>h - <high>h (mid: <mid>h)

### Breakdown

| Activity | Count | Rate | Effort | Notes |
|---|---|---|---|---|
| Requirement analysis | 1 | 0.5h | 0.5h | Simple req → 0.5h, complex → 2h |
| Test case authoring | <N cases> | 5min/case | <N × 5/60>h | Excel write via /qc-testcase |
| Execution (manual, first pass) | <N cases> | <X>min | <N × X/60>h | Manual mobile: 8min, web: 5min, API: 3min |
| Retest after fixes | <est defects × N> | 1× orig | <fraction>h | Assume 30% retest rate |
| Regression | <N cases from suite> | <X>min | | |
| Reporting + bug filing | <est bugs> | 15min | | |
| Buffer (20%) | | | | Setup, env issues, communication |

**Critical assumptions:**
- <list 2-4 assumptions that materially affect the number>

**De-risks for tighter estimate:**
- <2-3 follow-up questions that would shrink uncertainty>
```

**Calibration sources** (in order):
1. `defect-history.md` — past similar features and their actual test effort.
2. `project-profile.md` — team's manual execution rate (if curated).
3. `qa-conventions.md` — team standard buffer %.
4. Industry defaults (if no curated data): mobile 8min/case, web 5min/case, API 3min/case.

**Honest uncertainty**: if you don't have past data, say so and widen the range. Don't fake precision.

## Memory Integration

**Read on activation:**
- `defect-history.md` — past similar feature efforts.
- `project-profile.md` — team execution rate.
- Past `qc-estimate` outputs in personal session logs to calibrate against actuals.

**Write at end:**
- If the feature gets actually tested and effort is logged, that's gold for next estimate. Propose tracking actual vs estimated in a per-project file.
- Daily log: `- {time} [ES] Estimate for <feature>: <low>-<high>h`.

## After the Session

If {user_name} marks the estimate as "way off" (high or low), note in BOND.md their default calibration ("tends to halve my estimates" / "tends to double for cross-team work"). Apply the calibration next time.
