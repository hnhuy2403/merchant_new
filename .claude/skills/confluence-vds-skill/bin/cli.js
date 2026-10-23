#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const os = require('os');

// Load .env from project root or .claude directory
function loadEnv() {
  const envPaths = [
    path.join(process.cwd(), '.env'),
    path.join(process.cwd(), '.claude', '.env'),
    path.join(__dirname, '..', '.env')
  ];

  for (const envPath of envPaths) {
    if (fs.existsSync(envPath)) {
      const content = fs.readFileSync(envPath, 'utf-8');
      content.split('\n').forEach(line => {
        const [key, value] = line.split('=');
        if (key && value) {
          process.env[key.trim()] = value.trim();
        }
      });
      break;
    }
  }
}

loadEnv();

// ============= MULTI-DOMAIN CONFIG =============
const CONFIG_DIR = path.join(os.homedir(), '.confluence-vds-skill');
const CONFIG_FILE = path.join(CONFIG_DIR, 'domains.json');

// Domain công ty điền sẵn — để listDomains không bao giờ rỗng (BUG-1).
// Nếu config chưa có domain nào, ta tự bổ sung 2 domain này.
const DEFAULT_DOMAINS = {
  production: { label: 'Nội bộ sản xuất', url: 'http://10.254.136.32:8090' },
  partner: { label: 'Đối tác', url: 'http://10.254.136.35:8090' }
};

// Đảm bảo config luôn có sẵn 2 domain mặc định + activeDomain hợp lệ.
// Trả về true nếu có thay đổi (để caller lưu lại nếu muốn).
function ensureDefaultDomains(cfg) {
  let changed = false;
  if (!cfg.domains) { cfg.domains = {}; changed = true; }
  for (const [id, d] of Object.entries(DEFAULT_DOMAINS)) {
    if (!cfg.domains[id]) { cfg.domains[id] = d; changed = true; }
  }
  if (!cfg.activeDomain || !cfg.domains[cfg.activeDomain]) {
    cfg.activeDomain = 'production';
    changed = true;
  }
  return changed;
}

function loadConfig() {
  let cfg = null;
  if (fs.existsSync(CONFIG_FILE)) {
    cfg = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } else if (process.env.CONFLUENCE_URL) {
    cfg = {
      activeDomain: 'production',
      username: process.env.CONFLUENCE_USERNAME || '',
      token: process.env.CONFLUENCE_API_TOKEN || '',
      domains: { production: { label: 'Nội bộ sản xuất', url: process.env.CONFLUENCE_URL } }
    };
  } else {
    // Chưa có gì: tạo config khung với 2 domain điền sẵn (token vẫn rỗng).
    cfg = { activeDomain: 'production', username: '', token: '', domains: {} };
  }
  // Luôn đảm bảo có 2 domain mặc định; nếu vừa bổ sung thì ghi lại file.
  const changed = ensureDefaultDomains(cfg);
  if (changed && fs.existsSync(CONFIG_DIR)) {
    try { fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2)); } catch {}
  }
  return cfg;
}

function saveConfig(cfg) {
  if (!fs.existsSync(CONFIG_DIR)) fs.mkdirSync(CONFIG_DIR, { recursive: true });
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2));
}

function getActive() {
  const cfg = loadConfig();
  if (!cfg || !cfg.domains || !cfg.domains[cfg.activeDomain]) return null;
  // Domain đã có sẵn nhưng chưa có token -> coi như chưa setup (cần hỏi token).
  if (!cfg.token) return null;
  const d = cfg.domains[cfg.activeDomain];
  return { url: d.url, username: cfg.username, token: cfg.token, domainId: cfg.activeDomain, label: d.label };
}

