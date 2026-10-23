---
name: qc-test-results
description: Sync kết quả test run (auto / manual) vào file testcase .xlsx — sinh file MỚI có Pass/Fail/Mã lỗi/Ghi chú đã điền, không ghi đè bản gốc
code: TS
---

# Test Results Sync — sinh file kết quả không ghi đè

## What Success Looks Like

Owner kết thúc phiên với 1 file `.xlsx` MỚI là bản sao của testcase gốc, đã được điền 3 cột kết quả:
- **H (IOS Lần 1):** **`P`** (Pass) hoặc **`F`** (Fail). Test chưa chạy / skip → để trống.
  - Theo convention chốt 2026-05-14, **H/I/J được dùng như Lần 1/2/3 generic** cho mọi platform (kể cả web Playwright), không phải chỉ IOS. Label "IOS" trong template là legacy mobile-first.
  - Re-run lần 2 → ghi vào I (Lần 2). Lần 3 → J (Lần 3).
- **O (Mã lỗi):** BUG-ID nếu `F`
- **P (Ghi chú):** chi tiết kết quả + metadata run (framework / browser / env / timestamp / tester)

**KHÔNG ghi vào cột N (Kết quả M).** Cột N chứa **formula tự tính P/F** từ H..M:
```
=IF(OR(<IOS last run>="F", <Android last run>="F"),"F",
    IF(OR(...="PE", ...="PE"),"PE",
        IF(AND(...blank...),"","P")))
```
Ghi vào H đủ — formula N tự derive ra kết quả tổng hợp.

File gốc nguyên vẹn. Test ID không match thì giữ row trống, không xoá. Test ID có trong results.json nhưng không có trong file gốc → cảnh báo `unmatched_ids`.

**Status code convention:**
| Code | Ý nghĩa | Cột H (ghi vào) | Cột O (Mã lỗi) | Cột P (Ghi chú) |
|---|---|---|---|---|
| `P` | Pass | `P` | trống | optional |
| `F` | Fail | `F` | BUG-ID bắt buộc | trích assertion fail + evidence |
| (trống) | Chưa chạy / skip | để trống | trống | optional reason |

## Triggers

Owner gọi `/qc-test-results` thường kèm 2 input:
1. **Path testcase gốc** (`.xlsx`)
2. **Path run output** — Playwright report folder, JUnit xml, hoặc results JSON owner soạn sẵn

Owner CÓ THỂ tự soạn `results.json` (cho manual test) hoặc agent parse từ Playwright run.

## Your Approach

### Step 1: Khảo sát input

```bash
ls -la <testcase.xlsx>
ls -la <run-output-path>
```

Hỏi nếu chưa rõ:
- Source testcase ở đâu? (vd `_bmad-output/test-artifacts/test-cases/login-farm.xlsx`)
- Run output ở đâu? (vd `playwright-report/`, `test-results/`, hoặc 1 file JSON owner đã soạn)
- Cần ghi vào sheet nào? (mặc định: sheet đầu tiên không phải template/cover)
- Output file đặt ở đâu? (mặc định gợi ý dưới)

### Step 2: Parse run results → results.json

Tuỳ framework:

**Playwright (mode auto-test):**
1. Đọc `test-results/.last-run.json` để biết test ID nào fail.
2. Với mỗi folder con trong `test-results/`, đọc `error-context.md` → trích tên test (vd `LF-001: ...`).
3. Cross-reference với testcase Excel: đọc test cases từ source xlsx, lấy danh sách ID (LF-001, LF-002, ...). Test ID có trong list ⊃ test name → kết quả của nó.
4. Test ID không có folder trong `test-results/` → Pass (vì Playwright chỉ tạo folder cho FAIL).
5. Test ID được skip (vd `test.skip` cho browser khác) → status `N/A` với note "Skipped — không match browser".

Mẫu results.json sinh ra:

