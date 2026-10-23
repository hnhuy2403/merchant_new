---
name: qc-ingest-business-logic
description: Read a legacy business-logic doc and distill into curated module memory (legacy-logic/{topic}.md)
code: IB
---

# Ingest Legacy Business Logic

## What Success Looks Like

Given a path to a doc (`.md`, `.txt`, `.docx`, `.pdf`) or pasted content describing past business logic / requirements, the owner ends with one or more new files in `{project-root}/_bmad/memory/tts-qc/curated/legacy-logic/` containing **distilled, agent-loadable** knowledge. The original doc is summarized at top, key business rules extracted as numbered list, glossary defined, and edge cases (already encountered) captured. The shared memory `index.md` is updated.

This is how Senior QA "learns" — not by reading the same doc every session, but by curating once and referencing the curated form thereafter.

## Your Approach

**Step 1 — Identify input.**

- Path to file → read it (use `Read` for `.md`/`.txt`; for `.docx` use `python-docx` if installed, else ask user to paste plain-text export; for `.pdf` use `pypdf` if installed, else paste).
- Pasted content → use directly.

**Step 2 — Determine topic + filename.**

Pull the topic name from the doc title or first heading. Slugify: lowercase, hyphenated. Example: "Auto Recharge - End of day" → `auto-recharge-end-of-day`.

Output file: `{project-root}/_bmad/memory/tts-qc/curated/legacy-logic/<topic>.md`.

If the file already exists, ask {user_name}:
- **Append** — add new sections without modifying existing.
- **Merge** — agent merges new content with existing (resolves duplicates, keeps the better version of each rule).
- **Replace** — overwrite (rare; only if the existing file is wrong / outdated).

**Step 3 — Distill.**

Output structure:

```markdown
# <Topic>

_Source: <doc path or "pasted content"> — ingested YYYY-MM-DD by `/qc-ingest-business-logic`._

## Summary

<2-4 sentence summary of what this domain does and why it matters from a QA perspective>

## Glossary

| Term | Meaning |
|---|---|
| <term> | <definition in the project's domain> |

## Business rules

| ID | Rule | Source ref |
|---|---|---|
| BR-<topic>-001 | <rule statement> | <section/page in source> |
| BR-<topic>-002 | <rule> | <ref> |

## Known edge cases

- <edge case the doc surfaces>
- <edge case>

## Open questions / ambiguities

_Things the source doc leaves unclear. Surface to BA / dev when feature is touched again._

- <question>

## Related domains

_Other curated topics this connects to. Internal links to other `legacy-logic/*.md` files._

- See: `[other-topic.md](other-topic.md)` — <relationship>
```

**Distillation discipline:**

- **Don't summarize narratively** — extract structure (rules, glossary, edges).
- **One rule per row** — atomic, testable. "Phí recharge tính theo ngày làm việc" is one rule. "Phí recharge tính theo ngày làm việc và lưu vào audit log" is two.
- **Cite source location** — page number, section, or paragraph anchor. The dev can find the original.
- **Don't lose ambiguities** — if the doc says "the system should handle errors gracefully" without defining "gracefully", that's an open question. Capture it.
- **Cross-reference** — if rules in this topic connect to existing `legacy-logic/*.md`, add to "Related domains" + add reverse link in the other file.

**Step 4 — Update the index.**

Update `{project-root}/_bmad/memory/tts-qc/index.md`:
- Add to "Recent Activity": `- YYYY-MM-DD: Ingested legacy logic: <topic> (N rules, M edges)`.
- Update "Curated Files" table row for `legacy-logic/<topic>.md` with current date.

**Step 5 — Surface implications.**

If the ingestion reveals contradictions with existing curated content (e.g. a new rule contradicts an existing entry in `business-rules.md`), flag it for {user_name} resolution. Don't silently overwrite.

## Memory Integration

**Read on activation:**
- Existing `legacy-logic/*.md` — for cross-referencing.
- `business-rules.md` — for contradiction detection.
- `index.md` — for current state.

**Write at end:**
- New `legacy-logic/<topic>.md`.
- Updated `index.md`.
- If significant new rules surface, also append to `business-rules.md` with citation.
- Daily log: `- {time} [IB] Ingested <topic>: N rules, M edges`.

## After the Session

If a topic is ingested but never gets referenced in subsequent capabilities, it might be irrelevant — surface to {user_name} during next curate phase ("we ingested X 30 days ago and haven't used it; keep or prune?").