// ============= HTTP REQUEST =============
function makeRequest(url, method = 'GET', body = null, active = null) {
  return new Promise((resolve, reject) => {
    if (!active) active = getActive();
    if (!active) {
      reject(new Error('needSetup'));
      return;
    }
    // Confluence Data Center dùng Personal Access Token (PAT) qua Bearer.
    const parsedUrl = new URL(url);

    const options = {
      method,
      headers: {
        'Authorization': `Bearer ${active.token}`,
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'User-Agent': 'Confluence-MCP-Client'
      }
    };

    const protocol = parsedUrl.protocol === 'https:' ? https : http;
    const req = protocol.request(parsedUrl, options, (res) => {
      let data = '';
      res.on('data', chunk => (data += chunk));
      res.on('end', () => {
        resolve({ status: res.statusCode, body: data, headers: res.headers });
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ============= CONFLUENCE API METHODS =============
async function listSpaces(active) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');
  const result = await makeRequest(`${active.url}/rest/api/space?limit=100`, 'GET', null, active);
  if (result.status === 200) {
    return JSON.parse(result.body).results.map(s => ({ key: s.key, name: s.name, id: s.id }));
  }
  throw new Error(`Error: ${result.status}`);
}

async function getPageBySpaceAndTitle(spaceKey, pageTitle, active) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');
  const url = `${active.url}/rest/api/content?spaceKey=${spaceKey}&title=${encodeURIComponent(
    pageTitle
  )}&expand=body.storage,version`;
  const result = await makeRequest(url, 'GET', null, active);

  if (result.status === 200) {
    const data = JSON.parse(result.body);
    if (data.results?.length > 0) {
      const page = data.results[0];
      return {
        id: page.id,
        title: page.title,
        content: page.body?.storage?.value,
        url: `${active.url}${page._links.webui}`,
        version: page.version.number,
        status: page.status
      };
    }
  }
  throw new Error('Page not found');
}

async function getPageById(pageId, active) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');
  const url = `${active.url}/rest/api/content/${pageId}?expand=body.storage,version`;
  const result = await makeRequest(url, 'GET', null, active);

  if (result.status === 200) {
    const page = JSON.parse(result.body);
    return {
      id: page.id,
      title: page.title,
      content: page.body?.storage?.value,
      url: `${active.url}${page._links.webui}`,
      version: page.version.number,
      status: page.status,
      space: page.space?.key
    };
  }
  throw new Error(`Page not found: ${result.status}`);
}

async function searchPages(query, active) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');
  const url = `${active.url}/rest/api/content/search?cql=text ~ "${encodeURIComponent(
    query
  )}" AND type=page&limit=20`;
  const result = await makeRequest(url, 'GET', null, active);

  if (result.status === 200) {
    const data = JSON.parse(result.body);
    return data.results.map(p => ({
      id: p.id,
      title: p.title,
      space: p.space?.key,
      url: `${active.url}${p._links.webui}`
    }));
  }
  throw new Error(`Search failed: ${result.status}`);
}

async function createPage(spaceKey, title, content, active, parentId = null) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');
  const body = {
    type: 'page',
    title: title,
    space: { key: spaceKey },
    body: {
      storage: {
        value: content,
        representation: 'storage'
      }
    }
  };
  // Nếu có parentId -> tạo dưới dạng page con (ancestors). Thiếu dòng này thì
  // parentId bị bỏ qua và page rơi về gốc space.
  if (parentId) {
    body.ancestors = [{ id: String(parentId) }];
  }

  const url = `${active.url}/rest/api/content`;
  const result = await makeRequest(url, 'POST', body, active);

  if (result.status === 200 || result.status === 201) {
    const page = JSON.parse(result.body);
    return {
      id: page.id,
      title: page.title,
      url: `${active.url}${page._links.webui}`
    };
  }
  throw new Error(`Create failed: ${result.status} - ${result.body}`);
}

async function updatePage(pageId, title, content, active) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');
  const pageData = await getPageById(pageId, active);
  const newVersion = pageData.version + 1;

  const body = {
    type: 'page',
    title: title,
    body: {
      storage: {
        value: content,
        representation: 'storage'
      }
    },
    version: {
      number: newVersion
    }
  };

  const url = `${active.url}/rest/api/content/${pageId}`;
  const result = await makeRequest(url, 'PUT', body, active);

  if (result.status === 200) {
    const page = JSON.parse(result.body);
    return {
      id: page.id,
      title: page.title,
      url: `${active.url}${page._links.webui}`,
      version: page.version.number
    };
  }
  throw new Error(`Update failed: ${result.status} - ${result.body}`);
}

async function updatePageBySpaceAndTitle(spaceKey, pageTitle, newContent, active) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');
  const pageData = await getPageBySpaceAndTitle(spaceKey, pageTitle, active);
  return await updatePage(pageData.id, pageData.title, newContent, active);
}

