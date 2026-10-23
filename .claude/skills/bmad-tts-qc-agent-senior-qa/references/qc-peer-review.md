---
name: qc-peer-review
description: Mentor-toned review of a junior tester's test cases — teaching feedback, line-by-line annotations
code: PR
---

# Peer Review (Mentor Tone)

## What Success Looks Like

Given a junior tester's test case set, the owner ends with an HTML report at `{output_folder}/test-artifacts/peer-reviews/<date>.html` that walks through the cases line-by-line with **constructive, teaching annotations**. Tone is warm and explanatory — not just "this is wrong", but "this is risky because X, here's how to make it stronger". The report celebrates strengths as much as it flags gaps.

This is different from `qc-review` (neutral) and `qc-critique` (sharp). This capability exists to develop other testers, not just gate ship-readiness.

## Your Approach

**Step 1 — Gather inputs.**

- Junior's test case set (Markdown or `.xlsx` path).
- Optional: junior's name (for personalized greeting in the report).
- Optional: focus areas — "go gentle, this is their first review" or "they want sharp feedback".

**Step 2 — Read carefully.**

Read every case. Do NOT skim. The point of mentor review is *finding teachable moments* — those hide in details.

For each case:
- Identify what's working (specific, concrete strengths).
- Identify gaps and ambiguities (with reason).
- Suggest the specific fix in clear language.

**Step 3 — Generate HTML.**

Self-contained HTML at `{output_folder}/test-artifacts/peer-reviews/{YYYY-MM-DD}.html`.

```html
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>QC Peer Review — {feature} — {date}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 1100px; margin: 2rem auto; padding: 0 1rem; line-height: 1.6; }
  h1 { border-bottom: 3px solid #1976d2; padding-bottom: .5rem; }
  .greeting { background: #e3f2fd; padding: 1rem 1.25rem; border-radius: 4px; border-left: 4px solid #1976d2; }
  .case { margin: 2rem 0; padding: 1.25rem; background: #fafafa; border-radius: 4px; border-left: 4px solid #ccc; }
  .case h3 { margin-top: 0; color: #333; }
  .strength { color: #2e7d32; }
  .gap { color: #c62828; }
  .suggestion { background: #fff8e1; padding: .75rem; border-left: 4px solid #fbc02d; margin: .75rem 0; border-radius: 4px; }
  .summary-card { background: #f5f5f5; padding: 1.25rem; border-radius: 4px; margin: 2rem 0; }
  .summary-card h2 { margin-top: 0; }
  pre { background: #fff; border: 1px solid #ddd; padding: .75rem; border-radius: 3px; overflow-x: auto; }
</style>
</head>
<body>
<h1>Peer Review: {feature_name}</h1>

<div class="greeting">
  <p>Chào {junior_name},</p>
  <p>Mình đã đọc set test case của bạn cho <strong>{feature_name}</strong>. Đây là feedback chi tiết, mục đích là giúp bạn xây dựng test case ngày càng vững. Có chỗ mình bảo "nên cải thiện" nhưng cũng có rất nhiều chỗ bạn đã làm tốt — đừng bỏ qua những phần đó. Đọc từ đầu đến cuối, hỏi mình bất kỳ chỗ nào chưa rõ.</p>
</div>

<h2>Tổng quan</h2>
<p><strong>{N} test cases reviewed.</strong> Strengths: {summary_strength}. Areas to grow: {summary_growth}.</p>

<!-- Per-case section -->
<div class="case">
  <h3>{case_id}: {case_purpose}</h3>
  <pre>{full case content excerpt}</pre>
  <p class="strength"><strong>✓ Điểm mạnh:</strong> {what works}</p>
  <p class="gap"><strong>⚠ Có thể chặt hơn:</strong> {what's vague or missing}</p>
  <div class="suggestion">
    <strong>💡 Gợi ý:</strong> {specific suggestion with rewritten example}
  </div>
</div>

<!-- Summary at the end -->
<div class="summary-card">
  <h2>Tóm tắt — những điểm bạn đang làm tốt</h2>
  <ul>
    <li>{positive pattern noticed across cases}</li>
    <li>{...}</li>
  </ul>

  <h2>Tóm tắt — 3 điều cần luyện thêm</h2>
  <ol>
    <li><strong>{principle}:</strong> {explanation, không chỉ là "fix this" mà là "tại sao điều này quan trọng"}</li>
    <li><strong>{principle}:</strong> {explanation}</li>
    <li><strong>{principle}:</strong> {explanation}</li>
  </ol>

  <h2>Bước tiếp theo</h2>
  <p>{recommendation: rewrite top-3 cases with these patterns? pair-review next time? read a specific guide?}</p>
</div>

<footer>Reviewed by Senior QA. Bất kỳ phản hồi nào về cách review này, ping {user_name}.</footer>
</body>
</html>
```

**Mentor tone discipline:**

- **Strengths first** — start every per-case block with what's working. This is non-negotiable; mentor review without strengths is critique.
- **Explain the why** — never just "this is wrong". Always "this is risky because <concrete consequence>; here's a stronger version".
- **Show the rewrite** — if you flag a vague expected, show the sharper version.
- **Don't over-correct** — if the junior's style is consistent and clear (just different from yours), don't flatten their voice. Mention what makes their style work.
- **End with growth path** — a peer review without "what to practice next" leaves the junior with a list of corrections, not a learning path.

**Top 3 patterns** at the end is the most important section — it abstracts findings into principles the junior can apply across all future work.

## Memory Integration

**Read on activation:**
- `qa-conventions.md` — what standards to teach.
- `business-rules.md`, `common-edge-cases.md` — to identify missing items.

**Write at end:**
- Daily log: `- {time} [PR] Peer review for <junior> on <feature>: N cases, <K> strengths / <M> gaps`.

## After the Session

If the same junior is reviewed multiple times, track which patterns they're improving on (don't keep flagging fixed weaknesses) — adapt feedback over time. Note in BOND.md if this is recurring.
