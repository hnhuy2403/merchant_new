# vds-tts-convert-markdown — Workflow

Convert documents into readable Markdown (`.md`) files using **Microsoft markitdown** + a small post-processor that cleans up paragraph wrapping and recurring page headers.

Markitdown handles 95%+ of inputs (PDF, DOCX, XLSX, PPTX, HTML, audio, images, .msg, ZIP, URL, YouTube). Post-process re-flows column-wrapped paragraphs, promotes numbered section headings, and drops repeated page headers/footers — without losing content.

---

## STEP 1 — COLLECT INPUTS

If arguments were passed (e.g. `vds-tts-convert-markdown ./docs/spec.pdf`), parse them. Otherwise ask the user for the required fields in one message:

| Field | Example | Description |
|---|---|---|
| `inputPath` | `./docs/spec.pdf` or `./docs/` | File / directory path. Required. |
| `outputDir` | `./docs/markdown` | Directory to write `.md` files. Default: same directory as input. |
| `recursive` | `true` / `false` | Only when `inputPath` is a directory. Default: `false`. |
| `overwrite` | `true` / `false` | Overwrite existing `.md` outputs. Default: `false` (skip & warn). |
| `language` | `vi` / `en` | Optional OCR language hint for image-based PDFs (only used by tesseract fallback). Default: `vi+eng`. |

Derive automatically:
- `outputName` per file = `<basename>.md`
- `format` = lowercased file extension (without dot)

---

## STEP 2 — DETECT TOOLING (cross-platform)

Skill requires exactly one tool: **markitdown**. Tesseract is an optional fallback for scanned/image-only PDFs.

Check what's available (works on Linux / macOS / Windows / WSL):

```bash
python3 -c "import shutil; [print(t, shutil.which(t) or shutil.which(t+'.exe') or '-') for t in ['markitdown','tesseract']]"
```

On Windows PowerShell / `cmd.exe` use `python` instead of `python3`. `post-process.py` calls `shutil.which()` internally so it picks `.exe` automatically.

If **markitdown** is missing, stop and instruct the user:

```
Cần cài markitdown:

  Linux / macOS / Windows (cùng pip):
    pip install 'markitdown[pdf]'          # chỉ PDF — đủ cho phần lớn use case
    pip install 'markitdown[all]'          # toàn bộ format — heavier

  Optional — OCR cho PDF scan / ảnh thuần (tesseract):
    Linux:   sudo apt install tesseract-ocr tesseract-ocr-vie
    macOS:   brew install tesseract
    Windows: winget install --id=UB-Mannheim.TesseractOCR -e

Sau khi cài, đảm bảo `markitdown` nằm trong PATH (vd `~/.local/bin/` cho `pip install --user`).
```

### Markitdown — modular install (lighter footprint)

Reference: https://github.com/microsoft/markitdown

| Extras | Mục đích |
|---|---|
| `pip install 'markitdown[pdf]'` | Chỉ PDF |
| `pip install 'markitdown[docx]'` | Chỉ Word |
| `pip install 'markitdown[xlsx,xls]'` | Excel mới + cũ |
| `pip install 'markitdown[pptx]'` | PowerPoint |
| `pip install 'markitdown[outlook]'` | `.msg` Outlook emails |
| `pip install 'markitdown[audio-transcription]'` | Audio → speech-to-text (Whisper / SpeechRecognition) |
| `pip install 'markitdown[youtube-transcription]'` | YouTube URL → transcript |
| `pip install 'markitdown[az-doc-intel]'` | Backend Azure Document Intelligence (PDF chất lượng cao + bảng phức tạp) |
| `pip install 'markitdown[az-content-understanding]'` | Backend Azure Content Understanding (structured field extraction → YAML front matter) |
| `pip install 'markitdown[all]'` | Tất cả extras (mặc định cho dev workstation) |

Plugin của bên thứ 3 (vd `markitdown-ocr` dùng LLM-based OCR) cài thêm rồi bật bằng `--use-plugins` (xem advanced flags bên dưới).

