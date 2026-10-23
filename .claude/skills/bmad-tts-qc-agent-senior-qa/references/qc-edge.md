---
name: qc-edge
description: Hard / rare edge cases that testers commonly miss
code: EG
---

# Edge Cases

## What Success Looks Like

The owner ends with 8-15 edge cases for a feature, each non-obvious and concrete. The list contains at least 2 cases the owner wouldn't have written from a standard scenario sweep. Repeats from `common-edge-cases.md` are OK if relevant — but flag which are recurring vs novel.

## Your Approach

Output a Markdown list grouped by category:

```markdown
### Boundary
- <edge case> — _<why it matters>_

### Concurrency / timing
- <edge case>

### State corruption / partial state
- <edge case>

### External / environmental
- <edge case>

### Adversarial / abuse
- <edge case>

### Internationalization / locale
- <edge case>

### Accessibility
- <edge case>
```

Skip categories with no plausible edge for this feature.

**Generation lenses** (run through them all, take the live ones):

- **Boundary**: min-1, min, min+1, max-1, max, max+1, zero, negative, empty string, single character, max-length string, exact-multiple-of-page-size.
- **Time**: 23:59:59 → 00:00:00 transition, DST shift (Vietnam doesn't have DST but server might be UTC), timezone with non-Vietnam timezone, leap second, leap year Feb 29.
- **Concurrency**: same user two devices simultaneously, race between OTP send and OTP expiration, double-tap send button, two refunds for one transaction.
- **State**: app killed mid-flow, network drop mid-request, app foregrounded after 24h backgrounded, cookie expired mid-session, token refresh during request.
- **Environment**: low memory, slow 3G, airplane mode toggling, Wi-Fi vs cellular, battery saver mode, dark mode toggled mid-session.
- **Adversarial**: SQL injection in input fields, XSS in display fields, IDOR (changing IDs in URL), oversized payload, malformed JSON, replay attack on idempotent calls.
- **Locale**: Vietnamese diacritics, RTL languages, very long German compound words, decimal comma vs period, currency formatting, BCP-47 unusual locales.
- **Accessibility**: screen reader navigation, keyboard-only flow, font scaling 200%, high-contrast mode, reduced motion preference.

For each edge surfaced, the **why it matters** must be concrete (1 sentence), not generic.

## Memory Integration

**Read on activation:**
- `common-edge-cases.md` — incorporate team's recurring edges, flag duplicates.
- `defect-history.md` — past bug clusters in this area suggest where new edges hide.
- `project-profile.md` — platform mix dictates which categories are relevant (no a11y depth needed for backend service).

**Write at end:**
- New edges that recurred during the session → append candidates to `common-edge-cases.md` (mark as "tentative" until {user_name} confirms).
- Daily log: `- {time} [EG] N edges for <feature>`.

## After the Session

Note which edges {user_name} kept vs dropped — calibration. If the same category keeps getting trimmed (e.g. "we don't ship to RTL languages, skip those"), update `project-profile.md` to permanently exclude that category for this team.
