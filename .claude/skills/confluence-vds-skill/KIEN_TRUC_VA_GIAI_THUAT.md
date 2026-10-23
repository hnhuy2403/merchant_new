# Kiến Trúc & Giải Thuật — `confluence-vds-skill`

> Tài liệu kỹ thuật cho lập trình viên bảo trì dự án. Mô tả luồng dữ liệu, các giải
> thuật cốt lõi, và những điểm cần lưu ý khi sửa code. Toàn bộ nội dung bám sát mã
> nguồn thực tế trong [bin/cli.js](bin/cli.js) và [src/](src/).

---

## 1. Tổng quan

`confluence-vds-skill` là một **CLI Node.js thuần** (không framework, không build bắt
buộc để chạy) đóng vai trò cầu nối giữa **Claude Code** và **Confluence Data Center**
nội bộ. Người dùng cuối chat tiếng Việt với Claude; Claude dịch ý định thành lệnh CLI,
chạy ngầm qua Bash, rồi tóm tắt kết quả.

```
Người dùng (chat tiếng Việt)
        │
        ▼
   Claude Code  ──(đọc SKILL.md để biết cách dùng)──►  điều phối hội thoại
        │
        ▼  chạy ngầm: node bin/cli.js <command> [args]
   bin/cli.js  ────────────────────────────────────►  Confluence REST API
        │                                                (HTTP/HTTPS + Bearer PAT)
        ├─ render Mermaid → PNG (qua mmdc + Chrome hệ thống)
        ├─ convert Markdown → Confluence storage XHTML (markdown-it)
        └─ ghi/đọc registry cục bộ + config đa domain
```

### Hai loại "đầu vào điều khiển"
- **Người vận hành kỹ thuật**: gọi trực tiếp `node bin/cli.js <command>`.
- **Người dùng cuối**: chat với Claude; Claude tự sinh lệnh dựa trên
  [skills/confluence-vds-skill/SKILL.md](skills/confluence-vds-skill/SKILL.md).

### Đặc điểm kiến trúc quan trọng
- **`bin/cli.js` là runtime tự chứa (~855 dòng)**: chứa toàn bộ logic (HTTP, render,
  convert, registry, domain). Nó **không** require từ `dist/`. Chỉ phụ thuộc runtime
  vào `markdown-it` và binary `mmdc` (của `@mermaid-js/mermaid-cli`).
- **`src/*.ts`** là bản TypeScript song song của 3 mảng logic (registry, diagram,
  markdown), dùng để tham khảo/phát triển. Build ra `dist/` là tùy chọn, không cần
  cho việc chạy CLI.
- **Không tải Chromium bundled**: [.puppeteerrc.cjs](.puppeteerrc.cjs) đặt
  `skipDownload: true`. Render Mermaid dùng **Chrome/Chromium đã cài trên máy**.

---

## 2. Phân lớp & trách nhiệm

| Lớp | Vị trí trong cli.js | Trách nhiệm |
|---|---|---|
| **Cấu hình / xác thực** | `loadEnv`, `loadConfig`, `saveConfig`, `getActive` | Nạp `.env`, đọc/ghi `~/.confluence-vds-skill/domains.json`, chọn domain đang active |
| **Giao vận HTTP** | `makeRequest`, `addAttachment` | Gọi REST API bằng `http`/`https` thuần, Bearer PAT, multipart cho file |
| **API Confluence** | `listSpaces`, `getPage*`, `searchPages`, `createPage`, `updatePage*`, `deletePage` | Map REST endpoint ↔ object JS |
| **Pipeline tài liệu** | `pushDoc`, `updateDoc`, `convertMarkdown`, `renderMermaid` | Markdown → storage XHTML + đính kèm ảnh/diagram |
| **Registry** | `loadRegistry`, `saveRegistry`, `addRegistryEntry`, `findRegistry*` | "Trí nhớ" page đã đẩy, để cập nhật theo tiêu đề |
| **Quản lý domain** | `setCredentials`, `setToken`, `addDomain`, `useDomain`, `listDomains`, `testConn` | Đa môi trường (sản xuất / đối tác) |
| **CLI dispatcher** | IIFE `switch(command)` cuối file | Phân tuyến lệnh, in JSON, xử lý lỗi |

