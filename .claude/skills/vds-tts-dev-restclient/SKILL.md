---
name: vds-tts-dev-restclient
description: Generate a Spring REST client service class (outbound HTTP integration) following the VDS/Viettel pattern — RestTemplate + @Qualifier, @Value-backed host/product config, HttpHeaders with PRODUCT + AUTHORIZATION, UriComponentsBuilder URL build, restTemplate.exchange with ParameterizedTypeReference, flexible return type (GeneralResponse<T>, a raw DTO, a List, String, Void, etc.), and BaseResponseException on failure. Use when the user asks to "tạo rest client", "tạo service gọi API ngoài", "generate outbound REST service", or to add a new method calling an external HTTP service in a Spring project.
---

Follow the instructions in `./workflow.md`. Use `./template.java.md` as the canonical code template and `./checklist.md` to self-verify the output before presenting.
