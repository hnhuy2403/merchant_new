# Confluence Skill

Skill + CLI giúp tương tác với **Confluence nội bộ (Server/Data Center)** hoàn toàn bằng **hội thoại tiếng Việt** — dành cho người dùng không rành kỹ thuật. Hỗ trợ nhiều domain (sản xuất / đối tác) dùng chung một tài khoản, đẩy tài liệu Markdown kèm ảnh và biểu đồ Mermaid lên Confluence với định dạng đẹp.

> Người dùng cuối **không gõ lệnh**. Họ chỉ chat với Claude; Claude chạy CLI ngầm phía sau.

## Tính năng

- **Đa domain**: thêm/đổi giữa nhiều Confluence (vd nội bộ sản xuất và đối tác), một username + token chung.
- **Markdown → Confluence**: heading, danh sách, bảng, code block, link → định dạng storage của Confluence.
- **Ảnh & biểu đồ**: ảnh local được upload làm attachment; biểu đồ Mermaid được render thành PNG và nhúng vào trang.
- **Bộ nhớ tài liệu**: nhớ các trang đã đẩy (trong `.confluence/pages.json`) để sửa lại mà không cần nhớ link.
- **CRUD đầy đủ**: tìm space/page, tạo, sửa, xóa trang.

## Yêu cầu

- Node.js >= 18
- Google Chrome hoặc Chromium (để render biểu đồ Mermaid). Tự dò theo nền tảng; có thể chỉ định qua biến môi trường `PUPPETEER_EXECUTABLE_PATH`.

## Cài đặt (cho người dùng mới)

Người dùng non-tech: xem hướng dẫn từng bước có giải thích trong **[SETUP.md](SETUP.md)**.

Tóm tắt — chỉ **2 lệnh, làm 1 lần**:

```bash
git clone <bitbucket-url> confluence-vds-skill
cd confluence-vds-skill && node setup.js
```

`setup.js` tự động lo hết:
1. Kiểm tra Node + Chrome (cảnh báo nếu thiếu).
2. `npm install` (cài `markdown-it` + `mermaid-cli`).
3. Điền sẵn 2 domain công ty vào `~/.confluence-vds-skill/domains.json` (người dùng không cần biết IP).
4. Copy `SKILL.md` vào `~/.claude/skills/confluence-vds-skill/` để Claude tự nạp.

Chạy lại `node setup.js` an toàn (idempotent): giữ nguyên token/username đã có, chỉ bổ sung phần thiếu.

## Kết nối Confluence (qua chat — không gõ lệnh)

Sau khi cài, mở lại Claude Code và nói:

> "Kết nối Confluence sản xuất giúp tôi"

Claude hỏi API token, lưu vào `~/.confluence-vds-skill/domains.json` và kiểm tra kết nối. **Mỗi người dùng token riêng** — token không nằm trong repo.

> Lấy API token: Confluence → **Settings → Personal Access Tokens → Create token**.

**Xác thực:** Confluence Data Center dùng **Personal Access Token (PAT)** gửi qua header `Authorization: Bearer <token>` — **chỉ cần token, không cần tên đăng nhập** (khác Confluence Cloud vốn dùng Basic Auth email + token).

### Cấu hình thủ công (nếu cần, cho người kỹ thuật)

```bash
node bin/cli.js setToken <api-token>   # chỉ cần token (PAT)
node bin/cli.js useDomain production    # hoặc partner
node bin/cli.js testConn                # kỳ vọng {"ok": true, "status": 200}
```

## Lệnh CLI (Claude gọi ngầm)

| Nhóm | Lệnh |
|------|------|
| Domain | `addDomain <id> <label> <url>`, `setToken <token>`, `setCredentials <user> <token>`, `useDomain <id>`, `listDomains`, `testConn` |
| Đọc | `listSpaces`, `searchPages <query>`, `getPage <spaceKey> <title>`, `getPageById <id>` |
| Ghi | `createPage <spaceKey> <title>` (content qua stdin), `updatePage <id> <title>`, `updatePageByTitle <spaceKey> <title>`, `deletePage <id>` |
| Tài liệu | `pushDoc <spaceKey> <title> <file.md> [parentId]`, `updateDoc <title\|pageId> <file.md>`, `listPushed`, `addAttachment <pageId> <file>` |

Mọi lệnh in JSON để Claude tóm tắt cho người dùng bằng tiếng Việt.

### Ví dụ: đẩy tài liệu Markdown

```bash
node bin/cli.js pushDoc DIG "Báo cáo tháng 6" ./bao-cao.md
# → {"ok":true,"pageId":"123","url":"...","attachments":2,"domain":"production"}
```

File `bao-cao.md` có thể chứa ảnh local (`![](./logo.png)`) và khối ` ```mermaid ` — chúng được upload/render tự động.

## Cấu trúc thư mục

```
confluence-vds-skill/
├── setup.js              # Trình cài đặt một-lệnh (npm install + domain + skill)
├── SETUP.md              # Hướng dẫn cài đặt cho người dùng non-tech
├── bin/cli.js            # CLI tự chứa (nguồn chạy thực tế, không cần build)
├── src/                  # Bản TypeScript (tham chiếu / build tùy chọn)
│   ├── markdown.ts       # Markdown → Confluence storage
│   ├── diagram.ts        # Mermaid → PNG (tự dò Chrome)
│   └── registry.ts       # Bộ nhớ trang đã đẩy
├── skills/confluence-vds-skill/
│   ├── SKILL.md          # Hướng dẫn Claude điều phối hội thoại (UC1–UC9)
│   └── references/usage-vi.md   # Câu mẫu cho người dùng non-tech
├── package.json
├── tsconfig.json
└── README.md
```

> `bin/cli.js` là JavaScript thuần, chạy ngay không cần biên dịch. Các file `src/*.ts` là bản TypeScript mirror để tham khảo và build nếu muốn.

## Dùng với Claude Code

Đặt skill này vào dự án (hoặc tham chiếu `skills/confluence-vds-skill/SKILL.md`). Sau đó chỉ cần chat:

> "Đẩy file báo cáo này lên Confluence sản xuất, đặt tên 'Báo cáo Q1'."
> "Sửa lại tài liệu tôi đã đẩy hôm trước."
> "Chuyển sang Confluence đối tác."

Claude sẽ tự xác định domain, chạy lệnh ngầm và báo cáo kết quả.

## Bảo mật

- Token lưu cục bộ tại `~/.confluence-vds-skill/domains.json` — **không** nằm trong repo.
- `.confluence/` (bộ nhớ trang đã đẩy) được `.gitignore`.
- Không commit token vào mã nguồn.

## License

MIT