---

## 3. Mô hình dữ liệu

### 3.1. Config đa domain — `~/.confluence-vds-skill/domains.json`
Nằm ở **home directory**, ngoài repo. Chứa token nên KHÔNG bao giờ commit.

```json
{
  "activeDomain": "production",
  "username": "truongph1",
  "token": "<Personal Access Token>",
  "domains": {
    "production": { "label": "Nội bộ sản xuất", "url": "http://10.254.136.32:8090" },
    "partner":    { "label": "Đối tác",          "url": "http://10.254.136.35:8090" }
  }
}
```

Điểm thiết kế: **token & username dùng chung cho mọi domain**, chỉ `url` khác nhau.
Điều này phù hợp với giả định người dùng có cùng tài khoản trên các môi trường.

### 3.2. Registry — `<cwd>/.confluence/pages.json`
Nằm trong thư mục làm việc hiện tại (`process.cwd()`), được `.gitignore` chặn. Là một
**mảng** các entry:

```json
[
  {
    "title": "Báo cáo Q1",
    "pageId": "123456",
    "spaceKey": "DIG",
    "domain": "production",
    "url": "http://.../pages/123456",
    "sourceFile": "/abs/path/báo-cáo.md",
    "lastPushed": "2026-06-09T03:00:00.000Z",
    "version": 2
  }
]
```

> ⚠️ Lưu ý: registry theo `process.cwd()` — chạy CLI từ thư mục khác sẽ thấy registry
> khác. Đây là chủ ý (mỗi dự án có trí nhớ riêng) nhưng dễ gây nhầm khi debug.

---

## 4. Giải thuật cốt lõi

### 4.1. Phân giải cấu hình & domain active (`loadConfig` → `getActive`)

Thứ tự ưu tiên khi xác định "kết nối hiện hành":

```
1. Nếu ~/.confluence-vds-skill/domains.json tồn tại → đọc file này.
2. Ngược lại, nếu có biến môi trường CONFLUENCE_URL → dựng config tạm
   (1 domain "production" từ ENV).
3. Ngược lại → tạo config khung rỗng (token rỗng).
→ Sau đó LUÔN gọi ensureDefaultDomains() để đảm bảo có sẵn 2 domain mặc định
  (production + partner) và activeDomain hợp lệ; nếu vừa bổ sung thì ghi lại file.
```

> **Nâng cấp BUG-1:** trước đây khi chưa cấu hình, `loadConfig` trả `null` →
> `listDomains` rỗng (gây nhầm cho người non-tech). Nay `ensureDefaultDomains` đảm bảo
> 2 domain công ty **luôn có sẵn**, kể cả khi chưa chạy `setup.js`. Hằng số
> `DEFAULT_DOMAINS` định nghĩa 2 domain này.

`getActive()` lấy `cfg.domains[cfg.activeDomain]` rồi gộp với `username`/`token`
chung thành object `{ url, username, token, domainId, label }` dùng cho mọi request.

**Edge case quan trọng**:
- Nếu `activeDomain` trỏ tới domain không tồn tại → `getActive` trả null → `needSetup`.
- **Nếu domain đã có nhưng `cfg.token` rỗng → `getActive` vẫn trả `null`** (giữ tín
  hiệu `needSetup` để Claude hỏi token). Đây là điểm tinh tế sau BUG-1: domain tự điền
  sẵn nhưng token thì KHÔNG, nên không được coi "có domain = đã setup".

### 4.2. Xác thực — Bearer Personal Access Token (PAT)

Confluence Data Center dùng **PAT qua header `Authorization: Bearer <token>`**
(không phải Basic Auth username:password). Xem `makeRequest`:

```
headers:
  Authorization: Bearer <token>
  Content-Type: application/json
  Accept: application/json
```