async function deletePage(pageId, active) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');
  const url = `${active.url}/rest/api/content/${pageId}`;
  const result = await makeRequest(url, 'DELETE', null, active);

  if (result.status === 204 || result.status === 200) {
    return { success: true, message: `Page ${pageId} deleted` };
  }
  throw new Error(`Delete failed: ${result.status}`);
}

// ============= PUSH/UPDATE DOC =============
async function pushDoc(spaceKey, title, mdFilePath, parentId = null, active = null) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');

  // BUG-6: nếu không truyền tiêu đề -> lấy theo tên file (bỏ đuôi .md).
  if (!title) {
    title = path.basename(mdFilePath).replace(/\.md$/i, '');
  }

  const mdContent = fs.readFileSync(mdFilePath, 'utf-8');
  const baseDir = path.dirname(mdFilePath);
  const { storage, attachments, warnings } = convertMarkdown(mdContent, baseDir);

  // Create page (gắn parentId nếu có -> page con)
  const result = await createPage(spaceKey, title, storage, active, parentId);
  const { id: pageId, url } = result;

  // Upload attachments
  let attachCount = 0;
  for (const att of attachments) {
    try {
      await addAttachment(pageId, att.localPath, active, att.filename);
      attachCount++;
    } catch (err) {
      console.warn(`⚠️ Failed to upload ${att.filename}:`, err.message);
    }
  }

  // BUG-2 verify: nếu yêu cầu tạo page con, kiểm tra lại ancestors thực tế.
  // Nếu chưa đúng cha -> tự re-parent; vẫn sai -> báo rõ (không báo "thành công" giả).
  let parentVerified = null;
  if (parentId) {
    parentVerified = await verifyAndFixParent(pageId, parentId, active);
  }

  // Add to registry
  addRegistryEntry({
    title,
    pageId,
    spaceKey,
    domain: active.domainId,
    url,
    sourceFile: mdFilePath,
    lastPushed: new Date().toISOString(),
    version: 1
  });

  const out = { ok: true, pageId, url, title, attachments: attachCount, domain: active.domainId };
  if (parentId) out.parentId = String(parentId);
  if (parentVerified !== null) out.parentVerified = parentVerified;
  if (warnings && warnings.length) out.warnings = warnings;
  return out;
}

// Kiểm tra page có đúng cha mong muốn không; nếu không thì re-parent.
// Trả về true nếu cuối cùng đúng cha, false nếu vẫn sai (đã cố sửa).
async function verifyAndFixParent(pageId, parentId, active) {
  try {
    const res = await makeRequest(
      `${active.url}/rest/api/content/${pageId}?expand=ancestors,version`, 'GET', null, active
    );
    if (res.status !== 200) return false;
    const page = JSON.parse(res.body);
    const ancestors = page.ancestors || [];
    const hasParent = ancestors.some(a => String(a.id) === String(parentId));
    if (hasParent) return true;

    // Re-parent: PUT với ancestors + tăng version.
    const putBody = {
      type: 'page',
      title: page.title,
      ancestors: [{ id: String(parentId) }],
      version: { number: page.version.number + 1 }
    };
    const put = await makeRequest(
      `${active.url}/rest/api/content/${pageId}`, 'PUT', putBody, active
    );
    if (put.status !== 200) return false;
    const fixed = JSON.parse(put.body);
    return (fixed.ancestors || []).some(a => String(a.id) === String(parentId));
  } catch {
    return false;
  }
}

