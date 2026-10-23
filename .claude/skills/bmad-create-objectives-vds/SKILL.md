---
name: bmad-create-objectives-vds
description: Hỗ trợ viết Section 3 - Mục tiêu với phân tích thực trạng và nghiên cứu thị trường. Use when the user says "viết mục tiêu", "phân tích thực trạng", "create objectives VDS", hoặc cần tư vấn objectives
---

# Tạo Mục tiêu VDS (Section 3)

## Overview

Skill này hỗ trợ Product Owner viết Section 3 (Mục tiêu) của PRD - section phức tạp nhất, yêu cầu phân tích thực trạng, nghiên cứu thị trường, và xây dựng giải pháp.

**Đầu vào:**
- Tên dự án / feature / service
- Loại tác động (từ Section 1 của PRD)
- Thông tin hiện tại về dịch vụ, pain points, objectives đã duyệt
- (Tuỳ chọn) Dữ liệu market research, competitors

**Đầu ra:**
- 5 hàng của Section 3 (Thực trạng, Nghiên cứu thị trường, Nội dung triển khai, Mục tiêu, Lợi ích)
- Format: Text sẵn sàng copy-paste vào PRD hoặc AI tự update file nếu path được cung cấp

**Workflow:**
- 5 steps tuần tự: Context → Thực trạng → Research → Tổng hợp → Output

**Ngôn ngữ:** Tiếng Việt  
**Output format:** Markdown table rows  
**Config variables used:** `communication_language`

---

## Conventions

- Bare paths được resolve từ skill root
- `{skill-root}` = `_bmad/skills/bmad-create-objectives-vds/`
- `{project-root}` = `/Users/truong23/truong23_project/bmad-learn-1/`

---

## On Activation

### Load Config

Đọc config từ `{project-root}/_bmad/bmm/config.yaml`.

Biến cần thiết:
- `communication_language`: expected = `vietnamese`
- `user_name`: tên user (dùng cho attribution)

---

## Workflow: Tạo Mục tiêu

### Step 1: Thu thập Context

**Trigger:** User gọi skill

**Actions:**
- Chào user bằng tiếng Việt
- Giải thích: Section 3 có 5 hàng phải viết chi tiết:
  1. Thực trạng (Current state)
  2. Nghiên cứu thị trường & đối thủ (Market research & Competitors)
  3. Nội dung triển khai (Implementation approach)
  4. Mục tiêu (Objectives)
  5. Lợi ích (Benefits)
- Hỏi 4 câu context:
  1. "Tên dự án / feature / service là gì?"
  2. "Loại tác động là gì? (Xây mới / Nâng cấp tính năng / Nâng cấp UX / Thay đổi chính sách / Cập nhật nội dung)" - để tôi hiểu scope
  3. "Bạn đã có tờ trình phê duyệt hoặc proposal nào không? (nếu có, cung cấp link/tóm tắt)"
  4. "Mục tiêu chính của dự án là gì? (nói sơ qua)"

**Output:**
- Context lưu, ready for Step 2

---

### Step 2: Phân tích Thực trạng

**Trigger:** User hoàn thành Step 1

**Actions:**
- Nhắc lại: "Bước này chúng ta sẽ mô tả thực trạng hiện tại"
- Hỏi user loạt câu hỏi có cấu trúc:
  1. "Hiện tại, dịch vụ/feature này đang có tình hình như thế nào? (nếu nâng cấp)"
  2. "Pain points của khách hàng là gì? Cụ thể, ví dụ gì?"
  3. "Root cause của các pain points đó là gì? Vì sao khách hàng gặp vấn đề?"
  4. "Có dữ liệu/metrics nào mô tả thực trạng không? (VD: Current DAU, Conversion rate, User feedback, v.v.)"
  5. "Từ góc độ doanh nghiệp, vấn đề là gì? Revenue impact? Loss to competitors?"
- Tổng hợp câu trả lời → Draft Row 1 (Thực trạng)

**Output:**
- Row 1 draft, ready for review/edit

---

### Step 3: Nghiên cứu Thị trường & Đối thủ

