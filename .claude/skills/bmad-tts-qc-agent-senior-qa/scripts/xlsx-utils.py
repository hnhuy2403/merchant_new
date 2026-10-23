#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl>=3.1", "pillow>=10.0"]
# ///
"""
Excel utilities for the qc module — clone KBKTCN test case template,
write Suite-grouped test cases starting at row 15, preserve COUNTIF
formulas in R7-R11, read existing test cases back as JSON.

Subcommands:
    inspect TEMPLATE_PATH
        Print sheet names, dimensions, and the test case header layout.

    read-cases XLSX_PATH [--sheet SHEET_NAME]
        Emit existing test case rows as JSON (one record per row from R15+).

    write-testcase --template TEMPLATE --output OUTPUT --feature FEATURE
                    --id-prefix PREFIX --cases-json CASES_JSON [--sheet-name NAME]
        Clone the `template` sheet (or first non-cover sheet), rename to
        --sheet-name (default: --feature), fill R3 with --feature, fill R4
        with --id-prefix, then write rows starting R15 from CASES_JSON.

CASES_JSON schema (list of objects):
    [
      {
        "suite": "Suite-1: Login UI validations",
        "id": "AR-001",
        "purpose": "Verify accountId field accepts only digits",
        "case": "Input alphabet into accountId",
        "data": "abcXYZ",
        "steps": "1. Open Login\\n2. Type abcXYZ into accountId\\n3. Tap Continue",
        "expected": "Field rejects, error 'AccountId chỉ chấp nhận chữ số' shows",
        "priority": "P1",
        "screenshot": "",
        "note": ""
      },
      ...
    ]

Suite headers (rows where only `suite` is set, no `id`) are emitted as a
suite-divider row at column 2 with the suite label, matching the
'Suite-1: ...' style of the KBKTCN sample.
"""

import argparse
import json
import sys
from copy import copy
from pathlib import Path

try:
    import openpyxl
    from openpyxl.utils import get_column_letter
    from openpyxl.styles import PatternFill, Alignment
    from openpyxl.drawing.image import Image as XlsxImage
except ImportError:
    print(json.dumps({"error": "openpyxl is required. The script declares it via PEP 723 — run with `uv run scripts/xlsx-utils.py ...` to install automatically."}), file=sys.stderr)
    sys.exit(2)


# Match the KBKTCN sample's Suite-1 row fill (light pastel green).
# Applied across cols A..P (1..16) of each suite divider row.
SUITE_FILL_COLOR = "FFCCFFCC"
SUITE_FILL_COL_END = 16  # cols 1..16 get the green fill; col 17 (Q = Ghi chú) intentionally skipped to match sample
# Embedded screenshot sizing for `image_path` field on case rows.
# Shrunk 25% so the image fits inside col G (Ảnh màn hình) without bleeding
# over the IOS run-slots H/I/J or Android K/L/M. Col G is widened to match.
IMAGE_CELL_WIDTH_PX = 270   # 25% smaller than the previous 360px
IMAGE_CELL_HEIGHT_PX = 98   # kept proportional to the original 360x130 aspect
IMAGE_ROW_HEIGHT_PT = 80    # ~ matches IMAGE_CELL_HEIGHT_PX (1pt ≈ 1.333px)
# Excel column-width unit ≈ 7 px in Calibri 11. 38 units ≈ 266 px — small
# margin around the 270px image so anchored screenshots don't cross into H.
IMAGE_COL_WIDTH_UNITS = 38

