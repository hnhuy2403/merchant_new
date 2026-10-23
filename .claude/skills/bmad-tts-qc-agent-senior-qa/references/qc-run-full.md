---
name: qc-run-full
description: Full workflow macro — analyze → scenario → testcase → edge → review on a single requirement
code: RF
---

# Run Full Workflow

## What Success Looks Like

Given a requirement (pasted text or doc path), the owner ends with the complete chain executed end-to-end with one command: analysis → scenarios → test cases (Excel) → edge cases → review. The owner is consulted at gates between phases (with sensible defaults for "yes, continue") to allow course-correction without forcing a multi-command session.

This is the **happy path orchestrator** — for the most common QC workflow {user_name} runs.

## Your Approach

**Sequence:**

```
Stage 1: qc-test-analyze   → Markdown analysis (4 sections)
Gate:    "Analysis ready. Proceed to scenarios? (Y/n, or refine)"
Stage 2: qc-scenario       → scenario list (H/N/E)
Gate:    "Scenarios ready. Proceed to test cases? (Y/n, or refine — add/remove scenarios)"
Stage 3: qc-testcase       → .xlsx output
Gate:    "Test cases written to <path>. Proceed to edge expansion? (Y/n)"
Stage 4: qc-edge           → edge case list (Markdown)
Gate:    "Edges ready. Add to .xlsx as Suite-N: Edge cases? (Y/n) Or skip review?"
Stage 5: qc-testcase       → append edge cases to existing .xlsx (sheet append, not new file)
Stage 6: qc-review         → coverage + gaps + verdict
Final:   summary + paths to all artifacts
```

**Gate handling:**

- **Default Y** — pressing enter or saying "tiếp" / "yes" / "continue" advances. Aim to reduce friction.
- **Refine** — at any gate, {user_name} can say "thêm X" or "bỏ Y" or "đổi <field>" to refine the current stage's output before advancing.
- **Stop** — saying "dừng" / "stop" exits the macro cleanly. Already-written artifacts remain. Owner can resume manually with individual capabilities.

**Persistence:**

- **Each stage's output is preserved** — even if stage 5 fails, stages 1-4 outputs are saved to session log + artifact paths. The macro is restartable from any stage.
- **Owner can replay an early stage** — "redo stage 2 with X" rewinds without losing later work where possible.

**Final summary:**

```markdown
## qc-run-full complete

**Requirement:** <one-line summary>

**Artifacts:**
- Analysis: <inline or saved path>
- Scenarios: <inline>
- Test cases: `{output_folder}/test-artifacts/test-cases/<feature>.xlsx` (N cases, M suites)
- Edge cases: appended as Suite-K to the same .xlsx
- Review: <inline> — verdict <X>

**Total cases generated:** <N>
**Coverage estimate:** <X>%
**Recommendation for next:** <e.g. "Run /qc-codegen --target=web to generate Playwright scripts">
```

## Memory Integration

Each constituent capability handles its own memory reads/writes. The macro itself adds:

**Read on activation:**
- All curated files (the constituent caps will use them).

**Write at end:**
- Daily log: `- {time} [RF] Full workflow on <requirement>: <N cases> output, verdict <X>`.
- Personal session log: a denser entry summarizing the whole macro run, key decisions made at gates, time spent.

## After the Session

Track which gates {user_name} most often refines at — that's where your default generation is weakest. If they always refine scenarios but never test cases, scenario quality is the bottleneck to improve.
