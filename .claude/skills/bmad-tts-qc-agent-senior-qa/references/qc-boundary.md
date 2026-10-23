---
name: qc-boundary
description: Boundary value analysis for a field / logic — min, max, just below, just above
code: BV
---

# Boundary Value Analysis

## What Success Looks Like

The owner ends with a boundary value table covering `min`, `max`, `just-below-min`, `just-above-max`, plus zero/negative/empty/single where applicable. Each row has the input value, expected behavior, and reason. Off-by-one bugs are the most common defect category in input handling — this capability exists to catch them.

## Your Approach

Output a Markdown table:

| # | Value | Type | Expected | Why |
|---|---|---|---|---|
| 1 | `<min - 1>` | Just-below-min | <reject? clamp? error code?> | Off-by-one boundary |
| 2 | `<min>` | Min | <accept> | Lower bound exact |
| 3 | `<min + 1>` | Just-above-min | <accept> | Verify acceptance |
| 4 | `<typical>` | Mid-range | <accept> | Sanity |
| 5 | `<max - 1>` | Just-below-max | <accept> | Verify acceptance |
| 6 | `<max>` | Max | <accept> | Upper bound exact |
| 7 | `<max + 1>` | Just-above-max | <reject> | Off-by-one boundary |

Add as needed:
- `0`, `-1`, `null/None`, `empty string`, `space-only`, single-character, max-length-string, max-length+1.
- Type-of-value boundaries: `int max + 1` (overflow), `float vs int`, `unicode in ascii field`.

If the field is a **set** (enum, dropdown), boundaries become: each enum value, undefined value, case variations, leading/trailing whitespace.

If the field is a **date/time**, boundaries become: epoch, Y2K, far future, Feb 29 leap year, last second of year, first second of year, daylight saving boundary if applicable.

Always include the **why** column — it's what justifies the test case in code review.

## Memory Integration

**Read on activation:**
- `business-rules.md` — does a rule already define the field's range?
- `common-edge-cases.md` — past boundary bugs.

**Write at end:**
- If the field type is recurring across project (e.g. "amount field" appears in 5 features), promote a `business-rules.md` entry: "amount fields: 0 ≤ value ≤ 999,999,999".
- Daily log: `- {time} [BV] Boundary for <field>`.

## After the Session

If {user_name} adjusts a row (e.g. "max isn't 999, it's 9999"), update `business-rules.md` immediately — that's a domain rule worth keeping.