# Column widths for data cells (1 unit ≈ 7 px Calibri 11). Tuned so wrapped
# Vietnamese text in steps/expected reads without horizontal scrolling.
# Vietnamese chars (Calibri 11) wider than ASCII (~1.15x) → widths bumped
# accordingly so 6-10 line steps + multi-section Expected don't clip.
# Col 7 (Screenshot) handled separately via IMAGE_COL_WIDTH_UNITS.
CASE_COL_WIDTHS = {
    1: 10,    # A - ID
    2: 14,    # B - Mức độ ưu tiên (P0/P1/P2 — narrow)
    3: 32,    # C - Mục đích kiểm thử
    4: 38,    # D - Trường hợp kiểm thử
    5: 36,    # E - Data test
    6: 56,    # F - Các bước thực hiện
    7: 64,    # G - Kết quả mong muốn
    9: 6, 10: 6, 11: 6,    # I/J/K - IOS Lần 1/2/3
    12: 6, 13: 6, 14: 6,   # L/M/N - Android Lần 1/2/3
    15: 8,    # O - Kết quả (M)
    16: 14,   # P - Mã lỗi
    17: 32,   # Q - Ghi chú
}
# Row-height heuristic constants (Excel point, 1pt ≈ 1.333 px Calibri 11).
# Bumped per-line height + cap to fit dense Vietnamese cases without clipping
# (some Suite-2 validate cases have 9 steps + 6-line Expected = 30+ wrapped lines).
ROW_HEIGHT_PER_LINE_PT = 18
ROW_HEIGHT_MIN_PT = 45
ROW_HEIGHT_MAX_PT = 520
# Effective char-per-width-unit factor for wrap estimation. Vietnamese chars
# average ~0.87 chars per Calibri 11 width unit → divide line length by
# (col_width * 0.87) to get accurate line count.
WRAP_CHAR_FACTOR = 0.87


# Column indices in the KBKTCN template (1-based, matching openpyxl)
# Template v2 (2026-05-27 — added Priority col B sau ID):
#   R13: A=ID, B=Mức độ ưu tiên, C=Mục đích kiểm thử, D=Trường hợp kiểm thử,
#        E=Data test, F=Các bước thực hiện, G=Kết quả mong muốn,
#        H=Ảnh màn hình, I13:K13=IOS (merged), L13:N13=Android (merged),
#        O=Kết quả (M), P=Mã lỗi, Q=Ghi chú
#   R14: I=Lần 1, J=Lần 2, K=Lần 3 (IOS); L=Lần 1, M=Lần 2, N=Lần 3 (Android)
COL_ID = 1
COL_PRIORITY = 2
COL_PURPOSE = 3
COL_CASE = 4
COL_DATA = 5
COL_STEPS = 6
COL_EXPECTED = 7
COL_SCREENSHOT = 8
# Run-result columns — IOS (I/J/K) Lần 1/2/3, Android (L/M/N) Lần 1/2/3.
# Per Yennth72's convention, web Playwright runs go into the Lần-1 columns
# generically (I for run-1, J for run-2, K for run-3) even though the
# label says "IOS" — the team uses I/J/K as generic run slots.
COL_RUN_1 = 9    # I — Lần 1 (default write target for update-results)
COL_RUN_2 = 10   # J — Lần 2
COL_RUN_3 = 11   # K — Lần 3
COL_RESULT = 15   # O — formula cell, auto-computes P/F from I..N. DO NOT overwrite.
COL_DEFECT_ID = 16
COL_NOTE = 17

# Header rows
ROW_FEATURE_NAME = 3      # R3 C3 holds the feature name (column 3)
ROW_TEST_ID_PREFIX = 4    # R4 C3 holds the test ID prefix
ROW_HEADER_TOP = 13
ROW_HEADER_BOTTOM = 14
ROW_DATA_START = 15

# Suite divider rows: label đặt ở col Purpose (col 3) — sau ID + Priority, ngay dưới cột Mục đích
COL_SUITE_LABEL = 3


def find_template_sheet(wb: openpyxl.Workbook) -> str:
    """Return the name of the sheet to use as the testcase template.

    Prefers a sheet literally named 'template' (case-insensitive). Falls back
    to the first sheet that has the test case header structure (R13 col1='ID').
    """
    for name in wb.sheetnames:
        if name.strip().lower() == "template":
            return name
    # Fallback: first sheet whose R13 col1 == "ID"
    for name in wb.sheetnames:
        ws = wb[name]
        if ws.max_row >= ROW_HEADER_TOP:
            v = ws.cell(row=ROW_HEADER_TOP, column=COL_ID).value
            if v and str(v).strip().upper() == "ID":
                return name
    raise SystemExit("No template sheet found. Expected a sheet named 'template' "
                     "or a sheet with R13 col1='ID'.")


