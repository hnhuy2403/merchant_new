---
name: bmad-tts-qc-curl-gen
description: Generate curl + Postman-importable request from a brief API description. Use when the user runs /bmad-tts-qc-curl-gen or asks for a curl command / Postman request from an endpoint description.
---

# QC Curl & Postman Gen

## Overview

Quick API request generator. Given endpoint description, produces ready-to-run curl command + Postman-importable JSON. Light, stateless. The heavier `qc-api-case` capability (which generates full test case sets with project conventions) lives in the `/bmad-tts-qc-agent-senior-qa` agent.

## On Activation

1. Parse inputs (in args or pasted body):
   - **endpoint** (required) — `<METHOD> <URL>`, e.g. `POST https://api.example.com/v1/recharge`.
   - **body shape** (required for POST/PUT/PATCH) — described or sample JSON.
   - **auth** (optional) — `bearer <token>` / `basic <user:pass>` / `none` / `header X-API-Key: ...`.
   - **headers** (optional) — extra headers.
   - **path/query params** (optional) — describe.

2. If `{project-root}/_bmad/memory/tts-qc/curated/project-profile.md` exists, check for the project's standard headers (e.g. `X-Tenant-Id`) and apply automatically; otherwise skip.

## Output Format

Two sections — curl and Postman:

```markdown
### curl

\```bash
curl -X POST 'https://api.example.com/v1/recharge' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <YOUR_TOKEN>' \
  -d '{
    "accountId": "0123456789",
    "amount": 50000,
    "idempotencyKey": "<uuid>"
  }'
\```

### Postman (paste into Import → Raw text)

\```json
{
  "info": { "name": "<endpoint name>", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json" },
  "item": [{
    "name": "<request name>",
    "request": {
      "method": "POST",
      "header": [
        { "key": "Content-Type", "value": "application/json" },
        { "key": "Authorization", "value": "Bearer {{token}}" }
      ],
      "body": {
        "mode": "raw",
        "raw": "{\\"accountId\\": \\"0123456789\\", \\"amount\\": 50000, \\"idempotencyKey\\": \\"{{$guid}}\\"}"
      },
      "url": { "raw": "https://api.example.com/v1/recharge" }
    }
  }]
}
\```

### Variables to set
- `{{token}}` — auth bearer token (Postman environment variable)
- `{{$guid}}` — Postman built-in for unique idempotency key
```

## Style

- **Sample body fields populate with plausible values** — for unknown fields, use realistic placeholders.
- **Idempotency / dedup headers** — if the endpoint looks like a mutation, suggest `Idempotency-Key` header.
- **Don't hardcode secrets** — auth tokens / API keys → `<YOUR_TOKEN>` placeholder or Postman variable.
- Always include `Content-Type: application/json` for JSON bodies.
- For multipart, generate the right boundary syntax with placeholder file paths.

## Cross-skill notes

- For **full API test case sets with project conventions** (positive / negative / edge / security), invoke the `qc-api-case` capability on `/bmad-tts-qc-agent-senior-qa` instead.
- For **validation guidance** (what to check in the response), invoke the `qc-api-validate` capability on `/bmad-tts-qc-agent-senior-qa`.
- This skill writes no memory.
