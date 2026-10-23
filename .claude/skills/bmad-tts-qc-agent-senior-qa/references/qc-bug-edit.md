---
name: qc-bug-edit
description: Edit field bất kỳ trong 1 hoặc nhiều bug file cùng lúc — trigger /qc-bug-<BUG-ID>[-<BUG-ID>...] key=value...; thêm bảng "Lịch sử chỉnh sửa" vào bug file + sync defect-history memory
code: BE
---

# Bug Edit

## What Success Looks Like

Owner cần đổi 1–N field của 1 hoặc nhiều bug (reclassify severity, đổi assignee, sửa note, fix typo trong title…) → 1 command duy nhất, agent update tất cả file đó, ghi rõ "Lịch sử chỉnh sửa" để team trace back. Không edit thủ công 5 file rồi quên 1 file. Defect-history memory luôn sync — pattern matching tương lai không bị nhiễu vì record cũ.

## Trigger Pattern

**Primary syntax — embed BUG-ID(s) vào command name:**
```
/qc-bug-<BUG-ID>[-<BUG-ID>...] [key=value]...
```

Ví dụ:
- `/qc-bug-BUG-2026-05-14-001 severity=S1` — 1 bug, 1 field.
- `/qc-bug-BUG-2026-05-14-001 severity=S1 priority=P0 assignee=devB` — 1 bug, 4 field.
- `/qc-bug-BUG-2026-05-14-001-BUG-2026-05-14-002 priority=P1` — 2 bug, cùng 1 field.
- `/qc-bug-BUG-2026-05-14-001 reporter="QA2 Nam"` — value có khoảng trắng → bắt buộc quote.
- `/qc-bug-BUG-2026-05-14-001 note="Esc by PM" suspected-area="Auth service"` — multi-word values.

**Alternate syntax — positional:**
```
/qc-bug-edit <BUG-ID> [<BUG-ID> ...] [key=value]...
```

Dùng khi command-name pattern khó gõ (vd: copy bug ID từ nhiều nguồn):
- `/qc-bug-edit BUG-2026-05-14-001 severity=S1`
- `/qc-bug-edit BUG-2026-05-14-001 BUG-2026-05-14-002 priority=P1`

## Parse Rules

1. **Extract Bug IDs** từ command:
   - Regex `BUG-\d{4}-\d{2}-\d{2}-\d{3}` greedy match toàn bộ command string.
   - 0 match → reject, hỏi owner: thiếu Bug ID.
   - 1+ match → tiếp tục.
2. **Extract key=value pairs** từ phần còn lại (sau khi đã bóc Bug IDs):
   - Pattern: `key=value` hoặc `key="value with space"` hoặc `key='value'`.
   - Key cho phép kebab-case (vd: `suspected-area`, `test-id`) hoặc Vietnamese kebab (vd: `ngày-phát-hiện`).
   - Value chứa space → bắt buộc quote (single hoặc double).
   - 0 cặp key=value → reject, hỏi owner: muốn edit field nào.
3. **Validate values cho known fields:**
   - `severity` ∈ {S1, S2, S3, S4} — sai → reject, hỏi lại.
   - `priority` ∈ {P0, P1, P2, P3} — sai → reject, hỏi lại.
   - Date field (`ngày-phát-hiện` / `found-date`) phải đúng ISO `YYYY-MM-DD` — sai → reject.
   - `mã-bug` / `bug-id` → **CẤM** edit (đổi Bug ID = rename file = tách thành workflow riêng). Reject, gợi ý owner tạo bug mới + cancel bug cũ.
   - Unknown field → **CHO PHÉP** (per owner: "bất kỳ tham số nào đó"), nhưng warn owner: "Field này chưa có trong bug header, sẽ append vào header. Tiếp tục? (y/n)".

## Workflow

1. **Parse** command theo Parse Rules trên.
2. **Locate bug file(s)** — với mỗi BUG-ID:
   - Grep `_bmad-output/test-artifacts/bugs/` pattern `Mã bug: <BUG-ID>` → file path.
   - 0 match → log lỗi cho BUG-ID đó, skip, tiếp tục bug khác. Cuối flow báo owner danh sách bug không tìm thấy.
   - >1 match (lỗi convention) → báo owner, hỏi chọn file nào.
3. **Read current values** trong header của từng bug → biết giá trị cũ (cần cho history table).
4. **Đề xuất diff** trong chat — 1 block cho mỗi bug:
   ```
   BUG-2026-05-14-001 (file: _bmad-output/test-artifacts/bugs/2026-05-14/BUG-001-LF-001-...md)
     Severity:  S2 → S1
     Priority:  P1 → P0
     Assignee:  (chưa có) → devB
   BUG-2026-05-14-002 (file: _bmad-output/test-artifacts/bugs/2026-05-14/BUG-002-...md)
     Severity:  S2 → S1
     Priority:  P1 → P0
   ```
5. **Hỏi owner confirm** trước khi ghi: `Confirm` / `đồng ý` / `y`. Reject → dừng, không write gì.
6. **Sau confirm, với mỗi bug file:**
   - **Update field trong header** (line `- **<FieldName>:** <value>`). Match field name không phân biệt hoa thường, dùng bảng mapping ở cuối file. Field mới (chưa có trong header) → append cuối block header dạng `- **<Capitalized>:** <value>`.
   - **Legacy migration:** nếu bug file dùng `QA report:` (legacy) và owner edit `reporter=` → đổi tên field thành `Reporter:` luôn (giữ value cũ nếu owner chỉ rename, hoặc thay value mới nếu owner truyền).
   - **Append "Lịch sử chỉnh sửa"** (xem section dưới) — N rows / N field đã đổi, cùng timestamp + cùng note (nếu có).
   - **Sync defect-history memory** — tìm entry `BUG-ID` trong `_bmad/memory/tts-qc/curated/defect-history.md`, update các field có trong record (thường: Severity / Priority / Assignee / Reporter / Status / Suspected area).