`username` chỉ lưu để tham khảo, **không tham gia xác thực**. Đây là lý do `setToken`
(chỉ cần token) đủ để hoạt động — phù hợp luồng non-tech qua chat.

### 4.3. Giao vận HTTP "không phụ thuộc" (`makeRequest`)

Dùng module `http`/`https` lõi của Node (không axios/fetch lib) để giảm dependency:

```
1. Chọn protocol theo parsedUrl.protocol (https: → https, ngược lại http).
2. Gửi request; gom chunk vào `data`.
3. Resolve { status, body, headers } — KHÔNG tự parse JSON ở đây.
   → Mỗi hàm API tự kiểm tra status & JSON.parse, để kiểm soát lỗi riêng.
```

**Hệ quả thiết kế**: lỗi mạng → reject; lỗi HTTP (4xx/5xx) → resolve với status →
hàm gọi quyết định ném lỗi gì. Giúp `testConn` phân biệt 401/403/khác.

### 4.4. Pipeline đẩy tài liệu (`pushDoc`) — giải thuật trung tâm

Đây là luồng quan trọng nhất của dự án:

```
pushDoc(spaceKey, title, mdFilePath, parentId = null):
  0. Nếu title rỗng → lấy mặc định theo tên file (bỏ đuôi .md).   [BUG-6]
  1. Đọc nội dung Markdown + xác định baseDir (để resolve ảnh tương đối).
  2. convertMarkdown(md, baseDir) → { storage (XHTML), attachments[], warnings[] }
       - Mermaid được render thành PNG tạm trong bước này.
       - Ảnh local được thu thập vào attachments[].
       - warnings[]: cảnh báo (vd ảnh thiếu) để báo lại người dùng.   [BUG-4]
  3. createPage(spaceKey, title, storage, active, parentId) → pageId, url.
       (Page tạo TRƯỚC, vì attachment phải gắn vào pageId.)
       (parentId có → gắn body.ancestors=[{id}] để tạo page con.)     [BUG-2]
  4. Lần lượt addAttachment(pageId, file) cho từng attachment.
       - Lỗi 1 file KHÔNG chặn cả tiến trình (try/catch, đếm attachCount).
  5. Nếu có parentId → verifyAndFixParent(pageId, parentId):           [BUG-2 verify]
       kiểm tra ancestors thực tế; chưa đúng cha thì tự re-parent.
  6. addRegistryEntry(...) → ghi nhớ để updateDoc sau này.
  7. Trả { ok, pageId, url, title, attachments, domain,
            [parentId], [parentVerified], [warnings] }.
```

**Thứ tự "tạo page trước, đính kèm sau" là bắt buộc**: storage XHTML tham chiếu ảnh
qua `<ri:attachment ri:filename="...">`, nhưng Confluence chỉ hiển thị đúng khi file
đã được upload vào chính page đó. Tên file trong XHTML và tên khi upload **phải khớp
tuyệt đối** — xem mục 4.6.

**Tạo page con + tự xác minh (`verifyAndFixParent`)** — sửa lỗi nghiêm trọng từng gặp
(page con bị tạo nhầm ở gốc space):
```
verifyAndFixParent(pageId, parentId):
  1. GET /content/<pageId>?expand=ancestors,version
  2. Nếu ancestors đã chứa parentId → trả true (đúng cha).
  3. Nếu chưa → PUT /content/<pageId> với ancestors=[{parentId}] + version+1 (re-parent).
  4. Đọc lại kết quả PUT: ancestors có parentId → true, ngược lại → false.
```
Giá trị `parentVerified` (true/false) được trả về trong kết quả `pushDoc`. **Caller
(Claude) PHẢI đọc cờ này**: `false` nghĩa là chưa gắn được đúng cha → không báo
"thành công" giả, mà báo rõ để người dùng kiểm tra quyền/thử lại.

### 4.5. Cập nhật tài liệu (`updateDoc`) — phân giải định danh

`updateDoc(titleOrPageId, mdFile)` chấp nhận **tiêu đề HOẶC pageId**:

