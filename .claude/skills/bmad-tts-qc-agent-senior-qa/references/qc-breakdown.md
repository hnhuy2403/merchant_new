---
name: qc-breakdown
description: Break a testing task into concrete actionable steps with effort tags
code: BD
---

# Test Task Breakdown

## What Success Looks Like

The owner ends with an ordered list of **discrete, executable steps** for a testing task, each tagged with a rough effort estimate. Steps that depend on others are flagged. The breakdown is concrete enough that {user_name} could hand it to another QA tester and they'd execute roughly the same sequence.

## Your Approach

Output a numbered list:

```markdown
1. <step> — _<effort>_ <dependency-flag>
2. <step> — _<effort>_
3. ...
```

Effort tags: `5m`, `15m`, `30m`, `1h`, `2h`, `half-day`, `full-day`. Round generously — testers don't run on Gantt-chart precision.

Dependency flags: `(after #1)`, `(parallel with #3)`, `(blocks #5)`.

**Style:**
- Verbs first ("Setup test data for X", not "Test data should be set up").
- One responsibility per step. If a step contains "and", consider splitting.
- Include setup, execution, and teardown steps explicitly.
- Include the boring steps: provisioning test users, capturing screenshots, filing observations.

For larger tasks (1+ days), end with a **summary**: total effort range, critical path, suggested sequencing.

## Memory Integration

**Read on activation:**
- `qa-conventions.md` — does the team have a standard test prep checklist?
- `project-profile.md` — what test environment / device matrix is in scope?

**Write at end:**
- If a recurring task type has appeared 3+ times, propose curating a reusable breakdown template into `qa-conventions.md`.
- Daily log: `- {time} [BD] Breakdown for <task> → <step count> steps, ~<total effort>`.

## After the Session

If {user_name} adjusts the effort tags significantly, note their calibration in BOND.md ("tends to halve estimates for routine tasks; tends to double for first-time integrations").
