---
name: qc-reproduce
description: Suggest additional reproduction paths and conditions when a bug is hard to reproduce
code: RP
---

# Reproduction Path Discovery

## What Success Looks Like

When a bug is intermittent or only one tester saw it, the owner ends with 5-12 alternate reproduction conditions to try, ordered by how likely each is to expose the bug. Each path includes the specific environmental tweak and what to watch for.

## Your Approach

Output structure:

```markdown
## Reproduction paths: <bug summary>

**Original observation:** <where it was seen, by whom, what they did>
**Repro rate so far:** <e.g. 1/20>

### Path 1 — <descriptive title>
**Setup:** <env / device / data state>
**Action:** <specific user action sequence>
**Watch for:** <symptom indicators>
**Why this might work:** <reason this triggers the bug>

### Path 2 — ...
```

**Path generation lenses** (use them as a checklist):

- **Slow it down** — the bug might be a race that disappears at fast network speed. Try with throttled connection (Network Link Conditioner / Chrome DevTools throttling).
- **Speed it up** — try double-tapping the trigger button, rapid-fire input.
- **Pause mid-flow** — do step 1, switch apps for 5 minutes, come back, do step 2.
- **Background / kill** — background the app between steps; force-kill mid-flow.
- **Stale state** — start with a state from yesterday (cached login, old token, prior session).
- **Cold vs warm** — first launch after install vs Nth launch.
- **Different account state** — new account, account with prior history, account with rare data (>1000 transactions, special permissions).
- **Different network** — Wi-Fi → cellular mid-flow, weak signal, captive portal.
- **Concurrent user** — same account on two devices simultaneously.
- **Different timezone / locale** — device timezone offset from server, language non-default.
- **Different OS / browser version** — not just latest; try N-1 and N-2.
- **Edge data** — input at the boundary of valid range, special chars, non-ASCII.
- **Replay** — capture the exact HTTP requests from the original (HAR file) and replay.

For each path, the **why this might work** must hypothesize a mechanism — not just "different setup".

## Memory Integration

**Read on activation:**
- `defect-history.md` — past intermittent bugs and which reproduction tweak finally exposed them.
- `common-edge-cases.md` — environmental conditions that often trigger this team's bugs.

**Write at end:**
- When a path successfully reproduces, append to the bug entry in `defect-history.md`: which tweak worked, why. This builds your repro intuition over time.
- Daily log: `- {time} [RP] Repro paths for <bug>: <N> suggested`.

## After the Session

If three intermittent bugs in a row were finally reproduced via the same tweak (e.g. "all timing bugs reproduce only on slow 3G"), promote that to `common-edge-cases.md` as "always test on throttled network".
