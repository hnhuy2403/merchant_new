import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';
import MarkdownIt from 'markdown-it';
import { renderMermaid } from './diagram';

interface AttachmentInfo {
  filename: string;
  localPath: string;
}

interface ConvertResult {
  storage: string;
  attachments: AttachmentInfo[];
  warnings: string[];
}

/**
 * Chuyển Markdown -> Confluence storage XHTML.
 * - Code block -> macro `code`.
 * - Mermaid -> render PNG -> attachment -> <ac:image>.
 * - Ảnh local -> attachment; ảnh URL -> <ri:url>.
 *
 * Lưu ý: filename attachment được chuẩn hóa (bỏ dấu/space) và PHẢI khớp với tên
 * truyền vào khi upload (xem addAttachment trong bin/cli.js).
 */
export function convert(markdown: string, baseDir: string): ConvertResult {
  const md = new MarkdownIt({ html: true, linkify: true, typographer: true });
  const attachments: AttachmentInfo[] = [];
  const warnings: string[] = [];
  const tokens = md.parse(markdown, {});
  let html = '';
  let mermaidCount = 0;

  for (const token of tokens) {
    if (token.type === 'fence') {
      const code = token.content;
      const lang = (token.info || 'plaintext').trim();

      if (lang === 'mermaid') {
        mermaidCount++;
        const pngName = normalizeFilename(`diagram_${Date.now()}_${mermaidCount}.png`);
        const pngPath = path.join(os.tmpdir(), pngName);
        const ok = renderMermaid(code, pngPath);
        if (ok) {
          attachments.push({ filename: pngName, localPath: pngPath });
          html += `<ac:image><ri:attachment ri:filename="${escapeXml(pngName)}"/></ac:image>`;
        } else {
          // Fallback: giữ code mermaid trong macro để không mất nội dung
          html += `<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">text</ac:parameter>
<ac:plain-text-body><![CDATA[${code}]]></ac:plain-text-body>
</ac:structured-macro>`;
        }
      } else {
        html += `<ac:structured-macro ac:name="code">
<ac:parameter ac:name="language">${escapeXml(lang)}</ac:parameter>
<ac:plain-text-body><![CDATA[${code}]]></ac:plain-text-body>
</ac:structured-macro>`;
      }
    } else {
      html += md.renderer.render([token], {}, {});
    }
  }

  // Post-process: convert <img> (src/alt theo thứ tự bất kỳ)
  html = html.replace(/<img\b[^>]*>/g, (tag) => {
    const srcMatch = tag.match(/\bsrc="([^"]*)"/);
    // Thẻ <img> không có src -> bỏ hẳn (tránh thẻ thô làm Confluence lỗi 400).
    if (!srcMatch) {
      warnings.push('Bỏ qua một thẻ ảnh không có đường dẫn (src).');
      return '';
    }
    const src = srcMatch[1];
    if (src.startsWith('http')) {
      return `<ac:image><ri:url ri:value="${escapeXml(src)}"/></ac:image>`;
    }
    const fullPath = path.resolve(baseDir, src);
    if (fs.existsSync(fullPath)) {
      const fileName = normalizeFilename(path.basename(src));
      attachments.push({ filename: fileName, localPath: fullPath });
      return `<ac:image><ri:attachment ri:filename="${escapeXml(fileName)}"/></ac:image>`;
    }
    // Ảnh local KHÔNG tồn tại -> KHÔNG để lại <img> thô (gây vỡ tài liệu).
    warnings.push(`Không tìm thấy ảnh: ${src} (đã bỏ ảnh, phần còn lại vẫn được đẩy).`);
    return `<p><em>[Thiếu ảnh: ${escapeXml(path.basename(src))}]</em></p>`;
  });

  // Confluence storage format là XHTML nghiêm ngặt: mọi thẻ void phải tự đóng.
  const VOID_TAGS = ['hr', 'br', 'img', 'input', 'col', 'area', 'meta', 'link', 'source', 'wbr', 'embed', 'track', 'base'];
  for (const tag of VOID_TAGS) {
    const re = new RegExp(`<${tag}\\b([^>]*?)\\s*/?>`, 'gi');
    html = html.replace(re, (_m, attrs) => `<${tag}${attrs}/>`);
  }

  return { storage: html, attachments, warnings };
}

export function normalizeFilename(filename: string): string {
  return filename
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '') // bỏ dấu tiếng Việt
    .replace(/\s+/g, '_')
    .replace(/[^a-zA-Z0-9._-]/g, '');
}

function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}
