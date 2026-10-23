---
name: bmad-validate-prd-vds
description: Kiểm tra chất lượng và tính đầy đủ của PRD theo từng section. Use when the user says "validate PRD", "kiểm tra PRD", "review PRD VDS", hoặc "check PRD"
---

# Validate PRD VDS

## Overview

Skill này giúp kiểm tra chất lượng và tính đầy đủ của file PRD theo format VDS. Hỗ trợ validate **từng section riêng lẻ** hoặc **toàn bộ document**.

**Đầu vào:**
- File PRD đã tạo (hoặc đang tạo) từ `bmad-create-prd-vds`
- Lựa chọn section(s) cần validate

**Đầu ra:**
- Báo cáo validation (Markdown format) lưu tại `{planning_artifacts}/[tên-dự-án]-prd-validation.md`
- Hoặc output trực tiếp nếu user không muốn lưu file

**Validation Style: Section-by-Section (linh hoạt)**
- User chọn validate từng section cụ thể
- Hoặc validate tất cả 6 sections cùng lúc
- Với mỗi section: check completeness + quality + consistency

**Ngôn ngữ:** Tiếng Việt  
**Output format:** Markdown  
**Config variables used:** `planning_artifacts`, `communication_language`

---

## Conventions

- Bare paths (ví dụ: `prd-vds-template.md`) được resolve từ skill root
- `{skill-root}` = `/Users/truong23/truong23_project/bmad-learn-1/_bmad/skills/bmad-validate-prd-vds/`
- `{project-root}` = `/Users/truong23/truong23_project/bmad-learn-1/`
- `{planning_artifacts}` được resolve từ `_bmad/bmm/config.yaml`

---

## On Activation

### Load Config

Đọc config từ:
- `{project-root}/_bmad/bmm/config.yaml` (primary)
- `{project-root}/_bmad/config.yaml` (fallback)

Biến cần thiết:
- `planning_artifacts`: nơi lưu file report
- `communication_language`: ngôn ngữ hội thoại (expected: `vietnamese`)

Nếu không tìm được, sử dụng defaults.

---

## Workflow: Validate PRD VDS

### Step 1: Load & Select Section(s) to Validate

**Trigger:** User gọi skill hoặc chọn validate từ main skill

**Actions:**
- Chào user bằng tiếng Việt
- Hỏi: "Bạn có file PRD nào cần validate không?"
  - Nếu từ main skill: AI biết file path từ context
  - Nếu standalone: Hỏi user cung cấp file path hoặc tên dự án
- Cố gắng tìm file PRD:
  - Pattern tìm: `{planning_artifacts}/[tên]*-prd.md`
  - Hoặc user cung cấp path trực tiếp
- Nếu tìm được file:
  - ✅ Đọc file → parse các sections
  - ✅ Báo tóm tắt: "File tìm thấy: [tên file], có [n] sections"
- Nếu không tìm được:
  - Hỏi user cung cấp path hoặc tên dự án
  - Hoặc suggest: "Hãy chạy `/bmad-create-prd-vds` trước để tạo PRD"
- Hỏi user: "Bạn muốn validate section nào? (chọn 1 hoặc nhiều)"
  - [ ] Phân loại (Section 1)
  - [ ] Mục tiêu (Section 3)
  - [ ] Tiêu chí thành công (Section 4)
  - [ ] Tổng quan sản phẩm (Section 5.1.1)
  - [ ] User Stories & Yêu cầu chức năng (Section 5.1.2 + 5.1.3)
  - [ ] Event Tracking (Section 6)
  - [ ] ✅ **Tất cả (All)**
- Lưu lựa chọn user

**Output:**
- File content đã load, sections selected → ready for Step 2

---

### Step 2: Validate Từng Section Được Chọn

Với mỗi section được chọn, thực hiện **3 loại check:**

#### 2.1 Completeness Check (Hoàn chỉnh)

Kiểm tra: Tất cả trường bắt buộc đã điền chưa?

**Section 1 - Phân loại:**
- ✅ Đối tượng tác động: có lựa chọn ít nhất 1?
- ✅ Hình thức tác động: có lựa chọn ít nhất 1?
- **Status:** Pass/Fail

**Section 2 - Bảng thay đổi:**
- ✅ Ít nhất 1 row có:
  - STT ≠ trống
  - Thời gian (format dd/mm/yyyy)
  - Phiên bản (format x.x)
  - Nguồn gốc
- **Status:** Pass/Fail

**Section 3 - Mục tiêu:**
- ✅ 5 hàng đều có nội dung không trống:
  - Row 1: Thực trạng
  - Row 2: Nghiên cứu thị trường
  - Row 3: Nội dung triển khai
  - Row 4: Mục tiêu
  - Row 5: Lợi ích
- ❌ Nếu toàn bộ để trống: FAIL
- ⚠️ Nếu có 1-2 row trống: WARNING (partial)
- **Status:** Pass / Partial / Fail

