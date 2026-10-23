---
name: qc-state
description: State transition analysis with mermaid diagram + per-transition test cases
code: ST
---

# State Transition Analysis

## What Success Looks Like

The owner ends with:
1. A **mermaid state diagram** showing all states and transitions (renders in their editor).
2. A **transition table** — every legal transition gets at least one test case, every illegal transition gets a negative test case.
3. **Persistence test cases** — what happens when the app is killed, network drops, or app is backgrounded mid-state.

Multi-state features are where most production bugs hide (login + OTP + verify + retry + locked-out flows are bug magnets). This capability exists to make the state space explicit.

## Your Approach

**Step 1 — Identify states.**

States are noun-like (`Idle`, `OTP_Sent`, `Verifying`, `Locked_Out`). List them with a short description. A typical mobile/web feature has 5-12 states.

**Step 2 — Draw the mermaid diagram.**

```markdown
\```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> OTP_Sent: send OTP
    OTP_Sent --> Verifying: enter OTP
    OTP_Sent --> Idle: timeout (60s)
    OTP_Sent --> OTP_Sent: resend (max 3)
    Verifying --> Authenticated: correct OTP
    Verifying --> OTP_Sent: wrong OTP (attempt < 3)
    Verifying --> Locked_Out: wrong OTP × 3
    Locked_Out --> Idle: 30min cooldown
    Authenticated --> [*]
\```
```

**Step 3 — Transition table.**

| From | Trigger | To | Type | Test Case |
|---|---|---|---|---|
| Idle | send OTP | OTP_Sent | Legal | <test case description> |
| OTP_Sent | enter OTP | Verifying | Legal | <test case description> |
| OTP_Sent | timeout 60s | Idle | Legal | <test case description> |
| Verifying | wrong OTP × 3 | Locked_Out | Legal | <test case description> |
| Locked_Out | enter any OTP | Locked_Out | Illegal | <should not transition; verify cooldown remains> |

Cover **illegal transitions** explicitly — what happens if the user tries to skip a state via deep link or manipulated request?

**Step 4 — Persistence cases.**

For each non-terminal state:
- App killed in this state → on relaunch, what state should be restored?
- Network drops in this state → what UI feedback / retry behavior?
- Backgrounded 24h in this state → expired? recovered?

## Memory Integration

**Read on activation:**
- `business-rules.md` — rules about timeouts, retry limits, lockout durations.
- `defect-history.md` — past state-machine bugs.

**Write at end:**
- The state diagram itself is worth saving. Offer to write to `{project-root}/_bmad-output/test-artifacts/static-traces/<feature>-states.md` (mermaid + table) so dev can reference.
- Daily log: `- {time} [ST] States for <feature>: N states, M transitions, K illegal-transition cases`.

## After the Session

If transitions/timeouts {user_name} confirms are domain rules (not feature-specific), promote to `business-rules.md`. State machines re-appear; capture them.
