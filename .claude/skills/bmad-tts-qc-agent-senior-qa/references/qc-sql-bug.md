---
name: qc-sql-bug
description: SQL queries to investigate root cause of a bug, drawing on defect history
code: SB
---

# SQL for Bug Investigation

## What Success Looks Like

The owner ends with a sequence of SQL queries — each labeled with what it checks, why it's running, and what result would confirm or rule out a hypothesis. Queries are **safe to run on production** by default (read-only, no destructive ops, no `UPDATE`/`DELETE`/`DROP`). If a query needs production data scope, it includes `LIMIT` and a hashed/anonymized key suggestion where applicable.

## Your Approach

Output structure:

```markdown
## SQL investigation: <bug summary>

**Hypotheses to test:**
1. <hypothesis 1>
2. <hypothesis 2>
3. ...

### Q1 — <one-line purpose>
**Tests hypothesis:** #1
**Why:** <what we expect to learn>

\```sql
SELECT ...
FROM ...
WHERE ...
LIMIT 100;
\```

**Interpretation:** if <result>, then <conclusion>.

### Q2 — <purpose>
...
```

**Hypothesis sources** (in order):
1. `defect-history.md` — past bugs with similar symptoms. "This looks like the auto-recharge race condition from Q2/2025 — let's check `transaction_log` for double-entries first."
2. **Surface-area heuristics** — payment / auth / state machines / async jobs / cache layers are top suspects.
3. **Time correlation** — when did the bug start? `WHERE created_at BETWEEN ... AND ...` to scope to the bug window.

**Safety rules:**
- Never write a query that mutates data.
- Always include `LIMIT` for unbounded selects on production-sized tables.
- When dealing with PII, recommend column hashing or anonymization rather than selecting raw values.
- Mark queries that need elevated access ("requires DBA: needs read on `audit_log_v2`").

## Memory Integration

**Read on activation:**
- `defect-history.md` — past similar bugs and the SQL that found them. Reuse and adapt.
- `project-profile.md` — DB engine (Postgres / MySQL / SQL Server) — syntax differs.
- `legacy-logic/<topic>.md` — schema knowledge if curated.

**Write at end:**
- When the investigation finds the root cause, **append the bug + root SQL to `defect-history.md`**: bug summary, suspected root cause, the diagnostic SQL, the fix area. This becomes pattern-match gold for future bugs.
- Daily log: `- {time} [SB] SQL investigation for <bug>: <N> queries → <conclusion>`.

## After the Session

If a recurring schema pattern emerges across bugs (e.g. "transactions table needs a status_change_log to debug these"), suggest curating to `legacy-logic/`. SQL skill grows with project memory — every solved bug makes the next one faster.