```
- Nếu titleOrPageId là chữ (isNaN):
    → tra registry theo (title, activeDomain).
- Nếu là số:
    → tra registry theo pageId;
    → không có trong registry → gọi getPageById để lấy title/space từ Confluence.
- Sau khi có pageId/title/spaceKey:
    convertMarkdown → updatePage → upload attachment → cập nhật/đẩy registry.
```

**Edge case**: tiêu đề tiếng Việt có dấu vẫn so khớp chính xác (so sánh chuỗi
nguyên văn). Nếu page chưa từng đẩy qua tool (không có trong registry) và truyền
tiêu đề thay vì pageId → không tìm được → cần truyền pageId.

### 4.6. Render Mermaid → PNG (`renderMermaid` + `findChrome`)

Mermaid **không tự vẽ ảnh**; nó là thư viện chạy trong trình duyệt. `mmdc` điều khiển
một Chrome headless để dựng SVG rồi xuất PNG. Giải thuật:

```
renderMermaid(code, outPng):
  1. Ghi code Mermaid ra file tạm .mmd trong os.tmpdir().
  2. findChrome():
       - Ưu tiên ENV: PUPPETEER_EXECUTABLE_PATH / CHROME_PATH.
       - Nếu không, dò danh sách đường dẫn mặc định theo OS
         (macOS / Linux / Windows).
  3. Nếu tìm thấy Chrome → ghi puppeteer-config tạm
       { executablePath: <chrome>, args: ["--no-sandbox"] }.
  4. Chạy: node <mmdc> -i <tmp.mmd> -o <outPng> [-p <cfg>] -b transparent
       (execSync, stdio 'pipe'). Bọc try/catch: mmdc đôi khi log lỗi nhưng
       vẫn tạo file → quyết định thành/bại bằng fs.existsSync(outPng).
  5. Dọn file tạm. Trả true/false.
```

**Tại sao quan trọng**: vì `skipDownload: true` ở `.puppeteerrc.cjs`, **không có
Chromium bundled** — nếu `findChrome()` trả null thì render thất bại. Đó là lý do
[setup.js](setup.js) cảnh báo khi máy thiếu Chrome.

**Fallback an toàn**: trong `convertMarkdown`, nếu render thất bại, code Mermaid được
giữ lại trong macro `code` của Confluence thay vì làm vỡ tài liệu (xem 4.7).

### 4.7. Convert Markdown → Confluence storage XHTML (`convertMarkdown`)

Confluence không nhận Markdown; nó nhận **storage format** (một dạng XHTML có macro
riêng `<ac:...>`, `<ri:...>`). Giải thuật duyệt token của `markdown-it`:

```
parse(markdown) → tokens[]
for mỗi token:
  • token.type === 'fence' (code block):
      - lang === 'mermaid':
          render PNG → nếu OK: thu attachment + chèn <ac:image><ri:attachment.../>
                       → nếu FAIL: chèn macro code (giữ nguyên text) ← fallback
      - lang khác:
          chèn <ac:structured-macro ac:name="code"> ... <![CDATA[code]]> ...
  • token khác:
      render HTML chuẩn bằng md.renderer.render([token], ...)

Hậu xử lý toàn bộ HTML:
  • Quét mọi <img ...>:
      - không có src      → BỎ thẻ (push warning).                    [BUG-4]
      - src bắt đầu "http" → <ac:image><ri:url ri:value=...>
      - src local tồn tại → thu attachment + <ac:image><ri:attachment...>
      - src local KHÔNG tồn tại → KHÔNG để <img> thô; thay bằng
        <p><em>[Thiếu ảnh: tên]</em></p> + push warning.              [BUG-4]
  • Chuẩn hóa thẻ void tự đóng (VOID_TAGS):                           [BUG-3]
      hr, br, img, input, col, area, meta, link, source, wbr, embed, track, base
      → mọi <hr>, <br>, <img ...> thành <.../> (XHTML nghiêm ngặt).

Trả về: { storage, attachments, warnings }.
```

