---
name: bmad-tts-qc-data-bulk
description: Generate a bulk list of test data values for a single field given its rule (50 by default). Use when the user runs /bmad-tts-qc-data-bulk or asks for many test data values for a field — copy-paste-ready output.
---

# QC Data Bulk

## Overview

Mechanical bulk test data generator. Given a field name + rule + optional count, produces a list of representative values one per line. Light, no persona, no memory required. The richer designed-data capability (valid / invalid / boundary / special chars) lives in the `/bmad-tts-qc-agent-senior-qa` agent's `qc-data` capability.

## On Activation

1. Parse args:
   - **field** (required) — what's being generated, e.g. "Vietnamese phone number".
   - **rule** (required) — constraints, e.g. "10 digits, leading 0, must start with 03/05/07/08/09".
   - **count** (optional, default `50`) — how many values to generate.
   - **format** (optional, default `list`) — `list` (one per line), `csv` (single row), `json` (array).

2. If `{project-root}/_bmad/memory/tts-qc/curated/qa-conventions.md` exists, load it for any team-specific format/style hints. Otherwise proceed without context — this skill is intentionally lightweight.

3. Generate the values. Bias toward **diversity** within the rule:
   - Spread across the valid range / pattern space.
   - Include diverse first digits / suffixes / lengths where applicable.
   - For Vietnamese-domain fields (phone, CCCD, account ID), respect Vietnamese conventions.
   - For monetary fields, include round numbers, awkward fractions, and edge values within rule.
   - For date fields, span a meaningful range.

4. Output the list in the chosen format. Default header: `# {count} test data values for "{field}"` then the list. No explanations unless asked.

## Style

- Pure mechanical generation — don't lecture about test data theory.
- If the rule is ambiguous, ask one clarifying question and proceed with sensible defaults.
- Don't generate identical values; if the rule is too narrow for the requested count, generate as many as possible and explain the constraint.
- Never include real PII or production-looking data (synthesize random plausible values).

## Examples

```
/bmad-tts-qc-data-bulk field="Vietnamese phone" rule="10 digits, leading 0, prefix 03/05/07/08/09" count=20
```

→ Output: 20 plausible Vietnamese mobile phone numbers, one per line, with diverse prefixes and number patterns.

```
/bmad-tts-qc-data-bulk field="amount" rule="positive integer multiple of 10000, ≤ 100000000" count=30 format=csv
```

→ Output: 30 amounts as a single CSV row.

## Cross-skill notes

- For **designed** data (valid / invalid / boundary / special chars in structured groups), invoke the `qc-data` capability on `/bmad-tts-qc-agent-senior-qa` instead.
- This skill writes **no memory** — it's stateless. The agent handles curation.
