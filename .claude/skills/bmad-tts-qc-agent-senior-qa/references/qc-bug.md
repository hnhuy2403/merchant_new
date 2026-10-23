---
name: qc-bug
description: Professional bug report — owner cung cấp đường dẫn report (Playwright/Appium/…) + optional severity/priority/assignee/reporter khi gọi; output Vietnamese format (Tiêu đề / Data test / Các bước / Actual / Expect / Image-Video)
code: BG
---

# Bug Report

## What Success Looks Like

Owner kết thúc phiên với các bug report copy-paste sẵn, dev đọc xong tái hiện được trong 2 phút. Report không có lời mở đầu, không kể chuyện, không phán xét — chỉ structured fact. Tiêu đề searchable. Các bước tối thiểu. Severity / priority calibrate theo `qa-conventions.md`. Mỗi bug append vào `defect-history.md` để pattern-match về sau.

## Default Mode: Auto-Test Report (Playwright / Appium / Cypress …)

**Trigger:** owner gọi `/qc-bug` (hoặc `BG`) **kèm đường dẫn report file/folder**, có thể kèm các tham số inline `key=value`.

**Command syntax:**
```
/qc-bug <path> [severity=<S1|S2|S3|S4>] [priority=<P0|P1|P2|P3>] [assignee=<name>] [reporter=<name>]
```

- `<path>` (bắt buộc): đường dẫn tới report file/folder.
- `severity=` / `priority=` / `assignee=` / `reporter=` (optional, **không quan tâm thứ tự**): bổ sung data cho header bug. Có thể dùng alias viết tắt: `sev=`, `pri=`, `as=`, `rep=`.
- **Không truyền field nào → để trống → agent BẮT BUỘC hỏi owner trước khi write** (xem Confirmation Flow). Cấm tự đoán Severity/Priority/Assignee/Reporter khi owner không khai báo.

Ví dụ:
- `/qc-bug playwright-report/ severity=S2 priority=P1 assignee=devA reporter=Yennth72`
- `/qc-bug test-results/ sev=S3 pri=P2` → agent vẫn hỏi Assignee/Reporter
- `/qc-bug appium-report.json` → agent hỏi cả 4 field

Owner sẽ cung cấp path khác nhau cho từng phân hệ — **không tự đoán, không hardcode**:
- Web có thể là `playwright-report/index.html` + `test-results/`
- Mobile có thể là folder report Appium / Maestro / Detox / Xcode test
- API có thể là output Newman / Karate / pytest

**Quy trình khi nhận path:**

1. **Hỏi xác nhận path nếu chưa rõ** — owner chỉ ghi "report mobile" → hỏi đường dẫn cụ thể. Đừng đoán.
2. **Khảo sát cấu trúc** trước khi đọc — Bash `ls -la <path>` để hiểu owner đưa file đơn lẻ hay folder run output.
3. **Locate failure data** — tuỳ framework:
   - Playwright: `test-results/<slug>/error-context.md` (Name, Location, Error details, Page snapshot), `.last-run.json` (danh sách fail), `test-failed-*.png`, `video.webm`, `trace.zip`.
   - Appium / Maestro: thường có `report.json` hoặc `results.xml` + screenshot folder.
   - Generic JUnit XML: `<testcase>` có child `<failure>` là test fail.
   - HTML report đơn lẻ: nếu file quá lớn (>500KB) không Read toàn bộ — Grep keyword `failed|FAIL|error` trước, sau đó Read offset.
4. **Lấy data test** — nếu spec/test file được trỏ trong `Location:`, Read file đó để trích input cụ thể (SĐT, mật khẩu, mã NCC, payload API…).
5. **Sinh 1 bug block / 1 test fail** theo format dưới. Nếu nhiều test fail cùng 1 nguyên nhân (cùng selector, cùng URL) → gộp 1 bug gốc + list các test bị ảnh hưởng.

**Output format (Vietnamese — Yennth72 preference):**

Đầy đủ file `.md` cần các section sau (theo thứ tự):

