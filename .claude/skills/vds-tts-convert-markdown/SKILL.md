---
name: vds-tts-convert-markdown
description: 'Convert documents (PDF, DOCX, XLSX, PPTX, HTML, RTF, ODT, EPUB, CSV, TXT, JSON, YAML, images, audio with transcription, .msg Outlook emails, ZIP archives, URLs, YouTube transcripts) to readable Markdown for the VDS/Viettel stack. Uses Microsoft `markitdown` (https://github.com/microsoft/markitdown) as the single extraction backend, then a small Python post-processor that re-flows column-wrapped paragraphs, promotes numbered section headings (`1. Overview` → `## 1. Overview`), and drops repeated page headers/footers without losing content (JSON / code / table fields are preserved verbatim). Optional `--use-llm` (OpenAI) or `-d -e` (Azure Document Intelligence) for tough PDFs / complex tables. Tesseract OCR available as a separate pre-step for scanned PDFs without a text layer. Use when the user says "chuyển sang markdown", "convert to markdown", "đổi file sang md", or "tạo markdown từ file".'
---

Follow the instructions in ./workflow.md.
