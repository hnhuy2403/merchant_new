---
name: bmad-create-prd-vds
description: Hướng dẫn viết PRD theo chuẩn VDS cho dự án Fintech/Tech. Use when the user says "tạo PRD VDS", "viết PRD", "create VDS PRD", hay bắt đầu từ workflow 2-planning
---

# Tạo PRD VDS

## Overview

Skill này hướng dẫn Product Owner viết PRD (Product Requirements Document) tuân theo chuẩn VDS - template BRD đã được phát triển và sử dụng thực tế trong công ty.

**Đầu vào:**
- Tên dự án / feature
- Thông tin phân loại (Đối tượng tác động, Hình thức tác động)
- Thông tin chi tiết từng section (có thể do user điền hoặc gọi sub-skills)

**Đầu ra:**
- File PRD đầy đủ theo format VDS (.md) lưu tại `{planning_artifacts}/[tên-dự-án]-prd.md`
- Có thể validate liên tục qua skill `bmad-validate-prd-vds`

**Kiến trúc Hybrid:**
- Workflow tuần tự qua 6 bước chính
- Cuối mỗi bước: user chọn (1) tiếp tục bước kế, (2) validate section này, (3) quay lại chỉnh sửa
- Có thể gọi sub-skills để hỗ trợ: `bmad-create-objectives-vds`, `bmad-create-metrics-vds`, `bmad-create-user-stories-vds`

**Ngôn ngữ:** Tiếng Việt  
**Output format:** Markdown  
**Config variables used:** `planning_artifacts`, `communication_language`, `document_output_language`

---

## Conventions

- Đường dẫn bare (ví dụ: `templates/prd-vds-template.md`) được resolve từ thư mục skill root
- `{skill-root}` = `/Users/truong23/truong23_project/bmad-learn-1/_bmad/skills/bmad-create-prd-vds/`
- `{project-root}` = `/Users/truong23/truong23_project/bmad-learn-1/`
- `{planning_artifacts}` được resolve từ `_bmad/bmm/config.yaml` → `{project-root}/_bmad-output/planning-artifacts`

---

## On Activation

### Load Config

Đọc config từ:
- `{project-root}/_bmad/bmm/config.yaml` (primary)
- `{project-root}/_bmad/config.yaml` (fallback)

Biến cần thiết:
- `planning_artifacts`: nơi lưu file PRD
- `communication_language`: ngôn ngữ hội thoại (expected: `vietnamese`)
- `document_output_language`: ngôn ngữ output document (expected: `vietnamese`)
- `user_name`: tên user (dùng cho auto-fill author field)

Nếu không tìm được config, sử dụng defaults:
- `planning_artifacts` = `{project-root}/_bmad-output/planning-artifacts`
- `communication_language` = `vietnamese`
- `user_name` = `Truong23`

---

## Workflow: Tạo PRD VDS

### Step 1: Khởi tạo & Phân loại

**Trigger:** User gọi skill hoặc chọn "Start new PRD" từ menu.

**Actions:**
- Chào user bằng tiếng Việt, giải thích sẽ tạo PRD theo 6 bước
- Hỏi **Tên dự án**: user cung cấp tên feature/service mà PRD mô tả
- Hỏi **Đối tượng tác động** (multi-select, có thể chọn nhiều):
  - Dịch vụ
  - Tính năng
  - Chiến dịch
  - Công cụ nội bộ
  - Nền tảng/hệ thống backend
- Hỏi **Hình thức tác động** (multi-select, có thể chọn nhiều):
  - Xây mới
  - Nâng cấp bổ sung tính năng
  - Nâng cấp luồng trải nghiệm lớn
  - Nâng cấp luồng trải nghiệm nhỏ
  - Nâng cấp thay đổi chính sách
  - Nâng cấp cập nhật nội dung
- Khởi tạo file PRD mới từ template `templates/prd-vds-template.md`:
  - ✅ Copy template content
  - ✅ Replace placeholders: `[Tên dự án]` → user input
  - ✅ Auto-fill: `[ngày tạo]` → hôm nay (dd/mm/yyyy), `[tên PO]` → `{user_name}`
  - ✅ Điền Section 1 (Phân loại) với lựa chọn user
  - ✅ Điền Bảng thay đổi - Row 1: ngày hôm nay, phiên bản 1.0, "Khởi tạo", "Khởi tạo tài liệu"
  - ✅ Lưu draft file tại `{planning_artifacts}/[tên-dự-án]-prd.md`
- Báo file đã tạo & đường dẫn
- Lưu context (tên dự án, file path) để dùng cho bước tiếp theo