> **Nâng cấp BUG-3 (void tags):** Confluence storage là **XHTML nghiêm ngặt** — thẻ
> không tự đóng (`<hr>`, `<br>`, `<img>`) làm API trả **HTTP 400** ("expected </hr>").
> Bước chuẩn hóa VOID_TAGS ở cuối `convertMarkdown` ép mọi thẻ void về dạng tự đóng.
>
> **Nâng cấp BUG-4 (ảnh local thiếu):** trước đây ảnh không tồn tại để lại `<img>` thô
> → kéo theo lỗi 400, vỡ cả tài liệu. Nay thay bằng placeholder + gom vào `warnings[]`
> để **vẫn đẩy được phần còn lại** và báo rõ cho người dùng tên ảnh bị thiếu.

**Quy tắc đặt tên file (`normalizeFilename`)** — mấu chốt để ảnh hiển thị:
```
NFD normalize → bỏ dấu tiếng Việt → space thành "_" → bỏ ký tự không [a-zA-Z0-9._-]
```
Tên đã chuẩn hóa được dùng **đồng thời** ở 2 nơi: (a) trong XHTML
`ri:filename`, (b) khi `addAttachment` upload. Hai chỗ này **phải sinh ra cùng một
tên**, nếu lệch → Confluence không nối được ảnh vào vị trí. Đây là invariant cần giữ
khi refactor.

**An toàn XML (`escapeXml`)**: mọi giá trị nhúng vào XHTML đều escape `& < > " '`
để tránh vỡ storage format / injection.

### 4.8. Upload attachment đa phần (`addAttachment`)

Tự dựng **multipart/form-data thủ công** (không dùng form-data lib) bằng Buffer:

```
1. boundary = "----confluenceBoundary" + Date.now()
2. body = [ phần header field "file" ] + [ nội dung file nhị phân ] + [ phần đóng ]
3. POST .../content/<pageId>/child/attachment
   headers:
     Authorization: Bearer <token>
     X-Atlassian-Token: no-check          ← bắt buộc, chống CSRF của Confluence
     Content-Type: multipart/form-data; boundary=<boundary>
     Content-Length: <body.length>
```

`X-Atlassian-Token: no-check` là **bắt buộc** với endpoint attachment của Confluence,
thiếu sẽ bị từ chối. Tên file dùng `attachName` (đã chuẩn hóa từ pipeline) nếu có,
nếu không thì tự chuẩn hóa từ basename.

### 4.9. Registry — upsert theo pageId hoặc (title, domain)

```
addRegistryEntry(entry):
  - tìm entry cũ khớp pageId  HOẶC  (cùng title VÀ cùng domain)
  - có → ghi đè (cập nhật version, lastPushed)
  - không → push mới
```

Quy tắc khớp kép (pageId **hoặc** title+domain) cho phép cập nhật đúng cả khi người
dùng chỉ nhớ tiêu đề. `domain` tham gia khóa để cùng một tiêu đề trên 2 môi trường
không đè lên nhau.

### 4.10. Kiểm tra kết nối (`testConn`) — phân loại lỗi

Gọi `space?limit=1` rồi ánh xạ status sang gợi ý tiếng Việt:

```
200 → ok
401 → token sai/hết hạn
403 → token đúng nhưng tài khoản chưa được cấp quyền Confluence ở domain này
khác → không kết nối được
reject (mạng) → "Lỗi mạng: ..."
```

Việc phân biệt 401 vs 403 giúp Claude hướng dẫn người dùng đúng (nhập lại token vs
liên hệ quản trị).

---

## 5. Luồng CLI dispatcher

Cuối [bin/cli.js](bin/cli.js) là một IIFE `async`:

```
const [, , command, ...args] = process.argv;
switch (command) { ... }   // mỗi case in JSON kết quả ra stdout
catch (err):
  - err.message === 'needSetup' → in { needSetup: true }  (KHÔNG exit lỗi)
  - lỗi khác → in "Error: ..." ra stderr + exit(1)
```