def cmd_inspect(args) -> int:
    """Print template structure as JSON."""
    template_path = Path(args.template_path)
    if not template_path.exists():
        print(json.dumps({"error": f"Template not found: {template_path}"}), file=sys.stderr)
        return 1

    wb = openpyxl.load_workbook(template_path, data_only=False)
    template_sheet = find_template_sheet(wb)
    ws = wb[template_sheet]

    # Read header rows (R13 + R14) to identify columns
    headers_top = {}
    headers_bottom = {}
    for c in range(1, ws.max_column + 1):
        v_top = ws.cell(row=ROW_HEADER_TOP, column=c).value
        v_bot = ws.cell(row=ROW_HEADER_BOTTOM, column=c).value
        if v_top is not None:
            headers_top[c] = str(v_top)
        if v_bot is not None:
            headers_bottom[c] = str(v_bot)

    result = {
        "path": str(template_path),
        "sheets": wb.sheetnames,
        "template_sheet": template_sheet,
        "dimensions": ws.dimensions,
        "max_row": ws.max_row,
        "max_column": ws.max_column,
        "header_row_top": headers_top,
        "header_row_bottom": headers_bottom,
        "expected_columns": {
            "ID": COL_ID,
            "Mức độ ưu tiên": COL_PRIORITY,
            "Mục đích kiểm thử": COL_PURPOSE,
            "Trường hợp kiểm thử": COL_CASE,
            "Data test": COL_DATA,
            "Các bước thực hiện": COL_STEPS,
            "Kết quả mong muốn": COL_EXPECTED,
            "Ảnh màn hình": COL_SCREENSHOT,
            "Kết quả (M)": COL_RESULT,
            "Mã lỗi": COL_DEFECT_ID,
            "Ghi chú": COL_NOTE,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_read_cases(args) -> int:
    """Read test case rows from an existing xlsx and emit as JSON."""
    xlsx_path = Path(args.xlsx_path)
    if not xlsx_path.exists():
        print(json.dumps({"error": f"File not found: {xlsx_path}"}), file=sys.stderr)
        return 1
    wb = openpyxl.load_workbook(xlsx_path, data_only=False)
    sheet_name = args.sheet or find_template_sheet(wb)
    ws = wb[sheet_name]

    cases = []
    current_suite = None
    for row in range(ROW_DATA_START, ws.max_row + 1):
        id_val = ws.cell(row=row, column=COL_ID).value
        suite_raw = ws.cell(row=row, column=COL_SUITE_LABEL).value
        suite_str = str(suite_raw).strip() if suite_raw else ""

        # Detect suite divider rows: col 2 starts with "Suite" and col 1 is empty.
        if suite_str.lower().startswith("suite") and id_val is None:
            current_suite = suite_str
            continue

        # Skip blank rows
        if id_val is None:
            continue

        cases.append({
            "row": row,
            "suite": current_suite,
            "id": str(id_val),
            "priority": str(ws.cell(row=row, column=COL_PRIORITY).value or ""),
            "purpose": str(ws.cell(row=row, column=COL_PURPOSE).value or ""),
            "case": str(ws.cell(row=row, column=COL_CASE).value or ""),
            "data": str(ws.cell(row=row, column=COL_DATA).value or ""),
            "steps": str(ws.cell(row=row, column=COL_STEPS).value or ""),
            "expected": str(ws.cell(row=row, column=COL_EXPECTED).value or ""),
            "result": str(ws.cell(row=row, column=COL_RESULT).value or ""),
            "defect_id": str(ws.cell(row=row, column=COL_DEFECT_ID).value or ""),
            "note": str(ws.cell(row=row, column=COL_NOTE).value or ""),
        })

    print(json.dumps({
        "path": str(xlsx_path),
        "sheet": sheet_name,
        "case_count": len(cases),
        "cases": cases,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_write_testcase(args) -> int:
    """Clone template sheet, fill feature/prefix/cases, save to output."""
    template_path = Path(args.template)
    output_path = Path(args.output)
    cases_json_path = Path(args.cases_json)

    for label, p in [("template", template_path), ("cases-json", cases_json_path)]:
        if not p.exists():
            print(json.dumps({"error": f"{label} not found: {p}"}), file=sys.stderr)
            return 1

    cases = json.loads(cases_json_path.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        print(json.dumps({"error": "cases-json must be a JSON array"}), file=sys.stderr)
        return 1

    wb = openpyxl.load_workbook(template_path, data_only=False)
    template_sheet_name = find_template_sheet(wb)
    new_sheet_name = (args.sheet_name or args.feature)[:31]  # Excel max sheet name 31 chars

    # Avoid duplicate sheet names
    if new_sheet_name in wb.sheetnames:
        i = 2
        while f"{new_sheet_name[:28]}_{i}" in wb.sheetnames:
            i += 1
        new_sheet_name = f"{new_sheet_name[:28]}_{i}"

    # Clone the template sheet — openpyxl supports copy_worksheet
    new_ws = wb.copy_worksheet(wb[template_sheet_name])
    new_ws.title = new_sheet_name

    # Fill R3 (feature name) and R4 (test ID prefix). Row 3 col 3, Row 4 col 3.
    new_ws.cell(row=ROW_FEATURE_NAME, column=3, value=args.feature)
    new_ws.cell(row=ROW_TEST_ID_PREFIX, column=3, value=args.id_prefix)

    # Clear existing data rows from R15 onwards (template may have sample rows)
    # Only clear cells in the data range — leave formulas and merges alone.
    for row in range(ROW_DATA_START, new_ws.max_row + 1):
        for col in range(1, new_ws.max_column + 1):
            cell = new_ws.cell(row=row, column=col)
            # Don't touch cells with formulas (defensive — shouldn't be any in data area)
            if cell.value is not None and not (isinstance(cell.value, str) and cell.value.startswith("=")):
                cell.value = None

    # Image paths in cases JSON resolve relative to the cases-json file's dir.
    cases_json_dir = cases_json_path.parent.resolve()
    suite_fill = PatternFill(patternType="solid", fgColor=SUITE_FILL_COLOR)
    wrap_alignment = Alignment(wrap_text=True, vertical="top", horizontal="left")
    embedded_image_count = 0

    # Widen data columns so wrapped text reads without horizontal scroll.
    for col_idx, w in CASE_COL_WIDTHS.items():
        new_ws.column_dimensions[get_column_letter(col_idx)].width = w
    # If any case embeds a screenshot, widen col G (Ảnh màn hình) so the image
    # doesn't bleed over IOS (H/I/J) or Android (K/L/M) run-result columns.
    if any(c.get("image_path") for c in cases):
        new_ws.column_dimensions[get_column_letter(COL_SCREENSHOT)].width = IMAGE_COL_WIDTH_UNITS

    # Write cases starting at R15
    current_row = ROW_DATA_START
    current_suite = None
    for case in cases:
        suite = case.get("suite")
        if suite and suite != current_suite:
            # Write a suite divider row at column 2; tô màu xanh lá cols 1..15
            new_ws.cell(row=current_row, column=COL_SUITE_LABEL, value=suite)
            for c in range(1, SUITE_FILL_COL_END + 1):
                new_ws.cell(row=current_row, column=c).fill = suite_fill
            current_suite = suite
            current_row += 1

        new_ws.cell(row=current_row, column=COL_ID, value=case.get("id", ""))
        new_ws.cell(row=current_row, column=COL_PRIORITY, value=case.get("priority", ""))
        new_ws.cell(row=current_row, column=COL_PURPOSE, value=case.get("purpose", ""))
        new_ws.cell(row=current_row, column=COL_CASE, value=case.get("case", ""))
        new_ws.cell(row=current_row, column=COL_DATA, value=case.get("data", ""))
        new_ws.cell(row=current_row, column=COL_STEPS, value=case.get("steps", ""))
        new_ws.cell(row=current_row, column=COL_EXPECTED, value=case.get("expected", ""))
        new_ws.cell(row=current_row, column=COL_NOTE, value=case.get("note", ""))

        # Wrap text on every data cell so wrapped content shows without clipping.
        for col_idx in (COL_ID, COL_PRIORITY, COL_PURPOSE, COL_CASE, COL_DATA, COL_STEPS, COL_EXPECTED, COL_NOTE):
            new_ws.cell(row=current_row, column=col_idx).alignment = wrap_alignment

        # Estimate row height from explicit newlines + rough wrap heuristic per
        # the widest text columns (steps, expected). For image rows, keep the
        # image-tuned row height (set later). For non-image rows, use the
        # estimated height so wrapped Vietnamese text is fully visible.
        def _estimated_lines(text, col_width):
            if not text:
                return 1
            # Each \n forces a wrap; long lines also wrap by char count.
            # Vietnamese chars wider than ASCII → effective chars per col unit
            # is ~0.87 (WRAP_CHAR_FACTOR), so divide by (col_width * 0.87).
            effective_chars = max(1, int(col_width * WRAP_CHAR_FACTOR))
            total = 0
            for line in str(text).split("\n"):
                total += max(1, (len(line) + effective_chars - 1) // effective_chars)
            return total
        max_lines = max(
            _estimated_lines(case.get("steps"), CASE_COL_WIDTHS.get(COL_STEPS, 42)),
            _estimated_lines(case.get("expected"), CASE_COL_WIDTHS.get(COL_EXPECTED, 50)),
            _estimated_lines(case.get("case"), CASE_COL_WIDTHS.get(COL_CASE, 32)),
            _estimated_lines(case.get("data"), CASE_COL_WIDTHS.get(COL_DATA, 30)),
        )
        estimated_height = min(
            max(ROW_HEIGHT_MIN_PT, max_lines * ROW_HEIGHT_PER_LINE_PT + 6),
            ROW_HEIGHT_MAX_PT,
        )

        # Embed screenshot if case has image_path (resolved relative to cases JSON dir).
        image_path_str = case.get("image_path") or ""
        if image_path_str:
            ip = Path(image_path_str)
            if not ip.is_absolute():
                ip = (cases_json_dir / ip).resolve()
            if ip.exists():
                img = XlsxImage(str(ip))
                img.width = IMAGE_CELL_WIDTH_PX
                img.height = IMAGE_CELL_HEIGHT_PX
                anchor_cell = f"{get_column_letter(COL_SCREENSHOT)}{current_row}"
                new_ws.add_image(img, anchor_cell)
                # Row height = max(image height, estimated text height) so neither
                # the image nor the wrapped text gets clipped.
                new_ws.row_dimensions[current_row].height = max(IMAGE_ROW_HEIGHT_PT, estimated_height)
                embedded_image_count += 1
            else:
                print(json.dumps({"warning": f"image_path not found, skipped: {ip}"}), file=sys.stderr)
        else:
            # No image — row height driven entirely by wrapped text estimate.
            new_ws.row_dimensions[current_row].height = estimated_height

        current_row += 1

    # Optionally remove the original template sheet from output if requested
    if args.remove_template_sheet:
        if template_sheet_name in wb.sheetnames:
            del wb[template_sheet_name]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb.save(output_path)

    result = {
        "status": "success",
        "output_path": str(output_path.resolve()),
        "sheet_name": new_sheet_name,
        "case_count": sum(1 for c in cases if c.get("id")),
        "suite_count": len({c.get("suite") for c in cases if c.get("suite")}),
        "rows_written": current_row - ROW_DATA_START,
        "images_embedded": embedded_image_count,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def cmd_update_results(args) -> int:
    """Clone an existing test case xlsx and fill in run results.

    Reads run results from a JSON file mapping test ID → result, copies the
    source xlsx to a NEW file (does NOT overwrite source), then for each row
    whose column A matches a test ID writes:
        - col I (Lần 1) by default — or column from --run-column (I/J/K).
          Writes "P" / "F" / "" status. Column O (Kết quả M) stays untouched
          because it holds a formula that auto-computes P/F from I..N.
        - col P (Mã lỗi):     bug_id (only if Fail and bug_id provided)
        - col Q (Ghi chú):    note + framework/browser/timestamp footer

    results.json schema:
        {
          "run": {
            "framework": "playwright",
            "browser": "chromium",
            "env": "staging",
            "datetime": "2026-05-14T16:17:00+07:00",
            "tester": "Yennth72"
          },
          "results": {
            "LF-001": { "status": "F", "bug_id": "BUG-2026-05-14-001",
                        "note": "redirect /onboarding sai" },
            "LF-002": { "status": "P", "note": "" },
            "LF-003": { "status": "",  "note": "Skipped" }
          }
        }

    status values: "P" (Pass) | "F" (Fail) | "" (not run / skip).
    Empty status leaves column N blank — does NOT write empty string.
    """
    source_path = Path(args.source)
    output_path = Path(args.output)
    results_path = Path(args.results_json)

    if not source_path.exists():
        print(json.dumps({"error": f"Source not found: {source_path}"}), file=sys.stderr)
        return 1
    if not results_path.exists():
        print(json.dumps({"error": f"Results JSON not found: {results_path}"}), file=sys.stderr)
        return 1
    if source_path.resolve() == output_path.resolve():
        print(json.dumps({"error": "Source and output paths are the same. Choose a different output path to avoid overwriting."}), file=sys.stderr)
        return 1
    if output_path.exists() and not args.force:
        print(json.dumps({"error": f"Output already exists: {output_path}. Pass --force to overwrite."}), file=sys.stderr)
        return 1

    with open(results_path, encoding="utf-8") as f:
        results_data = json.load(f)

    run_meta = results_data.get("run", {})
    results_map = results_data.get("results", {})
    if not isinstance(results_map, dict):
        print(json.dumps({"error": "results.json must contain a 'results' object mapping test IDs to records"}), file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    wb = openpyxl.load_workbook(source_path, data_only=False)

    run_column_map = {"I": COL_RUN_1, "J": COL_RUN_2, "K": COL_RUN_3, "1": COL_RUN_1, "2": COL_RUN_2, "3": COL_RUN_3}
    run_col = run_column_map.get(str(args.run_column).upper(), COL_RUN_1) if args.run_column else COL_RUN_1

    note_footer_parts = []
    if run_meta.get("framework"): note_footer_parts.append(run_meta["framework"])
    if run_meta.get("browser"):   note_footer_parts.append(run_meta["browser"])
    if run_meta.get("env"):       note_footer_parts.append(run_meta["env"])
    if run_meta.get("datetime"):  note_footer_parts.append(run_meta["datetime"])
    if run_meta.get("tester"):    note_footer_parts.append(f"by {run_meta['tester']}")
    note_footer = " | ".join(note_footer_parts)

    # Scan all candidate sheets — fill row whose column A matches any test ID in results_map.
    # Test IDs are unique across the workbook so we don't need to pick a single sheet.
    cover_sheets = {"template", "trang bìa", "giới thiệu", "tổng hợp", "note"}
    target_sheets = [args.sheet] if args.sheet else [
        s for s in wb.sheetnames if s.strip().lower() not in cover_sheets
    ]

    matched_ids = set()
    rows_updated_by_sheet = {}
    for sheet_name in target_sheets:
        if sheet_name not in wb.sheetnames:
            continue
        ws = wb[sheet_name]
        if ws.max_row < ROW_DATA_START:
            continue
        # Only sheets with the ID header are real testcase sheets
        header = ws.cell(row=ROW_HEADER_TOP, column=COL_ID).value
        if not header or str(header).strip().upper() != "ID":
            continue

        rows_in_sheet = 0
        for row in range(ROW_DATA_START, ws.max_row + 1):
            id_val = ws.cell(row=row, column=COL_ID).value
            if id_val is None:
                continue
            test_id = str(id_val).strip()
            if test_id not in results_map:
                continue

            record = results_map[test_id]
            status = str(record.get("status", "")).strip()
            bug_id = str(record.get("bug_id", "")).strip()
            note = str(record.get("note", "")).strip()

            # Write status into the chosen run column (H/I/J), not N. N is a
            # formula cell that auto-derives P/F from H..M — leave untouched.
            ws.cell(row=row, column=run_col, value=status if status else None)
            if bug_id:
                ws.cell(row=row, column=COL_DEFECT_ID, value=bug_id)
            combined_note = note
            if note_footer:
                combined_note = (note + "\n" if note else "") + f"[{note_footer}]"
            if combined_note:
                ws.cell(row=row, column=COL_NOTE, value=combined_note)
            matched_ids.add(test_id)
            rows_in_sheet += 1
        if rows_in_sheet:
            rows_updated_by_sheet[sheet_name] = rows_in_sheet

    unmatched = sorted(set(results_map.keys()) - matched_ids)
    wb.save(output_path)

    result = {
        "status": "success",
        "source_path": str(source_path.resolve()),
        "output_path": str(output_path.resolve()),
        "sheets_scanned": target_sheets,
        "rows_updated_by_sheet": rows_updated_by_sheet,
        "results_count": len(results_map),
        "rows_updated_total": sum(rows_updated_by_sheet.values()),
        "unmatched_ids": unmatched,
        "run_meta": run_meta,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Excel utilities for the qc module (KBKTCN test case template I/O).",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_inspect = sub.add_parser("inspect", help="Inspect template structure")
    p_inspect.add_argument("template_path", help="Path to .xlsx template")

    p_read = sub.add_parser("read-cases", help="Read existing test cases as JSON")
    p_read.add_argument("xlsx_path", help="Path to .xlsx with test cases")
    p_read.add_argument("--sheet", help="Sheet name (default: auto-detect template sheet)")

    p_write = sub.add_parser("write-testcase", help="Write test cases into a cloned template sheet")
    p_write.add_argument("--template", required=True, help="Path to template .xlsx")
    p_write.add_argument("--output", required=True, help="Output .xlsx path")
    p_write.add_argument("--feature", required=True, help="Feature/screen name (R3)")
    p_write.add_argument("--id-prefix", required=True, help="Test case ID prefix (R4)")
    p_write.add_argument("--cases-json", required=True, help="Path to JSON file with cases array")
    p_write.add_argument("--sheet-name", help="New sheet name (default: --feature, max 31 chars)")
    p_write.add_argument("--remove-template-sheet", action="store_true",
                         help="Remove the original 'template' sheet from output (keeps cover/intro)")

    p_update = sub.add_parser("update-results", help="Clone a testcase xlsx and fill in run results (does NOT overwrite source)")
    p_update.add_argument("--source", required=True, help="Path to source testcase .xlsx (read-only)")
    p_update.add_argument("--output", required=True, help="Path to NEW xlsx (must differ from source)")
    p_update.add_argument("--results-json", required=True, help="Path to results JSON mapping test ID → {status, bug_id, note}")
    p_update.add_argument("--sheet", help="Sheet name to update (default: scan all non-cover sheets)")
    p_update.add_argument("--run-column", help="Which Lần column to write into: I/J/K or 1/2/3 (default: I = Lần 1)")
    p_update.add_argument("--force", action="store_true", help="Overwrite output if exists")

    args = parser.parse_args()
    if args.cmd == "inspect":
        return cmd_inspect(args)
    elif args.cmd == "read-cases":
        return cmd_read_cases(args)
    elif args.cmd == "write-testcase":
        return cmd_write_testcase(args)
    elif args.cmd == "update-results":
        return cmd_update_results(args)
    return 1


if __name__ == "__main__":
    sys.exit(main())