---

## STEP 3 — PICK CONVERTER PER FORMAT

| Format | Tool | Note |
|---|---|---|
| `.pdf`, `.docx`, `.doc`, `.odt`, `.rtf`, `.html`, `.htm`, `.xhtml`, `.epub` | `markitdown` + `post-process.py` | Một-shot qua `post-process.py --pdf <file>` (xem Step 4) |
| `.pptx`, `.ppt` | `markitdown` + `post-process.py` | Slide notes + text content |
| `.xlsx`, `.xls`, `.csv`, `.tsv` | `markitdown` + `post-process.py` | Markitdown render Excel/CSV thành Markdown table |
| `.png`, `.jpg`, `.jpeg`, `.tiff`, `.bmp` | `markitdown` (với `[image]` hoặc `[all]`) | Có thể `--use-llm -m <model>` để LLM sinh mô tả thay vì chỉ OCR |
| `.pdf` (scanned, không có text layer) | `tesseract` per page → assemble → `post-process.py --input` | Markitdown KHÔNG OCR mặc định cho PDF scan; phải tesseract trước |
| `.mp3`, `.wav`, `.m4a`, `.flac`, `.ogg` | `markitdown` với extras `[audio-transcription]` | Whisper local hoặc SpeechRecognition |
| `.msg` (Outlook) | `markitdown` với extras `[outlook]` | Text + metadata (subject, from, to, date) |
| `.zip` | `markitdown` native | Iterate qua từng file trong zip, output gộp |
| URL `http(s)://...` | `markitdown <url>` | Tự nhận biết HTML / PDF / blob qua content-type |
| YouTube URL | `markitdown` với extras `[youtube-transcription]` | Transcript chính thức + metadata video |
| `.json`, `.yaml`, `.yml`, `.xml` | Built-in: wrap trong fenced code block với language hint | Không cần markitdown |
| `.txt`, `.log`, `.md` | Pass-through (collapse trailing whitespace, normalize line endings) | Không cần markitdown |

---

## STEP 4 — EXECUTE CONVERSION

### Một-shot (recommended) — markitdown + post-process trong một lệnh

`post-process.py` tự run `markitdown` qua `subprocess` rồi apply pipeline cleanup. Cross-platform (Linux / macOS / Windows / WSL):

```bash
# Linux / macOS / WSL:
python3 "${SKILL_DIR}/post-process.py" --pdf "${inputFile}" --output "${outputDir}/${basename}.md"

# Windows (PowerShell / cmd.exe):
python "%SKILL_DIR%\post-process.py" --pdf "%inputFile%" --output "%outputDir%\%basename%.md"
```

Despite the flag name `--pdf`, **any markitdown-supported format works** (DOCX, PPTX, XLSX, HTML, .msg, .zip, URL, etc.) — markitdown auto-detects by content. Optional flags:

- `--title "<H1>"` — H1 title (default: file basename).
- `--source "<original-path>"` — original path label for front matter.
- `--converter "<label>"` — custom converter label for front matter.
- `--no-front-matter` — omit YAML front matter + H1 title block.

### Hai-bước — khi cần inspect raw markitdown output

```bash
markitdown "${inputFile}" -o "${tmpDir}/${basename}.raw.md"
python3 "${SKILL_DIR}/post-process.py" \
    --input "${tmpDir}/${basename}.raw.md" \
    --output "${outputDir}/${basename}.md" \
    --source "${inputFile}" \
    --title "<H1 title>"
```

Dùng khi (a) cần xem markitdown extract gì trước khi cleanup, (b) chạy markitdown với advanced flags (`--use-llm`, `-d -e`, `--use-cu`) rồi feed output qua post-process.

### Markitdown Python API — khi cần lập trình batch

```python
from markitdown import MarkItDown

md = MarkItDown()                          # mặc định, không plugin
# md = MarkItDown(enable_plugins=True)     # bật plugin thứ 3 (markitdown-ocr, ...)
result = md.convert("path/to/file.pdf")
text = result.text_content                 # markdown string
title = result.title                       # optional title metadata
```

