# Liên Kết Source Code — Story {{epic_num}}.{{story_num}}: {{story_title}}

> **Hướng dẫn:** File này lưu mọi đường dẫn / link đến source code liên quan tới story. Auto-fill từ `tts.bitbucket` config (nếu đã chạy `bmad-tts-bitbucket-connect`) và git working directory hiện tại. Nếu chưa kết nối Bitbucket, để placeholder để điền tay.

## 1. Repository chính

| Trường | Giá trị |
|--------|---------|
| Tên repo | {{src_main_repo_name}} |
| Bitbucket URL | {{src_main_repo_bitbucket_url}} |
| Đường dẫn local | {{src_main_repo_local_path}} |
| Branch dự kiến | `feature/{{epic_num}}-{{story_num}}-{{story_title_slug}}` |

<!-- Auto-fill rules:
- src_main_repo_name: từ `tts.bitbucket.workspace` + repo slug, hoặc `basename` của git remote origin URL.
- src_main_repo_bitbucket_url: ưu tiên đọc từ `git remote get-url origin`. Nếu là https/ssh Bitbucket → chuyển thành dạng web URL (ví dụ `https://bitbucket.org/<workspace>/<repo>` hoặc `https://<server-host>/projects/<KEY>/repos/<slug>`). Nếu không xác định được → `[CẦN BỔ SUNG: URL Bitbucket]`.
- src_main_repo_local_path: absolute path của project root hiện tại.
- story_title_slug: kebab-case của story_title.
-->

## 2. Module / thư mục cần đụng đến

> Liệt kê các module trong repo mà story này sẽ tạo/sửa. Lấy từ `detail-design.md § 2.1`.

{{src_modules_affected}}

<!-- Auto-fill ví dụ:
| Module | Đường dẫn | Loại | Ghi chú |
|--------|-----------|------|---------|
| Auth UI | `apps/web/src/features/auth/` | UPDATE | Thêm MFA component |
| Auth API | `apps/api/src/routes/auth/` | UPDATE | Endpoint `/mfa/verify` |
| Auth shared types | `packages/shared/src/auth.ts` | UPDATE | Thêm type `MfaSession` |
-->

## 3. Repository phụ thuộc (nếu có)

{{src_dependent_repos}}

<!-- Auto-fill: nếu story phụ thuộc service/library ở repo khác (ví dụ shared SDK, infrastructure repo), liệt kê tên + URL + role. Nếu không có → "_Không có_". -->

## 4. Tài liệu / link tham khảo

{{src_reference_links}}

<!-- Auto-fill các loại link sau (nếu xác định được):
- Pull request mẫu / pattern reference
- Issue / ticket Jira / Linear (nếu có integration)
- Wiki / Confluence / docs page liên quan
- Design doc trên Figma (nếu story có UI)
- Architecture decision record (ADR) liên quan
-->

## 5. Lệnh nhanh

```bash
# Vào thư mục project
cd {{src_main_repo_local_path}}

# Tạo branch làm việc
git checkout -b feature/{{epic_num}}-{{story_num}}-{{story_title_slug}}

# (tùy chọn) Mở Bitbucket repo
# {{src_main_repo_bitbucket_url}}
```

---

_Tài liệu này sinh tự động bởi `bmad-tts-create-story`. Khi có repo / module mới phát hiện trong quá trình implement, cập nhật ngay để các skill `bmad-tts-dev-story` và `bmad-tts-design-story-pr` dùng đúng nguồn._
