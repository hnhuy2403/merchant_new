---
name: qc-testcase-update
description: Incrementally update an existing test case .xlsx — add/modify/delete cases per change request, WITHOUT regenerating the whole file. Output a versioned .xlsx (-v2, -v3...) preserving template formatting + run results already filled in H/I/J.
code: TU
---

# Testcase Update (incremental)

## What Success Looks Like

Owner đã có 1 file test case `.xlsx` (vd `_bmad-output/test-artifacts/test-cases/auto-recharge.xlsx`) với N cases đã viết, có thể đã chạy & fill run results vào cột H/I/J. Spec/requirement thay đổi → owner muốn:
- **Thêm** vài case mới cho rule mới.
- **Sửa** steps/expected/priority của vài case bị ảnh hưởng.
- **Xoá** case đã obsolete.

Owner KHÔNG muốn LLM regenerate lại toàn bộ test cases (mất công design lại, mất run results đã fill, mất manual tweaks). Capability này chỉ patch delta lên file gốc, output ra file versioned (`auto-recharge-v2.xlsx`).

## Trigger Pattern

```
/qc-testcase-update <xlsx-path> [--sheet <name>] [change description...]
```

Ví dụ:
- `/qc-testcase-update _bmad-output/test-artifacts/test-cases/auto-recharge.xlsx Thêm rule mới: accountId phải >= 8 digits, dưới 8 reject`
- `/qc-testcase-update auto-recharge.xlsx --sheet "Auto Recharge" Xoá case AR-007 vì feature đã remove, thêm 2 case cho gateway lỗi 504`

Nếu owner gõ trống command (chỉ path) → agent hỏi "Thay đổi gì? Paste spec mới / diff / mô tả changes."

## Your Approach

**Step 1 — Read existing cases.**

```bash
uv run scripts/xlsx-utils.py read-cases <xlsx-path> [--sheet <name>]
```

Output JSON chứa toàn bộ cases hiện có (row, suite, id, purpose, case, data, steps, expected, result, defect_id, note). Cache lại trong context.

**Step 2 — Summarize current state cho owner.**

Echo gọn:
```
File: <path> (sheet: <name>)
Tổng: N cases trong M suites
  Suite-1: <name> — <count> cases (IDs: AR-001..AR-005)
  Suite-2: <name> — <count> cases (AR-006..AR-010)
  ...
Run results đã fill: <count> cases có data ở H/I/J (sẽ được preserve)
```

**Step 3 — Phân tích change request.**

Đọc mô tả của owner + memory (`business-rules.md`, `defect-history.md`, `common-edge-cases.md`). Phân loại:
- **MODIFY:** ID nào còn nguyên nhưng steps/expected/data/priority/note thay đổi. Chỉ list field thay đổi, không list field giữ nguyên.
- **ADD:** Case mới. Cần xác định: suite nào (existing hay new), ID mới (auto-increment từ max ID trong suite hoặc prefix), vị trí (after_id để đặt đúng chỗ).
- **DELETE:** ID nào obsolete. Warn nếu case đã có run result hoặc bug link — owner có thể muốn giữ làm history.

**Step 4 — Đề xuất patch plan trong chat.**

Format:
```
PATCH PLAN cho <path> (sheet: <name>)

ADD (3 cases):
  [Suite-2: Login validation] AR-008 — Reject accountId < 8 digits
    after: AR-005
    purpose: Verify field rejects under-length input
    data: 1234567 (7 digits)
    expected: Error "AccountId phải ít nhất 8 chữ số" hiển thị

  [Suite-2: Login validation] AR-009 — ...

  [Suite-4: Gateway errors] AR-010 — 504 timeout
    new suite divider: "Suite-4: Gateway errors"

MODIFY (2 cases):
  AR-003:
    steps:   (cũ) "1. Nhập 5 digits..." → (mới) "1. Nhập 7 digits..."
    expected:(cũ) "Reject với msg X" → (mới) "Reject với msg 'Phải ít nhất 8 chữ số'"
  AR-005:
    priority: P2 → P1

DELETE (1 case):
  AR-007 — Login bypass via deep link
    ⚠ Đã có run result Lần 1 (P) → confirm xoá sẽ mất history này

Output: <path-without-ext>-v2.xlsx (next available version)
```

