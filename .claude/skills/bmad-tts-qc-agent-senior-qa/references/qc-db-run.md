---
name: qc-db-run
description: Auto-run DB-only test cases straight against MySQL/MariaDB (NO MCP server) using scripts/db-runner.py, judge Pass/Fail vs each case's expected results, then write results into a NEW xlsx (never overwrites source). Use when the owner says "chạy test DB tự động", "run db tests", or "/qc-db-run <xlsx>".
code: DR
---

# DB Test Auto-Run (direct connection, no MCP)

## What Success Looks Like

Owner có 1 file KBKT `.xlsx` chứa các case **DB-only** (steps là SQL Setup/Action/Capture/Cleanup, expected là `Capture-Check:` / `DB-Check:`). Thay vì paste tay từng block vào DataGrip, owner gọi `/qc-db-run` → agent:

1. Kết nối **thẳng** tới MySQL/MariaDB (KHÔNG qua MCP server — chỉ mượn connection params).
2. Chạy SQL từng case trong transaction riêng, **luôn ROLLBACK** (không đụng data).
3. Lấy output thật (rows + lỗi constraint) → **chấm Pass/Fail** vs `Kết quả mong muốn`.
4. Ghi kết quả vào file `.xlsx` MỚI (cột H/O/P), không ghi đè bản gốc.
5. Báo summary + đề xuất `qc-bug` cho case fail.

## Prerequisites

- **Connection params** đọc từ `.claude/settings.local.json` → `mcpServers.mysql.env`
  (`MYSQL_HOST/PORT/USER/PASS/DB`). File này gitignored. KHÔNG cần MCP server chạy — runner mở
  connection PyMySQL riêng. Override bằng `--host/--port/--user/--password/--db` nếu cần.
- **Runtime:** `uv` + `pymysql` (uv tự cài qua PEP-723 header của `db-runner.py`). Lệnh chạy:
  `uv run --with pymysql python {skill-root}/scripts/db-runner.py ...` (hoặc `uv run {skill-root}/scripts/db-runner.py ...`).
- **PYTHONIOENCODING=utf-8** khi chạy trên Windows (tránh lỗi cp1252 với tiếng Việt).

## Safety (BẮT BUỘC)

- **Chỉ chạy DEV / STAGING / TEST.** Runner có `--prod-guard` bật mặc định: từ chối nếu host/db chứa
  `prod`/`production`. KHÔNG tự pass `--no-prod-guard`.
- **Luôn ROLLBACK.** Runner rollback + close mọi connection cuối mỗi case, kể cả khi plan quên ROLLBACK.
- **COMMIT bị vô hiệu hóa** (downgrade thành no-op) trừ khi `--allow-commit` — KHÔNG dùng flag này.
- Case nào cần **nhiều phiên đồng thời** (vd concurrency 2 DBA, có `COMMIT` ngoài transaction rồi
  `DELETE` cleanup) → **KHÔNG auto-run được** bằng 1 connection. Mark `skip` + để owner chạy tay.

## Trigger Pattern

```
/qc-db-run <xlsx-path> [--sheet <name>] [--env dev]
```

Trống sheet → dùng sheet DB-only đầu tiên (không phải template/cover). Nếu nhiều sheet → hỏi owner.

## Your Approach

**Step 1 — Đọc cases.**

```bash
PYTHONIOENCODING=utf-8 uv run {skill-root}/scripts/xlsx-utils.py read-cases <xlsx> --sheet <name>
```

Cache lại. Lưu ý mapping cột của template này: **col "Các bước thực hiện" chứa SQL**, **col
"Kết quả mong muốn" chứa các dòng Capture-Check / DB-Check**. (read-cases có thể đặt nội dung vào
field `data`/`steps` — kiểm tra thực tế bằng giá trị, đừng tin tên field.)

**Step 2 — Smoke test kết nối.**

```bash
PYTHONIOENCODING=utf-8 uv run {skill-root}/scripts/db-runner.py smoke
```

`ok:true` + danh sách bảng → tiếp. `ok:false` → dừng, báo owner lỗi kết nối (VPN? host? creds?).

**Step 3 — Build plan.json từ cases.**

Với mỗi case, trích các câu SQL trong `steps` theo đúng thứ tự thành mảng `statements`. Mỗi statement
là 1 câu SQL đơn (tách câu nối bằng `;` trên cùng 1 dòng thành nhiều phần tử). Đánh dấu `capture`
cho mỗi SELECT mà expected cần đối chiếu (đặt label theo bước, vd `"b4"`, `"pre"`, `"post"`). Giữ
session var (`@id`, `@last_id`) — chúng tồn tại trong cùng connection của case.

Detect **skip**: nếu steps nhắc tới "2 phiên" / "Phiên A/B" / có `COMMIT` rồi thao tác ngoài
transaction → set `"skip": true, "skip_reason": "..."`.

