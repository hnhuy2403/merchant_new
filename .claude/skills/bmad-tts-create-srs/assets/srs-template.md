# Đặc Tả Yêu Cầu Phần Mềm (SRS) — Story {{epic_num}}.{{story_num}}: {{story_title}}

> **Phạm vi:** Tài liệu này là **source of truth nghiệp vụ** cho story này — QA/PM/Dev đều tham chiếu khi tranh luận hệ thống PHẢI làm gì. Tập trung vào **WHAT + WHY**, không đi vào HOW (xem `detail-design.md`).
>
> **Quy ước:**
> - `AC-N` = Acceptance Criterion (copy verbatim từ epic).
> - `H#` = Happy-path scenario, `E#` = Edge-case scenario, `R#` = Error/Recovery scenario. Mỗi scenario phải tham chiếu ≥ 1 AC.
> - `BR-N` = Business Rule (invariant — luôn đúng trong mọi state).
> - `[CẦN BỔ SUNG: <lý do>]` = chỗ thiếu context, cần PM/SA điền.

## 1. Bối cảnh nghiệp vụ

{{srs_business_context}}

<!-- Vì sao story này tồn tại, pain point nào được giải quyết, stakeholder nào quan tâm. Trích từ epic objectives + story "so that..." clause + PRD problem statement. -->

## 2. Đối tượng người dùng & Vai trò

{{srs_personas}}

<!-- Bảng các persona/role có liên quan. Mỗi role: tên, mô tả ngắn, quyền/giới hạn áp dụng trong story này.

Format gợi ý:
| Role | Mô tả | Quyền liên quan tới story này |
|------|-------|-------------------------------|
| Customer | Người dùng cuối tự đăng ký | Xem & cập nhật profile của chính họ |
| Admin    | Quản trị viên hệ thống | Khoá tài khoản, reset MFA |
-->

## 3. Phạm vi

### 3.1 Trong phạm vi (In scope)

{{srs_in_scope}}

### 3.2 Ngoài phạm vi (Out of scope)

{{srs_out_of_scope}}

<!-- Cả hai mục bóc từ AC + non-goals trong epic + ranh giới rõ trong PRD. Out-of-scope đặc biệt quan trọng — nó ngăn dev "tiện tay làm thêm". -->

## 4. Tiền điều kiện & Hậu điều kiện chung

### 4.1 Tiền điều kiện (Pre-conditions)

{{srs_preconditions}}

<!-- State của hệ thống PHẢI có trước khi bất kỳ scenario nào trong story này chạy được. Ví dụ:
- User account đã tồn tại và đã verify email.
- Feature flag `mfa_v2` đang on cho tenant.
- Dependency story 1-1 đã deploy. -->

### 4.2 Hậu điều kiện (Post-conditions)

{{srs_postconditions}}

<!-- State của hệ thống SAU KHI story hoàn tất thành công. Ví dụ:
- Mọi user trong tenant đều có MFA enrolled hoặc grace-period flag.
- Audit log có entry cho mỗi MFA setup. -->

## 5. Acceptance Criteria

{{srs_acceptance_criteria}}

<!-- Copy verbatim từ epic, đánh số AC-1, AC-2, ... Giữ nguyên BDD wording gốc. Mỗi AC bắt đầu trên 1 dòng riêng:

**AC-1:** Given một user chưa bật MFA, When họ đăng nhập lần đầu sau ngày X, Then hệ thống bắt buộc enroll MFA trước khi vào dashboard.
-->

## 6. Kịch bản nghiệp vụ

> Mỗi scenario format chuẩn:
> - **<ID> — <Tên ngắn>** (refs: AC-1, AC-2, BR-1)
>   - **Pre:** state cần có trước scenario (nếu khác mục 4.1)
>   - **Given** ...
>   - **When** ...
>   - **Then** ...
>   - **Post:** state sau scenario (nếu khác mục 4.2)

### 6.1 Happy path (`H#`)

{{srs_scenario_happy_path}}

<!-- Tối thiểu 1 scenario / AC. Dùng dữ liệu cụ thể (không "user A nhập email"). Ví dụ:

**H1 — Đăng nhập thành công lần đầu với MFA bắt buộc** (refs: AC-1, AC-2, BR-2)
- **Given** user `nguyen.van.a@vss.gov.vn` chưa bật MFA và là login đầu tiên sau 2026-01-01
- **When** nhập đúng email + password
- **Then** hệ thống redirect tới `/mfa/enroll`, không cấp session token cho dashboard
- **Post:** flag `mfa_required_pending=true` được set trên user record
-->

### 6.2 Edge cases (`E#`)

{{srs_scenario_edge_cases}}

<!-- Áp dụng systematic checklist (xem references/scenario-patterns.md):
- Boundary: giá trị cực biên, empty, max length, unicode, timezone DST
- Concurrency: 2 actor cùng thao tác, double-submit, race với background job
- Network/Auth fail: token expired giữa flow, mất kết nối, retry idempotency
- Data corruption: record corrupt, foreign key broken, partial migration
- Role mismatch: actor đổi role giữa flow, permission revoked giữa session
- State machine illegal transition: gọi action ở state không hợp lệ

Chỉ thêm scenario khi domain của story thực sự đụng tới khía cạnh đó. KHÔNG pad.
-->

