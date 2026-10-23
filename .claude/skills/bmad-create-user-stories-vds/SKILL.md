---
name: bmad-create-user-stories-vds
description: Tạo User Story Map và bảng chi tiết từng story cho Section 5.1.2. Use when the user says "viết user story", "tạo user story map", "create user stories VDS", hoặc cần tư vấn functional requirements
---

# Tạo User Stories VDS (Section 5.1.2)

## Overview

Skill này hỗ trợ PO tạo Section 5.1.2 (Yêu cầu chức năng) của PRD - section quan trọng nhất, bao gồm:
- User Story Map: 7 chặng hành trình khách hàng + user stories
- Story Detail Tables: Chi tiết từng story (steps B1..Bn, inputs/outputs, mockups)

**Đầu vào:**
- Nội dung triển khai từ Section 3 (hoặc user describe feature)
- Target users từ Section 5.1.1
- (Tuỳ chọn) Existing design/wireframes

**Đầu ra:**
- Section 5.1.2 hoàn chỉnh:
  - User Story Map table (7 chặng + N stories)
  - N Story Detail tables (mỗi story có B1..Bn steps)
- Format: Markdown để copy-paste hoặc auto-update PRD

**Workflow:**
- 2 sub-processes: A (User Story Map) + B (Story Details - iterative)

**Ngôn ngữ:** Tiếng Việt

---

## Conventions

- `{skill-root}` = `_bmad/skills/bmad-create-user-stories-vds/`
- `{project-root}` = `/Users/truong23/truong23_project/bmad-learn-1/`

---

## On Activation

### Load Config

Đọc config từ `{project-root}/_bmad/bmm/config.yaml`.

---

## Workflow: Tạo User Stories

### SUB-PROCESS A: User Story Map

#### Step 1: Scope & Target Users

**Trigger:** User gọi skill

**Actions:**
- Chào user & explain: Sẽ tạo 2 phần:
  - Phần A: User Story Map (7 chặng hành trình + stories)
  - Phần B: Story Detail tables (steps & mockups)
- Hỏi:
  1. "Feature/service mô tả là gì?"
  2. "Target users là ai? (từ Section 5.1.1 hoặc user describe)"
  3. "Kênh chính là gì? (App / Web / v.v.)" - để AI adjust journey
  4. "Có existing design/wireframes không?" (để reference mockup steps)
  5. "User journey bao gồm những giai đoạn nào?" (hoặc: dùng 7 chặng mặc định?)

**Output:**
- Context lưu (feature, users, channel)

---

#### Step 2: Journey Framework

**Trigger:** User confirm context

**Actions:**
- Nhắc lại: "Template PRD có 7 chặng hành trình (chuẩn fintech):"
  1. Chặng 1: Nhận thức về thương hiệu (Brand awareness)
  2. Chặng 2: Tìm hiểu thông tin (Research info)
  3. Chặng 3: Onboard/Đăng ký dịch vụ (Onboarding)
  4. Chặng 4: Sử dụng (Usage)
  5. Chặng 5: Liên hệ xử lý lỗi, khiếu nại (Support/Issue handling)
  6. Chặng 6: Gắn bó/Rời bỏ (Retention/Churn)
  7. Chặng 7: Kết nối, yêu cầu hỗ trợ (Community/Feedback)
- Hỏi user: "Chặng nào relevant cho dự án của bạn?"
  - User confirm từng chặng (có thể bỏ chặng nào không relevant, hoặc thêm chặng custom)
  - AI ghi lại confirmed stages

**Output:**
- Confirmed journey stages

---

#### Step 3: User Story Generation

**Trigger:** User confirm stages

**Actions:**
- Nhắc lại: "Giờ chúng ta sẽ tạo user stories điển hình cho mỗi chặng"
- Với mỗi chặng confirmed, AI suggest 1-3 user stories điển hình:
  - VD Chặng 1 (Brand awareness): "User nhìn thấy quảng cáo / User tìm hiểu trên review sites / User được bạn bè recommend"
  - VD Chặng 3 (Onboarding): "User tải app / User đăng ký tài khoản / User xác minh KYC / User setup payment method"
  - VD Chặng 4 (Usage): "User thực hiện giao dịch / User check balance / User set spending limit / User link ngân hàng"
  - Etc.
- Hỏi user: "Các story này có phù hợp không? Có thêm story nào không? Có bỏ story nào không?"
- User chỉnh sửa → AI ghi lại final user stories

**Output:**
- List of user stories per stage (ordered)

---

#### Step 4: User Story Map Output

**Trigger:** User confirm all stories

**Actions:**
- Format User Story Map table:

