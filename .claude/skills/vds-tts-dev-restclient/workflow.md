# Workflow — Generate VDS REST Client Service

**Goal:** Produce a Spring `@Service` that calls an external HTTP API, matching the project's existing outbound-integration style. Keep the output drop-in ready: compiles, follows existing naming, reuses existing `RestTemplate` bean / constants / response wrapper / exception.

## Inputs to collect (ask once, batched)

Before generating code, confirm these from the user. If any can be derived from an existing example file in the project (e.g., another `*ServiceImpl.java` in the same package), derive and confirm rather than asking:

1. **Service name** — e.g., `CustomerService` → produces `CustomerService` interface + `CustomerServiceImpl`.
2. **Target package** — e.g., `vn.com.viettel.vds.varm.service`.
3. **Config prefix** — e.g., `rest.customer-service` → expects `rest.customer-service.host` and `rest.customer-service.product` in `application.properties`.
4. **RestTemplate qualifier** — e.g., `coreRestTemplate` (look for existing `@Bean` definition; do NOT invent a new one unless asked).
5. **Endpoints** — for each method:
   - HTTP method (GET/POST/PUT/DELETE)
   - Path (e.g., `/customer/v1/validate/pin`) — **MUST** be externalised via `@Value`, never hardcoded in the Java method. Ask the user for (or derive) a property key such as `customer.validate.pin.url` and a matching field name (`validatePinUrl`).
   - Request body DTO (if any) and query params (if any)
   - **Response return type** — the full Java return type of the method, which determines the `ParameterizedTypeReference` as well. Any type is allowed, e.g.:
     - `GeneralResponse<CustomerDTO>` — VDS-wrapped payload
     - `CustomerDTO` — raw DTO returned directly by the external API
     - `List<ItemDTO>`, `Map<String, Object>`, `String`, `Void` — any other shape
     Ask/confirm the exact type rather than assuming `GeneralResponse<T>`. Look at the external API doc or a sibling `*ServiceImpl` for precedent.
   - Whether admin token header is required
   - Failure status code enum value (e.g., `ResponseStatusCodeEnum.VALIDATE_PIN_FAILED`)
6. **Existing project artifacts to reuse** — scan for:
   - `HeaderConstant` (PRODUCT, AUTHORIZATION keys)
   - `Constant` (common request values)
   - `GeneralResponse` response wrapper
   - `BaseResponseException`
   - `ResponseStatusCodeEnum`
   - `token.admin.role` property (only if admin auth is needed)

   If any are missing from the target project, flag it — do not fabricate replacements.

## Steps

1. **Probe project structure.** Glob for one existing `*ServiceImpl.java` under `service/impl/` in the target project. Read it to lock in the exact imports, naming, and logging style. This is the source of truth over the template.
2. **Diff template vs. probed style.** If the project diverges (different response wrapper, no `@Qualifier`, different exception type), adapt — follow the project, not the template.
3. **Generate the interface** (`<Name>Service`) with the method signatures only.
4. **Generate the impl** (`<Name>ServiceImpl`) from `./template.java.md`, substituting all placeholders. One method per endpoint.
5. **Add properties to `application.properties`.** Locate the file under `src/main/resources/application.properties` (or project equivalent). Append a new grouped block at the end of the file, preceded by a `# <service-name> config` comment header matching the existing style (see `# customer service config`, `# sof recommendation service config`, etc.). Add:
   - `{{CONFIG_PREFIX}}.host=http://gw-staging.digital.vn` — **default host** unless the user specifies another. Always use `http://gw-staging.digital.vn` as the fallback staging gateway for this project.
   - `{{CONFIG_PREFIX}}.product=<PRODUCT_VALUE>` — reuse an existing product code if the user didn't give one (e.g. `VIETTELPAY`), otherwise use the given value.
   - One `{{URL_PROPERTY}}=<path>` line per endpoint with the path provided by the user (or a placeholder like `/TODO/fill-in` if not given — flag this back so they remember).
   - Do NOT duplicate `token.admin.role` if it already exists in the file.
   Check for duplicate keys before appending; if a key already exists, skip it and report.
6. **Self-check against `./checklist.md`.** Fix any misses before presenting.
7. **Present** the file path(s), a one-line summary of each generated method, AND the exact property lines that were appended to `application.properties` (so the user can review / tweak host + path without hunting).

## Rules

- Do not introduce new dependencies, new `RestTemplate` beans, or new exception types.
- Do not add retries, circuit breakers, or caching unless the user asks.
- Keep logging minimal: one `log.error(..., e)` in the catch, optional single `log.info` on success (match existing style — if the probed example has no info log, omit it).
- Never put secrets or tokens in code — always `@Value`-inject.
- Comments: none, unless a non-obvious constraint warrants one line.
- If the user gives a language preference in chat, respond in that language; code artifacts themselves stay standard (English identifiers, Vietnamese allowed only in log messages if the existing project does so).
