---
name: qc-test-eval
description: Evaluate health of a test cycle — pass rate, risk areas, flaky concentration, go/no-go
code: TE
---

# Test Cycle Evaluation

## What Success Looks Like

Given the results of a test cycle (pass/fail/blocked/flaky counts, optionally per-test breakdown), the owner ends with a Markdown health summary they can share with the team or stakeholders. The summary surfaces risk concentrations and gives a defensible go/no-go recommendation. Numbers are honest — if data is too thin for a recommendation, say so.

## Your Approach

Output structure:

```markdown
## Test cycle eval: <cycle name / date>

**Verdict:** <GO / GO with caveats / NO-GO / inconclusive>

### Snapshot
- Total cases: <N>
- Pass: <count> (<pct>%)
- Fail: <count> (<pct>%)
- Blocked: <count> (<pct>%)
- Flaky: <count> (<pct>%)
- Not run: <count> (<pct>%)

### Risk concentrations
| Area | Cases | Pass rate | Concern |
|---|---|---|---|
| Auto recharge | 23 | 78% | 5 fails clustered in OTP edge cases |
| Login | 15 | 100% | clean |

### Flaky concentration
- <test ID> — flaky 3/5 runs — <hypothesis>

### Blockers preventing GO
1. <fail in P0/P1 case — must resolve>
2. <blocker — must resolve>

### Soft caveats (could ship with mitigation)
- <pattern of low-priority fails>

### Recommendation
<concrete recommendation, e.g. "GO with caveats: ship after resolving blockers (1) and (2). Monitor auto-recharge area in production for OTP edge case symptoms.">
```

**Verdict logic:**

- **GO** — 0 P0/P1 fails, > 95% pass rate, no flaky in P0/P1.
- **GO with caveats** — fails are P2-P3, mitigations available, key flows green.
- **NO-GO** — any P0 fail, or P1 fail in critical path, or pass rate < 85% in core flows.
- **Inconclusive** — too many `Not run` or `Blocked` to draw conclusion (typically > 20% of suite). Ask for completion before evaluating.

**Style:**
- Don't pad with "great job team" — straight diagnosis.
- Cite numbers; don't say "many fails", say "8 fails".
- Distinguish blocker fails from acceptable fails. Not all fails block release.

## Memory Integration

**Read on activation:**
- `qa-conventions.md` — what's the team's GO threshold? Some teams ship with > 90%, others demand 100%.
- `defect-history.md` — does the failure pattern match a known historical pattern?

**Write at end:**
- Daily log: `- {time} [TE] Cycle eval: verdict <X>, pass rate <Y>%`.
- If a flaky pattern recurs across cycles (same test flaky 3+ cycles), surface as a candidate for `defect-history.md` (test infra defect).

## After the Session

Track verdict accuracy — if {user_name} overrides your GO recommendation and a production bug appears, your threshold is too loose. If they override your NO-GO and ship cleanly, threshold is too strict.
