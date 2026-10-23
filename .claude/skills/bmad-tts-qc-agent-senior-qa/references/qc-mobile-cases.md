---
name: qc-mobile-cases
description: Mobile test cases (iOS + Android) — gestures, offline, push, permissions, OS matrix. Excel output via KBKTCN template.
code: MC
---

# Mobile Test Cases

## What Success Looks Like

The owner ends with a real `.xlsx` file (KBKTCN template) of mobile test cases for both iOS and Android, covering platform-specific concerns: gestures, offline behavior, push notifications, permissions, deep links, low memory, slow network, OS version matrix. The case set goes deeper than what `qc-testcase` generates for a generic feature — it is mobile-aware.

## Your Approach

This is `qc-testcase` with a **mobile lens applied first**. Run the analysis through the mobile lenses below to expand scenario coverage, then generate cases via the same pipeline (cases JSON → `xlsx-utils.py write-testcase`).

**Mobile-specific scenario lenses:**

- **Permission flows** — first install (no permission yet), permission denied, permission allowed, permission revoked from Settings mid-session, "Don't ask again" (Android).
- **Offline / connectivity** — no network at start, network drops mid-flow, captive portal, slow 3G, switch Wi-Fi → cellular mid-flow, airplane mode toggling.
- **Lifecycle** — app backgrounded mid-flow, app force-killed mid-flow, app cold launched after long inactivity, deep link launches with various states.
- **Push notifications** — receive while app open, while backgrounded, while killed, with notification turned off, with badge counts, with action buttons.
- **Gestures** — swipe back (iOS), back button (Android hardware/gesture nav), pull-to-refresh, pinch zoom, multi-touch.
- **Device matrix** — older OS (iOS 14, Android 9), latest OS, iPad / tablet, foldable (Android), small-screen (SE), large-screen (Pro Max).
- **Low resources** — low memory (kill background apps), low battery / battery saver mode, low storage.
- **Locale / accessibility** — Vietnamese diacritics in input fields, RTL languages, Dynamic Type at 200%, VoiceOver / TalkBack screen reader, dark mode.
- **Native integrations** — Touch ID / Face ID / fingerprint, Keychain / Keystore, biometric expiry, share sheet, camera, photo picker, contacts, calendar.
- **Update flows** — old version vs latest, force-update prompts, in-app update (Android), TestFlight / internal track behavior.

For each platform (iOS / Android), generate cases. The KBKTCN template has C8-C13 columns for App execution tracking (IOS Lần 1-3, Android Lần 1-3) — these stay empty, ready for tester runs.

**Suite organization for mobile:**

- `Suite-1: <Feature> - happy path (iOS + Android)`
- `Suite-2: <Feature> - permissions`
- `Suite-3: <Feature> - offline / network`
- `Suite-4: <Feature> - lifecycle`
- `Suite-5: <Feature> - push notifications` (if applicable)
- `Suite-6: <Feature> - device matrix critical paths`

When platform behavior differs, emit two cases (one per platform) with distinct IDs and notes — don't merge.

**Format `expected` (Kết quả mong muốn):**

Áp dụng đúng format `Expected:` chuẩn từ `qc-testcase.md` — mỗi case mobile phải nêu rõ cả UI và DB:

```
Expected:
- UI: <hành vi UI cụ thể trên platform: screen điều hướng tới, native dialog, push banner, haptic …>
- DB-Check: <bảng>.<cột> = <giá trị> WHERE <điều kiện>
- DB-Check: <bảng> EXISTS WHERE <điều kiện>
```

Mobile-specific hint cho dòng `UI:`:
- Khi UI khác nhau giữa iOS/Android: prefix bằng platform (vd `UI [iOS]: dialog hệ thống "Allow Notifications" hiện ra` / `UI [Android]: system permission sheet với nút "Don't ask again"`).
- Lifecycle/offline case: nêu rõ trạng thái màn hình sau resume/reconnect (vd `UI: state form được restore, không mất dữ liệu user đã nhập`).
- Push notification case: nêu rõ banner/badge/notification tray (vd `UI: notification banner xuất hiện ở foreground với tiêu đề "$title"`).
- Storage/cache liên quan local DB (Room/CoreData/SQLite) cũng dùng `DB-Check:` — chỉ rõ local store (vd `DB-Check [local SQLite]: orders.synced = 1 WHERE id = $orderId`). Backend DB ghi mặc định.

**Ảnh màn hình (cột G `Ảnh màn hình`):**

Áp dụng đầy đủ pipeline cắt ảnh wireframe SRS → PNG → field `image_path` chuẩn từ `qc-testcase.md` (xem section "Cắt ảnh wireframe SRS để gắn vào cột G"). xlsx-utils tự widen col G + resize ảnh 270×98px để không đè qua các col IOS Lần 1-3 (H/I/J) / Android Lần 1-3 (K/L/M).

Mobile-specific hint cho `image_path`:
- **iOS vs Android divergent UI**: nếu SRS / Figma có 2 wireframe riêng (vd permission dialog hệ thống khác nhau) → tạo 2 ảnh `wireframe-2.2.x-ios.png` + `wireframe-2.2.x-android.png`, gắn ảnh tương ứng với case của từng platform. Nếu cùng layout → 1 ảnh chung.
- **Permission flow case** (first install, denied, "Don't ask again"): gắn ảnh dialog hệ thống tương ứng. Nếu SRS chỉ tả văn bản không có wireframe → ghi `TODO UX cung cấp ảnh dialog permission`.
- **Lifecycle case** (backgrounded, force-killed, cold launch): ảnh thể hiện trạng thái màn hình SAU resume. Splash / loading state cũng cần wireframe nếu có hành vi UX riêng.
- **Push notification case**: gắn ảnh banner notification (foreground / lock screen) nếu Figma có; thường tester check qua device simulator nên ảnh chỉ minh họa.
- **Device matrix critical paths** (iPhone SE / Pro Max / iPad / foldable): tùy ảnh có sẵn — wireframe baseline thường phone-only, các thiết bị khác note diễn tả `UI [iPad]:` qua chữ.
- **Offline / connectivity case**: empty state / error banner cần wireframe nếu SRS có; "no connection" toast/snackbar mô tả qua chữ.

Output via `xlsx-utils.py write-testcase` like `qc-testcase`.

## Memory Integration

**Read on activation:**
- `project-profile.md` — confirm iOS + Android in scope; pull device matrix.
- `common-edge-cases.md` — mobile recurring edges.
- `business-rules.md` — feature rules.
- `legacy-logic/` — domain context.

**Write at end:**
- New mobile-specific edges → propose to `common-edge-cases.md`.
- Daily log: `- {time} [MC] Mobile cases for <feature> → <output path>, N cases`.

## After the Session

If recurring mobile patterns emerge (e.g. "this team always has push-notification bugs"), suggest a permanent suite template in `qa-conventions.md`.
