#!/usr/bin/env node
/**
 * Trình cài đặt một-lệnh cho Confluence Skill.
 *
 * Chạy:  node setup.js
 *
 * Tự động:
 *  1. Kiểm tra Node + Chrome (cảnh báo tiếng Việt nếu thiếu).
 *  2. npm install (cài máy chạy).
 *  3. Điền sẵn 2 domain Confluence vào ~/.confluence-vds-skill/domains.json
 *     (KHÔNG điền token — mỗi người dùng token riêng, Claude sẽ hỏi qua chat).
 *  4. Copy SKILL.md vào ~/.claude/skills/confluence-vds-skill/ để Claude tự nạp.
 *  5. In hướng dẫn bước tiếp theo.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

const PKG_DIR = __dirname;
const HOME = os.homedir();

// Cấu hình domain mặc định của công ty (điền sẵn để người dùng không cần biết IP)
const DEFAULT_DOMAINS = {
  production: { label: 'Nội bộ sản xuất', url: 'http://10.254.136.32:8090' },
  partner: { label: 'Đối tác', url: 'http://10.254.136.35:8090' },
};

function log(msg) { console.log(msg); }
function step(msg) { console.log('\n▶ ' + msg); }
function ok(msg) { console.log('  ✅ ' + msg); }
function warn(msg) { console.log('  ⚠️  ' + msg); }
function fail(msg) { console.log('  ❌ ' + msg); }

// ---- 1. Kiểm tra Node + Chrome ----
function checkNode() {
  step('Kiểm tra Node.js');
  const major = parseInt(process.versions.node.split('.')[0], 10);
  if (major < 18) {
    fail(`Node.js phiên bản ${process.versions.node} quá cũ. Cần Node 18 trở lên.`);
    log('     → Cài Node mới tại: https://nodejs.org');
    process.exit(1);
  }
  ok(`Node.js ${process.versions.node}`);
}

function findChrome() {
  const fromEnv = process.env.PUPPETEER_EXECUTABLE_PATH || process.env.CHROME_PATH;
  if (fromEnv && fs.existsSync(fromEnv)) return fromEnv;
  const candidates = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/usr/bin/chromium-browser',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
  ];
  return candidates.find(p => { try { return fs.existsSync(p); } catch { return false; } }) || null;
}

function checkChrome() {
  step('Kiểm tra Google Chrome (để vẽ biểu đồ)');
  const chrome = findChrome();
  if (chrome) {
    ok('Đã tìm thấy Chrome: ' + chrome);
  } else {
    warn('Chưa tìm thấy Chrome/Chromium.');
    log('     → Biểu đồ Mermaid sẽ không vẽ được, nhưng các chức năng khác vẫn dùng tốt.');
    log('     → Cài Chrome tại: https://www.google.com/chrome/');
  }
}

// ---- 2. npm install ----
function npmInstall() {
  step('Cài đặt thư viện (npm install) — có thể mất 1–2 phút');
  if (fs.existsSync(path.join(PKG_DIR, 'node_modules'))) {
    ok('node_modules đã có sẵn, bỏ qua.');
    return;
  }
  try {
    execSync('npm install', { cwd: PKG_DIR, stdio: 'inherit' });
    ok('Đã cài xong thư viện.');
  } catch (e) {
    fail('npm install thất bại: ' + e.message);
    process.exit(1);
  }
}

// ---- 3. Điền sẵn domain config ----
function writeDomainConfig() {
  step('Thiết lập domain Confluence');
  const cfgDir = path.join(HOME, '.confluence-vds-skill');
  const cfgFile = path.join(cfgDir, 'domains.json');
  if (!fs.existsSync(cfgDir)) fs.mkdirSync(cfgDir, { recursive: true });

  let cfg;
  if (fs.existsSync(cfgFile)) {
    // Giữ lại token/username cũ nếu đã có, chỉ bổ sung domain còn thiếu
    try { cfg = JSON.parse(fs.readFileSync(cfgFile, 'utf-8')); } catch { cfg = null; }
  }
  if (!cfg || typeof cfg !== 'object') {
    cfg = { activeDomain: 'production', username: '', token: '', domains: {} };
  }
  if (!cfg.domains) cfg.domains = {};
  for (const [id, d] of Object.entries(DEFAULT_DOMAINS)) {
    if (!cfg.domains[id]) cfg.domains[id] = d;
  }
  if (!cfg.activeDomain || !cfg.domains[cfg.activeDomain]) cfg.activeDomain = 'production';

  fs.writeFileSync(cfgFile, JSON.stringify(cfg, null, 2));
  ok('Đã điền sẵn 2 domain: Nội bộ sản xuất + Đối tác.');
  if (cfg.token) {
    ok('Token đã có sẵn từ trước.');
  } else {
    log('     ℹ️  Token chưa có — Claude sẽ hỏi bạn lần đầu sử dụng (mỗi người dùng token riêng).');
  }
}

// ---- 4. Copy SKILL.md vào ~/.claude/skills/ ----
function installSkill() {
  step('Cài Skill cho Claude Code');
  const srcSkillDir = path.join(PKG_DIR, 'skills', 'confluence-vds-skill');
  const srcSkill = path.join(srcSkillDir, 'SKILL.md');
  if (!fs.existsSync(srcSkill)) {
    fail('Không tìm thấy SKILL.md trong package. File có thể đã bị xóa.');
    process.exit(1);
  }

  const dstDir = path.join(HOME, '.claude', 'skills', 'confluence-vds-skill');
  fs.mkdirSync(path.join(dstDir, 'references'), { recursive: true });

  // Copy SKILL.md
  copyFile(srcSkill, path.join(dstDir, 'SKILL.md'));
  // Copy references nếu có
  const srcRef = path.join(srcSkillDir, 'references', 'usage-vi.md');
  if (fs.existsSync(srcRef)) copyFile(srcRef, path.join(dstDir, 'references', 'usage-vi.md'));

  ok('Đã cài Skill vào: ' + dstDir);
  log('     ℹ️  Claude Code sẽ tự nhận skill này (mở mới hoặc khởi động lại Claude).');
}

function copyFile(src, dst) {
  fs.copyFileSync(src, dst);
}

// ---- 5. Hướng dẫn cuối ----
function printNext() {
  console.log('\n' + '='.repeat(56));
  console.log('🎉 CÀI ĐẶT XONG!');
  console.log('='.repeat(56));
  console.log('\nBước tiếp theo (chỉ cần CHAT, không gõ lệnh):');
  console.log('\n  1. Mở (hoặc khởi động lại) Claude Code.');
  console.log('  2. Gõ:  "Kết nối Confluence sản xuất giúp tôi"');
  console.log('  3. Claude sẽ hỏi tên đăng nhập + API token của bạn.');
  console.log('     (Lấy token tại: Confluence → Settings → Personal Access Tokens)');
  console.log('  4. Sau đó cứ chat: "đẩy file báo cáo này lên Confluence", v.v.');
  console.log('\nGặp khó? Mở file SETUP.md để xem hướng dẫn có hình.\n');
}

// ---- Main ----
(function main() {
  console.log('╔' + '═'.repeat(54) + '╗');
  console.log('║  Cài đặt Confluence Skill                            ║');
  console.log('╚' + '═'.repeat(54) + '╝');

  checkNode();
  checkChrome();
  npmInstall();
  writeDomainConfig();
  installSkill();
  printNext();
})();
