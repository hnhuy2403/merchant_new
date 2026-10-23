---
name: qc-web-cases
description: Web test cases — cross-browser, responsive, a11y, form validation. Excel output.
code: WC
---

# Web Test Cases

## What Success Looks Like

The owner ends with a real `.xlsx` of web-aware test cases for a feature: cross-browser matrix, responsive breakpoints, accessibility, form validation, keyboard navigation, browser-specific quirks. The set is denser on a11y and responsiveness than the generic `qc-testcase` output.

## Your Approach

This is `qc-testcase` with a **web lens applied first**. Run through these lenses, then generate cases.

**Web-specific scenario lenses:**

- **Browser matrix** — Chrome (latest, N-1), Safari (Mac + iOS Mobile Safari), Firefox, Edge. Specify per-feature where browser matters (e.g. WebKit IndexedDB quirks).
- **Responsive breakpoints** — mobile (375×667), tablet (768×1024), desktop (1280×800), wide (1920×1080), ultra-wide. Each major breakpoint gets at least a happy-path case.
- **Form validation** — client-side validation triggers, server-side echo, ARIA error announcements, focus management on validation error, submit-while-disabled, browser autofill behavior.
- **Keyboard navigation** — Tab order, Shift+Tab reverse, Enter submits, Escape cancels, focus traps in modals, skip-to-main-content link.
- **Accessibility (WCAG basics)** — color contrast (4.5:1 normal text, 3:1 large), screen reader announcements (NVDA/VoiceOver), alt text on images, ARIA labels on icon buttons, semantic HTML, form labels.
- **Performance / Loading** — slow network (throttle to 3G), large image lazy-load, loading skeleton states, error states, empty states.
- **Browser features** — back button, forward button, refresh mid-flow, deep link with params, query-string state restoration, history.pushState behavior.
- **Security** — XSS in user-generated content, CSP violations, mixed content (https + http resources), CORS errors visible to user.
- **Locale** — RTL languages (Arabic if in scope), date format per locale, timezone display, Vietnamese diacritics in inputs.
- **Print stylesheet** — does feature need to print? receipt / invoice / report?

**Suite organization:**

- `Suite-1: <Feature> - happy path (Chrome / Safari / Firefox / Edge)`
- `Suite-2: <Feature> - responsive (mobile / tablet / desktop)`
- `Suite-3: <Feature> - form validation`
- `Suite-4: <Feature> - keyboard / focus`
- `Suite-5: <Feature> - accessibility (a11y)`
- `Suite-6: <Feature> - browser back/forward/refresh`
- `Suite-7: <Feature> - locale / RTL` (if in scope)

When browsers diverge meaningfully, emit per-browser cases.

**Format `expected` (Kết quả mong muốn):**

Áp dụng đúng format `Expected:` chuẩn từ `qc-testcase.md` — mỗi case phải nêu rõ cả UI và DB:

```
Expected:
- UI: <hành vi UI cụ thể: redirect URL / toast / modal / aria-live announcement / focus target …>
- DB-Check: <bảng>.<cột> = <giá trị> WHERE <điều kiện>
- DB-Check: <bảng> EXISTS WHERE <điều kiện>
```

Web-specific hint cho dòng `UI:`:
- Với case cross-browser/responsive: ghi rõ breakpoint hoặc browser nếu UI khác nhau (vd `UI [Mobile 375px]: bottom-sheet xuất hiện, không phải modal`).
- Với case a11y/keyboard: `UI:` mô tả focus order, aria announcement, hoặc role thay vì chỉ "hiển thị".
- Case thuần frontend không đụng CSDL → ghi `DB-Check: N/A — frontend-only` và nêu lý do trong `note`.

**Ảnh màn hình (cột G `Ảnh màn hình`):**

Áp dụng đầy đủ pipeline cắt ảnh wireframe SRS → PNG → field `image_path` chuẩn từ `qc-testcase.md` (xem section "Cắt ảnh wireframe SRS để gắn vào cột G"). xlsx-utils tự widen col G + resize ảnh 270×98px để không đè qua H/I/J/K/L/M.

Web-specific hint cho `image_path`:
- **Cross-browser case** (Edge/Firefox/Safari): gắn cùng ảnh wireframe baseline (Chrome desktop) — divergent visual chỉ diễn tả qua dòng `UI [<browser>]:` trong `expected`. Không tạo ảnh per-browser trừ khi UX đã có Figma cho variant.
- **Responsive case** (mobile 375 / tablet 768 / desktop 1280): nếu SRS có wireframe responsive riêng (vd 2 SVG cho desktop + mobile) → tạo 2 ảnh `wireframe-2.2.x-desktop.png` + `wireframe-2.2.x-mobile.png`, gắn ảnh tương ứng với breakpoint case test.
- **Form validation case**: gắn ảnh form ở trạng thái có error inline để tester biết vị trí dự kiến của thông báo lỗi.
- **A11y / keyboard / contrast case**: thường KHÔNG cần ảnh (assertion qua axe-core hoặc contrast tool); để `image_path: ""`.
- **CSP / security header case**: KHÔNG cần ảnh; để `image_path: ""`.

Output via `xlsx-utils.py write-testcase` like `qc-testcase`.

## Memory Integration

**Read on activation:**
- `project-profile.md` — supported browser matrix, supported breakpoints, locale scope, a11y target (WCAG AA? AAA?).
- `qa-conventions.md` — does the team have a standard a11y checklist?
- `common-edge-cases.md` — web edges this team encounters.
- `defect-history.md` — past web-specific bugs.

**Write at end:**
- New web edges (e.g. "this team's lazy-load always breaks in Safari") → curate.
- Daily log: `- {time} [WC] Web cases for <feature>: <count>, <browsers>`.

## After the Session

If a11y findings recur, suggest pulling in a dedicated a11y review pattern. If responsive breakpoint coverage trims consistently, narrow the default matrix.
