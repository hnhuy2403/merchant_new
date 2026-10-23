---
name: bmad-create-metrics-vds
description: Thiết lập KPI/Metrics cho Section 4 - Tiêu chí thành công. Use when the user says "tạo metrics", "thiết lập KPI", "create metrics VDS", hoặc cần tư vấn success criteria
---

# Tạo Metrics VDS (Section 4)

## Overview

Skill này hỗ trợ PO thiết lập KPI và metrics cho Section 4 (Tiêu chí thành công) của PRD.

**Đầu vào:**
- Mục tiêu từ Section 3 (hoặc user cung cấp objectives)
- Loại dự án (từ Section 1)
- Metrics đã có từ tờ trình phê duyệt (nếu có)

**Đầu ra:**
- Section 4 hoàn chỉnh:
  - 4.1: Chỉ số đánh giá hiệu quả (Business Metrics)
  - 4.2: Chỉ số vận hành (Operational Metrics)
  - 4.3: Chỉ số chất lượng dịch vụ (KPI Compliance)
- Format: Text để copy-paste hoặc AI tự update PRD

**Workflow:**
- 4 steps: Context → Business Metrics → Operational Metrics → KPI Compliance → Output

**Ngôn ngữ:** Tiếng Việt

---

## Conventions

- `{skill-root}` = `_bmad/skills/bmad-create-metrics-vds/`
- `{project-root}` = `/Users/truong23/truong23_project/bmad-learn-1/`

---

## On Activation

### Load Config

Đọc config từ `{project-root}/_bmad/bmm/config.yaml`.

---

## Workflow: Tạo Metrics

### Step 1: Thu thập Context

**Trigger:** User gọi skill

**Actions:**
- Chào user & explain: Section 4 = 3 sub-sections
  - 4.1: Business Metrics (KPIs để measure success)
  - 4.2: Operational Metrics (metrics để monitor & improve towards 4.1)
  - 4.3: KPI Compliance (chất lượng dịch vụ tiêu chuẩn)
- Hỏi:
  1. "Bạn có Section 3 (Mục tiêu) đã viết không? Có thể copy-paste tóm tắt?"
  2. "Loại dự án là gì? (Fintech payment / Digital banking / VAS service / v.v.)" - để AI suggest relevant metrics
  3. "Có metrics nào trong tờ trình phê duyệt không?"
  4. "Mục tiêu chính là gì? (Tăng DAU / Tăng revenue / Giảm cost / Cải thiện UX / v.v.)"

**Output:**
- Context lưu

---

### Step 2: Thiết lập Business Metrics (4.1)

**Trigger:** User hoàn thành Step 1

**Actions:**
- Nhắc lại: "4.1 là metrics chính để đo liệu dự án có thành công không"
- Hỏi user:
  1. "Từ mục tiêu của bạn, metrics chính nên là gì?" (User provide hoặc AI suggest)
  2. "Có baseline hiện tại không? (Current value)"
  3. "Target là bao nhiêu? Trong bao lâu?" (Timeframe: 3/6/12 months?)
  4. "Có secondary metrics không?" (VD: DAU là primary, retention là secondary)
- Nếu user chưa clear:
  - AI suggest framework cho fintech/payment:
    - **Engagement:** DAU, MAU, Daily transaction volume
    - **Monetization:** Total revenue, ARPU, Transaction value
    - **Retention:** Churn rate, 30-day retention
    - **Quality:** Error rate, API uptime, User satisfaction
    - **Growth:** Month-over-month growth rate
  - User chọn metrics relevant
- Tổng hợp → Draft 4.1 (danh sách metrics + baseline + target)

**Output:**
- Section 4.1 draft

---

### Step 3: Thiết lập Operational Metrics (4.2)

**Trigger:** User xác nhận 4.1

