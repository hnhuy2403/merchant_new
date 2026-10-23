# Đặc Tả Yêu Cầu (SRS) — Story {{epic_num}}.{{story_num}}: {{story_title}}

> **Hướng dẫn:** Tài liệu này tập trung vào **nghiệp vụ / hành vi hệ thống** (WHAT + WHY), không đi sâu vào implementation (xem `detail-design.md`). Auto-fill từ `epics` + `prd`. Để placeholder `[CẦN BỔ SUNG: ...]` nếu thiếu ngữ cảnh.

## 1. Bối cảnh nghiệp vụ

{{srs_business_context}}

<!-- Auto-fill: vì sao cần story này, nó giải quyết pain point nào, ai là stakeholder. Trích từ epic objectives + story "so that ..." clause. -->

## 2. Đối tượng người dùng

{{srs_personas}}

<!-- Auto-fill: vai trò người dùng tác động (extract từ "As a <role>" của story + cross-references trong PRD). -->

## 3. Phạm vi

### 3.1 Trong phạm vi (In scope)

{{srs_in_scope}}

### 3.2 Ngoài phạm vi (Out of scope)

{{srs_out_of_scope}}

<!-- Auto-fill cả hai mục từ acceptance criteria + non-goals trong epic. -->

## 4. Acceptance Criteria

{{srs_acceptance_criteria}}

<!-- Auto-fill: copy ACs đã BDD-format từ epics, đánh số AC-1, AC-2, ... để các tài liệu khác (test plan, traceability) tham chiếu được. -->

## 5. Kịch bản nghiệp vụ

> Mỗi kịch bản tham chiếu rõ AC. Format Given / When / Then.

### 5.1 Happy path

{{srs_scenario_happy_path}}

<!-- Auto-fill ví dụ:
**Scenario H1 — Đăng nhập thành công với MFA** (AC-1, AC-2)
- **Given** user đã bật MFA và đang ở trang login
- **When** nhập đúng email + password + mã OTP
- **Then** hệ thống tạo session và redirect về dashboard
-->

### 5.2 Kịch bản phụ / edge case

{{srs_scenario_edge_cases}}

<!-- Auto-fill: các nhánh rẽ (validation fail, network error, concurrent action, edge data, ...). Đặc biệt chú ý tới các "nhánh không nói rõ trong AC nhưng cần tồn tại để hệ thống đúng". -->

### 5.3 Kịch bản lỗi (error path)

{{srs_scenario_error_path}}

<!-- Auto-fill: error code, thông báo cho người dùng, hành vi phục hồi. -->

## 6. Quy tắc nghiệp vụ (Business rules)

{{srs_business_rules}}

<!-- Auto-fill: các invariant / ràng buộc nghiệp vụ phải tuân thủ. Ví dụ:
- BR-1: Một user không được có quá 5 session đồng thời.
- BR-2: OTP có hiệu lực trong 60 giây.
-->

## 7. Yêu cầu phi chức năng (NFR)

{{srs_nfr}}

<!-- Auto-fill: performance / availability / security / accessibility / i18n. Trích từ PRD NFR section. Nếu không có yêu cầu cụ thể → ghi "Tuân theo NFR mặc định của hệ thống". -->

## 8. Phụ thuộc nghiệp vụ

{{srs_dependencies}}

<!-- Auto-fill: story / epic / hệ thống bên ngoài mà story này phụ thuộc (data, feature flag, integration prerequisite). -->

## 9. Tiêu chí Done (Definition of Done)

- [ ] Toàn bộ AC đạt
- [ ] Toàn bộ kịch bản happy path / edge / error pass test
- [ ] Code review approved
- [ ] Không có regression (verified bằng test suite)
- [ ] Tài liệu (`story.md`, `detail-design.md`, `source-code-links.md`) được cập nhật khớp implementation cuối

{{srs_additional_dod}}

<!-- Auto-fill nếu epic có thêm tiêu chí riêng. -->

---

_Tài liệu này sinh tự động bởi `bmad-tts-create-story`. Là nguồn truth nghiệp vụ cho dev / QA / PM trong story này._