**Step 5 — Owner confirm.**

Chờ owner gõ `Confirm` / `đồng ý` / `y`. Reject → dừng, không write gì. Nếu owner sửa 1 phần (vd: "đổi AR-008 priority thành P0") → cập nhật plan, hỏi lại confirm.

**Step 6 — Detect output version path.**

Scan thư mục chứa source xlsx, glob pattern `<base>-v*.xlsx`. Pick max version + 1. Nếu chưa có file `-v*` nào → output `<base>-v2.xlsx`. Owner override path bằng cách paste path mới.

```powershell
# PowerShell example for finding next version
Get-ChildItem "<dir>" -Filter "<base>-v*.xlsx" | ForEach-Object { [int]($_.BaseName -replace ".*-v(\d+)$", '$1') } | Measure-Object -Maximum
```

**Step 7 — Write patches JSON, invoke xlsx-utils.**

Sinh file `/tmp/qc_patches.json`:
```json
{
  "sheet": "<sheet name, optional>",
  "patches": [
    {"op": "modify", "id": "AR-003", "fields": {"steps": "...", "expected": "..."}},
    {"op": "modify", "id": "AR-005", "fields": {"priority": "P1"}},
    {"op": "delete", "id": "AR-007"},
    {"op": "add", "after_id": "AR-005", "case": {
       "id": "AR-008", "purpose": "...", "case": "...", "data": "1234567",
       "steps": "1. ...\n2. ...", "expected": "...", "note": ""
    }},
    {"op": "add", "after_id": "AR-008", "case": {"id": "AR-009", ...}},
    {"op": "add", "suite_divider": "Suite-4: Gateway errors", "case": {"id": "AR-010", ...}}
  ]
}
```

Run:
```bash
uv run scripts/xlsx-utils.py update-cases \
  --source <xlsx-path> \
  --output <xlsx-path-without-ext>-v2.xlsx \
  --patches-json /tmp/qc_patches.json \
  [--sheet <name>]
```

**Step 8 — Echo kết quả.**

Script output JSON status. Echo cho owner:
```
✓ Patched <output-path>
  Modified: 2 cases (AR-003, AR-005)
  Added:    3 cases (AR-008, AR-009, AR-010)
  Deleted:  1 case  (AR-007)
  Sheet:    <name>
  Run results preserved: <count> cases (H/I/J intact)

Next steps:
  - Verify changes: open file trong Excel
  - Update auto script tương ứng: /qc-codegen-update <script.spec.ts> --cases <new-xlsx-path>
```

**Step 9 — Write update log (BẮT BUỘC).**

Sau khi patch xlsx thành công (Step 8 OK), ghi log lại change description + kết quả vào file markdown song song với output xlsx. Mục đích: lưu vết "version này được sinh ra vì cái gì" để sau này tra ngược lại, không phải chỉ thấy `-v2.xlsx` mà không biết tại sao.

**Path log:** centralized tại `_bmad-output/test-artifacts/review-testcase-log/`, tên = `<output-xlsx-fullname>.log.md`.
- Vd output `_bmad-output/test-artifacts/test-cases/auto-recharge-v2.xlsx` → log `_bmad-output/test-artifacts/review-testcase-log/auto-recharge-v2.xlsx.log.md`.
- Mỗi version 1 file log riêng, self-contained — không append từ version trước.
- Đảm bảo folder `_bmad-output/test-artifacts/review-testcase-log/` tồn tại (tạo nếu chưa có) trước khi write.

**Lấy thông tin cần ghi:**
1. Timestamp: `Get-Date -Format "yyyy-MM-dd HH:mm:ss"` (PowerShell) hoặc `date "+%Y-%m-%d %H:%M:%S"` (Bash).
2. Reviewer: `git config user.name` → fallback `git config user.email` → fallback `unknown`.
3. Change description: nguyên văn input owner đã paste khi invoke `/qc-testcase-update` (cache lại từ đầu workflow, không hỏi lại).
4. Patch result: từ JSON output của Step 7 (list ID modified/added/deleted, run results preserved count, sheet name).

**Template log file (write bằng Write tool):**

