---
name: qc-scenario
description: Test scenarios — happy / negative / edge — for a feature
code: SC
---

# Test Scenarios

## What Success Looks Like

The owner ends with a scenario list grouped by type, dense enough to feed `qc-testcase` but not yet at test case granularity. Coverage of happy path is non-negotiable; negative and edge sections each have at least 3 distinct scenarios for any non-trivial feature.

## Your Approach

Output structure:

```markdown
### Happy path (<N>)
1. <scenario, 1 line>
2. ...

### Negative (<N>)
1. <scenario>

### Edge (<N>)
1. <scenario>
```

**Happy path** — what the feature does when everything goes right. List the *distinct* user journeys (e.g., "first-time user registers via email" and "first-time user registers via Google" are two scenarios, not one).

**Negative** — invalid input, unauthorized action, missing data, denied permission, rate-limited, expired session.

**Edge** — boundary values, concurrent operations, race conditions, network drops, low memory, slow connection, time-of-day boundaries, timezone, the 1000th item in a list, empty state, single item, max items, internationalization, RTL languages.

Cross-reference `common-edge-cases.md` — pre-existing team-specific edges should appear when relevant.

If the feature has multi-state behavior (login → OTP → verify → success), call `qc-state` instead of expanding state combinations into a flat scenario list.

## Memory Integration

**Read on activation:**
- `common-edge-cases.md` — incorporate team's recurring edges.
- `business-rules.md` — turn each rule into at least one scenario (positive case = rule satisfied; negative case = rule violated).

**Write at end:**
- Novel edge categories surfaced → append to `common-edge-cases.md` (after confirming with {user_name}).
- Daily log: `- {time} [SC] Scenarios for <feature> → H/N/E counts`.

## After the Session

Note which categories {user_name} expanded vs trimmed — calibration for next time. If they consistently add scenarios in a category, you're under-generating that category.