**Output:** 
- File PRD draft lưu tại disk, Section 1-2 đã điền
- Ready cho Step 2

---

### Step 2: Mục tiêu (Objective & Discovery)

**Trigger:** User chọn tiếp tục hoặc restart từ step này

**Actions:**
- Nhắc lại: Step này xử lý Section 3 (Mục tiêu) - 5 hàng quan trọng
- Hỏi user: "Bạn muốn:"
  - A) Tôi hỏi từng câu hỏi để nắm chi tiết (tư vấn sâu)
  - B) Điền trực tiếp hoặc dùng sub-skill `bmad-create-objectives-vds` rồi paste kết quả
  - C) Để trống lúc này, điền sau
- **Nếu chọn A (Tư vấn sâu):**
  - Hỏi 5 câu lần lượt (structured prompts):
    1. "Hãy mô tả thực trạng hiện tại của [dịch vụ] - pain points khách hàng, số liệu hiện tại?"
    2. "Các đối thủ giải quyết vấn đề này như thế nào? Bạn đã research chưa?"
    3. "Giải pháp của bạn sẽ triển khai như thế nào? Nội dung triển khai là gì?"
    4. "Mục tiêu cần đạt (cụ thể, có metrics)?"
    5. "Lợi ích cho business & customer là gì?"
  - AI phân tích đầu vào, tổng hợp & draft 5 dòng của Section 3
  - User review, chỉnh sửa
  - Update vào file PRD
- **Nếu chọn B (Sub-skill hoặc manual):**
  - Gợi ý: "Bạn có thể gọi `/bmad-create-objectives-vds` để AI hỗ trợ chi tiết hơn"
  - Hoặc: "Bạn điền trực tiếp vào template, tôi sẽ update file"
  - Nhận text từ user → update Section 3 vào file PRD
- **Nếu chọn C:**
  - Skip, để trống Section 3 tạm thời

**Output:**
- Section 3 của file PRD (hoặc để trống)

---

### Step 3: Tiêu chí thành công (Success Criteria & Metrics)

**Trigger:** User chọn tiếp tục

**Actions:**
- Nhắc lại: Step này xử lý Section 4 (Sections 4.1, 4.2, 4.3)
- Hỏi user: "Bạn muốn:"
  - A) Tôi hỏi về KPIs/Metrics và gợi ý khung (tư vấn)
  - B) Dùng sub-skill `bmad-create-metrics-vds` rồi paste
  - C) Điền manual hoặc để trống
- **Nếu chọn A:**
  - Hỏi: "Từ tờ trình phê duyệt, bạn có các metrics nào?"
  - Hỏi: "Loại dự án là [từ Section 1 Hình thức tác động], vậy KPIs chính nên là gì?"
  - AI gợi ý framework:
    - 4.1 Business Metrics (VD: DAU, Conversion rate, Transaction volume, v.v.)
    - 4.2 Operational Metrics (VD: API response time, Error rate, v.v.)
    - 4.3 KPI Compliance checkbox (confirm tiêu chuẩn chất lượng dịch vụ)
  - User confirm/chỉnh sửa
  - Update Section 4 vào file PRD
- **Nếu chọn B/C:** Handle tương tự Step 2

**Output:**
- Section 4 của file PRD (hoặc để trống)

---

### Step 4: Tổng quan sản phẩm (Product Overview)

**Trigger:** User chọn tiếp tục

**Actions:**
- Nhắc lại: Step này xử lý Section 5.1.1 (Tổng quan) - 4 hàng (Đối tượng, Kênh, Điều kiện, Chính sách)
- Hỏi user 4 câu lần lượt:
  1. "Đối tượng sử dụng là ai? Có giới hạn nào không?"
  2. "Khách hàng sẽ dùng qua kênh nào? (VD: App, Web, v.v.)"
  3. "Điều kiện để sử dụng? (VD: Smartphone, Internet connection, v.v.)"
  4. "Chính sách là gì? (Điều kiện tham gia, điều kiện hành động, phí, quyền lợi, v.v.)"
- Tập hợp câu trả lời → update Section 5.1.1 vào file PRD

**Output:**
- Section 5.1.1 của file PRD

---

### Step 5: User Stories & Yêu cầu chức năng

**Trigger:** User chọn tiếp tục

**Actions:**
- Nhắc lại: Step này xử lý Section 5.1.2 (User Story Map & Detail Tables) + Section 5.1.3 (Non-functional)
- Hỏi user: "Bạn muốn:"
  - A) Dùng sub-skill `bmad-create-user-stories-vds` (AI hỗ trợ sâu, có thể gọi riêng)
  - B) Điền manual hoặc paste kết quả từ doc khác
  - C) Để trống lúc này