```markdown
# Testcase Update Log: <output-xlsx-fullname>

Reviewer: <git-user>
Updated: <YYYY-MM-DD HH:mm:ss>
Source: <source-xlsx-path>
Output: <output-xlsx-path>
Sheet: <sheet-name | "(default)">

---

## Change description

<nguyên văn change description owner paste vào lúc invoke>

---

## Patch result

| Op | Count | IDs |
|----|-------|-----|
| Modified | N | AR-003, AR-005 |
| Added    | M | AR-008, AR-009, AR-010 |
| Deleted  | K | AR-007 |

Run results preserved: <count> cases (H/I/J intact)
```

Nếu 1 cột op count = 0 → vẫn liệt kê dòng với "—" ở IDs.

**Echo cho owner (bổ sung thêm 1 dòng vào output Step 8):**
```
  Update log: <log-path>
```

**Quy tắc khi ghi log:**
- CHỈ ghi log khi patch xlsx thành công ở Step 7 (script exit code 0). Nếu patch fail → KHÔNG ghi log, báo lỗi cho owner.
- Nếu owner reject patch plan ở Step 5 → KHÔNG ghi log (vì không có outcome).
- Nếu file log đã tồn tại tại path đó (cực hiếm — chỉ khi owner override output path trùng file cũ) → warn owner trước khi overwrite, hỏi xác nhận.
- Encoding UTF-8 để giữ dấu tiếng Việt trong change description.

## Patch Schema Details

| Op | Required keys | Optional keys | Behaviour |
|---|---|---|---|
| `modify` | `id`, `fields` (dict) | — | In-place cell update. Chỉ update field có trong `fields`, các field khác (run results, formulas) không đụng. Valid fields: `purpose`, `case`, `data`, `steps`, `expected`, `priority`, `note`. |
| `delete` | `id` | — | Xoá row bằng `delete_rows`. Mất luôn run results / bug links nếu có. |
| `add` | `case` (dict) | `after_id`, `suite_divider` | Insert row sau row có `after_id`. Thiếu `after_id` → append cuối sheet. `suite_divider` text → insert thêm 1 row divider trước row case mới (cho new suite). |

**Style discipline khi sinh case mới (giống `qc-testcase`):**
- ID format: `<prefix>-NNN` zero-padded, monotonically increasing từ max ID hiện có trong sheet.
- `steps`: numbered, `\n` separated.
- `expected`: verifiable, concrete (không "system works correctly").
- `data`: concrete values, không placeholder.

## Confirmation Flow (BẮT BUỘC)

1. Patch plan trong chat → chờ owner gõ `Confirm` / `y` / `đồng ý`.
2. Cấm write trực tiếp không qua confirm.
3. Case nào có run result H/I/J và bị DELETE → warn riêng, hỏi owner xác nhận thêm 1 nhịp.
4. ADD case mới có ID trùng case hiện có → reject, đề xuất ID khác.
5. MODIFY case không tồn tại → reject, list ID không tìm thấy.

## Memory Integration

**Read on activation:**
- `business-rules.md` — rule mới owner mô tả → check đã có chưa, nếu mới thì capture.
- `common-edge-cases.md` — case mới có lặp lại edge category nào không.
- `qa-conventions.md` — priority labels, naming style.
- `defect-history.md` — case bị xoá có link bug không.

**Write at end:**
- Rule mới (nếu owner confirm là rule, không phải edge case lẻ) → propose append vào `business-rules.md`.
- Daily log: `- {time} [TU] Updated <feature>: +N -M ~K cases → <output-path> (log: <log-path>)`.
- Update log file song song với output xlsx (xem Step 9) — chứa change description + patch result.

## After the Session

Pattern cần để ý qua nhiều session update:
- Cùng 1 feature update >3 lần trong tuần → spec không stable, flag cho Yennth72: nên freeze spec trước khi viết test.
- Mỗi update đều ADD heavy → coverage ban đầu thiếu, đề xuất rerun `qc-edge` cho feature đó.
- Mỗi update đều DELETE → over-coverage ban đầu (viết case suy diễn không có rule backing), nhắc owner tighten lại `qc-scenario` flow.

Echo path file output để owner copy. Đề xuất chạy tiếp [[qc-codegen-update]] nếu auto script cũng cần sync.

Related: [[qc-testcase]] [[qc-codegen-update]] [[qc-bug-edit]]
