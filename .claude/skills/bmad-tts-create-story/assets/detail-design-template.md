# Thiết Kế Chi Tiết — Story {{epic_num}}.{{story_num}}: {{story_title}}

> **Hướng dẫn:** Các section dưới đây là khung chuẩn. Mỗi section có (a) gợi ý nội dung và (b) phần auto-fill từ phân tích `architecture` + `epics` + `prd`. Nếu không đủ ngữ cảnh, để placeholder `[CẦN BỔ SUNG: <mô tả>]` để dev/architect điền sau. KHÔNG xóa heading.

## 1. Tổng quan

{{detail_design_overview}}

<!-- Auto-fill: 2-4 câu mô tả mục tiêu kỹ thuật của story (KHÁC với business goal trong SRS). Trích từ epic technical requirements + story description. -->

## 2. Phạm vi thay đổi

### 2.1 File / module bị ảnh hưởng

{{detail_design_files_affected}}

<!-- Auto-fill: bảng liệt kê file dự kiến NEW vs UPDATE (extract từ architecture source tree). Ví dụ:
| File | Loại | Ghi chú |
|------|------|---------|
| `apps/web/src/features/auth/login.tsx` | UPDATE | Thêm flow MFA |
| `apps/api/src/routes/auth.ts`         | NEW    | Endpoint `/mfa/verify` |
-->

### 2.2 Phạm vi KHÔNG thay đổi

{{detail_design_out_of_scope}}

<!-- Auto-fill: liệt kê rõ những gì story này KHÔNG đụng đến (để tránh scope creep). Trích từ acceptance criteria + non-goals. -->

## 3. Kiến trúc

### 3.1 Sơ đồ luồng (sequence / data flow)

{{detail_design_flow}}

<!-- Auto-fill: mô tả luồng xử lý chính (text hoặc mermaid). Trích từ architecture patterns + AC. Nếu architecture có sequence diagram liên quan → embed link/section reference. -->

### 3.2 Component / layer

{{detail_design_components}}

<!-- Auto-fill: phân rã thành các component (UI, service, repository, controller, ...) theo convention của project. Trích từ architecture component map. -->

## 4. Mô hình dữ liệu

{{detail_design_data_model}}

<!-- Auto-fill: schema mới hoặc thay đổi (table, column, index, migration). Trích từ architecture database section. Nếu không có thay đổi DB → ghi "Không thay đổi schema". -->

## 5. API / Interface

{{detail_design_api}}

<!-- Auto-fill: endpoint, method, request/response schema, auth scope. Trích từ architecture API patterns. Format ví dụ:
- `POST /api/v1/<resource>` — Auth: `<scope>` — Body: `{...}` — Response: `{...}`
-->

## 6. Phụ thuộc & tích hợp

{{detail_design_dependencies}}

<!-- Auto-fill: thư viện mới cần thêm (kèm version), service ngoài (Bitbucket, queue, cache, third-party API), feature flag. Trích từ architecture tech stack + research từ web research step. -->

## 7. Cân nhắc kỹ thuật

### 7.1 Hiệu năng

{{detail_design_performance}}

<!-- Auto-fill: caching strategy, N+1 risk, batch size, timeout. Trích từ architecture performance section. Nếu không liên quan → ghi "Không có yêu cầu hiệu năng đặc biệt". -->

### 7.2 Bảo mật

{{detail_design_security}}

<!-- Auto-fill: authn/authz, input validation, secret handling, audit log. Trích từ architecture security section. -->

### 7.3 Quan sát (logging / metrics / tracing)

{{detail_design_observability}}

<!-- Auto-fill: log gì, metric nào, alert threshold. Trích từ architecture observability patterns. -->

## 8. Chiến lược test

{{detail_design_test_strategy}}

<!-- Auto-fill: unit / integration / e2e split + tool. Trích từ architecture testing standards. Liên kết tới SRS scenarios để map AC ↔ test case. -->

## 9. Câu hỏi mở / Rủi ro

{{detail_design_open_questions}}

<!-- Auto-fill: các giả định cần xác nhận, vùng mơ hồ phát hiện trong quá trình phân tích. Nếu không có → để section trống với dấu `_Không có_`. -->

---

_Tài liệu này sinh tự động bởi `bmad-tts-create-story`. Cập nhật khi thiết kế thay đổi trong quá trình implement._