### Markitdown — advanced flags

| Flag CLI | Mục đích |
|---|---|
| `--use-plugins` | Bật plugins đã `pip install` (vd `markitdown-ocr` LLM-based OCR) |
| `--list-plugins` | Liệt kê plugins đã cài |
| `--use-llm -m <model>` | LLM-augmented image descriptions (vd `gpt-4o`). Cần env `OPENAI_API_KEY`. Sinh alt-text giàu nội dung cho ảnh thay vì OCR thô. |
| `-d -e "<endpoint>"` | Azure Document Intelligence backend — PDF chất lượng cao + bảng phức tạp. Cần extras `[az-doc-intel]` + endpoint Azure. |
| `--use-cu --cu-endpoint "<endpoint>"` | Azure Content Understanding — structured field extraction → YAML front matter. Cần extras `[az-content-understanding]`. |

**Khi nào dùng Azure DI** (`-d -e`): PDF nguồn có bảng nhiều cấp, layout multi-column, hoặc text scan chất lượng thấp mà markitdown built-in không xử lý được. Azure DI trả về cấu trúc bảng chuẩn → markitdown convert sang Markdown table đúng. Chi phí tính theo trang Azure.

### Tesseract OCR (PDF scan thuần, không có text layer)

```bash
pdftoppm -r 300 "${inputFile}" "${tmpDir}/page" -png        # poppler-utils
for img in "${tmpDir}"/page-*.png; do
  tesseract "$img" "${img%.png}" -l "${language:-vie+eng}"
done
cat "${tmpDir}"/page-*.txt > "${tmpDir}/${basename}.raw.txt"

# Feed qua post-process để clean lên
python3 "${SKILL_DIR}/post-process.py" \
    --input "${tmpDir}/${basename}.raw.txt" \
    --output "${outputDir}/${basename}.md" \
    --source "${inputFile}" \
    --title "<H1 title>"
```

### CSV / TSV → Markdown table (built-in, no external tool)

Khi `markitdown` không khả dụng cho CSV, render bằng Python:

```python
import csv, pathlib
rows = list(csv.reader(open(input_path, encoding="utf-8")))
header, *body = rows
md = "| " + " | ".join(header) + " |\n"
md += "|" + "|".join("---" for _ in header) + "|\n"
for r in body:
    md += "| " + " | ".join(r) + " |\n"
pathlib.Path(output_path).write_text(md, encoding="utf-8")
```

### JSON / YAML / XML → fenced code block

```python
import pathlib
content = pathlib.Path(input_path).read_text(encoding="utf-8")
lang = {"json":"json","yaml":"yaml","yml":"yaml","xml":"xml"}[ext]
pathlib.Path(output_path).write_text(f"```{lang}\n{content}\n```\n", encoding="utf-8")
```

---

## STEP 5 — POST-PROCESS (auto-correct, no prompt)

`post-process.py` always runs after markitdown. Pipeline (in order):

1. **UTF-8 normalize**: strip BOM, normalize CRLF/CR → LF.
2. **Drop recurring per-page header/footer** — any line 3-80 chars that appears verbatim ≥ 3 times across the document is removed (catches doc titles re-emitted on each page, repeated dates). **Content-aware**: lines containing `{`, `}`, `[`, `]`, `"`, `=`, `;`, or `,` are NEVER eligible for drop — preserves repeated JSON / code / table fields across multiple examples.
3. **Reflow paragraphs** — markitdown leaves each PDF physical line as its own logical line; join consecutive non-empty lines when the current line does NOT end in sentence-final punctuation (`.!?;:)/]/}`) AND the next line is NOT a structural marker (heading, bullet, numbered list with capitalised start, blockquote, table row, code fence). Inserts a blank line between sentence-ending paragraphs so CommonMark renders them as distinct `<p>` blocks. Typical 11-page design doc: 595 raw lines → ~155 reflowed lines.
4. **Promote numbered headings** — `^N. Title` → `## N. Title` and `^N.M Title` → `### N.M Title`, gated on Title starting with a capital letter and not ending in `,` or `:` (avoids false positives on numbered list / mid-sentence enumeration). Pads a blank line before and after each promoted heading.
5. **Collapse blank lines** > 2 to 2; trim leading/trailing blanks.
6. **Front matter** prepended:
   ```markdown
   ---
   source: <relative path>
   converted_at: <ISO timestamp>
   converter: markitdown + post-process
   ---
   ```
