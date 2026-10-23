# REST Client Service Template

Canonical pattern. Copy the structure; replace every `{{placeholder}}`. Delete any method block that doesn't apply.

## Placeholders

- `{{PACKAGE}}` — e.g. `vn.com.viettel.vds.varm.service`
- `{{SERVICE_NAME}}` — e.g. `Customer` → `CustomerService` / `CustomerServiceImpl`
- `{{CONFIG_PREFIX}}` — e.g. `rest.customer-service` (expects `.host` and `.product`)
- `{{RT_QUALIFIER}}` — e.g. `coreRestTemplate`
- `{{HOST_FIELD}}` — e.g. `customerServiceHost`
- `{{PRODUCT_FIELD}}` — e.g. `customerServiceProduct`
- `{{URL_PROPERTY}}` — full property key holding the endpoint path, e.g. `customer.validate.pin.url`. NEVER hardcode the path in Java.
- `{{URL_FIELD}}` — matching Java field, e.g. `validatePinUrl`
- `{{REQ_TYPE}}` — request DTO (for POST/PUT) or `Object` if none
- `{{RETURN_TYPE}}` — the **full** Java return type for the method AND the generic argument of `ParameterizedTypeReference`. Must match exactly what the external API returns. Examples:
  - `GeneralResponse<CustomerDTO>` — VDS-wrapped payload
  - `CustomerDTO` — raw DTO
  - `List<ItemDTO>`, `Map<String, Object>`, `String`
  - `Void` — no response body
  Pick whichever matches the actual external contract. Do NOT force `GeneralResponse<T>` if the external API doesn't use it.
- `{{FAIL_ENUM}}` — e.g. `ResponseStatusCodeEnum.VALIDATE_PIN_FAILED`
- `{{METHOD_NAME}}` — Java method name
- `{{PARAM_LIST}}` — method parameters
- `{{LOG_CONTEXT}}` — short phrase for the error log, e.g. `validate pin`

## Interface

```java
package {{PACKAGE}}.interfaces;

// Import only the types that actually appear in {{RETURN_TYPE}} / {{REQ_TYPE}} / {{PARAM_LIST}}.
// Examples you MAY need (add only what's used):
// import vn.com.viettel.vds.arch.factory.response.GeneralResponse;
// import java.util.List;
// + domain DTO imports

public interface {{SERVICE_NAME}}Service {
    // One signature per endpoint. Return type = {{RETURN_TYPE}}.
    {{RETURN_TYPE}} {{METHOD_NAME}}({{PARAM_LIST}});
}
```

## Implementation — skeleton

```java
package {{PACKAGE}}.impl;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;
import vn.com.viettel.vds.arch.exception.BaseResponseException;
// Only import GeneralResponse if at least one method's {{RETURN_TYPE}} uses it:
// import vn.com.viettel.vds.arch.factory.response.GeneralResponse;
// project-specific:
// import ...HeaderConstant;
// import ...ResponseStatusCodeEnum;
// import ...{{SERVICE_NAME}}Service;

@Service
@Slf4j
public class {{SERVICE_NAME}}ServiceImpl implements {{SERVICE_NAME}}Service {

    @Value("${{{CONFIG_PREFIX}}.host}")
    private String {{HOST_FIELD}};

    @Value("${{{CONFIG_PREFIX}}.product}")
    private String {{PRODUCT_FIELD}};

    // One @Value per endpoint path — NEVER hardcode paths in methods.
    @Value("${{{URL_PROPERTY}}}")
    private String {{URL_FIELD}};

    // Include ONLY if admin token is required by at least one method:
    @Value("${token.admin.role}")
    private String tokenAdmin;

    private final RestTemplate restTemplate;

    public {{SERVICE_NAME}}ServiceImpl(@Qualifier("{{RT_QUALIFIER}}") RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    // --- method blocks below ---
}
```

## Method — POST with body

```java
@Override
public {{RETURN_TYPE}} {{METHOD_NAME}}({{REQ_TYPE}} request) {
    HttpHeaders headers = new HttpHeaders();
    headers.set(HeaderConstant.PRODUCT, {{PRODUCT_FIELD}});
    // headers.set(HeaderConstant.AUTHORIZATION, tokenAdmin); // only if admin token required
    try {
        UriComponentsBuilder builder = UriComponentsBuilder.fromHttpUrl({{HOST_FIELD}});
        HttpEntity<Object> requestEntity = new HttpEntity<>(request, headers);
        ResponseEntity<{{RETURN_TYPE}}> r = restTemplate.exchange(
                builder.build().encode().toUri() + {{URL_FIELD}},
                HttpMethod.POST,
                requestEntity,
                new ParameterizedTypeReference<{{RETURN_TYPE}}>() {});
        return r.getBody();
    } catch (Exception e) {
        log.error("Error in sending request to {{LOG_CONTEXT}}", e);
    }
    throw new BaseResponseException({{FAIL_ENUM}});
}
```

## Method — GET with query params

```java
@Override
public {{RETURN_TYPE}} {{METHOD_NAME}}({{PARAM_LIST}}) {
    HttpHeaders headers = new HttpHeaders();
    headers.set(HeaderConstant.PRODUCT, {{PRODUCT_FIELD}});
    headers.set(HeaderConstant.AUTHORIZATION, tokenAdmin); // drop if not needed
    try {
        UriComponentsBuilder builder = UriComponentsBuilder
                .fromHttpUrl({{HOST_FIELD}} + {{URL_FIELD}});
        // builder.queryParam("key", value); // one per query param
        HttpEntity<Object> requestEntity = new HttpEntity<>(headers);
        ResponseEntity<{{RETURN_TYPE}}> r = restTemplate.exchange(
                builder.encode().toUriString(),
                HttpMethod.GET,
                requestEntity,
                new ParameterizedTypeReference<{{RETURN_TYPE}}>() {});
        return r.getBody();
    } catch (Exception e) {
        log.error("Error in sending request to {{LOG_CONTEXT}}", e);
    }
    throw new BaseResponseException({{FAIL_ENUM}});
}
```

## Return-type notes

- `{{RETURN_TYPE}}` must be **identical** in:
  1. the interface signature,
  2. the impl method signature (`@Override`),
  3. the `ResponseEntity<...>` declaration,
  4. the `new ParameterizedTypeReference<...>() {}`.
  A mismatch causes either a compile error or a silent `ClassCastException` at runtime.
- If the external API returns no body, use `{{RETURN_TYPE}} = Void` and `return r.getBody();` still compiles (it will be `null`).
- Do NOT unwrap `GeneralResponse` inside the service unless the user explicitly asks — callers expect whatever `{{RETURN_TYPE}}` declares.

## application.properties block (append to the file — do not just list)

Group under a header comment matching the existing style in the file. Use `http://gw-staging.digital.vn` as the default host unless the user specifies another.

```properties
# {{SERVICE_NAME}} service config
{{CONFIG_PREFIX}}.host=http://gw-staging.digital.vn
{{CONFIG_PREFIX}}.product={{PRODUCT_VALUE}}

# one line per endpoint — the path itself is config, not code:
{{URL_PROPERTY}}=/TODO/fill-in-real-path

# token.admin.role is usually already defined elsewhere in the file; only add if missing:
# token.admin.role=Bearer xxxxxxxx
```

Before appending:
- Verify each key does not already exist (`grep`-style check). Skip duplicates, don't overwrite.
- If the endpoint path is unknown, write `/TODO/fill-in-real-path` and call it out in the summary.
