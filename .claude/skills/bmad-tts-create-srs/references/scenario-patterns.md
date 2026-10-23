# Scenario Authoring & Edge-Case Discovery Checklist

> Loaded on demand by `SKILL.md` Step 2. Use this when synthesizing the `Kịch bản nghiệp vụ` section. The checklist is **systematic**, not exhaustive — apply only dimensions that the story's domain genuinely involves. Pad scenarios = noise that hides real risk.

## BDD Scenario Format

Every scenario follows the same skeleton — readers should be able to skim 20 of them in seconds:

```
**<ID> — <Tên ngắn mô tả tình huống>** (refs: AC-N, BR-N)
- **Pre:** <state khác mặc định mục 4.1, nếu có>
- **Given** <bối cảnh / state ban đầu, dùng dữ liệu cụ thể>
- **When** <hành động trigger>
- **Then** <kết quả quan sát được — không nói cách triển khai>
- **Post:** <state thay đổi sau scenario, nếu khác mặc định mục 4.2>
```

### ID conventions

| Prefix | Loại scenario | Khi nào dùng |
|--------|---------------|--------------|
| `H1, H2, ...` | Happy path | Đường đi thành công, AC mô tả trực tiếp |
| `E1, E2, ...` | Edge case | Boundary / concurrency / unusual state, vẫn kết thúc đúng |
| `R1, R2, ...` | Error & Recovery | Có lỗi rõ ràng — kiểm tra error message, recovery flow |

### Style rules

- **Concrete data over placeholders.** `nguyen.van.a@vss.gov.vn` thay vì "user X". Sai dữ liệu cụ thể dễ phát hiện hơn sai abstract.
- **Behavior, not implementation.** "Hệ thống từ chối submit" thay vì "endpoint POST /login trả 401". Implementation thuộc detail-design.
- **One trigger per When.** Nếu cần 2 actions liên tiếp, tách thành 2 scenarios hoặc dùng 2 dòng When riêng biệt.
- **Then phải observable.** Không viết Then cho state mà QA không kiểm tra được.
- **Refs bắt buộc.** Mỗi scenario phải link tới AC-N (và BR-N nếu liên quan). Scenario không link AC = scenario sai phạm vi.

## Edge-Case Discovery Checklist

Đi qua từng dimension bên dưới. Với mỗi dimension, hỏi: **"Story này có chạm tới chiều này không?"** Nếu có và nhánh đó chưa có scenario, viết một `E#`. Nếu không, bỏ qua — đừng pad.

### 1. Boundary values

- Giá trị tối đa / tối thiểu của input (length, range, count).
- Empty / null / whitespace-only.
- Unicode (dấu tiếng Việt, emoji, RTL chars).
- Timezone & DST: thao tác diễn ra đúng giờ chuyển DST? Cross-timezone user?
- Số lượng phần tử = 0, 1, N, N+1 (vd. limit collection).
- Floating point precision (tiền tệ — tránh ghi `0.1 + 0.2`).

### 2. Concurrency & race conditions

- Cùng một user thao tác từ 2 device cùng lúc.
- 2 user khác nhau cùng action trên cùng resource (vd. 2 admin cùng approve một record).
- Background job race với user action (vd. session expiry tick đúng lúc user submit).
- Double-submit (user click 2 lần do lag).
- Tạo trùng key trong race (idempotency key cần thiết?).
- Đọc-rồi-ghi không trong transaction (lost update).

### 3. Network & infrastructure failure

- Token (access/CSRF/idempotency) hết hạn giữa flow.
- Mất kết nối giữa step N và step N+1.
- Timeout từ downstream service.
- Retry: idempotent? Side effect duplicate?
- Partial success: bước A xong, bước B fail — rollback hay forward-fix?
- Rate limit hit (429).

### 4. Auth / Permission

- Permission bị revoke giữa session.
- User đổi role giữa flow (impersonation, scope thay đổi).
- Tenant suspended / user locked giữa transaction.
- Cross-tenant data leak (user X đọc resource của tenant Y).
- Read-only mode / maintenance mode.

### 5. Data corruption / invariants

- Record corrupt (json invalid, foreign key broken).
- Partial migration: schema mới + data cũ chưa migrate.
- Soft-deleted records xuất hiện trong query.
- Encoding mismatch (UTF-8 vs latin-1 trong import).
- Duplicate detection bypass (trim space, case sensitivity).

### 6. State machine violations

- Gọi action ở state không cho phép (vd. approve một record đã rejected).
- State revert (undo) — có cho phép không, có audit không.
- Event ordering: event A đến sau B dù timestamp ngược (clock skew).

### 7. Role-specific & UX edge cases

- Role mới chưa có UX định nghĩa.
- Accessibility: keyboard-only navigation, screen reader announcement của error.
- i18n: tên Việt có dấu, địa chỉ dài, số điện thoại 10 vs 11 chữ số.
- Mobile vs desktop: viewport, touch vs keyboard.
- First-run vs returning user.

### 8. Time-based behavior

- Cron / scheduled job có chạy đúng giờ không khi server timezone khác user timezone?
- Grace period boundary (vd. "có hiệu lực trước ngày X" — đúng 23:59 ngày X-1 là gì?).
- Long-running flow: session timeout giữa step.

## Anti-patterns — đừng làm

| Anti-pattern | Vì sao tệ | Sửa thành |
|--------------|-----------|-----------|
| `Given user nhập dữ liệu hợp lệ` | Quá generic, không kiểm tra được | `Given user nhập email "a@b.vn", password "Abc@1234"` |
| `Then hệ thống xử lý đúng` | Không observable | `Then UI hiển thị "Tạo tài khoản thành công" và redirect tới /dashboard` |
| Scenario E# không tham chiếu AC | Phạm vi mơ hồ — có thể là scope creep | Hoặc map về AC, hoặc move sang Câu hỏi mở để PM bổ sung AC |
| Lặp lại Pre đã ghi ở mục 4.1 trong mọi scenario | Noise, đọc mỏi | Chỉ ghi Pre khi scenario CẦN khác mặc định |
| 1 scenario có 5 dòng When | Không thể debug khi fail | Tách scenarios, hoặc gom 2 action sát nhau bằng dấu `+` |
| Scenario kiểm tra implementation (vd. "DB row được insert") | Vi phạm WHAT vs HOW | "User thấy record mới trong list" |

## Khi nào dừng

Bạn đã đủ scenario nếu:
1. Mỗi AC có ≥ 1 happy-path scenario.
2. Mỗi error path có thông báo định danh đã có ≥ 1 R# scenario.
3. Mỗi business rule (BR) có ≥ 1 scenario chứng minh nó held (positive) hoặc enforced (negative).
4. Đi qua 8 dimension checklist, mỗi dimension có quyết định "có thêm" hoặc "không liên quan" rõ ràng — không bỏ ngỏ.

Nếu thiếu context để quyết định, viết câu hỏi mở thay vì đoán scenario.
