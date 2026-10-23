---
name: qc-risk
description: Risk-based assessment for a feature — fragile areas, where to test deep, priority
code: RK
---

# Risk Assessment

## What Success Looks Like

The owner ends with a prioritized risk table they can use to decide where to spend their limited testing time. Each row has a concrete reason, not "this is risky" hand-waving. The output must call out at least one risk the owner wouldn't have flagged from reading the feature description alone.

## Your Approach

Output a Markdown table:

| Area | Risk | Why | Priority | Mitigation |
|---|---|---|---|---|

Use the team's priority scale per `qa-conventions.md` (default `P0-P3`). Order rows by priority descending.

**Reasoning sources** (use them in this order):
1. `defect-history.md` — past bugs in similar areas. If a similar feature shipped a P1 in the past, the new one inherits at least P2 risk by default.
2. **Surface area heuristics** — concurrency, money, dates/timezones, identity/permissions, file I/O, third-party integrations, mobile permissions, push notifications, payment, sensitive data → all default-elevated risk.
3. **Newness heuristic** — fresh code paths beat well-trodden ones. If the feature touches code that hasn't been touched in 6+ months, mark it.
4. `common-edge-cases.md` — known team-specific edge cases.

**Mitigations should be testing actions** ("add 5 boundary cases for amount field; run regression suite for payment module"), not generic advice ("test thoroughly").

## Memory Integration

**Read on activation:**
- `defect-history.md` (especially recent entries and entries tagged with related feature/module).
- `common-edge-cases.md`.
- `project-profile.md` (tech stack — risk profile differs for native mobile vs web).

**Write at end:**
- If a risk surfaces a new pattern (e.g. "this team's date features always have timezone bugs"), flag for curate phase.
- Daily log: `- {time} [RK] Risk-assessed: <feature> → top risk: <area>`.

## After the Session

Session log: feature name, top 3 risks. If a risk pattern repeats from prior sessions, note it for next curate.
