# VDS PRD Method - Quick Start Guide

**Start using the VDS PRD module in 5 minutes**

---

## 🚀 The Fastest Way to Create a PRD

### Option 1: Start from Scratch

```bash
/bmad-create-prd-vds
```

Then follow the prompts:
1. **Name your project** (e.g., "Tính năng thanh toán mới")
2. **Choose classification** (Đối tượng tác động + Hình thức tác động)
3. Work through 6 steps:
   - Step 1: Init & Phân loại ✅
   - Step 2: Mục tiêu (call sub-skill if needed)
   - Step 3: Metrics (call sub-skill if needed)
   - Step 4: Tổng quan sản phẩm
   - Step 5: User Stories (call sub-skill if needed)
   - Step 6: Event Tracking & Finalize

**Output:** PRD file at `_bmad-output/planning-artifacts/[project-name]-prd.md`

---

## 🔍 Quick Command Reference

### Create a New PRD
```bash
/bmad-create-prd-vds
```
Menu code: `PV`

### Validate an Existing PRD
```bash
/bmad-validate-prd-vds
```
Menu code: `VV`
- Checks completeness, quality, consistency
- Suggests improvements

### Get Help with Objectives (Section 3)
```bash
/bmad-create-objectives-vds
```
Menu code: `OV`
- Guided market research
- Thực trạng analysis
- Benefit articulation

### Design Metrics & KPIs (Section 4)
```bash
/bmad-create-metrics-vds
```
Menu code: `MV`
- Business metrics (DAU, Revenue, etc.)
- Operational metrics (Performance, Quality, etc.)
- KPI compliance

### Create User Stories (Section 5.1.2)
```bash
/bmad-create-user-stories-vds
```
Menu code: `UV`
- 7-stage customer journey
- User story mapping
- Iterative story detailing

---

## 💡 Tips for Success

### 1. Have These Ready
- ✅ Tờ trình / Approval document (for objectives & metrics)
- ✅ Basic market research (competitors, customer pain points)
- ✅ Target users & use channels info

### 2. Use Sub-skills When Needed
The main workflow will **suggest** sub-skills when helpful:
- Section 3 (Objectives) is complex? → Use `/bmad-create-objectives-vds`
- Section 4 (Metrics) needs guidance? → Use `/bmad-create-metrics-vds`
- Section 5.1.2 (User Stories) is detailed? → Use `/bmad-create-user-stories-vds`

### 3. Validate Early & Often
After each section:
- Choose **"Validate this section"** option
- Get immediate feedback
- Fix issues before moving forward

### 4. Iterate, Don't Perfect
- Complete basic flow first
- Validate to find gaps
- Refine with sub-skills
- Re-validate
- Ship! 🚀

---

## 📋 PRD Structure at a Glance

```
Your PRD will have 6 main sections:

1. Phân loại (Classification)
   - What type of project?
   - What kind of changes?

2. Bảng thay đổi (Change History)
   - Version tracking
   - Who changed what & when

3. Mục tiêu (Objectives)  ⭐ Complex section
   - Current state
   - Market research
   - Solution approach
   - Goals
   - Benefits

4. Tiêu chí thành công (Success Criteria)  ⭐ Metrics-heavy
   - Business metrics (DAU, Revenue, etc.)
   - Operational metrics (Performance, etc.)
   - KPI compliance

5. Yêu cầu sản phẩm (Product Specs)  ⭐ Most detailed
   - 5.1.1 Overview (users, channels, conditions, policies)
   - 5.1.2 User Stories & flows (7 customer journey stages)
   - 5.1.3 Non-functional requirements

6. Event Tracking
   - Which tracking system? (EVT / Adjust / None)
```

---

## 🎯 Common Workflows

### "I have 30 minutes to create a PRD"

1. Run `/bmad-create-prd-vds`
2. Fill in Steps 1-6 with basic info
3. Run `/bmad-validate-prd-vds`
4. Note gaps
5. Share for team feedback

### "I need a high-quality PRD"

1. Gather research & approval docs
2. Run `/bmad-create-objectives-vds` first (deep-dive Section 3)
3. Run `/bmad-create-metrics-vds` (design metrics)
4. Run `/bmad-create-prd-vds` (fill in rest)
5. Run `/bmad-create-user-stories-vds` (detail user flows)
6. Run `/bmad-validate-prd-vds` (ensure quality)
7. Share for review

### "I have an existing PRD to improve"

1. Open your markdown PRD file
2. Run `/bmad-validate-prd-vds` (find weaknesses)
3. Edit sections manually OR call sub-skills
4. Re-validate
5. Done!

---

## ❓ FAQ

**Q: Can I save my work in progress?**  
A: Yes! PRD is a Markdown file at `_bmad-output/planning-artifacts/[name]-prd.md`. Edit anytime.

**Q: What if I don't know something (e.g., market data)?**  
A: The sub-skills will ask guided questions. You can skip & fill in later.

**Q: Can I customize the PRD template?**  
A: Yes! Edit `_bmad/skills/bmad-create-prd-vds/templates/prd-vds-template.md`

**Q: How do I share the PRD?**  
A: It's a Markdown file → email it, commit to git, or paste into docs tool.

**Q: Can multiple people work on one PRD?**  
A: Yes! Use git to version-control & merge changes.

**Q: Which sections are required?**  
A: Sections 1, 3, 4, 5 are important. You can skip 2 & 6 if needed.

---

## 📖 Next Steps

- **Full Module Docs:** Read `README.md`
- **Integration Details:** See `INTEGRATION.md`
- **Detailed Workflows:** Check each `SKILL.md` file
- **PRD Template:** View `templates/prd-vds-template.md`

---

## ✨ You're Ready!

```bash
/bmad-create-prd-vds
```

This will:
1. Ask you 2-3 clarifying questions
2. Create a PRD template for your project
3. Guide you through 6 sections
4. Save to `_bmad-output/planning-artifacts/`
5. Suggest validation when done

**Good luck! 🎉**
