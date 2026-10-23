# vds-tts-fix-sonar — Verification Checklist

Use AFTER all fixes applied, BEFORE marking the run complete.

## Per-fix

- [ ] Mỗi fix có reference rõ ràng tới Sonar issue (rule key + file:line).
- [ ] KHÔNG thay đổi public API signature (method name, return type, param order) trừ khi rule cụ thể yêu cầu (vd `java:S00100` rename).
- [ ] KHÔNG xóa unused field/method nếu được dùng qua reflection / Spring annotation (`@Autowired`, `@PostConstruct`, `@EventListener`, `@Bean`, `@Component` scanning).
- [ ] KHÔNG đụng vào file generated (target/, build/, .git/).
- [ ] Mỗi rule "judgment required" (vd `java:S3776` cognitive complexity) đã được user confirm chiến lược fix.

## Per-batch (sau mỗi 5-10 file)

- [ ] `./mvnw -q -DskipTests compile` pass (Java compile sạch, không regression syntax).
- [ ] `git diff --stat` cho thấy thay đổi trong scope dự định (không vô tình modify file ngoài scope).

## Sau toàn bộ run

- [ ] Tổng số issue đã fix khớp với count user xác nhận.
- [ ] File List báo cáo include MỌI file modified.
- [ ] Skipped issues (user chọn) được ghi rõ lý do trong report.
- [ ] Flagged-judgment issues được ghi note để follow-up (vd ticket riêng cho long method refactor).
- [ ] KHÔNG commit token / credential vào git.
- [ ] User được nhắc trigger Sonar re-scan trên CI để confirm issues đã close.

## Cảnh báo phổ biến

- **Reflection / Spring magic:** `S1068`/`S1144` unused private có thể bị Spring inject qua proxy. Verify với `git grep <fieldName>` toàn repo trước khi xóa.
- **Test impact:** unused method trong `src/main` có thể được test reference. Check `src/test` trước khi xóa.
- **Override chain:** rename method có thể break override ở subclass. Dùng IDE refactor hoặc grep extends/implements.
- **Behavior preservation:** nếu fix làm đổi behavior (vd extract method change exception propagation), HALT và surface to user.