```markdown
## 5.1.2. Yêu cầu chức năng

### Biểu đồ mô tả chức năng
N/a (hoặc [Mermaid diagram nếu cần])

### Bảng mô tả hành trình khách hàng (User Story Map)

| Chặng | User Story | Note |
|-------|------------|------|
| Chặng 1: Nhận thức | US1: User nhìn thấy quảng cáo | |
| | US2: User được recommend từ bạn bè | |
| Chặng 2: Tìm hiểu | US3: User đọc review | |
| | US4: User xem website landingpage | |
| Chặng 3: Onboard | US5: User tải app | |
| | US6: User đăng ký & KYC | |
| | US7: User setup payment method | |
| Chặng 4: Sử dụng | US8: User thực hiện giao dịch | |
| | US9: User check balance & history | |
| Chặng 5: Support | US10: User report issue | |
| Chặng 6: Retention | US11: User receive promotional offer | |
| | US12: User churn (alternative path) | |
| Chặng 7: Community | US13: User provide feedback | |
```

- Hỏi user: "Bảng này OK không? Sẵn sàng sang Phần B (Story Details)?"

**Output:**
- User Story Map table formatted

---

### SUB-PROCESS B: Story Details (Iterative Loop)

#### Step 5: Detail Loop - Per Story

**Trigger:** User ready for details

**Actions:**
- Nhắc lại: "Giờ chúng ta sẽ detail từng User Story - mỗi story có multiple steps (B1, B2, B3...)"
- Start loop với story đầu tiên (US1):
  1. Hỏi user: "Story này có bao nhiêu steps? (hoặc tôi draft, bạn review?)"
  2. Nếu user chưa biết: AI draft steps dựa trên story name:
     - Story: "User nhìn thấy quảng cáo"
     - AI draft:
       - B1: User mở social media / website
       - B2: User nhìn thấy quảng cáo của dịch vụ
       - B3: User click vào quảng cáo
       - B4: User navigate tới landing page
     - User review + edit (add/remove/modify steps)
  3. Với mỗi step, AI hỏi:
     - "Input/condition gì?"
     - "Output/action result là gì?"
     - "Có mockup/screenshot reference không?" (user provide or mark as TBD)
  4. Format detail table:

```markdown
### User Story 1: US1 - User nhìn thấy quảng cáo

| User Story | Mô tả | Mockup | Note |
|------------|-------|--------|------|
| US1 | B1: User mở app / website → thấy feed / homepage | [Home page mockup] | Default landing |
| | B2: Ads appear → user nhìn thấy quảng cáo của dịch vụ | [Ads mockup] | Targeted ads |
| | B3: User click ads → open landing page | [LP mockup] | CTA button |
```

  5. Hỏi user: "Story này OK? Tiếp story kế?"
  6. Repeat với story tiếp theo

- **Loop control:**
  - Sau mỗi story: User chọn:
    - "Tiếp story kế"
    - "Review lại story này"
    - "Thêm story mới"
    - "Hoàn thành (tất cả stories đã detail)"

**Output:**
- N Story Detail tables (accumulating)

---

#### Step 6: Finalize & Output

**Trigger:** User confirm tất cả stories detailed

**Actions:**
- Tổng hợp tất cả content:
  - User Story Map (Step 4 output)
  - Story Detail tables (Step 5 output)
- Hỏi user: "Bạn muốn:"
  - A) Copy-paste vào PRD
  - B) Tôi tự update file PRD (cung cấp path)
  - C) Edit thêm (revise stories hoặc steps)
- Nếu chọn C: Allow iterative edits
- Nếu chọn A/B: Output content + confirm
- Báo: "Section 5.1.2 - Yêu cầu chức năng đã hoàn tất! 🎉"

**Output:**
- Section 5.1.2 formatted (User Story Map + Detail tables)

---

## Fintech Payment User Story Examples

Skill có thể reference fintech payment stories:

**Chặng 3 (Onboarding) Examples:**
- US: User tải app từ App Store/Play Store
- US: User đăng ký email/phone
- US: User hoàn thành KYC (upload ID, selfie, address)
- US: User setup PIN/biometric
- US: User link primary bank account
- US: User setup backup payment method

**Chặng 4 (Usage) Examples:**
- US: User view account balance & transaction history
- US: User initiate transfer to another account
- US: User pay bills / shopping
- US: User set spending limits / alerts
- US: User view investment portfolio / savings goals
- US: User request e-statement

**Chặng 5 (Support) Examples:**
- US: User report transaction issue
- US: User contact support via chat/call
- US: User dispute unauthorized transaction
- US: User request account freeze

---

## Non-functional Requirements (Section 5.1.3)

Sau khi complete Section 5.1.2, skill có thể prompt:
- "Có Non-functional requirements không?"
- Suggest standard NFRs: Performance, Security, Accessibility, Localization, v.v.
- User input or skip → Output as Section 5.1.3

---

## Troubleshooting

**Q: User không biết bao nhiêu steps cho mỗi story?**  
A: AI draft 3-5 steps mặc định, user confirm/adjust.

**Q: Mockup field - user chưa có design?**  
A: Mark as "[TBD - Design needed]" hoặc "[Reference from Figma link]".

**Q: Stories quá nhiều?**  
A: Suggest focus vào critical journeys (3-5 main stories), optional stories có thể skip.

**Q: User quay lại modify story sau khi detail?**  
A: Allow "Go back to story X" để re-edit.
