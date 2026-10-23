---
name: tts-figma-api
description: Read Figma design files via the Figma REST API using a personal access token stored in `_bmad/config.user.yaml` (key `tts.figma.token`, gitignored). Use when the user asks to inspect/list/export content from a Figma file — list pages/frames/sections, fetch a specific screen by name or id, export PNG/SVG, or enumerate components/styles. Ships a helper at `scripts/figma-cli.py` with `list-screens`, `get-screen <name|id>`, and `export <name|id>` subcommands. Covers the project's design file at key I3jxlZZi9hUlSAC2YBis8j. Do NOT use for Figma MCP server flows or write operations (use figma-use skill for writes).
---

# Figma REST API

Cách đọc file Figma của dự án qua Figma REST API.

## 1. Token

- Token lưu ở key `tts.figma.token` trong `{project-root}/_bmad/config.user.yaml` (gitignored — KHÔNG commit).
- Personal access token (prefix `figd_`) — **không phải** OAuth.
- **KHÔNG** dùng Figma MCP server (`mcp.figma.com/mcp`) — khác cơ chế auth.
- **KHÔNG** in / log / commit giá trị token. Luôn truyền qua header `X-Figma-Token`.
- Nếu user chưa cấu hình: hướng dẫn lấy token tại https://www.figma.com/settings → *Personal access tokens*, rồi paste vào `config.user.yaml` theo template comment có sẵn trong file.

### Cách load token vào biến shell (mỗi session)

```bash
export FIGMA_KEY=$(python3 -c "import yaml; print(yaml.safe_load(open('_bmad/config.user.yaml')).get('tts',{}).get('figma',{}).get('token',''))")
[ -z "$FIGMA_KEY" ] && echo "ERROR: tts.figma.token chưa được set trong _bmad/config.user.yaml" >&2
```

Sau đó dùng `$FIGMA_KEY` trong curl. **KHÔNG** echo `$FIGMA_KEY` ra console.

## 2. Scope của token

Token dự án có các scope đọc sau (không có `current_user:read`):

- `file_content:read` — đọc nội dung file (nodes, structure)
- `file_metadata:read` — đọc metadata
- `file_versions:read` — đọc lịch sử version
- `library_assets:read`, `library_content:read`, `team_library_content:read` — đọc library
- `file_dev_resources:read` — đọc dev resources
- `webhooks:read`

Endpoint `/v1/me` sẽ trả 403 — không dùng để test token. Dùng `/v1/files/<key>?depth=1` thay thế.

## 3. File key của dự án

Thứ tự ưu tiên:

1. Key `tts.figma.file_key` trong `_bmad/config.user.yaml` (nếu user override).
2. `docs/index.md` — dòng ghi Figma URL.
3. Default hiện tại: `I3jxlZZi9hUlSAC2YBis8j` (Web Dịch vụ & Mua sắm hoàn tiền).

Trích file key từ URL dạng `figma.com/design/<FILE_KEY>/...` hoặc `figma.com/file/<FILE_KEY>/...`.

## 4. Endpoint thường dùng

Base: `https://api.figma.com/v1`. Header: `X-Figma-Token: $FIGMA_KEY`.

| Mục đích | Endpoint | Ghi chú |
|---|---|---|
| Liệt kê canvas (pages) | `GET /files/<key>?depth=1` | Nhẹ, chỉ trả top-level |
| Liệt kê section/frame của 1 page | `GET /files/<key>/nodes?ids=<node_id>&depth=2` | Chỉ fetch page cần xem |
| Lấy toàn bộ children của 1 node | `GET /files/<key>/nodes?ids=<id1>,<id2>&depth=3` | Giới hạn bằng `depth` để tránh payload lớn |
| Xuất ảnh PNG/SVG của node | `GET /images/<key>?ids=<node_id>&format=png&scale=2` | Trả URL ảnh tạm |
| Danh sách component | `GET /files/<key>/components` | |
| Danh sách style | `GET /files/<key>/styles` | |

## 5. Nguyên tắc fetch tiết kiệm