**Actions:**
- Nhắc lại: "4.2 là metrics vận hành - giúp team monitor & improve để đạt 4.1 targets"
- Giải thích: "Nếu business metric là 'Tăng DAU', operational metrics là 'Reduce funnel drop-off ở step X', 'Improve onboarding time', v.v."
- Hỏi user:
  1. "Để đạt được 4.1 targets, team cần monitor gì?" (Funnel metrics, performance metrics, v.v.)
  2. "Có bottleneck nào cần track không?" (VD: Slow API → response time metric)
  3. "User feedback metrics?" (NPS, CSAT, v.v.)
- AI suggest operational framework:
  - **Funnel metrics:** Per-step conversion, drop-off rate
  - **Performance:** API response time, Load time, Error rate by endpoint
  - **Quality:** Bug count, User feedback sentiment, Support tickets
  - **Operational:** Feature adoption rate, A/B test results, Rollout progress
- User chọn relevant → Draft 4.2

**Output:**
- Section 4.2 draft

---

### Step 4: KPI Compliance (4.3)

**Trigger:** User xác nhận 4.2

**Actions:**
- Nhắc lại: "4.3 là checklist - confirm compliance với tiêu chuẩn chất lượng dịch vụ của công ty"
- Giải thích: "Theo quy định của bộ phận QLCL, cần đảm bảo các KPI tiêu chuẩn: uptime, latency, error rate, v.v."
- Hỏi user:
  1. "Bạn có biết tiêu chuẩn chất lượng dịch vụ của công ty không? (Tham chiếu tài liệu nào?)"
  2. "Dự án này có cần bổ sung KPI thêm không?" (Beyond standard)
- Default: Suggest standard fintech KPIs:
  - [ ] API uptime ≥ 99.9%
  - [ ] API latency < 500ms
  - [ ] Error rate < 0.5%
  - [ ] User onboarding time < 5 phút
  - [ ] v.v.
- User confirm + add extras → Draft 4.3

**Output:**
- Section 4.3 draft

---

### Step 5: Output & Save

**Trigger:** User review all 3 sub-sections

**Actions:**
- Format thành:

```markdown
## 4. Tiêu chí thành công (Success Criteria)

### 4.1. Chỉ số đánh giá hiệu quả (Metrics to measure success)

| Metric | Baseline | Target | Timeframe |
|--------|----------|--------|-----------|
| DAU | X | Y | 6 months |
| ... | | | |

### 4.2. Chỉ số vận hành (Metrics to monitor)

| Operational Metric | Current | Target | Owner |
|-------------------|---------|--------|-------|
| Funnel drop-off step 1 | X% | Y% | Team A |
| ... | | | |

### 4.3. Chỉ số chất lượng dịch vụ (KPI)

- [x] Đảm bảo chỉ số chất lượng dịch vụ KPI theo quy định tiêu chuẩn
- Các chỉ số bổ sung:
  - API uptime ≥ 99.9%
  - ...
```

- Hỏi user: Copy-paste / Auto-update file / Edit more?
- Báo: "Section 4 - Tiêu chí thành công đã hoàn tất! ✅"

**Output:**
- Section 4 formatted, ready for PRD

---

## Fintech-specific Metrics Framework

Skill này có thể gợi ý fintech-specific metrics:

**Payment Metrics:**
- Transaction volume, Transaction value, Failed transaction rate, Settlement time

**User Metrics:**
- DAU, MAU, Daily transaction users, User growth rate, Churn rate

**Financial Metrics:**
- ARPU, Total revenue, Profit margin, CAC (Customer Acquisition Cost), LTV

**Quality Metrics:**
- API uptime, Latency, Error rate, Support response time, NPS score

**Security/Compliance:**
- Fraud rate, Data breach incidents, Compliance audit score

---

## Troubleshooting

**Q: User không biết baseline/target?**  
A: Suggest lookup từ tờ trình hoặc historical data. Hoặc team leadership input.

**Q: Metrics quá nhiều?**  
A: Suggest 3-5 business metrics + 5-8 operational metrics (đủ detail, không quá overload).

**Q: Standard KPI gì?**  
A: Suggest liên hệ QLCL department hoặc lookup docs. Skill cung cấp framework, user confirm.
