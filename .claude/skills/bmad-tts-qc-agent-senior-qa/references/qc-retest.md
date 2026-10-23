---
name: qc-retest
description: Targeted retest plan after a bug fix — verify the fix + spot-check adjacent areas
code: RT
---

# Retest Plan

## What Success Looks Like

After a bug fix is deployed, the owner ends with a focused retest plan: the minimal steps to confirm the fix works, plus a small set of adjacent area spot-checks to catch fix-induced regressions. The plan must be executable in under 30 minutes for a typical bug; longer for complex fixes.

## Your Approach

Output structure:

```markdown
## Retest plan: <bug ID / title>

**Fix description:** <one-line summary of what was changed>
**Original reproduction:** <how the bug was first reproduced>
**Risk if fix is incomplete:** <what could still be broken>

### A. Verify the fix (must pass)
1. <reproduce original bug exactly — must NOT reproduce now>
2. <variant 1 of the bug — must NOT reproduce>
3. <variant 2 — must NOT reproduce>

### B. Spot-check adjacent areas (verify fix didn't break neighbors)
1. <related happy path — must still pass>
2. <related boundary — must still pass>
3. <flow that touches the same code — verify>

### C. Cross-platform verification (if relevant)
- iOS: <step>
- Android: <step>
- Web: <step>

### D. Regression suite hint
- Run regression suite for `<module>` if available
- If suite covers this area, the suite gates merge; if not, add a case via `/qc-regression-suggest`

**Time estimate:** <X> minutes
```

**Discipline:**

- **Verify the original repro path first** — the fix should make the original bug disappear. If you can't reproduce the original anymore (unrelated env change), call that out — don't pass without verifying.
- **Variants matter** — fixes often miss variants. If the bug was "submit button doesn't work when X", test "doesn't work when X+Y" and "doesn't work when X without Y".
- **Spot-checks are limited** — 3-5 max. The regression suite handles broader coverage; this plan is targeted.
- **Don't re-run the whole test suite** — that's not a retest, that's a regression run. Use `/qc-regression-suggest` for suite-level work.

Pull the original bug entry from `defect-history.md` if available — that gives you the exact reproduction path and any known variants.

## Memory Integration

**Read on activation:**
- `defect-history.md` — original bug entry, related past bugs.
- `legacy-logic/` — domain knowledge about adjacent areas.

**Write at end:**
- Update `defect-history.md` entry: status = "Fixed and retest passed" (or "Fixed but variant remained"), date, who retested.
- Daily log: `- {time} [RT] Retest plan for <bug>: <pass/fail/pending>`.

## After the Session

If the retest fails (variant not fixed), trigger `/qc-rootcause` on the variant. If a fix-induced regression is found, file via `/qc-bug` and link back to the original.