**Section 4 - Tiêu chí thành công:**
- ✅ 4.1 (Metrics to measure): có metrics ≥ 1
- ✅ 4.2 (Metrics to monitor): có metrics hoặc "N/a"
- ✅ 4.3 (KPI): checkbox đã tick ít nhất 1
- ⚠️ Nếu bất kỳ sub-section nào để trống: WARNING
- **Status:** Pass / Warning / Fail

**Section 5.1.1 - Tổng quan:**
- ✅ Đối tượng sử dụng: có nội dung
- ✅ Kênh sử dụng: có nội dung
- ✅ Điều kiện: có nội dung
- ✅ Chính sách: có nội dung (hoặc "N/a")
- **Status:** Pass / Fail

**Section 5.1.2 + 5.1.3 - User Stories & Non-functional:**
- ✅ User Story Map: có ít nhất 1 chặng + 1 story
- ✅ Story Detail tables: có ít nhất 1 story chi tiết
- ✅ Non-functional: có nội dung hoặc "N/a"
- ⚠️ Nếu User Story Map trống nhưng Story Detail có: WARNING (inconsistent)
- **Status:** Pass / Warning / Fail

**Section 6 - Event Tracking:**
- ✅ Có ít nhất 1 checkbox đã chọn
- ⚠️ Nếu tất cả empty: WARNING
- **Status:** Pass / Warning

#### 2.2 Quality Check (Chất lượng)

Kiểm tra: Nội dung có đủ cụ thể, rõ ràng, chi tiết không?

**Section 3 - Mục tiêu:**
- ❓ Row 1 (Thực trạng): có con số/metrics không? (cơ sở)
- ❓ Row 4 (Mục tiêu): có metrics cụ thể không? (VD: "Tăng DAU 20%" thay vì "Tăng DAU")
- ❓ Row 5 (Lợi ích): có mô tả benefit structure không? (Business + Customer)
- **Findings:** List những chỗ cần chi tiết hơn

**Section 4 - Tiêu chí thành công:**
- ❓ Metrics có cụ thể + measurable không? (SMART criteria)
- ❓ 4.1 vs 4.2: Operational metrics có dẫn đến Business metrics không? (Logic flow)
- **Findings:** List recommendation

**Section 5.1.1 - Tổng quan:**
- ❓ Chính sách có chi tiết đủ 4 sub-items: Điều kiện, Thao tác, Phí, Quyền lợi?
- **Findings:** List missing details

**Section 5.1.2 - User Stories:**
- ❓ Mỗi User Story có steps (B1, B2, B3...) đủ chi tiết không?
- ❓ Steps có input/output/condition cụ thể không?
- ❓ Mockup fields: có ghi placeholder hoặc tham chiếu designs?
- **Findings:** List stories cần chi tiết hơn

#### 2.3 Consistency Check (Nhất quán)

Kiểm tra: Các sections có khớp với nhau không?

**Section 3 ↔ Section 4:**
- ❓ Mục tiêu (Section 3 Row 4) có cụ thể + metrics không? (nền tảng cho Section 4)
- ❓ Metrics (Section 4) có derived từ Mục tiêu (Section 3) không? (logic match)
- **Finding:** Nếu mục tiêu là "Tăng DAU 20%", metrics phải có DAU; nếu metric là "Error rate < 1%", phải có mục tiêu về reliability

**Section 3 ↔ Section 5:**
- ❓ User Stories (Section 5.1.2) có cover các mục tiêu (Section 3) không?
- ❓ Mỗi User Story có map tới ít nhất 1 mục tiêu không?
- **Finding:** List unmapped objectives hoặc stories

**Section 5.1.1 ↔ Section 5.1.2:**
- ❓ User Story Map: hành trình khách hàng có match với "Đối tượng" + "Kênh" (Section 5.1.1)?
- **Finding:** Nếu kênh là "Mobile App", các story có assume mobile user không?

**Section 1 ↔ Section 3+:**
- ❓ Loại tác động (Section 1) có hợp lý với nội dung triển khai (Section 3)?
- **Finding:** Nếu chọn "Xây mới", các sections có mô tả như feature mới không?

---

### Step 3: Generate & Output Validation Report

**Actions:**
- Tổng hợp tất cả findings từ Step 2 vào báo cáo
- Format báo cáo (Markdown):