### 6.3 Error & Recovery (`R#`)

{{srs_scenario_error_path}}

<!-- Cho mỗi error path:
- Trigger condition
- Error code (nếu có quy ước trong architecture)
- Thông báo cho user (vietnamese, copy chuẩn)
- Hành vi phục hồi: retry tự động? rollback transaction? notify admin?
- Audit/log expectation

**R1 — OTP hết hạn** (refs: AC-3)
- **Given** user đang ở trang nhập OTP, OTP đã sinh ra cách đây > 60s
- **When** user submit OTP
- **Then** API trả `MFA_OTP_EXPIRED`, UI hiển thị "Mã đã hết hạn. Vui lòng yêu cầu mã mới." kèm nút "Gửi lại"
- **Recovery:** user nhấn "Gửi lại" → quay về scenario H1 step 2
-->

## 7. Quy tắc nghiệp vụ (Business rules)

{{srs_business_rules}}

<!-- Invariants — luôn đúng bất kể scenario. Đánh số BR-1, BR-2.

- **BR-1:** Một user không được có quá 5 session đồng thời (tính cả mobile + web).
- **BR-2:** OTP có hiệu lực trong 60 giây kể từ thời điểm sinh; sau đó bắt buộc gen mới.
- **BR-3:** Mọi thao tác MFA setup PHẢI ghi audit log với actor_id, timestamp, ip, user_agent.

Nguồn: PRD constraints, epic non-goals, architecture security policy, project-context. Không có nguồn → ghi [CẦN BỔ SUNG: ...].
-->

## 8. Test data tham chiếu

{{srs_test_data}}

<!-- Dữ liệu mẫu QA/dev paste được trực tiếp. Cover: valid baseline, boundary, malformed, role variant. Dùng dữ liệu sát domain Việt Nam (CMND/CCCD format, số điện thoại VN, dấu tiếng Việt).

Format gợi ý:

**Valid baseline (H1):**
```json
{ "email": "nguyen.van.a@vss.gov.vn", "password": "P@ssw0rd!2026", "role": "customer" }
```

**Boundary — email tối đa (E2):**
```
Email length 254 chars, valid format.
```

**Malformed — password thiếu ký tự đặc biệt (R2):**
```json
{ "email": "...", "password": "Abcdef123" }
```
-->

## 9. Yêu cầu phi chức năng (NFR)

{{srs_nfr}}

<!-- Trích từ PRD NFR section, lọc cái thực sự áp dụng cho story này:
- Performance: thời gian phản hồi p95, throughput
- Security: encryption, audit, PII handling
- Reliability: availability target, recovery RTO/RPO
- Accessibility: WCAG level, keyboard nav, screen reader
- i18n: ngôn ngữ hỗ trợ, currency/date format

Nếu story không có NFR riêng → ghi "Tuân theo NFR mặc định của hệ thống" và chấm hết. Không pad.
-->

## 10. Phụ thuộc nghiệp vụ

{{srs_dependencies}}

<!-- - Story/epic upstream phải done trước
- Feature flag phải on
- Hệ thống ngoài (Bitbucket API, SMS gateway, ...) phải sẵn sàng
- Data migration phải hoàn tất

Format:
| Loại | Mô tả | Trạng thái | Owner |
|------|-------|------------|-------|
| Story | 1-1 SSO config | done | Backend team |
| Feature flag | mfa_v2 | enabled prod | Platform |
| External | OTP SMS gateway (vendor X) | active | Vendor |
-->

## 11. Câu hỏi mở (Open questions)

{{srs_open_questions}}

<!-- Ambiguity thật sự cần PM/SA/UX trả lời trước khi dev. Mỗi câu một dòng, gắn role:

- **[PM]** AC-2 nói "lần đầu sau ngày X" — ngày X cụ thể là gì? Áp dụng theo tenant hay global?
- **[SA]** Khi user enroll MFA fail 3 lần, có lock account không? Lock bao lâu?
- **[UX]** Trang `/mfa/enroll` có cho phép skip "remind me later" không?
- **[QA]** OTP retry có giới hạn số lần / phút? Cần để viết rate-limit test.

KHÔNG biến đây thành chỗ "for safety, ask PM". Câu hỏi phải là rào cản thực sự cho dev.
-->

## 12. Định nghĩa hoàn thành (Definition of Done)

- [ ] Toàn bộ AC đạt (chứng minh bằng test pass mapping AC-N → test-id).
- [ ] Toàn bộ scenario H/E/R có test tương ứng pass.
- [ ] Business rules có unit/integration test cover invariant.
- [ ] NFR đạt (perf benchmark, security scan, a11y audit khi áp dụng).
- [ ] Code review approved, không regression trong test suite.
- [ ] Audit log entries verified cho các action trong BR.
- [ ] Tài liệu khớp implementation cuối: story.md / detail-design.md / source-code-links.md đã update.
- [ ] Mọi câu hỏi mở (mục 11) đã được PM/SA resolve và phản ánh vào AC/BR.

{{srs_additional_dod}}

<!-- Thêm tiêu chí riêng nếu epic có. -->

---

_SRS sinh tự động bởi `bmad-tts-create-srs`. Là source of truth nghiệp vụ — sửa trực tiếp file này khi nghiệp vụ thay đổi, không sửa ngầm trong code._