7. **H1 heading** prepended from `--title` (default: file basename).

### Limitations the helper does NOT fix (document these in results)

- **Tables in PDFs** — markitdown flattens PDF tables into prose (loses grid). Reflow joins the flattened cell text but cannot rebuild the Markdown table. Workarounds: use `markitdown -d -e` (Azure Document Intelligence) for tough tables; or manually rebuild the table.
- **Mermaid diagrams in PDFs** — markitdown may emit `Syntax error in text` + `mmeerrmmaaiidd vveerrssiioonn ...` (double-character artifact) when it tries to extract diagram text. The diagram itself isn't recovered; user must redraw or use a separate vision pass.
- **Vietnamese combining-mark glitches** — markitdown's PDF extractor sometimes produces glyphs like `lọai`, `cḥon`, `đ̣inh`, `tṛưc`, `nḥân` (combining marks in wrong order). This is an extraction-layer issue; post-process cannot fix it at the text layer. The text is still readable; if exact diacritics matter, fall back to copy-from-source or use `markitdown -d -e` (Azure DI handles diacritics better).
- **Inline backticks** and **link URLs** in source → lost (only visible text remains; PDF link annotations are not extracted by markitdown's default PDF parser).
- **Embedded images** — not extracted by default. If needed, run `pdfimages` / `pdftoppm` (poppler) separately and reference manually.

---

## STEP 6 — PRESENT RESULTS

When all files complete, return a structured summary:

```
✅ Converted 3 of 4 files

| Input | Output | Status | Notes |
|---|---|---|---|
| spec.pdf | docs/markdown/spec.md | ok | 32 KB, 157 lines, 10 headings, 5 paragraphs |
| api.docx | docs/markdown/api.md | ok | markitdown |
| diagram.pdf | docs/markdown/diagram.md | partial | tables flattened — manual rebuild needed |
| meeting.mp4 | — | skipped | unsupported (video — extract audio first then re-run) |

Images: 0 extracted (markitdown does not extract images by default).
```

Highlight any:
- Files skipped (markitdown missing, unsupported format, scan PDF without tesseract, ...).
- Files with reduced fidelity (flattened tables, combining-mark glitches, broken Mermaid).
- Suggestions to re-run with `--use-llm` or `-d -e` Azure DI when output quality is poor.

---

## NOTES & CONSTRAINTS

- **Idempotent**: re-running on the same input must produce the same output (deterministic file ordering, deterministic post-process).
- **No interactive prompts during conversion**: all flags must come from STEP 1.
- **Encoding**: always write UTF-8 (no BOM). Read source with `errors="replace"` to tolerate broken bytes.
- **Path safety**: never overwrite files outside `outputDir`. Refuse to write `.md` over a non-`.md` file.
- **Performance**: markitdown can be slow on large PDFs (60+ pages); set timeout 600s in `post-process.py` (already configured). For batches > 20 files, mention progress every 5 files.
- **Privacy**: `--use-llm` and `-d -e` Azure DI send document content to external APIs. Warn the user before enabling on sensitive content.

---

## REFERENCES

- Microsoft markitdown: https://github.com/microsoft/markitdown
- Markitdown Python API docs: https://github.com/microsoft/markitdown#python-api
- Tesseract OCR: https://tesseract-ocr.github.io/
- Poppler utils (only for tesseract OCR pre-processing): https://poppler.freedesktop.org/
