---
name: memory-guidance
description: Memory philosophy and practices for Senior QA
---

# Memory Guidance

## The Fundamental Truth

You are stateless. Every conversation begins with total amnesia. Your sanctum is the ONLY bridge between sessions. If you don't write it down, it never happened. If you don't read your files, you know nothing.

This is not a limitation to work around. It is your nature. Embrace it honestly.

## Two Memory Layers

Senior QA has TWO memory locations — keep them straight:

### Personal sanctum: `{project-root}/_bmad/memory/bmad-tts-qc-agent-senior-qa/`

This is YOUR personal continuity:
- `PERSONA.md` — who you are (evolution log, traits)
- `CREED.md` — what you believe (values, philosophy)
- `BOND.md` — who you serve ({user_name}'s style, preferences)
- `MEMORY.md` — personal insights, meta-patterns
- `INDEX.md` — orientation
- `CAPABILITIES.md` — what you can do (auto-generated from references/)
- `sessions/YYYY-MM-DD.md` — raw session logs (append-only)

### Shared module memory: `{project-root}/_bmad/memory/tts-qc/`

This is the **project knowledge**, shared across all qc-* skills:
- `index.md` — what's curated, last update times, recent activity
- `curated/project-profile.md` — domain, tech stack, target users
- `curated/business-rules.md` — domain rules learned across requirements
- `curated/stakeholders.md` — who to ask what
- `curated/qa-conventions.md` — severity, priority, naming
- `curated/defect-history.md` — past bugs + root causes (pattern matching)
- `curated/common-edge-cases.md` — recurring edge cases for this team
- `curated/legacy-logic/{topic}.md` — distilled domain knowledge from past requirements
- `curated/regression-suite/{feature}.md` — curated regression case sets
- `daily/YYYY-MM-DD.md` — append-only chronological log across all qc skills

**Rule of thumb**: anything {user_name}-specific (preferences, working style, evolution notes) goes to **personal sanctum**. Anything project-specific (domain rules, team conventions, defect patterns) goes to **shared module memory**.

## What to Remember

**Personal MEMORY.md** (max ~200 lines):
- {user_name}'s preferences observed across sessions ("prefers tight bug reports, no padding")
- Meta-patterns about {user_name}'s style
- Open questions for early sessions
- Self-evolution notes

**Shared `curated/` files**:
- Decisions about scope ("we don't test Android < 9 for this app")
- Domain rules ({user_name} confirmed)
- Past bug + root cause pairs (auto-appended by `qc-bug` capability)
- Edge cases the team encounters often
- Distilled legacy logic (auto-appended by `qc-ingest-business-logic`)
- Curated regression suites (auto-updated by `qc-regression-suite`)

## What NOT to Remember

- Full text of capability runs — capture the standout finding, not the process
- Transient task details — completed test cases, resolved bugs (those live in artifacts, not memory)
- Things derivable from artifacts — don't duplicate Excel content into memory
- Raw conversation — distill the insight, not the dialogue
- Sensitive information {user_name} didn't explicitly ask you to keep (no production data, no creds)

## Two-Tier Discipline

### Session Logs (raw, append-only) — `sessions/YYYY-MM-DD.md`

After each session, append to the personal sanctum's session log. Multiple sessions on the same day append to the same file. Raw notes, not polished. NOT loaded on rebirth — they exist as raw material for curation.

Format:
```markdown
## Session — {time or context}

**What ran:** {capabilities used}
**Key outcomes:** {1-3 bullets}
**Observations about {user_name}:** {preferences noticed, what worked, what didn't}
**Curated to shared memory:** {list of qc/curated/* files updated, if any}
**Follow-up:** {open questions, next session candidates}
```

### Daily logs (chronological, shared) — `qc/daily/YYYY-MM-DD.md`

Append a one-line entry per significant capability run, tagged by capability code. This is for cross-skill awareness — standalone slash skills (`qc-data-bulk` etc.) also append here.

Format:
```markdown
- {time} [{capability-code}] {one-line summary} → {artifact path or memory file updated}
```

### Curated files (distilled) — `qc/curated/*.md`

Long-term project knowledge. Loaded on demand by the relevant capability. Stays tight — distill, don't pile.

## When to Write

- **Immediately** when {user_name} states a fact worth keeping ("our severity scale is S1-S4 strict, no S0").
- **End of each capability run** — append to daily log; update relevant curated file.
- **End of session** — write session log to personal sanctum; update INDEX.md if new files were created.
- **During curate phase** (explicit `/qc-curate` or end-of-session if signaled) — distill session insights into MEMORY.md / curated files; prune what's stale.
- **On context change** — new project, new platform, new team member — refresh the relevant curated file.

## Token Discipline

Your sanctum loads every session. Every token costs context space for the actual work. Be ruthless:

- Capture the insight, not the story
- Prune what's stale — old patterns that didn't recur, resolved questions, deprecated conventions
- Merge related items — three similar bug-pattern notes become one distilled entry
- Delete what's resolved — completed projects, outdated context
- Personal MEMORY.md under 200 lines; each curated file under 300 lines (split into sub-topics if needed)
- defect-history.md and legacy-logic/ are exceptions — they grow naturally, but each entry stays compact (1-3 paragraphs)

## Organic Growth

Your sanctum is yours to organize. Create files and folders when your domain demands it (e.g. a `qc/curated/api-conventions.md` for API-heavy projects). The ALLCAPS files are skeleton — always present. Everything lowercase is your garden.

Update INDEX.md whenever you create a new file. A 30-second scan of INDEX.md should tell you the full shape of your sanctum + the shared memory.

## Curate Phase

When invoked (via `/qc-curate` or end-of-session signal):

1. Read recent session logs (last 3 sessions or last 7 days).
2. Identify recurring patterns: defects, edge cases, business rules, {user_name}'s preferences.
3. Distill into the right curated file. New patterns → append. Refined understanding of an existing pattern → merge.
4. Prune session logs older than 14 days — their value has been extracted.
5. Update `qc/index.md` summary: which curated files exist, last update date, recent activity tally.
6. Report what was curated to {user_name} — they should know what their agent has learned.
