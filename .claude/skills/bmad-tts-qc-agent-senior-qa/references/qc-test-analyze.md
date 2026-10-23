---
name: qc-test-analyze
description: Analyze a requirement — function summary, business rules, user flow, gaps
code: TA
---

# Analyze Requirement

## What Success Looks Like

The owner ends with a Markdown analysis that surfaces **what the requirement actually says, what it assumes, and what it's missing**. The "Điểm chưa rõ / thiếu" section must contain at least one specific question the writer hasn't answered. If the requirement is well-written, the analysis is short and confident. If the requirement is vague, the analysis names the vagueness without padding.

## Your Approach

Output structure (always 4 sections, in this order):

1. **Tóm tắt chức năng** — 2-5 bullets, what the system does at a behavioral level. No tech detail unless it's load-bearing.
2. **Business rules** — explicit rules. Format: `R-N: <rule>` (so they can be referenced later in test cases). Pull from `business-rules.md` if a rule overlaps with prior project knowledge.
3. **User flow** — happy path as a numbered list, then 1-2 alternate paths. Use a mermaid diagram if there are 3+ states.
4. **Điểm chưa rõ / thiếu** — concrete questions, each linked to a stakeholder when known (e.g., "→ hỏi BA"). Pull stakeholder names from `stakeholders.md`.

**Read the requirement twice.** First pass: extract what's stated. Second pass: hunt for what isn't — boundaries, error paths, concurrency, permissions, timezone, currency, persistence, retry behavior, audit trail, accessibility. The hidden half is where the bugs live.

If the input references domain concepts you've already curated, cite them: "Theo `legacy-logic/auto-recharge.md`: phí tính theo ngày làm việc — requirement này có theo quy ước đó không?"

## Memory Integration

**Read on activation:**
- `{project-root}/_bmad/memory/tts-qc/curated/business-rules.md` — pre-existing rules to cross-check.
- `{project-root}/_bmad/memory/tts-qc/curated/legacy-logic/*.md` — past domain knowledge.
- `{project-root}/_bmad/memory/tts-qc/curated/stakeholders.md` — who to direct questions to.

**Write at end:**
- New unique business rules → append to `business-rules.md` with source citation.
- Significant gap patterns (recurring missing-rule types) → flag for curate phase.
- Append one-line entry to `{project-root}/_bmad/memory/tts-qc/daily/YYYY-MM-DD.md`: `- {time} [TA] Analyzed: <requirement title> → N gaps surfaced`.

## After the Session

Append to personal `sessions/YYYY-MM-DD.md`: requirement title, the 1-2 most important gaps (the ones the dev/BA should hear about first), and any new domain rule worth raising at curate time.
