---
name: qc-miniapp-cases
description: MiniApp test cases (Zalo / WeChat / generic) — lifecycle, sandbox, sharing, deep links. Excel output.
code: MA
---

# MiniApp Test Cases

## What Success Looks Like

The owner ends with a real `.xlsx` file of test cases tailored to the MiniApp platforms in scope (default: Zalo + WeChat per `qc_codegen_miniapp_platforms` config). MiniApps differ from native apps: they run inside a host app's sandbox, have a constrained API surface, and behave differently for lifecycle, sharing, and deep links. This case set captures those constraints.

## Your Approach

**Determine target platforms** from config or input — Zalo MiniApp, WeChat MiniApp, generic, or multiple. Generate cases per platform (or platform-agnostic where behavior is shared).

**MiniApp-specific scenario lenses:**

- **Lifecycle** — onLaunch (first start), onShow (after backgrounded), onHide, onError, onPageNotFound. Behavior under host-app suspend / resume / kill.
- **Sandbox limits** — file size limits, storage quota, network domain whitelist, restricted APIs (no clipboard read on some platforms?).
- **Sharing** — share to chat, share to feed, share with custom path, share thumbnail rendering, deep-back from a shared link with state restoration.
- **Deep links / scheme URLs** — direct entry into a sub-page from outside the app (QR code, URL scheme), back stack handling.
- **Authentication** — host-app login pass-through (Zalo / WeChat session), permission scope (`scope.userInfo`, `scope.userLocation`), expired session.
- **Performance** — first-paint time, package size limits (1MB main / 8MB total for WeChat MA), subpackage loading.
- **Capability availability** — feature works on lower API versions of host? graceful degradation when API not supported?
- **Host-specific quirks**:
  - **Zalo MiniApp**: Zalo OA integration, Zalo Pay if applicable, share to Zalo group/page.
  - **WeChat MiniApp**: official account binding, WeChat Pay, mp-html rendering quirks.
  - **Generic**: assume least-common-denominator API.

**Suite organization:**

- `Suite-1: <Feature> - happy path (per platform)`
- `Suite-2: <Feature> - sandbox / API constraints`
- `Suite-3: <Feature> - lifecycle / state`
- `Suite-4: <Feature> - sharing flows`
- `Suite-5: <Feature> - host integration (auth / pay)`
- `Suite-6: <Feature> - performance / size`

When generating cases for multiple platforms, prefix the case purpose with platform: `[Zalo] ...`, `[WeChat] ...`, `[All platforms] ...`. When behavior diverges, separate cases per platform.

**Format `expected` (Kết quả mong muốn):**

Áp dụng đúng format `Expected:` chuẩn từ `qc-testcase.md` — mỗi case MiniApp phải nêu rõ cả UI và DB:

```
Expected:
- UI: <hành vi UI cụ thể trong host app: navigateTo page, toast, host-app share sheet, auth prompt …>
- DB-Check: <bảng>.<cột> = <giá trị> WHERE <điều kiện>
- DB-Check: <bảng> EXISTS WHERE <điều kiện>
```

MiniApp-specific hint cho dòng `UI:`:
- Khi UI khác nhau giữa Zalo / WeChat / generic host: prefix bằng platform (vd `UI [Zalo]: share sheet Zalo mở với title "$title"` / `UI [WeChat]: wx.showToast hiển thị "$msg" duration 2000ms`).
- Lifecycle case (`onShow` / `onHide` / `onLaunch`): nêu rõ page hiện ra và state restored (vd `UI: page /pages/order/detail mở lại với orderId từ query string`).
- Sandbox/storage: dùng `DB-Check:` cho cả local storage của host (vd `DB-Check [wx.storage]: token EXISTS với key = "auth_token"`) lẫn backend DB.
- Case thuần host integration (share, auth pass-through) mà không đụng backend → ghi `DB-Check: N/A — host-only` và giải thích trong `note`.

**Ảnh màn hình (cột G `Ảnh màn hình`):**

Áp dụng đầy đủ pipeline cắt ảnh wireframe SRS → PNG → field `image_path` chuẩn từ `qc-testcase.md` (xem section "Cắt ảnh wireframe SRS để gắn vào cột G"). xlsx-utils tự widen col G + resize ảnh 270×98px để không đè qua col khác.

MiniApp-specific hint cho `image_path`:
- **Zalo vs WeChat divergent UI** (share sheet, auth screen, payment): nếu SRS có 2 wireframe riêng → tạo 2 ảnh `wireframe-2.2.x-zalo.png` + `wireframe-2.2.x-wechat.png`. Nếu cùng layout (most case) → 1 ảnh chung tag `multi-platform`.
- **Sandbox / API constraints case** (file size limit, storage quota, restricted API): thường thiếu wireframe vì error chỉ là toast `wx.showToast` / `zmp-ui.showSnackbar` — ghi `image_path: ""` + note `UI assertion qua toast text trong $msg`.
- **Lifecycle case** (`onShow` / `onHide` / `onLaunch`): gắn ảnh page hiện ra sau lifecycle event nếu có; nếu chỉ là state restore in-place → wireframe baseline của page đó.
- **Sharing flow case** (share to chat, share to feed): gắn ảnh host-app share sheet — Zalo / WeChat có sheet riêng, ảnh khác nhau.
- **Host integration case** (auth pass-through, host payment): wireframe host-app login/payment screen — UX thường KHÔNG vẽ chi tiết vì là host UI, set `image_path: ""` + note `UI host-app, không thuộc miniapp scope`.
- **Capability degradation case** (API not supported on lower host version): gắn ảnh fallback UI nếu SRS có.

Output via `xlsx-utils.py write-testcase` like `qc-testcase`. Sheet name should include platform if single-platform: `<feature>-zalo`. Multi-platform sets can use a single sheet with platform-tagged rows.

## Memory Integration

**Read on activation:**
- `project-profile.md` — which miniapp platforms are in scope, host-app versions.
- `legacy-logic/` — past miniapp domain knowledge.
- `defect-history.md` — past miniapp-specific bugs.
- `common-edge-cases.md` — miniapp edges.

**Write at end:**
- Platform-specific patterns (e.g. "WeChat always has issues with image upload size") → propose `legacy-logic/wechat-miniapp.md` or `common-edge-cases.md` entry.
- Daily log: `- {time} [MA] MiniApp cases for <feature> on <platforms>: <count>`.

## After the Session

If multiple bugs in `defect-history.md` cluster around one miniapp behavior (e.g. "Zalo onShow lifecycle is unreliable"), surface that as a standing edge for future case generation.