- **Nếu chọn A:**
  - Gợi ý: "Bạn gọi `/bmad-create-user-stories-vds` - AI sẽ hỗ trợ tạo User Story Map 7 chặng hành trình + detail tables từng story"
  - Sau khi user chạy sub-skill, nhận kết quả → update Section 5.1.2 vào file PRD
- **Nếu chọn B/C:**
  - Hỏi user cung cấp nội dung hoặc skip
  - Update hoặc leave blank
- Hỏi thêm: "Có yêu cầu phi chức năng (non-functional) không? (VD: Performance, Security, Availability, v.v.)"
  - Nếu có: update Section 5.1.3
  - Nếu không: ghi "N/a"

**Output:**
- Section 5.1.2 & 5.1.3 của file PRD (hoặc để trống)

---

### Step 6: Event Tracking & Finalize

**Trigger:** User chọn tiếp tục

**Actions:**
- Nhắc lại: Step cuối cùng - Section 6 (Event Tracking) + finalize
- Hỏi user: "Hệ thống tracking event nào?"
  - [ ] Đặt event tracking trên hệ thống EVT
  - [ ] Đặt event tracking trên hệ thống Adjust
  - [ ] Không đặt event tracking
- Update checkbox tương ứng vào Section 6
- Update Bảng thay đổi (Row 1) nếu chưa có:
  - Thời gian: ngày hôm nay (dd/mm/yyyy)
  - Phiên bản: 1.0
  - Nguồn gốc: "Khởi tạo"
  - Căn cứ: user input (hoặc để trống)
  - Nội dung mới: "Khởi tạo tài liệu"
- Đọc file PRD hiện tại, báo tóm tắt nội dung đã fill (% hoàn chỉnh)
- Gợi ý: "Bạn có thể chạy `/bmad-validate-prd-vds` để kiểm tra chất lượng từng section"
- Lưu file (nếu có thay đổi)

**Output:**
- File PRD hoàn chỉnh (hoặc partial nếu user skip sections)
- Ready for validation

---

## User Choice at Step Endings

Cuối mỗi step, user có **3 lựa chọn:**

1. **"Tiếp tục bước kế tiếp"** → Chuyển sang step tiếp theo
2. **"Validate section vừa làm"** → Gọi `bmad-validate-prd-vds` với tham số: section name (VD: "Section 3" hoặc "Objectives")
3. **"Quay lại chỉnh sửa step trước"** → Quay lại step trước để edit

---

## Integration with Sub-skills

Mỗi step có thể trigger sub-skill nếu user yêu cầu:

- **Step 2 → `bmad-create-objectives-vds`**: User chọn tư vấn sâu hoặc muốn AI draft Section 3
- **Step 3 → `bmad-create-metrics-vds`**: User chọn tư vấn KPI hoặc muốn AI suggest metrics
- **Step 5 → `bmad-create-user-stories-vds`**: User chọn dùng AI để tạo User Story Map

Sub-skill có thể được gọi:
- **Từ main skill**: Gợi ý trong hội thoại, user xác nhận → gọi `/[sub-skill-name]`
- **Standalone**: User tự gọi `/[sub-skill-name]` bất cứ lúc nào

---

## File Management

**File paths:**
- Input template: `{skill-root}/templates/prd-vds-template.md`
- Output PRD: `{planning_artifacts}/[tên-dự-án]-prd.md` (auto-generated từ tên dự án, replace spaces với dấu gạch)
- VD: Dự án "Tính năng thanh toán mới" → file output: `tính-năng-thanh-toán-mới-prd.md`

**File operations:**
- **Read template:** Load từ file lúc Step 1
- **Create new PRD:** Copy template → save với tên theo dự án
- **Update sections:** Đọc file hiện tại → update sections tương ứng → save lại
- **Read for validation:** Cung cấp file path cho skill validate nếu user request

---

## Troubleshooting

**Q: User quên tên dự án hoặc muốn thay đổi?**  
A: Cho phép user input lại, generate tên file mới, offer move/rename.

**Q: File đã tồn tại?**  
A: Hỏi user muốn (1) overwrite, (2) append version number (VD: `-v2`), (3) save as new.

**Q: User skip nhiều sections, PRD bị incomplete?**  
A: Báo % hoàn chỉnh, gợi ý fill từng section sau, offer section-by-section validation thay vì toàn bộ.

**Q: Encoding/Language issues?**  
A: Ensure all output là UTF-8, Vietnamese characters được hỗ trợ trong Markdown.