**Trigger:** User xác nhận Row 1 hoặc skip

**Actions:**
- Nhắc lại: "Bước này chúng ta sẽ phân tích cách thị trường + đối thủ giải quyết vấn đề"
- Hỏi user:
  1. "Bạn đã research competitors chưa? Họ giải quyết vấn đề này như thế nào?"
  2. "Có lessons/insights gì từ competitors? Cách nào hiệu quả, cách nào không?"
  3. "Thị trường hiện tại đang di chuyển theo hướng nào? Trends?"
  4. "Khách hàng đón nhận cách nào tốt nhất? Ưu tiên gì? (Price? UX? Features?)"
  5. "Có gap nào mà công ty chúng ta có thể chiếm lợi thế không?"
- Nếu user chưa research:
  - Gợi ý: "Bạn có thể skip, tôi sẽ suggest framework phân tích"
  - Hoặc: "Bạn tự research & quay lại"
- Tổng hợp → Draft Row 2 (Nghiên cứu thị trường)

**Output:**
- Row 2 draft

---

### Step 4: Xây dựng Giải pháp & Tổng hợp

**Trigger:** User hoàn thành Step 3

**Actions:**
- Nhắc lại: "Dựa trên thực trạng + research, chúng ta sẽ xây dựng giải pháp"
- Hỏi user:
  1. "Giải pháp của bạn sẽ triển khai như thế nào? (High level overview)"
  2. "Những feature/change chính là gì?"
  3. "Tại sao cách này sẽ giải quyết được pain points ở Step 2?"
  4. "Điểm khác biệt so với competitors là gì?"
- Tổng hợp → Draft Row 3 (Nội dung triển khai)
- Hỏi tiếp:
  1. "Mục tiêu sau 3/6/12 tháng là gì? (Quantifiable)"
  2. "KPIs chính là gì? (VD: Tăng DAU từ X lên Y, Revenue tăng Z%, v.v.)"
  3. "Có milestone/phase nào không?"
- Tổng hợp → Draft Row 4 (Mục tiêu)
- Hỏi tiếp:
  1. "Lợi ích cho khách hàng là gì? (User benefit)"
  2. "Lợi ích cho doanh nghiệp là gì? (Business benefit - revenue, retention, v.v.)"
  3. "Có lợi ích strategic khác không? (Market position, brand, v.v.)"
- Tổng hợp → Draft Row 5 (Lợi ích)

**Output:**
- Rows 3, 4, 5 draft

---

### Step 5: Output & Save

**Trigger:** User review tất cả 5 rows

**Actions:**
- Format tất cả 5 rows thành bảng Markdown:

```markdown
| STT | Hạng mục | Nội dung |
|-----|----------|----------|
| 1 | Thực trạng | [Row 1 content] |
| 2 | Nghiên cứu thị trường, đối thủ | [Row 2 content] |
| 3 | Nội dung triển khai (tổng quan) | [Row 3 content] |
| 4 | Mục tiêu | [Row 4 content] |
| 5 | Lợi ích triển khai | [Row 5 content] |
```

- Hỏi user: "Bạn muốn:"
  - A) Copy-paste vào PRD manual
  - B) Tôi tự update vào file PRD (cần cung cấp file path)
  - C) Edit bất kỳ row nào trước khi save
- Nếu chọn C: Allow iterative editing tới khi user satisfied
- Nếu chọn A hoặc B: Output content và xác nhận
- Báo: "Section 3 - Mục tiêu đã hoàn tất! 🎯"

**Output:**
- 5 rows formatted, ready for PRD

---

## Troubleshooting

**Q: User không biết competitors/market info?**  
A: Suggest framework phân tích, user có thể tự research & quay lại, hoặc AI gợi ý general fintech trends.

**Q: Mục tiêu quá chung chung (VD: "Tăng DAU")?**  
A: Hỏi thêm: "Tăng bao nhiêu? Trong bao lâu? Từ con số nào?"

**Q: File PRD không tìm thấy khi save?**  
A: Fallback to copy-paste method, user tự điền.
