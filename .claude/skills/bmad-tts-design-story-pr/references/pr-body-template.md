## Detail Design Review

**Story:** `{{story_key}}` — {{story_title}}
**Epic:** {{epic_num}} · **Story:** {{story_num}}
**Head:** `{{head_branch}}` → **Base:** `{{base_branch}}`
**Team:** {{team}} · **Reviewers:** {{reviewers}}

---

### 📐 Design Document

📄 [`{{design_doc_path}}`]({{design_doc_path}})

> Vui lòng đọc design doc trước khi review PR này. Mọi quyết định kiến trúc, contract, file change, và test plan đã được mô tả chi tiết trong tài liệu đó.

---

### ✅ Acceptance Criteria

{{ac_summary}}

---

### ⚠️ Breaking Changes

{{breaking_changes}}

---

### 🧪 Test Plan (tóm tắt)

{{test_plan_summary}}

---

### ❓ Open Questions

{{open_questions}}

---

### 🎯 Review Focus

Reviewer được mong đợi đánh giá:

- **Tính khả thi kiến trúc** — design có phù hợp với codebase và pattern hiện tại?
- **Contract & data model** — API, schema, state transitions đầy đủ và đúng?
- **Edge cases & error handling** — đã cover các kịch bản failure quan trọng?
- **Breaking changes** — impact và migration path đã rõ ràng?
- **Test plan** — coverage có đáp ứng acceptance criteria?

Approve PR này = phê duyệt design để dev bắt đầu implementation. Sau khi merge, dev sẽ chạy `/bmad-dev-story` để triển khai.
