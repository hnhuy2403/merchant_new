# Design Doc Self-Review Checklist

Apply this checklist to the draft design doc before adversarial review. For each failed item, fix the design doc directly. Items that genuinely require user input go to **Open Questions**, not the failure pile.

## Story alignment

- [ ] Every Acceptance Criterion in the story file has at least one explicit handling in the design (component, data flow, API, or test).
- [ ] No design decision contradicts the story's Dev Notes (architecture, tech stack, file layout). If it must contradict, the rationale is recorded in **Open Questions / Risks**.
- [ ] Out-of-scope items mentioned in the story are explicitly marked out of scope here, not silently included.

## Component & code surface

- [ ] Every new/modified module, class, or function appears in **Component Breakdown** with a real name, signature, and single-sentence responsibility — no placeholder names like `Helper` or `doStuff`.
- [ ] Every existing file the design touches has been opened and read; precise changes are described in **File Changes** (e.g. "extract method X from class Y into helper Z"), not vague verbs.
- [ ] No `// TODO` or `[fill in later]` placeholders remain in the design doc.

## Data & flow

- [ ] If schema changes exist, the design lists added/modified/removed columns with type, nullability, default, and migration notes.
- [ ] The primary happy path is captured as a Mermaid sequence diagram with concrete actor/component names — not generic boxes.
- [ ] Stateful entities have explicit state transitions; concurrency assumptions (locks, ordering, idempotency) are stated where relevant.
- [ ] **No foreign key constraint** (Architecture Rule #11). DDL must NOT declare `FOREIGN KEY`. JPA entity must NOT use `@ManyToOne` / `@OneToMany` / `@JoinColumn` for cross-table linkage. Relationships are enforced at service layer with pre-check queries inside transactions. If a design needs FK, the rationale must be in **Open Questions** for tech-lead override.
- [ ] **Local datetime for timestamps** (Architecture Rule #16). Entity fields like `createdAt`, `updatedAt`, `assignedAt`, `occurredAt` use `java.time.LocalDateTime` — NOT `Instant` / `OffsetDateTime` / UTC.
- [ ] **No event-for-cache-invalidation** (Architecture Rule #17). If the design proposes publishing a Kafka/outbox event whose ONLY purpose is to invalidate consumer cache, REMOVE it — consumer handles staleness via TTL (5-10s) or invalidate-on-demand. Events are reserved for real-time business reactions (downstream workflow trigger, cross-service state sync, mandatory audit trail). Each retained event must justify "what nghiệp vụ reaction the consumer triggers" in the design doc.
- [ ] **SQL column comments** (Architecture Rule #18). Every `CREATE TABLE` / `ALTER` / migration block has a short inline `-- <Vietnamese name>` comment after every column definition (e.g. `name VARCHAR(200) NOT NULL, -- Tên sản phẩm`). Comments are just the column's business meaning — NOT architecture rationale, FK notes, or nullable reasons. Table / constraint / index comments are NOT required.

## API contracts (if applicable)

- [ ] Every endpoint has full request/response schema, validation rules, status codes for success and error, and a concrete error shape.
- [ ] Idempotency, retry behavior, and auth requirements are stated. "Default behavior" is not acceptable — say what it is.
- [ ] **Response envelope `GeneralResponseV2<T>`** (Architecture Rule #12) is used in every response sample. Success path shows `status.code = "00"`; error path shows `status.code = "<DOMAIN>-XXX"` with `data: null` or partial. Controller must NOT build error responses directly — `BaseResponseExceptionV2` + global handler pattern only.
- [ ] **All HTTP responses use status 200** (Architecture Rules #14, #15). Business success/error codes live in `status.code` of envelope — NOT in HTTP status. Do NOT use 201/204/2xx-non-200, 4xx-business, 5xx for business outcomes. **Allowed exceptions** (must be in design doc): `401` (no token), `403` (auth filter rejects token: invalid/expired/missing scope), `400` (framework body parse fail). Service / controller layer must NOT manually throw 401/403/400 — only the auth filter / framework does.
- [ ] **Design references upstream + downstream** (Architecture Rule #13). Every cross-reference in the design doc points to a concrete artifact (file path with section anchor, API contract URL, PR URL) — not generic mentions like "phụ thuộc story 1.x".

## Edge cases & errors

- [ ] At least three meaningful edge cases are enumerated with chosen handling. If fewer, the design explicitly justifies why this feature has a small failure surface.
- [ ] Each edge case has a handling decision (not "TBD"). Items that genuinely cannot be decided live in **Open Questions** with an owner.

## Test plan

- [ ] Each Acceptance Criterion is mapped to at least one concrete test name (unit, integration, or e2e).
- [ ] Test names are specific enough that the dev can author them directly — not "test login works" but `LoginRejectsExpiredTokenWith401`.

## Self-coherence

- [ ] No section is empty. Sections that genuinely do not apply (e.g. no API surface) carry an explicit "N/A — reason" line, not silence.
- [ ] The design doc's Open Questions section honestly captures every unresolved decision. If you found yourself guessing, the guess is logged as a risk.
- [ ] A competent dev who has never seen this story could read the design doc end-to-end and start coding without a clarification meeting.