**Quy ước I/O quan trọng cho Claude**:
- Kết quả thành công luôn là **JSON ra stdout** → Claude parse để tóm tắt.
- `createPage`/`updatePage*` đọc **nội dung HTML từ stdin** (`fs.readFileSync(0)`),
  còn `pushDoc`/`updateDoc` đọc từ **file Markdown** theo đường dẫn.
- `{ needSetup: true }` là tín hiệu mềm để Claude khởi động luồng cấu hình (hỏi token),
  không phải lỗi cứng.

---

## 6. Bản đồ lệnh ↔ giải thuật

| Lệnh | Hàm chính | REST endpoint / hành vi |
|---|---|---|
| `listSpaces` | `listSpaces` | `GET /rest/api/space?limit=100` |
| `getPage <space> <title>` | `getPageBySpaceAndTitle` | `GET /content?spaceKey&title&expand=body.storage,version` |
| `getPageById <id>` | `getPageById` | `GET /content/<id>?expand=body.storage,version` |
| `searchPages <query>` | `searchPages` | `GET /content/search?cql=text ~ "..." AND type=page` |
| `createPage <space> <title>` | `createPage` | `POST /content` (HTML qua stdin; nhận `parentId` → gắn `ancestors`) |
| `updatePage <id> <title>` | `updatePage` | `GET` lấy version → `PUT /content/<id>` (version+1) |
| `updatePageByTitle <space> <title>` | `updatePageBySpaceAndTitle` | tìm page → `updatePage` |
| `deletePage <id>` | `deletePage` | `DELETE /content/<id>` |
| `pushDoc <space> <title> <md> [parentId]` | `pushDoc` | convert → create (con nếu có parentId) → attach → **verify parent** → registry. `title` rỗng → theo tên file |
| `updateDoc <title|id> <md>` | `updateDoc` | phân giải id → convert → update → attach → registry |
| `addAttachment <id> <file>` | `addAttachment` | `POST /content/<id>/child/attachment` |
| `listPushed` | `loadRegistry` | đọc `.confluence/pages.json` |
| `setCredentials` / `setToken` | tương ứng | ghi token vào domains.json |
| `addDomain` / `useDomain` / `listDomains` | tương ứng | quản lý domains.json |
| `testConn` | `testConn` | `GET /space?limit=1` + phân loại lỗi |

---

## 7. Cập-nhật-page: vì sao phải đọc version trước

Confluence dùng **optimistic locking** theo `version.number`. `updatePage`:

```
1. getPageById → đọc version hiện tại.
2. PUT với version.number = current + 1.
```

Nếu gửi version sai (không phải current+1) Confluence trả lỗi xung đột. Vì vậy KHÔNG
được cache version cũ qua nhiều lần update — luôn đọc lại trước mỗi lần ghi.

---

## 8. Bất biến (invariants) cần giữ khi refactor

1. **Tên file chuẩn hóa phải nhất quán** giữa XHTML (`ri:filename`) và lúc upload
   (`addAttachment`). Đổi `normalizeFilename` phải đổi đồng bộ cả hai nhánh.
2. **Tạo page trước, attach sau** trong `pushDoc` — không đảo thứ tự.
3. **Luôn đọc version trước khi updatePage** (mục 7).
4. **Mọi giá trị nhúng XHTML phải qua `escapeXml`**.
5. **`X-Atlassian-Token: no-check`** bắt buộc cho upload attachment.
6. **Không bao giờ ghi token vào repo** — chỉ ở `~/.confluence-vds-skill/domains.json`.
   Lưu ý: `.claude/settings.local.json` cũng có thể chứa token (Claude lưu lệnh đã
   cho phép) → đã đưa vào `.gitignore`, KHÔNG đẩy lên git.
7. **Render Mermaid phụ thuộc Chrome hệ thống** (do `skipDownload: true`); giữ fallback
   macro-code khi render thất bại để không làm vỡ tài liệu.
8. **Đầu ra XHTML phải tự đóng mọi thẻ void** (VOID_TAGS) trước khi gửi Confluence —
   thiếu sẽ bị HTTP 400. [BUG-3]