```markdown
# BUG-<NNN> — <TEST-ID>: <Tiêu đề ngắn>

- **Mã bug:** BUG-<YYYY-MM-DD>-<NNN>
- **Test ID:** <vd LF-001>
- **Ngày phát hiện:** <YYYY-MM-DD>
- **Reporter:** <giá trị từ `reporter=` hoặc hỏi owner>
- **Assignee:** <giá trị từ `assignee=` hoặc hỏi owner>
- **Severity:** <giá trị từ `severity=` hoặc hỏi owner — S1/S2/S3/S4>
- **Priority:** <giá trị từ `priority=` hoặc hỏi owner — P0/P1/P2/P3>
- **Suspected area:** <module/file từ Location:>
- **Repro rate:** <fail/total>

---

## Trạng thái

- **Hiện tại:** 🟢 Open
- **Lần cập nhật:** <YYYY-MM-DD HH:mm> by <Yennth72 (QA)>

### Lịch sử trạng thái
| Ngày giờ | Từ | Sang | Người | Ghi chú |
|---|---|---|---|---|
| <YYYY-MM-DD HH:mm> | — | 🟢 Open | <Reporter> (QA) | File bug từ <auto test ID / mô tả ngắn> |

---

## Tiêu đề
<verb-led, ≤80 chars, gồm screen + symptom>

## Data test
| Field | Value |
|---|---|
| <field> | <value> |

## Các bước thực hiện
1. <step user-facing>
2. <step>
3. <step>

## Actual Result
<trích từ Error details / assertion fail>

## Expect Result
<trích từ Expected pattern / assertion>

## Image/Video đính kèm
- Screenshot: `<path>`
- Video: `<path>`
- Trace / Log: `<path>` (nếu có)
- Report tổng: `<path owner cung cấp>`

## Note cho dev (optional)
<insight giúp dev debug nhanh — nếu QA có>

---

## Hướng dẫn cập nhật trạng thái (cho dev / QC)

**Dev sau khi fix:**
1. Đổi `Hiện tại:` thành `🟡 Resolved`.
2. Cập nhật `Lần cập nhật:` = `<YYYY-MM-DD HH:mm> by <tên dev>`.
3. Thêm row vào table "Lịch sử trạng thái": `| <thời gian> | 🟢 Open | 🟡 Resolved | <tên dev> | Fix tại <commit/PR>, build <môi trường> |`.
4. Commit file thay đổi này cùng commit fix code, ping QA retest.

**QC sau khi retest:**
- PASS → `Resolved → ✅ Done`.
- FAIL → `Resolved → 🔴 Reopen`, thêm note về behaviour vẫn sai.
- Có thể chạy `/qc-bug-status <BUG-ID> <new-state> [note]` để agent tự cập nhật.

**Edit field khác (Severity / Priority / Assignee / Reporter / Suspected area / Note …):**
- Chạy `/qc-bug-<BUG-ID> <field>=<value> [<field>=<value>...]` — agent sẽ update header + ghi "Lịch sử chỉnh sửa".
- Vd: `/qc-bug-BUG-2026-05-14-001 severity=S1 priority=P0 assignee=devB`.
- Chi tiết: xem skill `qc-bug-edit` (code [BE]).
```

**Mỗi bug file mới sinh ra luôn ở state `🟢 Open`** với 1 row history đầu tiên. Cấm sinh bug ở state khác — phải qua `qc-bug-status` để transition.

**Các bước thực hiện — cách suy ra:**
- Test name thường dạng `Suite-N: <Feature> >> <Test-ID>: <Action>` → tách: vào màn Feature → thực hiện Action.
- Cần chi tiết hơn: Read file ở `Location:` (`*.spec.ts:line` / `*.py:line` …) → diễn dịch các `goto / fill / tap / click / expect` sang ngôn ngữ user-facing tiếng Việt.

**Severity default (khi `qa-conventions.md` trống):**
- S1: blocker — không vào được app, mất tiền, sai data nghiêm trọng.
- S2: critical — luồng chính fail, workaround khó.
- S3: major — feature fail nhưng workaround dễ.
- S4: minor — UI lệch, text sai, cosmetic.

**Priority default:**
- P0: fix trong ngày — P1: fix trong sprint — P2: sprint sau — P3: backlog.

## Manual Mode: Owner Mô Tả Bug Bằng Text

**Trigger:** owner paste mô tả bug bằng lời (không kèm report file).

Vẫn dùng cùng format Vietnamese ở trên, nhưng **probe owner** các trường còn thiếu (Environment, Steps, Evidence) trước khi sinh report.

**Title discipline (áp dụng mọi mode):**
- Verb-led: "User không submit được form khi X" / "App crash sau khi Y" — KHÔNG dùng "Lỗi form" / "Crash".
- Concrete trigger: nêu rõ action gây lỗi.
- Searchable: gồm tên màn + symptom keyword.