```markdown
# PRD Validation Report: [Tên dự án]
**Ngày validate:** [dd/mm/yyyy]
**File PRD:** {planning_artifacts}/[tên-file].md

---

## Tóm tắt Kết quả

| Section | Completeness | Quality | Consistency | Status |
|---------|--------------|---------|-------------|--------|
| 1. Phân loại | ✅ Pass | N/A | N/A | ✅ PASS |
| 2. Bảng thay đổi | ⚠️ Warning | N/A | N/A | ⚠️ WARNING |
| 3. Mục tiêu | ✅ Pass | ⚠️ Cần cải thiện | ✅ Pass | ⚠️ NEEDS REVIEW |
| 4. Tiêu chí thành công | ✅ Pass | ✅ Pass | ✅ Pass | ✅ PASS |
| 5. Yêu cầu sản phẩm | ✅ Pass | ⚠️ Stories quá ngắn | ✅ Pass | ⚠️ NEEDS REVIEW |
| 6. Event Tracking | ✅ Pass | N/A | N/A | ✅ PASS |

---

## Chi tiết Findings

### Section 3 - Mục tiêu

**Completeness:** ✅ PASS - Tất cả 5 row đều có nội dung

**Quality:** ⚠️ NEEDS REVIEW
- ⚠️ Row 1 (Thực trạng): Thiếu con số cụ thể. Recommend: "Hiện tại DAU = X, Conversion = Y%"
- ⚠️ Row 4 (Mục tiêu): Mục tiêu "Tăng DAU" quá chung chung. Recommend: "Tăng DAU từ X lên Y (Δ +Z%) trong 3 tháng"
- ✅ Row 5: Chi tiết tốt

**Consistency:** ✅ PASS - Mục tiêu khớp với metrics Section 4

**Recommend:**
- Cập nhật Row 1 + Row 4 với metrics cụ thể
- Có thể gọi `/bmad-create-objectives-vds` để AI hỗ trợ chi tiết hơn

---

### Section 5.1.2 - User Stories

**Completeness:** ✅ PASS - Có 5 user stories

**Quality:** ⚠️ NEEDS REVIEW
- Story 1 (Onboarding): Chỉ có 2 steps (B1, B2). Recommend: Bổ sung B3-B5 cho flow hoàn chỉnh
- Story 3: Mockup field trống. Cần tham chiếu design file hoặc ghi placeholder
- Story 5: Steps mô tả quá chung chung (VD: "User nhấn submit"). Recommend: Chi tiết validation logic, error handling

**Consistency:** ✅ PASS - Tất cả stories cover mục tiêu

**Recommend:**
- Gọi `/bmad-create-user-stories-vds` để AI draft steps chi tiết hơn
- Hoặc manually chỉnh sửa từng story

---

## Điểm Tổng Thể

**Completion:** 85/100
- 5/6 sections đã điền đầy đủ (Section 2 chỉ có 1 row)
- Recommend: Thêm rows vào Bảng thay đổi khi có cập nhật

**Quality:** 75/100
- 3 sections cần improve chi tiết nội dung
- Recommend: Follow suggestions từng section để improve

**Consistency:** 90/100
- Sections liên kết tốt, logic flow rõ ràng
- Minor: Bổ sung mapping stories ↔ objectives

**Overall:** 🟨 NEEDS REVIEW (83/100)
- ✅ PRD có cấu trúc cơ bản, có thể đi đơn phê duyệt
- ⚠️ Recommend chỉnh sửa 3 sections để improve chất lượng trước submit leadership

---

## Hành động Tiếp Theo

1. **Cập nhật Section 3:** Thêm metrics cụ thể → Chạy `/bmad-create-objectives-vds`
2. **Cập nhật Section 5.1.2:** Bổ sung steps chi tiết → Chạy `/bmad-create-user-stories-vds`
3. **Re-validate:** Chạy `/bmad-validate-prd-vds` lại sau khi cập nhật
4. **Submit:** Khi tất cả sections đạt PASS/GOOD

---

*Báo cáo tạo bởi: Validate PRD VDS Skill*
*Config: Vietnamese mode, Planning Artifacts location*
```

- Hỏi user: "Bạn muốn:"
  - A) Lưu báo cáo vào file (`{planning_artifacts}/[tên-dự-án]-prd-validation.md`)
  - B) Chỉ hiện kết quả trong chat, không lưu file
  - C) Export & share (copy to clipboard)
- Thực hiện theo lựa chọn user
- Gợi ý: "Dựa trên báo cáo này, bạn có thể:"
  - Chỉnh sửa PRD trực tiếp
  - Gọi sub-skills để AI hỗ trợ từng section
  - Validate lại sau khi cập nhật

**Output:**
- Báo cáo validation (file hoặc chat)
- Checklist hành động tiếp theo

---

## Standalone vs. Integrated Usage

Skill này có thể được dùng:

**1. Integrated (từ main skill):**
- User ở Step N của `bmad-create-prd-vds`
- Chọn "Validate section này"
- AI tự biết file path từ context
- Validate section specific
- Return kết quả, user chọn tiếp tục/quay lại

**2. Standalone:**
- User gọi `/bmad-validate-prd-vds` riêng
- Cung cấp file path hoặc tên dự án
- Validate toàn bộ hoặc sections lựa chọn
- Output report file

---

## Troubleshooting

**Q: File PRD không tìm thấy?**  
A: Hỏi user cung cấp tên dự án hoặc path đầy đủ. List files có sẵn trong `{planning_artifacts}`.

**Q: User muốn validate nhưng không chỉ định section?**  
A: Default = validate tất cả 6 sections, hoặc hỏi user chọn.

**Q: Report quá dài?**  
A: Tùy chọn: (1) summary report (pass/fail), (2) detailed report (findings), user chọn.

**Q: Encoding issues?**  
A: Ensure UTF-8, Vietnamese characters fully supported.