1. **Luôn bắt đầu với `depth=1`** để map cấu trúc trước khi drill-down.
2. **Chỉ fetch node cần thiết** qua `/nodes?ids=...` thay vì `/files/<key>` toàn bộ (file có thể hàng chục MB).
3. **Parse JSON bằng `python3 -c "import json, sys; ..."`** thay vì `cat` / `head` — tránh đổ payload lớn ra console.
4. Không tải toàn bộ file ra disk trừ khi được yêu cầu.

## 6. Helper CLI — lấy từng màn hình cụ thể

`scripts/figma-cli.py` (chạy từ project root) tự load token + file_key từ `_bmad/config.user.yaml`. **Ưu tiên dùng helper này** thay vì raw curl khi cần thao tác trên 1 màn hình.

```bash
# Liệt kê toàn bộ "screens" (top-level FRAME/COMPONENT/SECTION) theo từng page
python3 skills/tts-figma-api/scripts/figma-cli.py list-screens

# Filter theo tên page
python3 skills/tts-figma-api/scripts/figma-cli.py list-screens --page "Refund"

# Output dạng JSON (cho agent parse tiếp)
python3 skills/tts-figma-api/scripts/figma-cli.py list-screens --raw

# Lấy design tree 1 màn hình theo tên (substring, case-insensitive)
python3 skills/tts-figma-api/scripts/figma-cli.py get-screen "Đăng nhập"

# Hoặc theo id (chính xác, không bị trùng tên)
python3 skills/tts-figma-api/scripts/figma-cli.py get-screen 1:42

# Default output là compact (id/type/name/size/text/color). Lấy raw JSON khi cần đầy đủ:
python3 skills/tts-figma-api/scripts/figma-cli.py get-screen 1:42 --raw --depth 6

# Export PNG 2x ra _bmad-output/figma-exports/<safe-name>.png
python3 skills/tts-figma-api/scripts/figma-cli.py export "Đăng nhập" --format png --scale 2

# SVG, output path tự chọn
python3 skills/tts-figma-api/scripts/figma-cli.py export 1:42 --format svg --output /tmp/login.svg
```

### Khi name khớp nhiều màn

CLI sẽ liệt kê tất cả match + bắt dùng `id` thay vì `name`. Workflow chuẩn: chạy `list-screens` trước → copy id → truyền vào `get-screen` / `export`.

## 7. Raw API (khi helper không đủ)

Nếu cần endpoint helper chưa support (components, styles, versions, …), dùng curl trực tiếp:

```bash
# Load token tạm vào shell var
export FIGMA_KEY=$(python3 -c "import yaml; print(yaml.safe_load(open('_bmad/config.user.yaml')).get('tts',{}).get('figma',{}).get('token',''))")

# Map cấu trúc top-level (pages only)
curl -s -H "X-Figma-Token: $FIGMA_KEY" \
  "https://api.figma.com/v1/files/I3jxlZZi9hUlSAC2YBis8j?depth=1" \
  | python3 -c "import json,sys; d=json.load(sys.stdin)['document']; [print(f\"[{c['id']}] {c['name']}\") for c in d['children']]"

# Danh sách component
curl -s -H "X-Figma-Token: $FIGMA_KEY" \
  "https://api.figma.com/v1/files/I3jxlZZi9hUlSAC2YBis8j/components"
```

## 8. Xử lý lỗi thường gặp

| Status | Nguyên nhân | Xử lý |
|---|---|---|
| 403 "Invalid scope" | Endpoint yêu cầu scope token không có (ví dụ `/v1/me` cần `current_user:read`) | Dùng endpoint tương đương trong scope hiện có |
| 404 | Sai file key hoặc node id | Kiểm tra lại URL Figma nguồn |
| 429 | Rate limit | Đợi, giảm tần suất request, dùng `depth` nhỏ hơn |
| Token rỗng | `tts.figma.token` chưa set trong `_bmad/config.user.yaml` | Hướng dẫn user paste token vào (template comment đã có sẵn ở cuối file) |
