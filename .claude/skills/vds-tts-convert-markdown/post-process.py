#!/usr/bin/env python3
"""Post-process markitdown output into clean, readable Markdown.

Pipeline:
  1. UTF-8 normalize (strip BOM, normalize line endings).
  2. Drop recurring per-page header/footer — content-aware: lines containing
     structured-data punctuation ({}[]"=;,) are NEVER eligible for drop so
     repeated JSON / code fields across multiple examples are preserved.
  3. Reflow paragraphs — markitdown leaves each PDF physical line as its
     own logical line; join consecutive non-empty lines when the current
     line does not end in sentence-final punctuation AND the next is not
     a structural marker (heading / list / quote / table / code fence).
     Inserts a blank line between sentence-ending paragraphs so CommonMark
     renders them as separate <p> blocks.
  4. Promote numbered headings — `1. Overview` → `## 1. Overview`,
     `2.3 Subtopic` → `### 2.3 Subtopic`. Pads blank lines around each.
  5. Collapse blank-line runs > 2 to 2; trim leading/trailing blanks.
  6. Prepend YAML front matter + optional H1 title.

Two invocation modes:
  A. --pdf <file>    : one-shot. Runs `markitdown` via subprocess, then
                       post-processes the output.
  B. --input <text>  : post-process an already-extracted text file
                       (markitdown stdout dump, tesseract OCR output, etc.)

Requires:
  - markitdown (`pip install 'markitdown[pdf]'` — or `[all]` for full format
    coverage). https://github.com/microsoft/markitdown
  - Python >= 3.10
"""
import re, argparse, datetime, pathlib, subprocess, shutil, sys, tempfile


# ----------------------------------------------------------------------
# Recurring header/footer detection (content-aware)
# ----------------------------------------------------------------------

# Lines containing any of these characters are likely structured data
# (JSON, code, table rows, key-value config) and must NOT be considered
# recurring-header candidates — otherwise repeated payload fields
# across multiple API examples (e.g. `"code": "PHONE",` appearing in
# §4.1, §4.2, §4.3) get silently dropped from the output.
_STRUCTURED_DATA_CHARS = re.compile(r'[{}\[\]"=;,]')


def drop_recurring(lines, min_repeat=3, max_len=80):
    """Drop short content-free lines that repeat across the document
    (page headers, footers, doc title re-emitted each page)."""
    counts = {}
    for ln in lines:
        k = ln.strip()
        if 3 <= len(k) <= max_len and not _STRUCTURED_DATA_CHARS.search(k):
            counts[k] = counts.get(k, 0) + 1
    drop = {k for k, c in counts.items() if c >= min_repeat}
    return [ln for ln in lines if ln.strip() not in drop]


# ----------------------------------------------------------------------
# Paragraph reflow
# ----------------------------------------------------------------------

# Structural line-starts that must NOT be joined into the previous line.
_STRUCTURAL_START = re.compile(
    r"^("
    r"#{1,6}\s"                       # markdown heading
    r"|[-*+]\s"                       # bullet list
    r"|\d+\.\s+[A-ZĐÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ]"
    r"|>\s"                           # blockquote
    r"|\|"                            # table row
    r"|```"                           # code fence
    r"|~~~"                           # code fence
    r")"
)
_SENTENCE_END = re.compile(r'[.!?;:。．！？；：…]["”’)\]\}]?\s*$')


def reflow_paragraphs(lines):
    """Join lines wrapped mid-paragraph by markitdown's column-width line
    folding. Emits a blank separator between consecutive sentence-ending
    paragraphs so CommonMark renders them as distinct blocks."""
    out, i, n = [], 0, len(lines)
    while i < n:
        cur = lines[i]
        stripped = cur.strip()
        # Empty / structural / sentence-end → emit as-is, no merging down.
        if (not stripped or _STRUCTURAL_START.match(stripped)
                or _SENTENCE_END.search(stripped)):
            out.append(cur)
            # Insert blank between this paragraph and the next content line.
            if (stripped and not _STRUCTURAL_START.match(stripped)
                    and _SENTENCE_END.search(stripped)):
                j = i + 1
                while j < n and not lines[j].strip():
                    j += 1
                if j < n:
                    nxt_stripped = lines[j].strip()
                    if nxt_stripped and not _STRUCTURAL_START.match(nxt_stripped):
                        out.append("")
            i += 1
            continue
        if i + 1 >= n:
            out.append(cur)
            break
        nxt = lines[i + 1]
        nxt_stripped = nxt.strip()
        if not nxt_stripped or _STRUCTURAL_START.match(nxt_stripped):
            out.append(cur)
            i += 1
            continue
        # Merge cur into next line so further wraps keep joining.
        lines[i + 1] = cur.rstrip() + " " + nxt_stripped
        i += 1
    return out


# ----------------------------------------------------------------------
# Heading promotion: `1. Overview` → `## 1. Overview`, etc.
# ----------------------------------------------------------------------
_VN_CAPS = ("A-ZĐÀÁẢÃẠÂẦẤẨẪẬĂẰẮẲẴẶÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴ")
_H2_NUMBERED = re.compile(rf"^(\d{{1,2}})\.\s+([{_VN_CAPS}][^\n]{{1,80}})\s*$")
_H3_NUMBERED = re.compile(rf"^(\d{{1,2}}\.\d{{1,2}})\s+([{_VN_CAPS}][^\n]{{1,80}})\s*$")


