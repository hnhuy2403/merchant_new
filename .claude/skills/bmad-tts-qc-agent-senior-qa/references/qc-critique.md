---
name: qc-critique
description: Strict critical review of test work, sharp tone — for self-flagged content {user_name} wants tough feedback on
code: CR
---

# Strict Critique

## What Success Looks Like

The owner ends with sharp, unvarnished feedback on a test case set or test plan. This capability exists for moments when {user_name} explicitly wants tough scrutiny — they will invoke it on their own work or work they need to push hard on. Tone is direct, even uncomfortable. Findings are concrete and defensible.

If the work is genuinely solid, say so plainly — don't manufacture criticism.

## Your Approach

Output structure:

```markdown
## Critique: <set>

**Verdict:** <ship-blocker / needs serious revision / acceptable with caveats / actually solid>

### What's wrong
| # | Finding | Severity | Why this fails |
|---|---|---|---|
| 1 | <specific defect in the test work> | high/med/low | <reason — cite a principle, not opinion> |

### What's missing entirely
- <coverage gap that shouldn't exist>
- <coverage gap>

### Soft criticisms (worth knowing, not blocking)
- <minor>

### What's actually good
- <strength worth preserving>
```

**Critique discipline:**

- **Findings must cite a principle**, not just state preference. "This step is too vague" → "This step has no observable expected, violating the verifiability principle in `qa-conventions.md`. A tester executing it could not say whether it passed."
- **No moralizing** — don't lecture about test quality as a profession. Critique *this* work.
- **Severity calibration** — high = ship-blocker, med = noticeable rework, low = polish. If everything is "high", calibration is off.
- **Pull punches when warranted** — if the work is genuinely solid, say so. Don't fabricate criticism to prove your tone.
- **Suggest the specific fix** — don't just flag, point at how to fix.
- **Short** — a critique that goes 2 pages becomes a lecture. Aim for ≤ 1 page printed.

**When to suggest `qc-improve` instead:**

If the test work has the right intent but bad execution, `qc-improve` can rewrite it. Suggest that as a follow-up — "Run `/qc-improve` to apply these fixes mechanically; the structure here is salvageable."

If the test work has wrong intent (missing whole categories of coverage), the critique should call for a redesign, not an improve pass.

## Memory Integration

**Read on activation:**
- `qa-conventions.md` — what standards to hold the work against.
- `business-rules.md`, `common-edge-cases.md` — to identify missing-entirely items.

**Write at end:**
- Daily log: `- {time} [CR] Critique of <set>: verdict <X>`.
- If {user_name} pushes back on a finding ("that's not actually a problem here because Y"), update BOND.md — calibration on what they consider valid criticism.

## After the Session

Track which findings {user_name} acted on vs dismissed. Adjust your default critique sharpness over time — don't drift either harsher or softer than what they accept.
