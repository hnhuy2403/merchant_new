---
name: qc-bug-status
description: Cập nhật trạng thái bug (Open / Resolved / Reopen / Done / Cancelled) — ghi history table trong bug file + sync defect-history memory
code: BS
---

# Bug Status Transition

## What Success Looks Like

Bug file luôn phản ánh trạng thái hiện tại của bug. Mỗi lần đổi state có 1 row mới trong lịch sử (timestamp, người, ghi chú). Defect-history memory sync theo — pattern matching tương lai biết bug nào còn Open, bug nào đã Done. Không có bug "mồ côi" giữa dev và tester.

## State Machine

| State | Icon | Ý nghĩa | Ai set |
|---|---|---|---|
| Open | 🟢 | QC vừa tạo bug, dev chưa pickup | QC (tự động khi `qc-bug`) |
| Resolved | 🟡 | Dev đã fix code + đã build lên môi trường test | Dev (edit file) hoặc tester relay |
| Reopen | 🔴 | QC retest fail / bug tái xuất hiện regression | QC |
| Done | ✅ | QC đã verify PASS, bug đóng | QC |
| Cancelled | ⚫ | Không xử lý (duplicate, by-design, won't fix) | QC + Dev align |

**Transitions hợp lệ:**
- `(create)` → `Open`
- `Open` → `Resolved` (dev fix xong)
- `Open` → `Cancelled` (huỷ trước khi fix)
- `Resolved` → `Done` (retest PASS)
- `Resolved` → `Reopen` (retest FAIL — fix chưa đúng)
- `Reopen` → `Resolved` (dev fix lại)
- `Reopen` → `Cancelled`
- `Done` → `Reopen` (regression — bug quay lại sau khi đã Done)
- `Cancelled` → `Open` (đảo quyết định)

**Transitions cấm:** `Open → Done` (phải qua Resolved), `Done → Resolved/Cancelled` (đã đóng terminal — muốn mở phải Reopen trước), `Resolved → Open` (đã có fix rồi không quay lại Open).

## Trigger Modes

### Mode A — Tester gọi qua agent

Cú pháp:
```
/qc-bug-status <BUG-ID> <new-state> [ghi chú]
```

Ví dụ:
- `/qc-bug-status BUG-2026-05-14-001 Resolved Dev fix tại commit abc123, build staging 17:00`
- `/qc-bug-status BUG-2026-05-14-001 Done Retest pass 5/5 trên Chromium`
- `/qc-bug-status BUG-2026-05-14-001 Reopen Vẫn redirect /onboarding sau fix v1.2.3`

**Workflow agent:**
1. Locate bug file:
   - Nếu owner đưa path đầy đủ → dùng.
   - Nếu chỉ có BUG-ID → Grep `_bmad-output/test-artifacts/bugs/` pattern `Mã bug: <BUG-ID>` → tìm file.
   - Không tìm thấy → hỏi owner path.
2. Đọc current Status trong file (section `## Trạng thái`).
3. **Validate transition** theo bảng trên. Cấm → dừng + giải thích lý do.
4. Update `**Hiện tại:**` thành new state + icon.
5. Update `**Lần cập nhật:**` thành timestamp ISO + người (mặc định `Yennth72 (QA)`, hoặc lấy theo owner chỉ định).
6. **Append row** vào "Lịch sử trạng thái" table.
7. Sync defect-history: tìm entry `BUG-ID` trong `_bmad/memory/tts-qc/curated/defect-history.md`, update field Status.
8. Echo: bug ID + state mới + path file để owner relay cho dev/team.

### Mode B — Dev tự edit file (không qua Claude)

Dev có thể edit trực tiếp file bug `.md` (file nằm trong repo). Hướng dẫn dev (ghi trong section "Hướng dẫn cập nhật cho dev" của mỗi bug file):

1. Mở file bug ở repo path đã cho.
2. Tìm section `## Trạng thái`.
3. Đổi giá trị `**Hiện tại:**` thành state mới + icon đúng.
4. Đổi `**Lần cập nhật:**` thành timestamp + tên dev.
5. Thêm 1 row vào table "Lịch sử trạng thái": `| YYYY-MM-DD HH:mm | <từ> | <sang> | <dev name> | <commit/PR/note> |`
6. Commit file thay đổi cùng commit fix code (vd: `git add _bmad-output/test-artifacts/bugs/... && git commit -m "fix(login-farm): redirect onboarding (BUG-2026-05-14-001)"`).
7. Báo tester biết để retest.

### Mode C — Auto-set từ qc-retest

Khi tester chạy `/qc-retest` và bug có result:
- Retest PASS → đề xuất transition `Resolved → Done`, hỏi confirm.
- Retest FAIL → đề xuất transition `Resolved → Reopen`, hỏi confirm + tạo note tóm tắt retest fail.

## Format Status Block (gắn vào mỗi bug file)

```markdown
## Trạng thái

- **Hiện tại:** 🟢 Open
- **Lần cập nhật:** 2026-05-14 16:50 by Yennth72 (QA)

### Lịch sử trạng thái
| Ngày giờ | Từ | Sang | Người | Ghi chú |
|---|---|---|---|---|
| 2026-05-14 16:50 | — | 🟢 Open | Yennth72 (QA) | File bug từ auto test fail LF-001 |
```

Section này luôn đặt **ngay sau header bug** (trước "Tiêu đề") để dev/QC nhìn thấy đầu tiên khi mở file.

## Hướng dẫn dev cập nhật (block chèn cuối mỗi bug file)

```markdown
## Hướng dẫn cập nhật trạng thái (cho dev / QC)

**Dev sau khi fix:**
1. Đổi `Hiện tại:` thành `🟡 Resolved`.
2. Cập nhật `Lần cập nhật:` = `<YYYY-MM-DD HH:mm> by <tên dev>`.
3. Thêm row vào table "Lịch sử trạng thái": `| <thời gian> | 🟢 Open | 🟡 Resolved | <tên dev> | Fix tại <commit/PR>, build <môi trường> |`.
4. Commit file kèm commit fix, ping QA retest.

**QC sau khi retest:**
- PASS → `Resolved → ✅ Done`.
- FAIL → `Resolved → 🔴 Reopen`, thêm note về behaviour vẫn sai.
- Có thể chạy `/qc-bug-status <BUG-ID> <new-state> [note]` để agent tự cập nhật.
```

## Memory Integration

**Read:**
- `defect-history.md` — locate entry để sync.
- Bug file hiện tại — đọc Status block cũ.

**Write:**
- Update Status block trong bug file (file `_bmad-output/test-artifacts/bugs/...`).
- Update field **Status** ở entry tương ứng trong `defect-history.md`.
- Daily log (nếu bật): `- {time} [BS] Bug <BUG-ID> chuyển <from> → <to> (by <person>)`.

## After the Session

Nếu nhiều bug stuck ở 1 state (5 bug Open >7 ngày chưa Resolved, hay 3 bug Reopen sau retest) → flag cho Yennth72 như pattern bottleneck, đề xuất escalate dev lead / standup.
