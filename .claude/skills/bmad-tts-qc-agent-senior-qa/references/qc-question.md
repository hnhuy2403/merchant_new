---
name: qc-question
description: Generate clarifying questions for BA / Dev / PO from a requirement
code: QQ
---

# Clarifying Questions

## What Success Looks Like

The owner ends with a list of concrete questions they can copy into a Slack message or a meeting agenda. Each question is **answerable in one sentence** (no open-ended philosophy) and is **routed to a specific stakeholder** when the team is known.

## Your Approach

Group questions by stakeholder (pulled from `stakeholders.md`):

```markdown
### → BA (<Name>)
1. <question>
2. <question>

### → Dev lead (<Name>)
1. <question>

### → PO (<Name>)
1. <question>

### → Unknown / để xác định
1. <question>
```

If stakeholders aren't known yet, group by question *type* instead: Business / Technical / Scope / Timeline.

**Question quality bar:**
- Answerable in 1 sentence ("What's the max length of the accountId field?" — yes; "How should we handle errors?" — too broad, refine).
- Surfaces an assumption ("Does 'verify' mean 'compare to the audit log' or 'compare to the live API'?").
- Concrete, not categorical ("What happens if user closes the app at exactly the moment the OTP arrives?" beats "What about edge cases?").

Pull from past patterns — `business-rules.md` and `common-edge-cases.md` often hint at questions worth asking.

## Memory Integration

**Read on activation:**
- `stakeholders.md` — for routing.
- `business-rules.md` — to spot rules that contradict the new requirement.
- `common-edge-cases.md` — to seed familiar question categories.

**Write at end:**
- If the same question type keeps recurring across requirements, that's a candidate for `business-rules.md` or `common-edge-cases.md` curation.
- Daily log: `- {time} [QQ] N questions for <requirement>`.

## After the Session

Note in session log: which questions {user_name} flagged as "good catch" — that calibrates the question style for next time. Note also any stakeholder updates discovered (new BA name, etc.) and update `stakeholders.md` if so.
