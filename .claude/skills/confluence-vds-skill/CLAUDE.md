# Confluence Skill — Tài liệu kỹ thuật

**Loại:** Claude Skill + CLI tự chứa
**Ngôn ngữ:** JavaScript (bin/cli.js — nguồn chạy thực tế) + TypeScript mirror (src/)
**Mục đích:** Cho người dùng non-tech tương tác Confluence nội bộ (đa domain) bằng hội thoại tiếng Việt.

---

## Nguyên tắc cốt lõi

**Người dùng cuối KHÔNG gõ lệnh.** Họ chat tiếng Việt với Claude; Claude chạy `node bin/cli.js <command>` ngầm qua Bash và tóm tắt kết quả. Toàn bộ logic điều phối hội thoại nằm trong [skills/confluence-vds-skill/SKILL.md](skills/confluence-vds-skill/SKILL.md).

`bin/cli.js` là JavaScript thuần, **chạy ngay không cần build**. Các file `src/*.ts` là bản mirror để tham khảo/biên dịch tùy chọn — khi sửa logic, ưu tiên sửa `bin/cli.js` trước.

---

## ⚙️ Tự cài skill khi người dùng yêu cầu kết nối (bootstrap)

**Bối cảnh:** Skill nguồn nằm ở `skills/confluence-vds-skill/SKILL.md`. Để gõ `/` trong
Claude Code thấy được skill, nó phải nằm ở thư mục skills mà Claude quét:
`.claude/skills/<tên>/` (project-level) hoặc `~/.claude/skills/<tên>/` (global).

**Yêu cầu của chủ dự án:** giai đoạn này CHỈ cài **project-level** (để còn chỉnh sửa).
Khi nào chạy ổn mới cài global.

**Việc Claude PHẢI làm — khi người dùng chat ý "kết nối Confluence" / "connect
confluence" / "cài/bật skill confluence" lần đầu trong dự án này:**

1. Kiểm tra đã có `.claude/skills/confluence-vds-skill/SKILL.md` ở **gốc dự án** chưa.
2. Nếu CHƯA → copy từ nguồn sang:
   ```bash
   mkdir -p .claude/skills/confluence-vds-skill/references
   cp skills/confluence-vds-skill/SKILL.md \
      .claude/skills/confluence-vds-skill/SKILL.md
   cp skills/confluence-vds-skill/references/usage-vi.md \
      .claude/skills/confluence-vds-skill/references/usage-vi.md
   ```
   (Chạy từ thư mục gốc dự án `confluence-vds-skill`.)
3. Báo người dùng: skill đã được cài vào dự án; **mở lại / khởi động lại Claude Code**
   thì gõ `/` sẽ thấy `confluence-vds-skill`. Từ lần sau gọi skill trực tiếp được.
4. Tiếp tục luồng cấu hình token/domain như SKILL.md mô tả (UC1–UC3).

> Lưu ý: `.claude/skills/` (bản đã cài) là bản sao để chạy. Khi sửa skill, sửa ở
> **nguồn** `skills/confluence-vds-skill/SKILL.md` rồi copy lại (hoặc nhờ Claude copy lại).
> Cân nhắc thêm `.claude/` vào `.gitignore` nếu không muốn đẩy bản đã cài lên Bitbucket.

---

## Kiến trúc

```
bin/cli.js          # CLI: config đa domain, CRUD, pushDoc/updateDoc, registry, mermaid
src/markdown.ts     # convert(md, baseDir) → { storage, attachments }
src/diagram.ts      # renderMermaid(code, outPng) + findChrome()
src/registry.ts     # bộ nhớ trang đã đẩy (.confluence/pages.json)
skills/confluence-vds-skill/
  SKILL.md          # bộ não điều phối hội thoại (UC1–UC9)
  references/usage-vi.md   # hướng dẫn non-tech
```

### Cấu hình đa domain — `~/.confluence-vds-skill/domains.json`
```json
{
  "activeDomain": "production",
  "username": "<user>",
  "token": "<api-token>",
  "domains": {
    "production": { "label": "Nội bộ sản xuất", "url": "http://10.254.136.32:8090" },
    "partner":    { "label": "Đối tác",         "url": "http://10.254.136.35:8090" }
  }
}
```
Một username + token chung cho mọi domain. Nếu file chưa tồn tại, `loadConfig()` fallback sang biến môi trường `.env` cũ (`CONFLUENCE_URL/USERNAME/API_TOKEN`) → coi như domain "production". Các hàm chính trong cli.js: `loadConfig`, `saveConfig`, `getActive`.

