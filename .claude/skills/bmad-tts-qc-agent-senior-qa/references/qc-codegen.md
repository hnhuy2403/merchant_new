---
name: qc-codegen-update
description: Incrementally update an existing automation script khi test cases thay đổi — auto-diff giữa xlsx (or md) và script, chỉ patch test() blocks bị ảnh hưởng. Preserve helper functions, locators owner đã tinh chỉnh, before/after hooks, DB query helpers. Output versioned file (.v2.spec.ts ...).
code: GU
---

# Codegen Update (incremental)

## What Success Looks Like

Owner đã có 1 auto script (vd `_bmad-output/test-artifacts/automation/web/auto-recharge.spec.ts`) — script đã chạy ổn, owner đã tinh chỉnh locator (đổi `getByText` thành `getByRole`, fix timing), thêm custom `test.beforeEach` setup, link sang `db/<feature>.ts` helper.

Test cases trong xlsx đã update (qua `/qc-testcase-update`) → một số case mới, một số case đổi steps/expected, vài case bị xoá.

Owner muốn:
- **Auto detect** test() block nào trong script tương ứng với case nào trong xlsx.
- **Patch** chỉ tests bị ảnh hưởng (add new test blocks, modify steps/assertions của existing, delete tests obsolete).
- **Preserve** mọi thứ owner tinh chỉnh: helper imports, `test.describe` setup, `test.beforeEach/afterAll`, locator strategy, DB helpers, comments owner thêm vào.

Output: versioned file `<base>.v2.spec.ts` (hoặc `.yaml.v2` cho Maestro, `.js.v2` cho miniapp).

## Trigger Pattern

```
/qc-codegen-update <script-path> [--cases <xlsx-or-md-path>] [--target=web|mobile|miniapp] [--with-db]
```

Ví dụ:
- `/qc-codegen-update _bmad-output/test-artifacts/automation/web/auto-recharge.spec.ts --cases _bmad-output/test-artifacts/test-cases/auto-recharge-v2.xlsx`
- `/qc-codegen-update login-farm.spec.ts --cases login-farm-v3.xlsx --with-db`

Thiếu `--cases` → hỏi owner: file xlsx test cases mới ở đâu (default: cùng base name trong `qc_output_folder/test-cases/` — chọn version cao nhất).

Thiếu `--target` → infer từ extension (`.spec.ts`/`.spec.js` → web Playwright, `.yaml` → mobile Maestro, `.js` trong miniapp/ → miniapp). Ambiguous → hỏi.

## Your Approach

**Step 1 — Load script + cases.**

Read script file (Read tool). Parse `test('<ID>: ...', ...)` blocks bằng regex hoặc literal scan:
- Playwright TS: `test('<ID>: <title>', async ({ ... }) =>` hoặc `test('<ID>: <title>', async ({ ... }) => { ... })`.
- Maestro YAML: comment markers `# <ID>: <title>` đứng trên block YAML.
- Miniapp JS: `test('<ID>: ...', async () => ...` hoặc function-named theo ID.

Extract list: `[{id, title, block_start_line, block_end_line, body}]`.

Read cases JSON từ xlsx (`xlsx-utils.py read-cases <xlsx>`) hoặc parse Markdown nếu input là `.md`.

**Step 2 — Auto-diff xlsx ↔ script.**

Build 2 set IDs. Compare:

| Trạng thái | Hành động |
|---|---|
| ID có trong xlsx, KHÔNG có trong script | **ADD** — sinh test block mới (apply [[qc-codegen]] mapping rules) |
| ID có trong script, KHÔNG có trong xlsx | **DELETE candidate** — warn owner, vì có thể là custom test owner thêm tay |
| ID có ở cả 2, **steps/expected khác** so với khi gen lần trước | **MODIFY** — patch chỉ phần body trong test block |
| ID có ở cả 2, steps/expected giống → no-op |

**Phát hiện MODIFY:** so sánh "steps + expected" của case trong xlsx với code trong test body. Vì code đã dịch sang framework idioms, so sánh trực tiếp string không khả thi → dùng heuristics:
- Steps count khác → MODIFY.
- Expected text (Vietnamese error message hay UI text) không xuất hiện trong `expect(...)` assertion → MODIFY.
- Data value (số phone, email, password) trong case không xuất hiện trong `fill('...')` call → MODIFY.