async function updateDoc(titleOrPageId, mdFilePath, active = null) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');

  let entry = null;
  let pageId = titleOrPageId;
  let title = titleOrPageId;
  let spaceKey = null;

  // Try to find in registry
  if (isNaN(titleOrPageId)) {
    // It's a title
    entry = findRegistryByTitle(titleOrPageId, active.domainId);
    if (entry) {
      pageId = entry.pageId;
      spaceKey = entry.spaceKey;
      title = entry.title;
    }
  } else {
    // It's a pageId
    entry = findRegistryByPageId(titleOrPageId);
    if (entry) {
      pageId = entry.pageId;
      title = entry.title;
      spaceKey = entry.spaceKey;
    } else {
      // Fetch from Confluence
      try {
        const page = await getPageById(titleOrPageId, active);
        title = page.title;
        spaceKey = page.space;
      } catch (err) {
        throw new Error(`Page ${titleOrPageId} not found`);
      }
    }
  }

  const mdContent = fs.readFileSync(mdFilePath, 'utf-8');
  const baseDir = path.dirname(mdFilePath);
  const { storage, attachments, warnings } = convertMarkdown(mdContent, baseDir);

  // Update page
  const result = await updatePage(pageId, title, storage, active);
  const { version, url } = result;

  // Upload attachments
  let attachCount = 0;
  for (const att of attachments) {
    try {
      await addAttachment(pageId, att.localPath, active, att.filename);
      attachCount++;
    } catch (err) {
      console.warn(`⚠️ Failed to upload ${att.filename}:`, err.message);
    }
  }

  // Update registry
  if (entry) {
    entry.lastPushed = new Date().toISOString();
    entry.version = version;
    addRegistryEntry(entry);
  } else {
    addRegistryEntry({
      title,
      pageId,
      spaceKey,
      domain: active.domainId,
      url,
      sourceFile: mdFilePath,
      lastPushed: new Date().toISOString(),
      version
    });
  }

  const out = { ok: true, pageId, url, version, attachments: attachCount };
  if (warnings && warnings.length) out.warnings = warnings;
  return out;
}

// ============= REGISTRY (Page Memory) =============
const REGISTRY_FILE = path.join(process.cwd(), '.confluence', 'pages.json');

function loadRegistry() {
  if (!fs.existsSync(REGISTRY_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(REGISTRY_FILE, 'utf-8'));
  } catch {
    return [];
  }
}

function saveRegistry(entries) {
  const dir = path.dirname(REGISTRY_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(REGISTRY_FILE, JSON.stringify(entries, null, 2));
}

function addRegistryEntry(entry) {
  const entries = loadRegistry();
  const idx = entries.findIndex(e => e.pageId === entry.pageId || (e.title === entry.title && e.domain === entry.domain));
  if (idx >= 0) {
    entries[idx] = entry;
  } else {
    entries.push(entry);
  }
  saveRegistry(entries);
}

function findRegistryByTitle(title, domain) {
  const entries = loadRegistry();
  return entries.find(e => e.title === title && (!domain || e.domain === domain));
}

function findRegistryByPageId(pageId) {
  const entries = loadRegistry();
  return entries.find(e => e.pageId === pageId);
}

// ============= MERMAID RENDER =============
const { execSync } = require('child_process');

// Tự dò đường dẫn Chrome/Chromium theo nền tảng (đa máy, không hardcode).
// Ưu tiên biến môi trường CHROME_PATH / PUPPETEER_EXECUTABLE_PATH nếu có.
function findChrome() {
  const fromEnv = process.env.PUPPETEER_EXECUTABLE_PATH || process.env.CHROME_PATH;
  if (fromEnv && fs.existsSync(fromEnv)) return fromEnv;
  const candidates = [
    // macOS
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    // Linux
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    // Windows
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
  ];
  return candidates.find(p => { try { return fs.existsSync(p); } catch { return false; } }) || null;
}

function renderMermaid(code, outPng) {
  try {
    const tmpMmd = path.join(os.tmpdir(), `diagram_${Date.now()}.mmd`);
    fs.writeFileSync(tmpMmd, code);

    const mmdc = path.join(__dirname, '..', 'node_modules', '.bin', 'mmdc');

    // Tạo puppeteer config tạm với Chrome dò được (nếu tìm thấy)
    let cfgArg = '';
    let tmpCfg = null;
    const chrome = findChrome();
    if (chrome) {
      tmpCfg = path.join(os.tmpdir(), `puppeteer_${Date.now()}.json`);
      fs.writeFileSync(tmpCfg, JSON.stringify({ executablePath: chrome, args: ['--no-sandbox'] }));
      cfgArg = ` -p "${tmpCfg}"`;
    }

    const cmd = `node "${mmdc}" -i "${tmpMmd}" -o "${outPng}"${cfgArg} -b transparent`;
    try {
      execSync(cmd, { stdio: 'pipe' });
    } catch (e) {
      // mmdc có thể báo lỗi nhưng file vẫn được tạo — kiểm tra ở dưới
    }

    try { fs.unlinkSync(tmpMmd); } catch {}
    if (tmpCfg) { try { fs.unlinkSync(tmpCfg); } catch {} }
    return fs.existsSync(outPng);
  } catch (err) {
    console.warn('⚠️ Mermaid render failed:', err.message);
    return false;
  }
}

// ============= MARKDOWN CONVERT =============
function normalizeFilename(filename) {
  return filename
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/\s+/g, '_')
    .replace(/[^a-zA-Z0-9._-]/g, '');
}

