# VDS PRD Method - Module Documentation

## Overview

**VDS PRD Method** is a custom BMad module designed for Fintech/Tech companies using Vietnamese as the primary language. It provides a complete workflow for creating Product Requirements Documents (PRD) following VDS company standards.

**Created:** May 7, 2026  
**Version:** 1.0.0  
**Status:** ✅ Ready for use  

---

## Module Contents

This module includes 5 skills:

### Main Skill
- **`bmad-create-prd-vds`** (Menu: **PV**)  
  Orchestrator skill that guides users through 6 steps of PRD creation

### Supporting Skills
- **`bmad-validate-prd-vds`** (Menu: **VV**)  
  Validates PRD quality section-by-section
  
- **`bmad-create-objectives-vds`** (Menu: **OV**)  
  Assists with Section 3 (Objectives) with market research support
  
- **`bmad-create-metrics-vds`** (Menu: **MV**)  
  Helps define KPIs and success metrics for Section 4
  
- **`bmad-create-user-stories-vds`** (Menu: **UV**)  
  Creates user story maps and functional requirement details for Section 5.1.2

---

## PRD Template Structure

The module uses a standardized PRD template based on VDS company standards:

```
1. Phân loại (Classification)
2. Bảng tổng hợp thay đổi (Change History)
3. Mục tiêu (Objectives)
4. Tiêu chí thành công (Success Criteria)
5. Yêu cầu sản phẩm (Product Specifications)
   5.1.1 Tổng quan (Overview)
   5.1.2 Yêu cầu chức năng (Functional Requirements)
   5.1.3 Yêu cầu phi chức năng (Non-Functional Requirements)
6. Yêu cầu đặt event tracking (Event Tracking Requirements)
```

---

## Quick Start

### 1. Create a New PRD

```bash
/bmad-create-prd-vds
```

The skill will guide you through:
- **Step 1:** Initialize project + classification
- **Step 2:** Define objectives (use sub-skill if needed)
- **Step 3:** Set success criteria (use sub-skill if needed)
- **Step 4:** Describe product overview
- **Step 5:** Create user stories (use sub-skill if needed)
- **Step 6:** Finalize and suggest validation

### 2. Validate a PRD

```bash
/bmad-validate-prd-vds
```

Checks:
- ✅ Completeness (all required fields filled)
- ✅ Quality (content is specific and detailed)
- ✅ Consistency (sections align with each other)

### 3. Get Help with Objectives

```bash
/bmad-create-objectives-vds
```

Guides you through:
- Current state analysis
- Market & competitor research
- Implementation approach definition
- Objective and benefit articulation

### 4. Design Metrics

```bash
/bmad-create-metrics-vds
```

Helps define:
- Business metrics (DAU, Revenue, Retention, etc.)
- Operational metrics (Performance, Quality, etc.)
- KPI compliance with company standards

### 5. Create User Stories

```bash
/bmad-create-user-stories-vds
```

Supports:
- 7-stage customer journey framework
- User story mapping
- Iterative story detail definition

---

## Configuration

### Output Location

PRD files are saved to:
```
{project-root}/_bmad-output/planning-artifacts/[project-name]-prd.md
```

### Language

- **UI/Chat:** Vietnamese (tiếng Việt)
- **Document output:** Vietnamese
- **All prompts & help text:** Vietnamese

---

## File Structure

```
_bmad/skills/
├── bmad-create-prd-vds/
│   ├── SKILL.md
│   ├── README.md (this file)
│   ├── templates/
│   │   └── prd-vds-template.md
│   └── config.yaml
├── bmad-validate-prd-vds/
│   └── SKILL.md
├── bmad-create-objectives-vds/
│   └── SKILL.md
├── bmad-create-metrics-vds/
│   └── SKILL.md
└── bmad-create-user-stories-vds/
    └── SKILL.md
```

---

## Integration with BMad

### Catalog Registration

All 5 skills are registered in:
- `_bmad/_config/bmad-help.csv` (5 entries)
- `_bmad/_config/skill-manifest.csv` (5 entries)

They appear in `/bmad-help` under **"VDS PRD Method"** group.

### Phase

All skills are in phase **2-planning**:
- `bmad-create-prd-vds`: Required (`required=true`)
- Others: Optional (`required=false`)

### Dependencies

- `bmad-validate-prd-vds` comes after `bmad-create-prd-vds`
- Sub-skills (`objectives`, `metrics`, `user-stories`) can be called from main skill or standalone

---

## Fintech-Specific Features

The module includes fintech/payment-specific considerations:

### Suggested Business Metrics
- DAU / MAU / Daily Active Transactions
- Conversion Rate (signup → first transaction)
- Average Transaction Value / ARPU
- Customer Retention Rate / Churn
- Total Revenue / Revenue Growth

### Suggested Operational Metrics
- Funnel drop-off rates per step
- API response time / latency
- Transaction error rate
- User onboarding time
- Support response time

### KPI Compliance
- Checks against company quality standards
- Supports additional KPI configuration

---

## Workflow: Hybrid Architecture

The main skill (`bmad-create-prd-vds`) uses **Hybrid workflow**:

```
Linear flow through 6 steps
    ↓
Each step offers 3 choices:
  1. Continue to next step
  2. Validate this section
  3. Go back to previous step
    ↓
Can invoke sub-skills anytime for deeper support
    ↓
Final step suggests full PRD validation
```

---

## Tips for Best Results

### 1. Preparation
- Have approval/proposal documents ready (for metrics & objectives)
- Prepare competitor/market research (for objectives)
- Know your target users and channels

### 2. Iterative Approach
- Complete basic flow first
- Use validation to identify gaps
- Call sub-skills for detailed sections
- Re-validate after improvements

### 3. Collaboration
- PRD file is Markdown → easy to share
- Use git to track versions
- Team can provide feedback on generated content

### 4. Customization
- Edit template if needed: `templates/prd-vds-template.md`
- Adjust metrics per company standards
- Customize user journey stages if needed

---

## Troubleshooting

### Q: Skills not showing in /bmad-help?
A: Restart Claude Code or refresh the session. CSV entries should be auto-detected.

### Q: File not being saved?
A: Check that `{planning_artifacts}` directory exists at `_bmad-output/planning-artifacts/`

### Q: How to edit generated content?
A: All output is Markdown files. Edit directly in your editor, then re-validate with `/bmad-validate-prd-vds`

### Q: Can I customize the template?
A: Yes! Edit `templates/prd-vds-template.md` and it will be used for new PRDs.

---

## Support & Documentation

- **Quick Start:** Read this README
- **Detailed Workflows:** Check each SKILL.md file
- **Template:** `templates/prd-vds-template.md`
- **Config:** `config.yaml`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-05-07 | Initial release - 5 skills module |

---

**Status:** ✅ Ready for production use

For questions or improvements, check the SKILL.md files or review the module plan at `/Users/truong23/.claude/plans/warm-brewing-meerkat.md`
