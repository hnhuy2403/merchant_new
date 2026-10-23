# Self-Verification Checklist

Run through this before presenting generated files. Fix any miss.

## Structure
- [ ] Interface in `service/interfaces/` (or matching project convention); impl in `service/impl/`.
- [ ] Class annotated with `@Service` and `@Slf4j`.
- [ ] Constructor-injected `RestTemplate` with `@Qualifier`. No field injection.
- [ ] `@Value` fields for host + product; no hardcoded URLs or tokens.
- [ ] **Every endpoint path is a separate `@Value`-injected field** (e.g. `@Value("${customer.validate.pin.url}") private String validatePinUrl;`). No literal path string (`"/foo/bar"`) appears anywhere in a method body — reject the output if any method still has a hardcoded path.
- [ ] `tokenAdmin` field only present if at least one method uses it.

## Per method
- [ ] `HttpHeaders` built fresh inside each method (not shared across methods).
- [ ] `HeaderConstant.PRODUCT` set on every call.
- [ ] `HeaderConstant.AUTHORIZATION` set iff the endpoint requires admin token.
- [ ] URL built via `UriComponentsBuilder`; `.encode()` called; no string concatenation of user input into URL.
- [ ] Query params added via `builder.queryParam(...)`, not string concat.
- [ ] `restTemplate.exchange(...)` uses `ParameterizedTypeReference<{{RETURN_TYPE}}>` matching the method's declared return type exactly — never a raw `.class` (type erasure bug). `{{RETURN_TYPE}}` may be `GeneralResponse<T>`, a plain DTO, `List<T>`, `Map<...>`, `String`, `Void`, or any other type the external API actually returns.
- [ ] The same `{{RETURN_TYPE}}` appears in **all four** places: interface signature, impl signature, `ResponseEntity<...>`, and `ParameterizedTypeReference<...>`. A mismatch is a bug.
- [ ] The method returns `r.getBody()` directly; it does NOT unwrap `GeneralResponse` internally unless the user explicitly asked for that.
- [ ] Correct `HttpMethod` constant (matches HTTP verb).
- [ ] `HttpEntity` has body for POST/PUT, headers-only for GET/DELETE.
- [ ] Catch block: `log.error("Error in sending request to <short context>", e);` — exception passed as second arg, not string-concatenated.
- [ ] After catch, `throw new BaseResponseException(<specific failure enum>);` — not swallowed, not a generic enum.
- [ ] No `@Transactional` on outbound REST methods.
- [ ] No retries/circuit breaker unless explicitly requested.

## Imports & hygiene
- [ ] Only imports that are actually used.
- [ ] No `import java.util.*` wildcard.
- [ ] No TODO comments, no debug `System.out`.
- [ ] No speculative helper methods or extra abstractions.

## Config surface
- [ ] `application.properties` **was actually edited** — a new `# <service> config` block was appended containing `{{CONFIG_PREFIX}}.host`, `{{CONFIG_PREFIX}}.product`, and one URL key per endpoint.
- [ ] Default host is `http://gw-staging.digital.vn` unless the user gave another value.
- [ ] No duplicate keys introduced (checked existing file first; skipped any already present, especially `token.admin.role`).
- [ ] If any endpoint path was unknown, it was written as `/TODO/fill-in-real-path` and flagged to the user.
- [ ] Flagged any missing project artifact (`HeaderConstant`, `GeneralResponse`, `BaseResponseException`, `ResponseStatusCodeEnum`, `coreRestTemplate` bean) instead of inventing one.

## Final
- [ ] Presented the generated file path(s), one-line summary per method, AND the exact property lines appended to `application.properties`.
