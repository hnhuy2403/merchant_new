---
name: qc-review
description: Standard review of a test case set — what's missing, what to improve, coverage estimate
code: RV
---

# Test Case Review

## What Success Looks Like

The owner ends with a structured review of a test case set: what's missing, where to improve, an estimated coverage %, and a prioritized action list. Tone is neutral and direct — not mentor-toned (use `qc-peer-review` for that), not harsh (use `qc-critique` for that). The review must call out at least one gap the author wouldn't see from re-reading their own work.

## Your Approach

Output structure:

```markdown
## Test review: <feature / test case set>

**Cases reviewed:** <N>
**Coverage estimate:** <X>%
**Verdict:** <ready / needs revision / not ready>

### Strengths
- <what's working well>

### Gaps
| # | What's missing | Why it matters | Severity |
|---|---|---|---|
| 1 | <gap> | <impact> | <high/med/low> |

### Improvements
| # | Current | Suggested | Why |
|---|---|---|---|
| 1 | "Verify system displays result" | "Verify result panel shows '$<exact-amount>' within 2s" | Vague expected |

### Action list (in priority order)
1. <action>
2. <action>
```

**Review lenses:**

- **Outcome verifiability** — every `expected` field must be observable. "System works correctly" → flag.
- **Coverage breadth** — happy path covered? primary negatives? boundaries? state transitions?
- **Coverage depth** — for the most critical scenario, is there ≥1 case per business rule and ≥1 per known edge?
- **Dedup** — cases that differ only in trivial wording → flag, suggest merging.
- **Order / grouping** — are cases organized into Suites that make execution efficient?
- **Data concreteness** — placeholders like "<valid input>" → flag, suggest concrete values.
- **Step minimality** — steps that include verification logic in the middle (rather than at the end) → flag.
- **ID convention** — IDs follow `qa-conventions.md` naming?

**Coverage estimate** is a rough %, not a number to defend rigorously. Use heuristic: full happy path + most negatives + obvious edges = 70-80%. Add 10% per: full state coverage, full boundary coverage, regression-risk cases.

## Memory Integration

**Read on activation:**
- `qa-conventions.md` — naming, severity/priority labels.
- `business-rules.md` — every rule should map to ≥1 case in the set.
- `common-edge-cases.md` — flag missing common edges.

**Write at end:**
- If a recurring gap pattern emerges (e.g. "this team consistently misses pagination edge cases"), curate to `common-edge-cases.md` for future generation defaults.
- Daily log: `- {time} [RV] Reviewed <set>: <verdict>, <N> gaps`.

## After the Session

If the review uncovered a missing convention (e.g. "the team has no standard for negative case data formatting"), suggest a `qa-conventions.md` entry.
