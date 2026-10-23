---
name: qc-api-validate
description: Validation guide for an API response — status code, body, schema, side effects
code: AV
---

# API Response Validation

## What Success Looks Like

The owner ends with a structured validation guide for one API endpoint that any tester could apply to verify a response is correct. Covers status code, body structure, body content, schema/typing, and observable side effects (DB rows, audit log, cache, downstream events).

## Your Approach

Output structure:

```markdown
## Validation guide: `<METHOD> <path>`

### Status code
- ✅ `<code>` — <when>
- 🚫 Anything else — fail with reason from `error_code` body field

### Response body — structure
\```json
{
  "field1": "<type, required>",
  "field2": <type, optional>,
  "nested": {
    "sub": "<type>"
  }
}
\```

### Response body — content
| Field | Validation |
|---|---|
| `field1` | matches pattern `<regex>` |
| `field2` | within range `[min, max]` |
| `nested.sub` | one of `[a, b, c]` |

### Schema (if formal contract exists)
- Validate against `<spec file path>` using `jsonschema` lib or Postman test script.

### Side effects to verify
| Where | What | How to check |
|---|---|---|
| DB table `transactions` | new row with status=`pending` | `SELECT … WHERE id = <returned_id>` |
| Audit log | event `transaction_created` | `SELECT … FROM audit_log WHERE …` |
| Cache | key `tx:<id>` populated | `redis-cli GET tx:<id>` |
| Downstream queue | message in `tx-events` queue | check queue depth or consumer log |

### Negative validations (must NOT happen)
- ❌ Duplicate rows (idempotency check)
- ❌ Stale cache entries
- ❌ PII in audit log unmasked
```

**Validation discipline:**
- Schema validation alone is necessary but not sufficient — content rules and side effects matter more.
- Side effects are where async bugs hide (e.g. response says `success` but DB insert fails silently).
- Always include at least one negative validation (what should NOT happen).

## Memory Integration

**Read on activation:**
- `qa-conventions.md` — team's standard validation policy (do they require schema validation? side-effect checks?).
- `defect-history.md` — past API bugs caused by missing validation steps.

**Write at end:**
- If a side-effect validation pattern recurs (audit log + cache + downstream queue), promote to `qa-conventions.md` as a template.
- Daily log: `- {time} [AV] Validation guide for <endpoint>`.

## After the Session

Note any team-specific contract conventions {user_name} mentions — promote to `qa-conventions.md` (e.g. "we always return `error_code` and `error_message`, never just HTTP status").
