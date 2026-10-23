---
name: bmad-tts-qc-sql-snippet
description: Quick one-shot SQL helper — given scenario + schema, returns SQL with brief explanation. Use when the user runs /bmad-tts-qc-sql-snippet or asks for an ad-hoc SQL verification query without project context.
---

# QC SQL Snippet

## Overview

One-shot SQL helper. User provides scenario + table schema → get SQL back. Light, stateless, no memory or persona. The heavier `qc-sql-bug` capability (which mines `defect-history.md`) lives in the `/bmad-tts-qc-agent-senior-qa` agent.

## On Activation

1. Parse args:
   - **scenario** (required) — what the SQL should verify, e.g. "find users who registered in last 7 days but haven't completed OTP".
   - **schema** (required) — table(s) + columns. Inline format: `users(id, phone, registered_at, otp_verified_at)` or pasted DDL.
   - **dialect** (optional, default `auto`) — `postgres` / `mysql` / `mssql` / `sqlite` / `oracle` / `auto`. If `auto`, target ANSI SQL with notes where dialects diverge.

2. If `{project-root}/_bmad/memory/tts-qc/curated/project-profile.md` exists, check for the team's DB engine and use it as default dialect. Otherwise proceed without.

3. Generate SQL.

## Output Format

```sql
-- Scenario: <one-line summary>
-- Dialect: <postgres / mysql / etc.>

SELECT ...
FROM ...
WHERE ...
LIMIT 100;
```

Followed by a short explanation:

```markdown
**What it does:** <1-2 sentence summary>

**Why these joins / filters:** <1-2 sentences if non-obvious>

**Caveats:** <if any — e.g. "assumes phone is unique; adjust if not">
```

## Style

- **Always include `LIMIT`** for unbounded selects on production-shaped tables — safety first.
- **Read-only by default** — if the scenario implies a mutation, refuse and suggest the user run via a transaction with rollback.
- **Cite assumptions** — if the schema is incomplete, state assumptions clearly.
- Keep query indented and readable; avoid one-line SQL.
- For production-sensitive queries (PII columns), suggest hashing or anonymizing.

## Cross-skill notes

- For **bug investigation SQL** (mining defect history, multi-step hypothesis-driven queries), invoke the `qc-sql-bug` capability on `/bmad-tts-qc-agent-senior-qa` instead.
- This skill writes no memory.
