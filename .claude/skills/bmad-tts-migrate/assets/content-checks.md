# Content Quality Checks — Evaluation Rubric

This rubric guides the LLM content evaluator for each story's artifacts. Return compact JSON per the schema in SKILL.md Step 2. Only report findings with genuine quality concerns — do not flag style preferences or minor phrasing.

## Severity Levels

- `error` — Missing required content that blocks implementation or review (AC not testable, missing entity definition, no API contracts when designed)
- `warning` — Content present but incomplete, inconsistent, or likely to cause rework
- `info` — Enhancement opportunity; does not block work

## Check Codes and Criteria

### story.md Checks (`story_checks`)

| Code | Severity | Trigger Condition |
|---|---|---|
| `story-ac-not-testable` | warning | An AC item describes behavior in vague terms without a measurable outcome (e.g. "works correctly", "handles properly", "good performance") — flag the specific item |
| `story-ac-missing-error-code` | warning | AC describes an error scenario but no error code is referenced (e.g. "returns error" without `ERR-XXX-NNN`) |
| `story-tasks-no-ac-ref` | warning | Task list exists but no tasks reference their corresponding ACs (e.g. no `(AC: N)` annotations at all in the task list) |
| `story-task-ac-mismatch` | warning | A task references an AC number that does not exist in the AC list (off-by-one, typo, or stale reference) |
| `story-dev-notes-empty` | warning | Dev Notes section is present but contains less than 3 substantive lines — likely a placeholder with no useful context |
| `story-dev-notes-no-tech-stack` | info | Dev Notes does not mention the technology stack or framework being used |
| `story-design-ref-broken` | error | Story references a design doc path but the path uses the old root-level naming convention (`{implementation_artifacts}/{story_key}-design.md`) instead of the canonical folder path (`{story_key}/detail-design.md`), or uses an absolute path instead of a relative one |
| `story-srs-ref-broken` | warning | Story references an SRS file by old naming convention (`srs-{story_key}.md`) rather than `srs.md` |
| `story-status-inconsistent` | warning | Story `Status` field does not align with what's present: `designed` but no design doc reference found; `in-progress` or `done` but task checkboxes are all unchecked |
| `story-no-project-structure` | info | Dev Notes has no `Project Structure` or package/path notes — harder for dev agents to place new files correctly |

### srs.md Checks (`srs_checks`)

**Detect SRS format first:**
- **KBNV format**: Contains sections like `Luồng nghiệp vụ`, `Activity diagram`, `Điều kiện`, `Bước`
- **BDD format**: Contains sections like `Bối cảnh nghiệp vụ`, scenario headers with `H#`/`E#`/`R#` codes, `Tiêu chí chấp nhận`
- **Unknown format**: Neither pattern matches — report `srs-format-unknown` (warning) and skip format-specific checks

#### Common Checks (both formats)

| Code | Severity | Trigger Condition |
|---|---|---|
| `srs-format-unknown` | warning | SRS content does not match KBNV or BDD format patterns — may be an older or custom format |
| `srs-placeholder-found` | warning | SRS contains obvious placeholder text: `[TODO`, `[TBD`, `[PLACEHOLDER`, `<<`, `>>`, `???` |
| `srs-ac-story-mismatch` | error | SRS defines ACs that do not align with story.md ACs (numbering gap > 2, or an AC described in SRS is missing from story, or vice versa) — only flag clear mismatches, not minor phrasing differences |
| `srs-no-error-codes` | warning | SRS describes error scenarios but no error codes (e.g. `ERR-XXX-NNN` or `CAT-ADM-NNN` pattern) appear anywhere in the document |
| `srs-business-rules-sparse` | info | SRS has fewer than 3 business rules (BR-N items or equivalent) despite story having 5+ ACs — may indicate incomplete BRs |
| `srs-entity-fields-missing` | warning | SRS mentions entities or data models but does not define field names, types, or constraints — only flag when entity section header is present but field list is absent |

#### KBNV-specific Checks

| Code | Severity | Trigger Condition |
|---|---|---|
| `srs-kbnv-no-activity-diagram` | info | KBNV format but no Activity diagram (Mermaid or textual) present |
| `srs-kbnv-flow-no-error-path` | warning | Business flow (Luồng nghiệp vụ) section has happy-path steps but no error/exception branches described |

#### BDD-specific Checks

| Code | Severity | Trigger Condition |
|---|---|---|
| `srs-bdd-no-error-scenarios` | warning | BDD format has H# happy-path scenarios but no E# error scenarios despite story ACs covering error cases |
| `srs-bdd-scenario-no-steps` | warning | A scenario heading (H# or E#) exists with no Given/When/Then or step list beneath it |
| `srs-bdd-r-codes-missing` | info | BDD format with no R# (rule/constraint) codes even though story has explicit constraints |

### design doc Checks (`design_checks`)

Only run these checks if a design doc file is present for the story.

| Code | Severity | Trigger Condition |
|---|---|---|
| `design-no-status` | warning | Header metadata table lacks a `Status` row (draft / in-review / approved) |
| `design-no-api-contracts` | error | Story has API tasks (endpoints in task list or AC) but design doc has no API contract section with request/response definitions |
| `design-api-contracts-incomplete` | warning | API contract section exists but at least one endpoint is listed without request body schema, response schema, or status codes |
| `design-no-db-schema` | warning | Story creates new entities (DB migration task) but design doc has no schema section with table/field definitions |
| `design-no-component-breakdown` | warning | Design doc does not identify which classes/packages/modules will be created or modified — harder for dev agent to start |
| `design-no-sequence-diagram` | info | No sequence or flow diagram (Mermaid) present — often helpful for multi-service or async flows |
| `design-file-changes-empty` | warning | File Changes table exists but has no rows — should list at minimum the files the dev agent will create |
| `design-placeholder-found` | warning | Design doc contains obvious placeholder text: `[TODO`, `[TBD`, `[PLACEHOLDER`, `???` |
| `design-ac-coverage` | warning | Design doc does not address at least one AC from the story — specifically, if an AC describes a system behavior (not just "create X") and no design section covers how it will be implemented |

## Evaluation Instructions

1. Read each artifact fully before generating findings.
2. Apply only checks relevant to what is present (e.g. skip `design_checks` if no design doc).
3. For `srs_checks`, detect format first — KBNV or BDD — then apply the appropriate subset.
4. Avoid hallucinating missing content — if a section is present but brief, check if the brevity is a genuine gap vs. an intentionally minimal spec.
5. Cross-reference story.md ↔ srs.md ACs: mismatches are errors; minor phrasing differences are not.
6. Return only findings that meet the trigger condition. If no issues found for a document, return an empty array for that key.

## Output Schema

```json
{
  "story_key": "1-1",
  "story_checks": [
    { "code": "story-ac-not-testable", "severity": "warning", "message": "AC 3: 'works correctly' is not measurable — specify the expected system response or error code." }
  ],
  "srs_checks": [
    { "code": "srs-bdd-no-error-scenarios", "severity": "warning", "message": "No E# error scenarios found despite 6 ACs covering error conditions." }
  ],
  "design_checks": []
}
```