### Bộ nhớ trang — `.confluence/pages.json` (theo `process.cwd()`)
Mỗi entry: `{ title, pageId, spaceKey, domain, url, sourceFile, lastPushed, version }`. Cho phép `updateDoc` tìm trang theo tiêu đề mà không cần link. Hàm: `loadRegistry`, `addRegistryEntry`, `findRegistryByTitle`, `findRegistryByPageId`.

---

## Luồng đẩy tài liệu (pushDoc)

1. `convertMarkdown(md, baseDir)` → storage XHTML + danh sách attachment.
   - Code block → macro `code`.
   - ` ```mermaid ` → `renderMermaid` ra PNG (tmp) → attachment + `<ac:image>`. Nếu render lỗi → fallback hiển thị code trong macro (không chặn tài liệu).
   - Ảnh local → attachment; ảnh URL → `<ri:url>`. Tên file attachment được chuẩn hóa (`normalizeFilename`, NFD bỏ dấu tiếng Việt) và **khớp** với tên truyền vào `addAttachment`.
2. `createPage(spaceKey, title, storage)` → pageId.
3. `addAttachment(pageId, localPath, active, att.filename)` cho từng file (multipart, header `X-Atlassian-Token: no-check`).
4. Ghi registry.

`updateDoc(titleOrPageId, mdFile)` tương tự nhưng tra registry/`getPageById` để lấy pageId rồi `updatePage`.

### Render Mermaid đa nền tảng
`findChrome()` dò Chrome/Chromium theo macOS/Linux/Windows, hoặc dùng `PUPPETEER_EXECUTABLE_PATH`/`CHROME_PATH`. `renderMermaid` tạo puppeteer-config tạm trỏ tới Chrome dò được — **không hardcode đường dẫn máy nào**.

---

## Lệnh CLI

**Domain:** `addDomain <id> <label> <url>`, `setCredentials <user> <token>`, `useDomain <id>`, `listDomains`, `testConn`
**Đọc:** `listSpaces`, `searchPages <q>`, `getPage <spaceKey> <title>`, `getPageById <id>`
**Ghi:** `createPage <spaceKey> <title>` (stdin), `updatePage <id> <title>` (stdin), `updatePageByTitle <spaceKey> <title>` (stdin), `deletePage <id>`
**Tài liệu:** `pushDoc <spaceKey> <title> <file.md> [parentId]`, `updateDoc <title|pageId> <file.md>`, `listPushed`, `addAttachment <pageId> <file>`

Mọi lệnh in JSON. Khi chưa cấu hình → in `{"needSetup": true}` để Claude biết cần setup qua hội thoại.

---

## Xử lý lỗi (Claude diễn giải cho người dùng)

| JSON / HTTP | Ý nghĩa | Thông điệp |
|---|---|---|
| `{"needSetup": true}` | Chưa cấu hình | Hỏi người dùng setup (UC1–UC3) |
| 401 | Token sai/hết hạn | "Token chưa đúng, kiểm tra lại" |
| 404 | Sai space/page | "Không tìm thấy space hoặc trang" |
| timeout / status 0 | Mạng nội bộ | "Không kết nối được, thử lại sau" |

---

## Phát triển & kiểm thử

```bash
npm install                    # cài markdown-it + mermaid-cli
node -c bin/cli.js             # syntax check
node bin/cli.js help

# Test không cần Confluence thật (dùng HOME tạm để không đụng config thật):
HOME=/tmp/cf_test node bin/cli.js addDomain production "SX" http://10.254.136.32:8090
HOME=/tmp/cf_test node bin/cli.js setCredentials <user> <token>
HOME=/tmp/cf_test node bin/cli.js testConn        # cần token thật → 200

# Build TypeScript (tùy chọn):
npm run build
```

---

## Lưu ý bảo mật
- Token lưu tại `~/.confluence-vds-skill/domains.json` (ngoài repo).
- `.confluence/` và `.env` đã trong `.gitignore`.
- Confluence nội bộ chạy HTTP (không TLS) — `makeRequest` tự chọn http/https theo protocol URL.