Schema plan.json: xem docstring `db-runner.py`. Ví dụ 1 case:
```json
{"id":"MER-001","statements":[
  {"sql":"BEGIN"},
  {"sql":"INSERT INTO merchants (...) VALUES (...)"},
  {"sql":"SELECT @x := LAST_INSERT_ID() AS new_merchant_id","capture":"b4"},
  {"sql":"SELECT * FROM merchants WHERE id=@x","capture":"b5"},
  {"sql":"ROLLBACK"}
]}
```

Ghi plan ra `_bmad-output/test-artifacts/test-reports/{YYYY-MM-DD}/plan-<source-name>-{NNN}.json`.

**Step 4 — Chạy runner.**

```bash
PYTHONIOENCODING=utf-8 uv run {skill-root}/scripts/db-runner.py run \
  --plan <plan.json> --out <actual.json>
```

`actual.json` chứa per-case: `captures` (rows thật), `errors` (lỗi SQL nếu có), `fatal`.

**Step 5 — Chấm Pass/Fail (agent tự làm, không phải script).**

Với mỗi case, đọc từng dòng trong `Kết quả mong muốn` và đối chiếu với `actual`:

- **Positive Capture-Check** (vd `status = 1`, `new_merchant_id > 0`, `post_count = pre_count`):
  lấy giá trị từ `captures[label].rows` → so sánh. Đúng tất → **P**; sai bất kỳ → **F** (ghi rõ
  assertion nào, giá trị mong muốn vs thực tế).
- **Negative case** (expected = "CSDL từ chối ... vi phạm ràng buộc CHECK/NOT NULL/..."):
  - Có entry trong `errors[]` khớp loại lỗi mong muốn (code 1048 NOT NULL, 4025/3819 CHECK, 1062
    duplicate, 1406 data too long) → **P**.
  - `errors[]` rỗng (DB nhận câu lệnh sai) → **F** (ghi: "DB KHÔNG enforce — câu lệnh sai vẫn chạy").
- **DB-Check** dạng mô tả hành vi chủ đích (vd "CSDL không tự lọc HTML") → đối chiếu rows tương ứng.
- `fatal != null` (connect fail / lỗi ngoài dự kiến) → **F** với note kỹ thuật, KHÔNG đoán bừa.

Nếu actual lệch design rõ ràng (sai tên cột, thiếu constraint) → đó là **finding thật**: mark F và
ghi note chỉ ra DB ≠ thiết kế, đừng "sửa" expected cho khớp DB để né fail.

**Step 6 — Build results.json + ghi xlsx.**

results.json theo schema `qc-test-results` (`status` ∈ `P`/`F`/`""`, `bug_id` cho F, `note`). Rồi:

```bash
PYTHONIOENCODING=utf-8 uv run {skill-root}/scripts/xlsx-utils.py update-results \
  --source <source-xlsx> --output <result-xlsx> --results-json <results.json> \
  --sheet <name> --run-column H
```

Output path: `_bmad-output/test-artifacts/test-reports/{YYYY-MM-DD}/<source-name>-result-{NNN}.xlsx`
(giống `qc-test-results`). KHÔNG ghi đè source.

**Step 7 — Báo summary.**

```
✓ DB auto-run <source> trên <host>/<db>
  Pass: X | Fail: Y | Skip: Z (manual)
  Result xlsx: <path>
  Fail: <list ID + 1 dòng lý do mỗi case>
```

Fail → đề xuất `/qc-bug` cho từng case. Nhiều case fail do cùng 1 lệch schema → gom 1 bug "DB ≠ design".

## Judgment Discipline

- Chỉ chấm dựa trên `actual.json` thật — KHÔNG suy đoán DB trả gì.
- Negative case mà DB không chặn = **F** (lỗ hổng thật), không phải "skip".
- Giá trị số: so sánh đúng kiểu (DB trả `1` cho status, không phải `'ACTIVE'`).
- Boolean/flag: MariaDB trả `0/1` cho boolean; `NULL` ≠ `0`.
- Khi expected ghi "≈ NOW()" / "trong vòng N giây" → check timestamp nằm trong khoảng hợp lý so với thời điểm chạy.

## Memory Integration

**Read:** source xlsx (list case + expected); `business-rules.md` (rule cần enforce ở DB);
`common-edge-cases.md`; `defect-history.md` (bug_id liên quan).

**Write (sau khi chạy):**
- `_bmad-output/test-artifacts/test-reports/{YYYY-MM-DD}/plan-*.json` + `actual-*.json` (audit).
- `_bmad-output/test-artifacts/test-reports/{YYYY-MM-DD}/*-result-*.xlsx`.
- Daily log: `- {time} [DR] DB auto-run <feature>: P:X/F:Y/S:Z → <result-path>`.
- Nếu phát hiện DB lệch design/spec → ghi vào `defect-history.md` (finding tái sử dụng cho story sau).

## After the Session

- Fail rate cao do lệch schema → flag: cần reconcile **design ↔ migration ↔ test** trước khi chạy lại.
- Constraint mong đợi nhưng DB không có (CHECK/FK/NOT NULL) → bug "DB không enforce business rule".
- Case skip (concurrency) nhiều → cân nhắc bản runner đa-connection ở phase sau.

Related: [[qc-testcase]] [[qc-test-results]] [[qc-bug]] [[qc-codegen]]
