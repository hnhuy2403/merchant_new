---
name: qc-api-case
description: API test cases — positive / negative / edge / security
code: AC
---

# API Test Cases

## What Success Looks Like

The owner ends with a structured set of API test cases for an endpoint, covering positive flows, negative flows (4xx behavior), edge cases (boundary, malformed), and security (auth bypass, injection, rate limit). Each case is concrete enough to run via curl or Postman immediately.

## Your Approach

Output structure:

```markdown
## API: `<METHOD> <path>`

**Auth:** <none / bearer / basic / API key>
**Content-Type:** <application/json | ...>

### Positive (<N>)
| # | Case | Request | Expected response |
|---|---|---|---|
| 1 | Happy path | `<body summary>` | `200`, body contains `<key>` |
| 2 | Optional field omitted | `<body>` | `200`, default applied |

### Negative (<N>)
| # | Case | Request | Expected response |
|---|---|---|---|
| 1 | Missing required field | `<body>` | `400 BAD_REQUEST`, error code `MISSING_FIELD` |
| 2 | Invalid auth token | header: `Bearer invalid` | `401 UNAUTHORIZED` |

### Edge (<N>)
| # | Case | Request | Expected response |
|---|---|---|---|
| 1 | Body at max payload | `<8MB body>` | `413` or `200` if accepted |
| 2 | Concurrent identical requests (idempotency) | 2× same `Idempotency-Key` | both return same response, no duplicate side effect |

### Security (<N>)
| # | Case | Request | Expected response |
|---|---|---|---|
| 1 | SQL injection in path param | `/users/1';DROP TABLE` | `400` or `404`, NOT `500` |
| 2 | Cross-user IDOR | other user's resource ID | `403` or `404`, never `200` |
| 3 | Rate limit | 1000 requests in 1 minute | `429 TOO_MANY_REQUESTS` after threshold |
```

**Coverage checklist** (don't skip these):
- All listed status codes from the spec must appear in at least one case.
- Authorization: missing token, invalid token, expired token, wrong role.
- Idempotency: duplicate requests, replay attacks (if `Idempotency-Key` is supported).
- Pagination: page 0, page 1, page beyond last, limit at 0, limit beyond max.
- Date/time formats: ISO-8601 vs locale strings, future dates, very old dates.

## Memory Integration

**Read on activation:**
- `business-rules.md` — domain rules that constrain valid request bodies.
- `qa-conventions.md` — does the team have a standard error code taxonomy?
- `defect-history.md` — past API bugs (especially auth / IDOR / injection).

**Write at end:**
- Recurring API patterns (e.g. "all POST endpoints in this project return `201 Created` with location header") → curate to `qa-conventions.md` API section.
- Daily log: `- {time} [AC] API cases for <METHOD path>: P/N/E/S counts`.

## After the Session

If the team uses Postman, offer to follow with `qc-curl-gen` (standalone slash skill) to produce the matching curl/Postman collection.