7. **Echo kết quả** cho owner: list bug ID + field đã đổi + path file.

## Format "Lịch sử chỉnh sửa" (chèn vào bug file)

Section này đặt **ngay sau `## Trạng thái`, trước `## Tiêu đề`**:

```markdown
## Lịch sử chỉnh sửa
| Ngày giờ | Field | Cũ | Mới | Người | Ghi chú |
|---|---|---|---|---|---|
| 2026-05-18 09:15 | Severity | S2 | S1 | Yennth72 (QA) | Reclassify per PM escalation |
| 2026-05-18 09:15 | Priority | P1 | P0 | Yennth72 (QA) | Reclassify per PM escalation |
```

Quy tắc:
- Section chưa tồn tại → tạo mới đúng vị trí (sau `## Trạng thái`, trước `## Tiêu đề`).
- Đã tồn tại → append rows mới vào cuối table, KHÔNG ghi đè rows cũ.
- 1 command đổi N field → N rows mới, cùng timestamp + cùng note.
- **Field "Cũ":** giá trị trước khi edit. Field mới (chưa có) → ghi `(chưa có)` / `—`.
- **Field "Người":** mặc định `Yennth72 (QA)`, override bằng `editor=` trong command.
- **Field "Ghi chú":** mặc định `—`, lấy từ `note=` trong command (cùng note cho cả batch).

## Confirmation Flow (BẮT BUỘC trước khi write)

1. Diff trong chat → chờ owner gõ `Confirm` / `y` / `đồng ý`.
2. Cấm write trực tiếp không qua confirm.
3. Field unknown → warn riêng + hỏi confirm thêm 1 nhịp trước khi append vào header.
4. Bug ID không tìm thấy → liệt kê cuối confirm, hỏi owner có muốn skip + tiếp tục bug còn lại không.

## Memory Integration

**Read:**
- Bug file hiện tại — đọc header lấy giá trị cũ, đọc cấu trúc để biết vị trí chèn "Lịch sử chỉnh sửa".
- `_bmad/memory/tts-qc/curated/defect-history.md` — locate entry để sync.
- `qa-conventions.md` — biết severity/priority valid values, default editor.

**Write:**
- Bug file: update header + append "Lịch sử chỉnh sửa" table.
- `defect-history.md`: update các field có trong record (severity / priority / assignee / reporter / status / suspected-area).
- Daily log (nếu owner bật): `- {time} [BE] Edit <BUG-ID>: <field>: <old> → <new>` — 1 dòng / 1 field / 1 bug.

## After the Session

Nhiều bug edit cùng 1 field trong cùng phiên (≥3 bug reclassify priority hàng loạt, hoặc đổi assignee đồng loạt) → flag pattern cho Yennth72: spec có gap, convention thay đổi, hay org structure thay đổi? Đề xuất update `qa-conventions.md` / `stakeholders.md`.

## Field Name Mapping (cho parser)

Bảng dưới map key trong command → tên field thực tế trong bug file. Field không có trong bảng → dùng nguyên key (capitalize từ đầu mỗi từ) + warn owner.

| Key (command) | Aliases | Bug file field name | Validate |
|---|---|---|---|
| severity | sev | Severity | ∈ {S1, S2, S3, S4} |
| priority | pri | Priority | ∈ {P0, P1, P2, P3} |
| assignee | as | Assignee | free text |
| reporter | rep, qa-report | Reporter (legacy: "QA report" → rename khi edit) | free text |
| suspected-area | area, suspected | Suspected area | free text |
| repro-rate | repro | Repro rate | free text (vd `1/1`, `3/5`) |
| test-id | tid | Test ID | free text |
| ngày-phát-hiện | found-date, date | Ngày phát hiện | `YYYY-MM-DD` |
| tiêu-đề | title | Tiêu đề (section body, không phải header) | free text, ≤80 chars |
| note | — | (KHÔNG vào header — vào cột "Ghi chú" của Lịch sử chỉnh sửa) | — |
| editor | — | (KHÔNG vào header — vào cột "Người" của Lịch sử chỉnh sửa) | — |
| mã-bug | bug-id, id | **CẤM EDIT** — rename = workflow riêng | reject |

## Common Pitfalls

- **Mã bug chứa nhiều dấu `-`** (`BUG-2026-05-14-001`). Parser KHÔNG split bằng `-` đơn — dùng regex `BUG-\d{4}-\d{2}-\d{2}-\d{3}` greedy.
- **Bug ID không hợp lệ format** (vd: `BUG-001` cũ kiểu legacy) → fallback Grep `Mã bug: <raw-input>` trước khi báo lỗi.
- **Tiêu đề bug khác section header**: `## Tiêu đề` là section body, KHÔNG nằm trong block header dấu `-` ở đầu file. Edit `tiêu-đề` / `title` → thay nội dung dòng dưới `## Tiêu đề`, không thêm vào header block.
- **Đa bug + 1 bug fail locate** → vẫn process các bug còn lại, không abort toàn batch. Cuối flow tổng hợp lỗi.
- **Owner truyền `editor=` hoặc `note=`** → KHÔNG ghi vào header bug (đây là metadata cho history table thôi).
