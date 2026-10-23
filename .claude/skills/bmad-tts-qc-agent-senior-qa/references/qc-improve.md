---
name: qc-improve
description: Rewrite a test case set to be more professional — concrete, executable, deduplicated
code: IM
---

# Improve Test Cases

## What Success Looks Like

The owner ends with a **rewritten** test case set that preserves the intent of the original but is concrete, executable by a stranger, deduplicated, and properly grouped into suites. If the input was a Markdown set, output a Markdown set. If the input was an `.xlsx` path, output a new `.xlsx` (via `xlsx-utils.py write-testcase`) with `_improved` suffix.

Don't redesign the test plan — that's a different task. Improve **what's there**, don't replace.

## Your Approach

**Step 1 — Detect input format.**

- Markdown table or list → output Markdown.
- `.xlsx` path → run `xlsx-utils.py read-cases` to load, improve, then `write-testcase` to a new file.

**Step 2 — Transformations to apply (in this order):**

1. **Concretize placeholders** — `<valid input>` → actual value (`"1234567890"`). Pull from `business-rules.md` or `legacy-logic/` if value is domain-specific.
2. **Sharpen expected** — `system works` → `success toast 'OTP đã gửi' shown within 2s, button disabled for 60s`.
3. **Verb-lead steps** — "User clicks the button" → "Tap 'Send OTP' button".
4. **Number steps consistently** — `1.`, `2.`, `3.` (not bullets, not paragraphs).
5. **Dedup** — cases that test the same condition with trivially different wording → merge into one with a multi-row data table.
6. **Group into suites** — cases on the same flow → same `Suite-N: ...`. Re-number IDs if needed.
7. **Strip narrative** — remove "this case verifies that..." preambles.
8. **Preserve quirks** — if the author used a specific style or phrasing consistently, keep it (don't flatten their voice — that's `qc-peer-review`'s problem, not yours).

**Step 3 — Output.**

For Markdown: produce the rewritten set with a brief change-log at the top.

```markdown
## Improved test cases: <feature>

**Changes applied:**
- Concretized 8 placeholder data values
- Merged 3 duplicate cases into 1 with multi-row data
- Renumbered IDs to follow Suite-N convention
- Sharpened 5 vague expected fields
```

For `.xlsx`: invoke `xlsx-utils.py write-testcase --output <path>_improved.xlsx`. Print a summary mirroring the change-log.

## Memory Integration

**Read on activation:**
- `business-rules.md` — for concretizing placeholders.
- `legacy-logic/` — for domain-specific data values.
- `qa-conventions.md` — for naming and structure conventions.

**Write at end:**
- Daily log: `- {time} [IM] Improved <set>: N changes`.

## After the Session

If the same improvement category appears repeatedly across sessions (e.g. "always need to sharpen vague expected fields"), suggest curating an "expected field discipline" entry in `qa-conventions.md`.
