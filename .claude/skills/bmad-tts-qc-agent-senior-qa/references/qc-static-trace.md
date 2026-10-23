---
name: qc-static-trace
description: Static (non-executing) simulation of test case execution against source code, with HTML report
code: SX
---

# Static Test Trace

## What Success Looks Like

Given a test case + a path to the source code that implements the feature, the owner ends with an HTML report at `{output_folder}/test-artifacts/static-traces/<feature>.html` that simulates the test case step-by-step against the code. Each step gets a predicted pass / fail / unclear verdict, with a code reference (`file:line` link to the project source) and reasoning.

This capability does NOT run code. It uses LLM reasoning over code reads. It catches bugs **before the code is run** — the inverse of traditional testing. The most valuable output is a `unclear` verdict on a step the test author didn't write a clear-enough expectation for.

## Your Approach

**Step 1 — Gather inputs.**

- The test case (single case, copied or fetched from `.xlsx`).
- A path or paths to the source code area being tested. Can be a directory; agent navigates with Read / Glob / Grep as needed.

**Step 2 — Trace each step.**

For step `N`:
1. Identify the code path the step would exercise. Use Grep on entry points (button handlers, API endpoints, state mutations) named near the step description.
2. Read the relevant file(s).
3. Reason: given the test case's `data` and prior state, what would each line of code do?
4. Compare predicted outcome to the test case's `expected`.
5. Record verdict (✅ pass / ❌ fail / ⚠️ unclear) + code reference.

**Step 3 — Generate HTML report.**

Self-contained HTML at `{output_folder}/test-artifacts/static-traces/<feature>.html`. Inline CSS, no JS dependency.

```html
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<title>QC Static Trace — {feature}</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; max-width: 1200px; margin: 2rem auto; padding: 0 1rem; }
  h1 { border-bottom: 3px solid #1976d2; padding-bottom: .5rem; }
  .step { margin: 1rem 0; padding: 1rem; border-left: 4px solid #ccc; background: #fafafa; border-radius: 4px; }
  .step-pass { border-color: #2e7d32; background: #e8f5e9; }
  .step-fail { border-color: #c62828; background: #ffebee; }
  .step-unclear { border-color: #ef6c00; background: #fff3e0; }
  .verdict { font-weight: 600; text-transform: uppercase; letter-spacing: .5px; }
  .ref { font-family: ui-monospace, SFMono-Regular, monospace; background: #fff; padding: 2px 6px; border-radius: 3px; border: 1px solid #ddd; }
  details { margin: .5rem 0; }
  summary { cursor: pointer; color: #1976d2; }
  pre { background: #1a1a1a; color: #f0f0f0; padding: 1rem; border-radius: 4px; overflow-x: auto; }
</style>
</head>
<body>
<h1>Static Trace: {test_case_id} — {test_case_purpose}</h1>
<p><strong>Source area:</strong> <span class="ref">{source_path}</span></p>
<p><strong>Verdict overall:</strong> {overall_verdict}</p>

<div class="step step-{class1}">
  <div class="verdict">Step 1 — ✅ Pass (predicted)</div>
  <p><strong>Action:</strong> Tap "Send OTP" button</p>
  <p><strong>Code reference:</strong> <a class="ref" href="file://{path}/src/login/SendOtpButton.tsx#L23">src/login/SendOtpButton.tsx:23</a></p>
  <p><strong>Reasoning:</strong> Handler `onSendOtp` validates accountId is non-empty (line 25), calls `api.sendOtp()` (line 30), shows toast on success (line 35). Test data "1234567890" passes validation; expected "OTP sent toast" matches behavior.</p>
  <details><summary>Code excerpt</summary>
  <pre>const onSendOtp = async () => {
    if (!accountId) return;
    const r = await api.sendOtp(accountId);
    if (r.ok) toast.show('OTP đã gửi');
  };</pre>
  </details>
</div>

<div class="step step-fail">
  <div class="verdict">Step 2 — ❌ Fail (predicted)</div>
  <p><strong>Issue:</strong> Code path on line 27 does NOT clear the OTP input field on resend, but test expects empty field. Likely bug.</p>
  <p><strong>Code reference:</strong> <a class="ref" href="...">src/login/OtpInput.tsx:27</a></p>
</div>

<div class="step step-unclear">
  <div class="verdict">Step 3 — ⚠️ Unclear (predicted)</div>
  <p><strong>Issue:</strong> Test expected says "shows error message" but doesn't specify which error. Code shows two distinct errors depending on response code (401 vs 429). Recommend tightening the test case's expected field.</p>
</div>

<h2>Recommendations</h2>
<ul>
  <li>Fix predicted bug at <span class="ref">OtpInput.tsx:27</span>: clear input on resend.</li>
  <li>Tighten test case expected for Step 3.</li>
</ul>
</body>
</html>
```

**Step 4 — Confirm.**

Output the HTML path + a one-line summary: "<feature>: 5 steps traced — 3 pass predicted, 1 fail predicted (likely bug at <ref>), 1 unclear (test ambiguity)."

**Style discipline:**
- "Predicted" — never claim certainty. The trace is reasoning, not execution.
- Cite specific lines — `file:line` makes findings actionable.
- Distinguish "bug" findings from "test ambiguity" findings — both are valuable but route differently (bug → file `/qc-bug`; ambiguity → file `/qc-improve` on the test case).

## Memory Integration

**Read on activation:**
- `project-profile.md` — language, framework conventions for navigating code.
- `defect-history.md` — past bugs in this code area sharpen prediction.

**Write at end:**
- If a predicted bug is later confirmed (after the dev runs the actual test), append to `defect-history.md` with note "found via static trace before code was run".
- Daily log: `- {time} [SX] Static trace: <case> over <source>: <verdict counts>`.

## After the Session

Track prediction accuracy. If predicted bugs consistently turn out to be true positives, this capability becomes the team's earliest catch. If false positive rate is high, calibrate the reasoning style ("be more conservative on async control flow").