```json
{
  "run": {
    "framework": "playwright",
    "browser": "chromium",
    "env": "staging",
    "datetime": "2026-05-14T16:17:00+07:00",
    "tester": "Yennth72"
  },
  "results": {
    "LF-001": {
      "status": "F",
      "bug_id": "BUG-2026-05-14-001",
      "note": "URL kết thúc /freso/seller/onboarding thay vì /danh-sach-san-pham. Evidence: test-results/login-farm-Suite-1-Happy-p-bd65a-..."
    },
    "LF-002": { "status": "P", "note": "" },
    "LF-003": { "status": "", "note": "Skipped — chỉ chạy trên webkit" }
  }
}
```

**Mỗi `status` chỉ nhận `P`, `F`, hoặc rỗng `""`.** Không dùng "Pass"/"Fail"/"N/A" full word.

**Manual / mode owner-soạn:** owner đưa thẳng results.json hoặc đọc miệng → agent soạn JSON từ chat.

Save results.json tại `_bmad-output/test-artifacts/test-reports/{YYYY-MM-DD}/results-<source-name>-{NNN}.json` để audit về sau.

### Step 3: Đề xuất output path + xác nhận trước khi write

**Path convention:**
```
_bmad-output/test-artifacts/test-reports/{YYYY-MM-DD}/<source-name>-result-{NNN}.xlsx
```

Trong đó:
- `{YYYY-MM-DD}` = ngày chạy update
- `<source-name>` = basename không có `.xlsx` của file gốc (vd `login-farm`)
- `{NNN}` = số thứ tự run trong ngày (001, 002, ...) — đếm file hiện có trong folder cùng ngày

Ví dụ: `_bmad-output/test-artifacts/test-reports/2026-05-14/login-farm-result-001.xlsx`

Hỏi owner confirm path (mặc định đề xuất ở trên). Đợi `Confirm` / `đồng ý` trước khi write.

### Step 4: Execute script

```bash
PYTHONIOENCODING=utf-8 python skills/bmad-tts-qc-agent-senior-qa/scripts/xlsx-utils.py update-results \
  --source <source-xlsx> \
  --output <output-xlsx> \
  --results-json <results-json> \
  [--sheet <sheet-name>] \
  [--run-column H|I|J]    # default H = Lần 1
```

Script sẽ:
- Load source .xlsx (chỉ đọc)
- Clone toàn bộ workbook → output path
- Tìm sheet đầu tiên không phải template/cover (hoặc dùng `--sheet`)
- Với mỗi row R15+: nếu col A khớp test ID trong results.json → ghi cột N/O/P
- Save output file
- Echo JSON: status, output_path, rows_updated, unmatched_ids

### Step 5: Báo path + summary

Echo lại cho owner:
- Output file path
- Số test case đã match / tổng
- Pass count, Fail count, Block count, N/A count
- Unmatched IDs (nếu có) — đề xuất investigate (sai prefix? testcase chưa có trong Excel?)

## Memory Integration

**Read:**
- Source xlsx — để biết list test ID hiện có.
- `defect-history.md` — cross-reference bug_id trong results.json có tồn tại không.

**Write (sau khi owner confirm):**
- `_bmad-output/test-artifacts/test-reports/{YYYY-MM-DD}/results-<source-name>-{NNN}.json` — results.json audit
- `_bmad-output/test-artifacts/test-reports/{YYYY-MM-DD}/<source-name>-result-{NNN}.xlsx` — Excel kết quả
- Daily log (nếu owner bật): `- {time} [TS] Results merged: <feature> → <output path> (Pass:X / Fail:Y)`

## After the Session

Nếu Fail rate cao (>30%) → flag cho owner: có thể test issue (data sai, env down) hoặc regression diện rộng. Đề xuất `qc-test-eval` để phân tích sâu trước khi báo PO.

Nếu unmatched IDs nhiều → testcase Excel chưa sync với automation spec. Đề xuất `qc-testcase` regenerate hoặc cập nhật manual.
