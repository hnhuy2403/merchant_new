---
name: qc-rootcause
description: Root cause hypotheses ranked, with evidence and verification steps
code: RC
---

# Root Cause Analysis

## What Success Looks Like

The owner ends with 3-7 ranked hypotheses for what's causing a bug, each with evidence supporting/contradicting it and a concrete next step to verify. The top hypothesis is the one with the strongest evidence, not the one that "sounds right". When `defect-history.md` contains a similar past bug, that hypothesis is bolded and surfaced first.

## Your Approach

Output structure:

```markdown
## Root cause analysis: <bug summary>

### Hypothesis 1 — <concise statement>
**Likelihood:** <high / medium / low>
**Evidence supporting:**
- <observation>
- <log line or pattern>

**Evidence contradicting:**
- <observation>

**Verification step:**
- Run: <SQL / log query / specific test case / code review of file:line>

**Past precedent:** <if defect-history.md has similar — cite ID + outcome>

---

### Hypothesis 2 — ...
```

Order by likelihood. The top hypothesis must have at least 2 supporting pieces of evidence — if it only has 1, broaden the search before ranking.

**Hypothesis lenses** (run through them all):
1. **Race condition / async** — symptoms intermittent? recent traffic surge? shared state mutation?
2. **State corruption** — partial state from interrupted flow? cache stale? token expired mid-flight?
3. **Boundary** — value at the edge? off-by-one? overflow? underflow?
4. **Configuration** — env-specific? feature flag? recently deployed config change?
5. **Third-party** — dependency change? rate limit? auth expiry? upstream incident?
6. **Data** — corrupt or unexpected production data? null where expected non-null? legacy record?
7. **Timing / scheduling** — cron job late? retry storm? backoff misconfigured?
8. **Permission / auth** — wrong role? token scope? CORS?
9. **Caching** — stale cache returning old data? cache miss producing inconsistent result?
10. **Concurrency on resource** — DB lock contention? duplicate processing?

For each lens, ask: "is there evidence FOR this lens being involved? evidence AGAINST?"

## Memory Integration

**Read on activation:**
- `defect-history.md` — find past bugs with similar symptoms. The fastest path to root cause is often "this exact thing happened before".
- `legacy-logic/<topic>.md` — domain knowledge that constrains valid hypotheses.

**Write at end:**
- When a hypothesis is verified (true root cause found), update the corresponding `defect-history.md` entry with the resolution. This makes the next similar bug investigable in minutes.
- Daily log: `- {time} [RC] Root cause analysis for <bug>: top hypothesis = <H>`.

## After the Session

Track hypothesis-vs-actual hit rate over time. If a particular lens (e.g. "concurrency") consistently lands as the actual root cause, surface that pattern — it suggests a class of fragility in the team's code that needs structural fix, not just per-bug fix.
