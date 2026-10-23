---
name: qc-data
description: Test data designed against a field rule — valid / invalid / boundary / special characters
code: DA
---

# Test Data Design

## What Success Looks Like

The owner ends with structured test data sets for a single field/rule, each set has 5-10 representative values. The output is **copy-paste-ready** for execution — no placeholders. If they need bulk volume, route them to `/bmad-tts-qc-data-bulk`; this capability is about *designed* data, not bulk generation.

## Your Approach

Output 4 sets:

```markdown
### Valid (<N>)
| # | Value | Note |
|---|---|---|
| 1 | <value> | Typical |
| 2 | <value> | Edge of valid range |

### Invalid (<N>)
| # | Value | Why invalid |
|---|---|---|
| 1 | <value> | Type mismatch |
| 2 | <value> | Out of range |

### Boundary (<N>)
| # | Value | Position |
|---|---|---|
| 1 | <min> | Lower edge |
| 2 | <max> | Upper edge |

### Special characters (<N>)
| # | Value | Category |
|---|---|---|
| 1 | `<empty>` | Empty |
| 2 | `   ` | Whitespace only |
| 3 | `O'Brien` | Apostrophe (SQL injection risk) |
| 4 | `<script>alert(1)</script>` | XSS payload |
| 5 | `🎉` | Emoji / multi-byte |
| 6 | `Nguyễn` | Vietnamese diacritics |
| 7 | `日本語` | Non-Latin script |
```

For Vietnamese projects (per `project-profile.md`), include diacritics, đ/Đ, Vietnamese phone formats (10/11 digits, leading 0), Vietnamese ID numbers (CCCD = 12 digits, CMND = 9 digits, varies by issue date).

For monetary fields, include 0, negative, very large, fractional cents, exact integer.

For dates, include past, future, leap year (Feb 29), DST boundary (if relevant), invalid format strings.

If `{field + rule}` references domain knowledge from `legacy-logic/`, cite it: "Theo `legacy-logic/auto-recharge.md`: amount > 0 và là bội số của 10,000".

## Memory Integration

**Read on activation:**
- `business-rules.md` — known constraints on this field.
- `legacy-logic/*.md` — domain conventions.
- `qa-conventions.md` — what data formats this team standardizes on.

**Write at end:**
- If a special-character category surfaces a real validation gap, suggest curating it to `common-edge-cases.md`.
- Daily log: `- {time} [DA] Test data for <field>`.

## After the Session

Note which categories {user_name} expanded — your generation should match their habits next time.