Heuristic không chắc chắn → liệt kê "MAYBE MODIFY" cho owner quyết định, không tự patch.

**Step 3 — Đề xuất patch plan trong chat.**

Format:
```
PATCH PLAN cho <script-path>
Cases source: <xlsx-path>

ADD (2 tests):
  AR-008: Reject accountId < 8 digits
    Insert after: existing test 'AR-005' (line 47)
    Body preview:
      test('AR-008: Reject accountId < 8 digits', async ({ page }) => {
        await page.goto('...');
        await page.getByLabel('Account ID').fill('1234567');
        ...
        await expect(page.getByText('AccountId phải ít nhất 8 chữ số')).toBeVisible();
      });

  AR-009: ...

MODIFY (1 test):
  AR-003: steps + expected changed
    Lines: 28-38
    Diff:
      -    await page.getByLabel('Account ID').fill('12345');
      +    await page.getByLabel('Account ID').fill('1234567');
      -    await expect(page.getByText('Reject với msg X')).toBeVisible();
      +    await expect(page.getByText('Phải ít nhất 8 chữ số')).toBeVisible();

DELETE candidate (1 test):
  AR-007: Login bypass via deep link
    Lines: 60-72
    ⚠ Owner đã thêm custom comment '// keep for regression' → có thể intentional, confirm xoá?

MAYBE MODIFY (cần owner confirm):
  AR-002: Heuristic không match — case data đổi từ '02863255523' sang '0987654321'
          nhưng script vẫn dùng '02863255523'. Owner có ý đồ không?

Preserve (không đụng):
  - Imports + helper imports (`./db/<feature>`)
  - test.beforeEach / test.afterAll hooks
  - Custom utility functions
  - Comments owner đã thêm

Output: <script-base>.v2<ext> (next available version)
```

**Step 4 — Owner confirm.**

Chờ `Confirm` / `y` / `đồng ý`. Owner có thể chỉnh:
- Skip 1 ADD: "skip AR-009"
- Convert DELETE candidate → keep: "keep AR-007"
- Accept MAYBE MODIFY: "update AR-002 theo case mới"
- Force MODIFY 1 test mà agent không detect: "modify AR-004 theo case mới"

Cập nhật plan → hỏi confirm lại.

**Step 5 — Detect output version path.**

Glob `<dir>` cho `<base>.v*<ext>`. Max + 1. Chưa có → `.v2`. Format:
- `auto-recharge.spec.ts` → `auto-recharge.v2.spec.ts` (chèn `.v2` trước extension cuối nếu là `.spec.ts/.spec.js`, trước `.ts/.js/.yaml` nếu khác).

**Step 6 — Apply patches bằng Edit tool.**

Copy source sang output path trước (read source → Write to output). Sau đó apply patches lên file output theo thứ tự an toàn:

1. **MODIFY** trước (no line shifts ngoài phạm vi block bị sửa).
2. **DELETE** sau, **descending line order** (xoá block dưới trước, block trên sau, để line numbers không drift).
3. **ADD** cuối, **descending insertion point** (insert dưới trước, trên sau).

Mỗi operation = 1 Edit call với old_string đủ unique (lấy block test cùng signature `test('ID: title', ...)` đến `});`).

Bắt buộc:
- Giữ nguyên indentation, format, comments giữa test blocks.
- Giữ nguyên header (imports, describe, beforeEach, helpers).
- Mới thêm test block → indent + style giống tests xung quanh.

**Step 7 — Validate output.**

Đọc lại output file. Spot check:
- Import statements intact?
- Test count = (old count − deletes + adds)?
- Helpers (`./db/<feature>`) còn import nếu có DB test?
- Nếu MODIFY/ADD test có DB-Check → có gọi helper từ `db/<feature>.ts` không? Nếu helper chưa có function tương ứng → warn owner cần update file `db/<feature>.ts` (or auto-suggest helper signature).

**Step 8 — Echo kết quả.**

```
✓ Patched <output-path>
  Added:    2 tests (AR-008, AR-009)
  Modified: 1 test  (AR-003)
  Deleted:  1 test  (AR-007)
  Preserved: 4 hooks/helpers, 7 untouched tests

Output:  <output-path>
Old:     <source-path> (unchanged)

Run command (same as before):
  npx playwright test <output-path>

Note:
  - File mới <base>.v2<ext> — owner update test runner config nếu cần.
  - File cũ giữ nguyên để rollback nếu cần.
```