9. **Không để `<img>` thô trỏ file không tồn tại** trong storage — thay placeholder +
   ghi `warnings`. [BUG-4]
10. **Khi tạo page con, phải đọc `parentVerified`** trong kết quả; `false` → KHÔNG báo
    thành công giả. [BUG-2 verify]
11. **`getActive` trả `null` khi thiếu token** dù domain đã có sẵn — giữ tín hiệu
    `needSetup`. [BUG-1]

---

## 9. Phụ thuộc & lý do

| Phụ thuộc | Loại | Vai trò | Vì sao |
|---|---|---|---|
| `markdown-it` | runtime | Parse Markdown → token | Bộ parser chuẩn, mở rộng tốt |
| `@mermaid-js/mermaid-cli` (`mmdc`) | runtime | Render Mermaid → PNG | Cung cấp binary `mmdc` |
| `http`/`https`/`fs`/`path`/`os`/`child_process` | lõi Node | HTTP, file, spawn mmdc | Giảm dependency, nhẹ |
| `typescript`, `@types/*` | dev | Build `src/*.ts` (tùy chọn) | Không cần để chạy CLI |

> Chromium **không** nằm trong dependency cây cài đặt theo nghĩa tải về: bị chặn bởi
> `.puppeteerrc.cjs`. Render dùng Chrome đã cài trên máy.

---

## 10. Điểm cần lưu ý / hướng cải tiến

- **Cảnh báo bảo mật npm**: `@mermaid-js/mermaid-cli@10.9.1` kéo `puppeteer@19`
  (deprecated, có CVE). Nâng mermaid-cli lên bản mới sẽ giảm cảnh báo nhưng cần test
  lại render.
- **Registry theo `process.cwd()`**: tiện cho từng dự án nhưng dễ nhầm khi chạy CLI ở
  thư mục khác. Cân nhắc cho phép cấu hình đường dẫn registry.
- **`makeRequest` không timeout**: mạng treo có thể làm request chờ vô hạn. Có thể bổ
  sung `req.setTimeout`.
- **`loadEnv` parse `.env` thủ công** bằng `split('=')`: giá trị chứa dấu `=` sẽ bị cắt
  sai. Dùng `split('=')` với `slice(1).join('=')` nếu cần hỗ trợ token có `=`.

---

## 11. Lịch sử nâng cấp (2026-06-09)

Sau một phiên thử nghiệm thực tế (đẩy PRD làm page con), các lỗi sau đã được vá trong
`bin/cli.js` (và đồng bộ `src/markdown.ts` mirror + `SKILL.md`):

| Mã | Vấn đề | Cách vá | Mục liên quan |
|---|---|---|---|
| BUG-1 | `listDomains` rỗng khi chưa setup | `ensureDefaultDomains` tự điền 2 domain; `getActive` vẫn báo needSetup khi thiếu token | 4.1 |
| BUG-2 | `parentId` bị bỏ qua → page con tạo nhầm ở gốc space | `createPage` gắn `ancestors`; `pushDoc` truyền xuống | 4.4 |
| BUG-2v | Báo "thành công" giả khi parent sai | `verifyAndFixParent` + cờ `parentVerified` | 4.4 |
| BUG-3 | Thẻ void không tự đóng → HTTP 400 | Chuẩn hóa `VOID_TAGS` cuối `convertMarkdown` | 4.7 |
| BUG-4 | Ảnh local thiếu làm vỡ tài liệu | Placeholder + `warnings[]`, bỏ `<img>` thô | 4.7 |
| BUG-6 | Phải gõ tiêu đề thủ công | `pushDoc` lấy tiêu đề theo tên file khi rỗng | 4.4 |

---

*Tài liệu này mô tả trạng thái mã nguồn tại thời điểm đóng gói `confluence-vds-skill`
(đã gồm nâng cấp 2026-06-09). Khi sửa logic cốt lõi (pipeline tài liệu, render, xác
thực), hãy cập nhật mục tương ứng.*
