# Fix Catalog — Auto-fix vs Manual

Defines what the migrate skill may fix automatically vs. what requires human review. Referenced in SKILL.md Step 3.

## Auto-fixable (safe, deterministic, no content loss)

These are applied by the script (`--fix` mode) or by the LLM when the user selects [F].

| Fix ID | What | How |
|---|---|---|
| `rename-srs-canonical` | Rename `srs-{story_key}.md` → `srs.md` inside story folder | `os.rename` — deterministic, reversible via git |
| `story-srs-ref-update` | Update the SRS reference link in `story.md` from old naming to `srs.md` | LLM reads file, updates the markdown link in References section, writes back |
| `design-add-status` | Insert `\| Status \| draft \|` into design doc header table if Status row is absent | LLM reads file, inserts row after the last metadata row before `---`, writes back |

## Requires Human Action (never auto-fix)

These findings are reported with guidance but not touched automatically.

| Code | Why Not Auto-fixable | Guidance for Human |
|---|---|---|
| `story-md-missing` | Cannot synthesize story content — requires product context | Run `/bmad-tts-create-story --story <key>` to generate |
| `srs-missing` | SRS content requires domain knowledge | Run `/bmad-tts-create-srs --story <key>` to generate |
| `design-missing` | Design requires architectural decisions | Run `/bmad-tts-design-story --story <key>` to generate |
| `story-ac-not-testable` | Requires PM/BA to clarify the expected outcome | Rewrite the AC with a measurable condition or error code reference |
| `story-ac-missing-error-code` | Need to know which error code applies | Add the `ERR-XXX-NNN` reference from the error code catalog |
| `story-task-ac-mismatch` | Could be a task error or an AC numbering error — ambiguous | Align task `(AC: N)` refs with the actual AC list |
| `srs-ac-story-mismatch` | Could mean story is outdated or SRS is ahead — needs product decision | Reconcile story.md and srs.md ACs; update whichever is stale |
| `srs-format-unknown` | Cannot safely reformat SRS content | Manually identify the format and restructure if needed |
| `srs-kbnv-flow-no-error-path` | Adding error paths requires domain knowledge | Add error branches to the business flow with product input |
| `srs-bdd-no-error-scenarios` | Error scenarios require acceptance criteria clarification | Add E# scenarios aligned with story ACs covering error cases |
| `srs-entity-fields-missing` | Field definitions require data modeling decisions | Add entity field definitions in the SRS data model section |
| `design-no-api-contracts` | Requires design decisions on request/response schema | Add API contract section with endpoint definitions |
| `design-no-component-breakdown` | Requires architectural decisions | Add list of files/classes to create or modify |
| `config-yaml-missing` | New config format setup | Run `/bmad-tts-setup` to register the module and write config |
| `sprint-status-missing` | Need to know which stories are in sprint | Create `_bmad-output/sprint-status.yaml` manually |
| `sprint-status-orphan-story` | Story folder exists but not in sprint-status — may be intentional | Add to sprint-status or delete folder if abandoned |

## Dry-run Output Format

When `--dry-run` is passed, report each planned fix as:

```
[DRY-RUN] Would rename: srs-1-1-story-name.md → srs.md  (in 1-1-story-name/)
[DRY-RUN] Would update: story.md link [Source: SRS 1.1](./srs-1-1-story-name.md) → ./srs.md
[DRY-RUN] Would insert: | Status | draft | into 1-1-story-name/detail-design.md header table
```

No files are written in dry-run mode.