function escapeXml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function convertMarkdown(markdown, baseDir) {
  const MarkdownIt = require('markdown-it');
  const md = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: true,
  });

  const attachments = [];
  const warnings = [];   // BUG-4: gom cảnh báo (ảnh thiếu...) để báo người dùng
  const tokens = md.parse(markdown, {});
  let html = '';
  let mermaidCount = 0;

  for (const token of tokens) {
    if (token.type === 'fence') {
      const code = token.content;
      const lang = (token.info || 'plaintext').trim();

      if (lang === 'mermaid') {
        // Render mermaid -> PNG -> attachment -> ac:image
        mermaidCount++;
        const pngName = normalizeFilename(`diagram_${Date.now()}_${mermaidCount}.png`);
        const pngPath = path.join(os.tmpdir(), pngName);
        const ok = renderMermaid(code, pngPath);
        if (ok) {
          attachments.push({ filename: pngName, localPath: pngPath });
          html += `<ac:image><ri:attachment ri:filename="${escapeXml(pngName)}"/></ac:image>`;
        } else {
          // Fallback: hiển thị code mermaid trong macro code để không mất nội dung
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

  // Post-process: convert <img> tags (src/alt theo thứ tự bất kỳ)
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
    // BUG-4: ảnh local KHÔNG tồn tại -> KHÔNG để lại <img> thô (gây vỡ tài liệu).
    // Thay bằng chú thích nhẹ để giữ ngữ cảnh, và ghi cảnh báo cho người dùng.
    warnings.push(`Không tìm thấy ảnh: ${src} (đã bỏ ảnh, phần còn lại vẫn được đẩy).`);
    return `<p><em>[Thiếu ảnh: ${escapeXml(path.basename(src))}]</em></p>`;
  });

  // Confluence storage format là XHTML nghiêm ngặt: mọi thẻ void phải tự đóng.
  // markdown-it (và HTML thô trong md) có thể sinh <hr>, <br>, <img>, ... không
  // đóng -> Confluence trả 400 "expected </hr>". Chuẩn hóa tất cả ở bước cuối.
  const VOID_TAGS = ['hr', 'br', 'img', 'input', 'col', 'area', 'meta', 'link', 'source', 'wbr', 'embed', 'track', 'base'];
  for (const tag of VOID_TAGS) {
    const re = new RegExp(`<${tag}\\b([^>]*?)\\s*/?>`, 'gi');
    html = html.replace(re, (_m, attrs) => `<${tag}${attrs}/>`);
  }

  return { storage: html, attachments, warnings };
}

// ============= ATTACHMENT UPLOAD =============
async function addAttachment(pageId, filePath, active, attachName) {
  if (!active) active = getActive();
  if (!active) throw new Error('needSetup');

  return new Promise((resolve, reject) => {
    // attachName: tên đã chuẩn hóa khớp với storage XHTML (nếu có)
    const fileName = attachName || normalizeFilename(path.basename(filePath));
    const fileData = fs.readFileSync(filePath);
    const boundary = '----confluenceBoundary' + Date.now();
    const pre = Buffer.from(
      `--${boundary}\r\nContent-Disposition: form-data; name="file"; filename="${fileName}"\r\n` +
      `Content-Type: application/octet-stream\r\n\r\n`
    );
    const post = Buffer.from(`\r\n--${boundary}--\r\n`);
    const body = Buffer.concat([pre, fileData, post]);

    const url = new URL(`${active.url}/rest/api/content/${pageId}/child/attachment`);
    const protocol = url.protocol === 'https:' ? https : http;
    const req = protocol.request(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${active.token}`,
        'X-Atlassian-Token': 'no-check',
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length
      }
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => resolve({ filename: fileName, status: res.statusCode, body: data }));
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// ============= DOMAIN MANAGEMENT =============
// Với Personal Access Token (PAT) của Confluence Data Center, chỉ cần token
// (gửi qua Bearer). username là tùy chọn, chỉ lưu để tham khảo.
async function setCredentials(username, token) {
  const cfg = loadConfig() || { activeDomain: 'production', domains: {} };
  if (username !== undefined && username !== '') cfg.username = username;
  cfg.token = token;
  saveConfig(cfg);
  return { ok: true };
}

// Chỉ đặt token (đủ để xác thực với PAT) — dùng cho luồng non-tech.
async function setToken(token) {
  const cfg = loadConfig() || { activeDomain: 'production', domains: {} };
  cfg.token = token;
  saveConfig(cfg);
  return { ok: true };
}

async function addDomain(id, label, url) {
  const cfg = loadConfig() || { activeDomain: 'production', domains: {} };
  if (!cfg.domains) cfg.domains = {};
  cfg.domains[id] = { label, url };
  if (!cfg.activeDomain || Object.keys(cfg.domains).length === 1) {
    cfg.activeDomain = id;
  }
  saveConfig(cfg);
  return { ok: true, activeDomain: cfg.activeDomain };
}

async function useDomain(id) {
  const cfg = loadConfig();
  if (!cfg || !cfg.domains || !cfg.domains[id]) {
    throw new Error(`Domain ${id} not found`);
  }
  cfg.activeDomain = id;
  saveConfig(cfg);
  return { ok: true, activeDomain: id };
}

async function listDomains() {
  const cfg = loadConfig();
  if (!cfg) return { activeDomain: null, domains: [] };
  const domains = Object.entries(cfg.domains || {}).map(([id, d]) => ({
    id,
    label: d.label,
    url: d.url,
    active: id === cfg.activeDomain
  }));
  return { activeDomain: cfg.activeDomain, domains };
}

async function testConn() {
  const active = getActive();
  if (!active) throw new Error('needSetup');
  try {
    const result = await makeRequest(`${active.url}/rest/api/space?limit=1`, 'GET', null, active);
    if (result.status === 200) {
      return { ok: true, status: 200 };
    } else if (result.status === 401) {
      return { ok: false, status: 401, hint: 'Token sai hoặc hết hạn' };
    } else if (result.status === 403) {
      return { ok: false, status: 403, hint: 'Token đúng nhưng tài khoản chưa được cấp quyền dùng Confluence trên domain này — cần liên hệ bộ phận quản trị Confluence nội bộ' };
    } else {
      return { ok: false, status: result.status, hint: 'Không thể kết nối' };
    }
  } catch (err) {
    return { ok: false, status: 0, hint: 'Lỗi mạng: ' + err.message };
  }
}

// ============= CLI HANDLER =============
const [, , command, ...args] = process.argv;

(async () => {
  try {
    switch (command) {
      case 'listSpaces':
        console.log(JSON.stringify(await listSpaces(), null, 2));
        break;

      case 'getPage':
        {
          const [spaceKey, pageTitle] = args;
          console.log(JSON.stringify(await getPageBySpaceAndTitle(spaceKey, pageTitle), null, 2));
        }
        break;

      case 'getPageById':
        {
          const [pageId] = args;
          console.log(JSON.stringify(await getPageById(pageId), null, 2));
        }
        break;

      case 'searchPages':
        {
          const query = args.join(' ');
          console.log(JSON.stringify(await searchPages(query), null, 2));
        }
        break;

      case 'createPage':
        {
          const [spaceKey, title] = args;
          const content = fs.readFileSync(0, 'utf-8');
          console.log(JSON.stringify(await createPage(spaceKey, title, content), null, 2));
        }
        break;

      case 'updatePage':
        {
          const [pageId, title] = args;
          const content = fs.readFileSync(0, 'utf-8');
          console.log(JSON.stringify(await updatePage(pageId, title, content), null, 2));
        }
        break;

      case 'updatePageByTitle':
        {
          const [spaceKey, pageTitle] = args;
          const content = fs.readFileSync(0, 'utf-8');
          console.log(JSON.stringify(await updatePageBySpaceAndTitle(spaceKey, pageTitle, content), null, 2));
        }
        break;

      case 'deletePage':
        {
          const [pageId] = args;
          console.log(JSON.stringify(await deletePage(pageId), null, 2));
        }
        break;

      case 'setCredentials':
        {
          const [username, token] = args;
          console.log(JSON.stringify(await setCredentials(username, token), null, 2));
        }
        break;

      case 'setToken':
        {
          const [token] = args;
          console.log(JSON.stringify(await setToken(token), null, 2));
        }
        break;

      case 'addDomain':
        {
          const [id, label, url] = args;
          console.log(JSON.stringify(await addDomain(id, label, url), null, 2));
        }
        break;

      case 'useDomain':
        {
          const [id] = args;
          console.log(JSON.stringify(await useDomain(id), null, 2));
        }
        break;

      case 'listDomains':
        console.log(JSON.stringify(await listDomains(), null, 2));
        break;

      case 'testConn':
        console.log(JSON.stringify(await testConn(), null, 2));
        break;

      case 'addAttachment':
        {
          const [pageId, filePath] = args;
          console.log(JSON.stringify(await addAttachment(pageId, filePath), null, 2));
        }
        break;

      case 'listPushed':
        {
          const entries = loadRegistry();
          console.log(JSON.stringify({ pages: entries }, null, 2));
        }
        break;

      case 'pushDoc':
        {
          const [spaceKey, title, mdFilePath, parentId] = args;
          const result = await pushDoc(spaceKey, title, mdFilePath, parentId || null);
          console.log(JSON.stringify(result, null, 2));
        }
        break;

      case 'updateDoc':
        {
          const [titleOrPageId, mdFilePath] = args;
          const result = await updateDoc(titleOrPageId, mdFilePath);
          console.log(JSON.stringify(result, null, 2));
        }
        break;

      case 'help':
        console.log(`
Confluence MCP Client - Full CRUD + Multi-Domain

Commands:
  Domain Management:
    setCredentials <username> <token>
      Set Confluence credentials (shared for all domains)
    addDomain <id> <label> <url>
      Add/update a Confluence domain
    useDomain <id>
      Switch to a domain
    listDomains
      List all configured domains
    testConn
      Test connection to active domain

  Page Operations:
    listSpaces
      List all spaces
    getPage <spaceKey> <pageTitle>
      Get page content by space and title
    getPageById <pageId>
      Get page content by page ID
    searchPages <query>
      Search pages by query
    createPage <spaceKey> <title> < content.html
      Create new page (pass HTML via stdin)
    updatePage <pageId> <title> < content.html
      Update page by ID
    updatePageByTitle <spaceKey> <pageTitle> < content.html
      Update page by space and title
    deletePage <pageId>
      Delete page by ID

  Document Operations (Markdown):
    pushDoc <spaceKey> <title> <file.md> [parentId]
      Push a Markdown file as a new page.
      - title rỗng ("") -> tự lấy theo tên file.
      - parentId -> tạo làm page con (tự verify ancestors sau khi tạo).
    updateDoc <title|pageId> <file.md>
      Update an existing page from a Markdown file.
    listPushed
      List documents pushed via registry.
    addAttachment <pageId> <file>
      Upload a file as attachment to a page.

Examples:
  node bin/cli.js addDomain production "Nội bộ" http://10.254.136.32:8090
  node bin/cli.js setCredentials truongph1 my-token
  node bin/cli.js testConn
  node bin/cli.js listSpaces
  node bin/cli.js pushDoc TK "" ./baocao.md 100931894   # page con, tiêu đề theo tên file
        `);
        break;

      default:
        if (!command) {
          console.log('Use: node bin/cli.js <command> [args]');
          console.log('Try: node bin/cli.js help');
          process.exit(0);
        }
        console.error(`Unknown command: ${command}`);
        console.error('Run "node bin/cli.js help" for usage');
        process.exit(1);
    }
  } catch (err) {
    if (err.message === 'needSetup') {
      console.log(JSON.stringify({ needSetup: true }, null, 2));
    } else {
      console.error('Error:', err.message);
      process.exit(1);
    }
  }
})();