## Preserve Rules (BẮT BUỘC)

**TUYỆT ĐỐI không đụng** trừ khi MODIFY/DELETE 1 test cụ thể:
- `import` statements (kể cả helper imports owner thêm).
- `test.describe('...')` wrapper + setup args.
- `test.beforeAll`, `test.beforeEach`, `test.afterEach`, `test.afterAll` hooks.
- Custom utility functions (`async function loginAs(page, role) { ... }`).
- Comments owner thêm (đặc biệt comments có pattern `// KEEP` / `// MANUAL` / `// FIX`).
- Locator strategy tinh chỉnh: nếu owner đổi từ `getByText` sang `getByRole` cho 1 element nào đó, agent KHÔNG được revert về `getByText` khi MODIFY khác test cùng dùng element đó.

**Detect manual tweaks heuristics:**
- Comment marker patterns: `// KEEP`, `// MANUAL`, `// FIX-`, `// HACK`, `// TODO`, `// PRESERVE`.
- Locator dùng `data-qa` hoặc `data-test-id` selector → custom convention, không revert.
- Hardcoded waits (`page.waitForTimeout(2000)`) → thường là manual flakiness fix, không xoá.

Nếu MODIFY 1 test mà locator owner đã tinh chỉnh → giữ locator cũ, chỉ update data/assertion text.

## Confirmation Flow

1. Patch plan trong chat → chờ `Confirm` / `y` / `đồng ý`.
2. DELETE candidate có comment `// KEEP` / custom hook reference → warn 2 lần, owner phải confirm thêm 1 nhịp.
3. MAYBE MODIFY → owner phải explicit confirm từng case (`update AR-002` hoặc `skip AR-002`), không bulk confirm.
4. ADD test cần DB helper chưa tồn tại → warn, hỏi: tạo helper trong `db/<feature>.ts` cùng patch hay defer cho owner.

## Cross-target Notes

**Web (Playwright TS):**
- Test block boundary = `test('<ID>:` đến `});` khớp brace.
- DB-Check rows trong case → gen thêm `test.step('DB: ...', async () => { ... })`.
- Helper file `db/<feature>.ts` cần thêm function mới → đề xuất diff cho file này riêng, owner confirm.

**Mobile (Maestro YAML):**
- Mỗi case = 1 file YAML hoặc 1 block trong file gộp. Convention: marker `# <ID>: <title>` đứng trên block.
- Steps là YAML list nên patch line-based, không phải brace-based.
- Append assertVisible / inputText theo case mới.

**MiniApp (WeChat/Zalo JS):**
- Test functions wrapped trong async IIFE hoặc `describe`. Block boundary giống Playwright.
- `miniProgram.close()` ở cuối — không đụng.

## Memory Integration

**Read on activation:**
- `qa-conventions.md` — locator convention nếu team đã curate (vd: `data-qa` không phải `data-testid`).
- `db-config.md` (nếu `--with-db`) — feature→table mapping để gen DB step cho test mới.
- `project-profile.md` — framework version, browser matrix nếu test mới cần.

**Write at end:**
- Daily log: `- {time} [GU] Update auto <target>/<feature>: +N -M ~K tests → <output-path>`.
- Pattern "owner repeatedly skip cùng 1 type of ADD" (vd: skip cases về responsive) → suggest update `qa-conventions.md` rule "responsive cases ngoài scope auto, manual only".

## After the Session

Pattern cần để ý:
- MODIFY rate cao mỗi update → assertion text trong test fragile, đề xuất switch sang ID-based assertions (data-testid trong UI) thay vì text matching.
- DELETE rate cao → test cases sinh ban đầu over-coverage, feedback ngược về [[qc-testcase]] flow để tighten.
- Owner thường xuyên override "MAYBE MODIFY" theo cùng direction → cải thiện heuristic next session (update [[qc-codegen-update]] heuristics ghi vào memory).

Echo path + offer chạy test ngay: `npx playwright test <output-path> --reporter=list` để verify.

Related: [[qc-codegen]] [[qc-testcase-update]] [[qc-bug-edit]]