def promote_numbered_headings(lines):
    """Promote numbered-section lines to `##` / `###` and pad blank lines
    around them. Conservative: title must start with a capital and not end
    with `,` or `:` (avoids matching mid-sentence enumeration)."""
    out = []
    for ln in lines:
        s = ln.rstrip()
        m3 = _H3_NUMBERED.match(s)
        m2 = _H2_NUMBERED.match(s)
        new, promoted = s, False
        if m3 and not s.endswith((",", ":")):
            new, promoted = f"### {m3.group(1)} {m3.group(2)}", True
        elif m2 and not s.endswith((",", ":")):
            new, promoted = f"## {m2.group(1)}. {m2.group(2)}", True
        if promoted:
            if out and out[-1].strip():
                out.append("")
            out.append(new)
            out.append("")
        else:
            out.append(new)
    return out


# ----------------------------------------------------------------------
# Blank-line collapse
# ----------------------------------------------------------------------
def collapse_blanks(lines, max_run=2):
    out, blank = [], 0
    for ln in lines:
        if not ln.strip():
            blank += 1
            if blank <= max_run:
                out.append("")
        else:
            blank = 0
            out.append(ln)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


# ----------------------------------------------------------------------
# Main pipeline
# ----------------------------------------------------------------------
def post_process(raw_text: str,
                 source: str = "",
                 title: str = "",
                 converter: str = "markitdown + post-process",
                 add_front_matter: bool = True) -> str:
    if raw_text.startswith("﻿"):
        raw_text = raw_text[1:]
    raw_text = raw_text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in raw_text.split("\n")]
    lines = drop_recurring(lines)
    lines = reflow_paragraphs(lines)
    lines = promote_numbered_headings(lines)
    lines = collapse_blanks(lines)
    body = "\n".join(lines) + "\n"
    head = []
    if add_front_matter:
        ts = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
        head.append("---\n")
        if source:
            head.append(f"source: {source}\n")
        head.append(f"converted_at: {ts}\n")
        head.append(f"converter: {converter}\n")
        head.append("---\n\n")
    if title:
        head.append(f"# {title}\n\n")
    return "".join(head) + body


# ----------------------------------------------------------------------
# Markitdown subprocess wrapper
# ----------------------------------------------------------------------
def run_markitdown(input_path: pathlib.Path) -> str:
    """Run markitdown on a file and return its Markdown output."""
    markitdown = shutil.which("markitdown") or shutil.which("markitdown.exe")
    if not markitdown:
        sys.exit(
            "markitdown not found. Install:\n"
            "  pip install 'markitdown[pdf]'   # PDF only\n"
            "  pip install 'markitdown[all]'   # all formats (heavier)\n"
            "Then ensure it's on PATH (e.g. ~/.local/bin for --user installs)."
        )
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False,
                                     mode="w", encoding="utf-8") as tmp:
        tmp_path = pathlib.Path(tmp.name)
    try:
        proc = subprocess.run(
            [markitdown, str(input_path), "-o", str(tmp_path)],
            capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=600,
        )
        if proc.returncode != 0:
            sys.exit(f"markitdown failed (rc={proc.returncode}):\n{proc.stderr}")
        return tmp_path.read_text(encoding="utf-8", errors="replace")
    finally:
        try:
            tmp_path.unlink()
        except OSError:
            pass


# ----------------------------------------------------------------------
# CLI
# ----------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--pdf",
                     help="Source document (PDF/DOCX/PPTX/XLSX/...): run "
                          "markitdown then post-process. Despite the name, "
                          "any markitdown-supported format is accepted.")
    src.add_argument("--input",
                     help="Already-extracted text/markdown file to post-process")
    ap.add_argument("--output", required=True, help="markdown output path")
    ap.add_argument("--source", default="",
                    help="original filename (for front matter)")
    ap.add_argument("--title", default="",
                    help="H1 title (default: basename of --pdf)")
    ap.add_argument("--converter", default="",
                    help="converter label for front matter")
    ap.add_argument("--no-front-matter", action="store_true",
                    help="omit YAML front matter and H1 title block")
    args = ap.parse_args()

    if args.pdf:
        pdf_path = pathlib.Path(args.pdf).resolve()
        if not pdf_path.is_file():
            sys.exit(f"File not found: {pdf_path}")
        raw = run_markitdown(pdf_path)
        title = args.title or pdf_path.stem
        source = args.source or pdf_path.name
        converter = args.converter or "markitdown + post-process"
    else:
        raw = pathlib.Path(args.input).read_text(encoding="utf-8",
                                                 errors="replace")
        title = args.title
        source = args.source
        converter = args.converter or "markitdown + post-process"

    md = post_process(
        raw, source=source, title=title, converter=converter,
        add_front_matter=not args.no_front_matter,
    )

    out = pathlib.Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(md, encoding="utf-8")
    print(f"Wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