**Severity vs Priority** (nhắc):
- Severity = mức impact nếu lọt prod.
- Priority = mức cần fix sớm. Hai cái có thể lệch nhau (S1 ở feature ship quý sau vẫn có thể P3).

## Confirmation Flow (BẮT BUỘC trước khi write)

Yennth72 **luôn xác nhận trước khi tôi write bất kỳ artifact nào**. Quy trình:

1. **Parse command args** — đọc các cặp `key=value` từ command (severity / priority / assignee / reporter, gồm cả alias `sev` / `pri` / `as` / `rep`). Validate Severity ∈ {S1..S4}, Priority ∈ {P0..P3}. Sai format → báo owner, hỏi lại.
2. **Hỏi field còn thiếu — KHÔNG tự đoán:**
   - Severity / Priority / Assignee / Reporter thiếu cái nào → liệt kê tất cả và hỏi owner 1 lượt (gộp câu hỏi, không hỏi từng cái).
   - Có thể gợi ý dựa trên `qa-conventions.md` (severity scale, default assignee theo area, v.v.) nhưng vẫn phải owner confirm.
3. Sinh bug report block(s) trong chat — đầy đủ 6 trường + Reporter/Assignee/Severity/Priority/Suspected area.
4. Nếu nghi ngờ test-issue thay vì product-bug → **probe owner trước** (xem Sherlock note pattern: hỏi account đã onboard chưa, spec có gap không, v.v.).
5. Hỏi owner xác nhận: bug thật hay test-issue. Nếu test-issue → KHÔNG ghi gì vào defect-history (tránh nhiễu).
6. Nếu bug thật → đề xuất output path + hỏi: defect-history append? daily log? — chờ owner gõ `Confirm` / `đồng ý` / equivalent.
7. **Chỉ khi owner xác nhận** → mới write các artifact dưới.

## Output Artifacts (sau khi owner confirm)

### 1. Bug report file (dành cho dev)

**Path convention:**
```
{project-root}/_bmad-output/test-artifacts/bugs/{YYYY-MM-DD}/BUG-{NNN}-{TEST-ID}-{slug}.md
```
- `{YYYY-MM-DD}` = ngày phát hiện bug
- `{NNN}` = số thứ tự bug trong ngày, padded 3 chữ số (001, 002…)
- `{TEST-ID}` = mã test (LF-001) hoặc bỏ qua nếu là Manual Mode
- `{slug}` = mô tả ngắn kebab-case, ≤6 từ

**Nội dung file:** đầy đủ format 6 trường + metadata header (mã bug, ngày, QA report, severity/priority/area/repro) + "Note cho dev" cuối file (nếu QA có insight giúp dev debug nhanh hơn).

Ví dụ: `_bmad-output/test-artifacts/bugs/2026-05-14/BUG-001-LF-001-login-redirect-onboarding.md`.

### 2. Defect history memory (knowledge layer — pattern matching)

**Append vào `{project-root}/_bmad/memory/tts-qc/curated/defect-history.md`** với full structure: bug ID, title, sev/pri, suspected area, data test rút gọn, actual/expect rút gọn, repro, link tới bug report file, evidence path, root cause (nếu biết), fix PR (nếu biết), pattern note. Nhóm theo ngày bằng heading `## YYYY-MM-DD`.

### 3. Daily log (optional — chỉ khi owner yêu cầu)

**Append vào `{project-root}/_bmad/memory/tts-qc/daily/YYYY-MM-DD.md`:** `- {time} [BG] Bug filed: <title> (<sev>/<pri>) → <bug report path>`.

Default Mode N failures → write N bug report files (đánh số 001, 002, …), append N entries vào defect-history, gộp dòng trong daily log nếu owner bật.

### 4. Báo lại path cho owner

Sau khi write xong, **luôn echo đường dẫn đầy đủ** của (các) bug report file để owner copy gửi dev.

## Memory Integration — Read on activation

- `defect-history.md` — bug này có giống pattern cũ không? Match aggressive.
- `qa-conventions.md` — severity / priority definitions của team.
- `stakeholders.md` — assign / CC cho ai.

## After the Session

Nhiều bug 1 phiên lộ pattern (3 bug payment / 1 ngày, hay cùng 1 selector fail nhiều test) → flag cho Yennth72 như "smell", escalate dev lead. Nhóm bug gốc thay vì file trùng lặp.
