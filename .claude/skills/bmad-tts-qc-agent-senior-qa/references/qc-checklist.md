---
name: qc-checklist
description: Quick tick-box test checklist for a feature — actionable, scannable
code: CL
---

# Test Checklist

## What Success Looks Like

The owner ends with a flat tick-box checklist they can paste into Notion / Slack / a Word doc. Every item is **executable in under 2 minutes**. The checklist covers happy path, primary negatives, and the most-likely-to-break edges — but is intentionally NOT exhaustive (use `qc-testcase` for that).

## Your Approach

Output as Markdown checkboxes:

```markdown
## Test checklist: <feature>

### Happy path
- [ ] <step 1 — must verify the core flow>
- [ ] <step 2>
- [ ] <step 3>

### Common negatives
- [ ] <step>
- [ ] <step>

### Cross-cutting
- [ ] Test on iOS (latest)
- [ ] Test on Android (latest)
- [ ] Test offline / poor network
- [ ] Test app backgrounded mid-flow
- [ ] Verify analytics events fire (if applicable)

### Pre-prod gates
- [ ] All P0/P1 cases pass
- [ ] No new console errors
- [ ] Regression suite green
```

**Style rules:**
- Imperative verb first: "Verify X", "Confirm Y", "Trigger Z and observe W".
- Include the verification: "Tap submit → check that the success toast appears within 2s."
- Trim aggressively. Aim for ≤ 15 items for a typical feature, ≤ 25 for a complex one. Long checklists don't get checked.
- Avoid duplicates with the team's standard pre-prod gates if those are documented.

If `qa-conventions.md` has a team-standard pre-prod checklist, append it as the final section instead of duplicating items.

## Memory Integration

**Read on activation:**
- `qa-conventions.md` — team's standard checklist baseline.
- `common-edge-cases.md` — recurring edges that should always be on a checklist.

**Write at end:**
- If new universal items emerge (e.g. "always check Vietnamese diacritics in text input"), promote to `qa-conventions.md` standard checklist.
- Daily log: `- {time} [CL] Checklist for <feature> (<N> items)`.

## After the Session

Note items {user_name} adds — recurring additions = update the standard.
