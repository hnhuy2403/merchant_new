import { execSync } from 'child_process';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

/**
 * Tự dò đường dẫn Chrome/Chromium theo nền tảng (đa máy, không hardcode).
 * Ưu tiên biến môi trường PUPPETEER_EXECUTABLE_PATH / CHROME_PATH nếu có.
 */
export function findChrome(): string | null {
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

/**
 * Render Mermaid code -> PNG. Trả true nếu thành công.
 * Lỗi không ném ra ngoài (để caller bỏ qua diagram, không chặn cả tài liệu).
 */
export function renderMermaid(code: string, outPng: string): boolean {
  try {
    const tmpMmd = path.join(os.tmpdir(), `diagram_${Date.now()}.mmd`);
    fs.writeFileSync(tmpMmd, code);

    const mmdc = path.join(__dirname, '..', 'node_modules', '.bin', 'mmdc');

    let cfgArg = '';
    let tmpCfg: string | null = null;
    const chrome = findChrome();
    if (chrome) {
      tmpCfg = path.join(os.tmpdir(), `puppeteer_${Date.now()}.json`);
      fs.writeFileSync(tmpCfg, JSON.stringify({ executablePath: chrome, args: ['--no-sandbox'] }));
      cfgArg = ` -p "${tmpCfg}"`;
    }

    const cmd = `node "${mmdc}" -i "${tmpMmd}" -o "${outPng}"${cfgArg} -b transparent`;
    try {
      execSync(cmd, { stdio: 'pipe' });
    } catch {
      // mmdc có thể báo lỗi nhưng file vẫn được tạo — kiểm tra ở dưới
    }

    try { fs.unlinkSync(tmpMmd); } catch {}
    if (tmpCfg) { try { fs.unlinkSync(tmpCfg); } catch {} }
    return fs.existsSync(outPng);
  } catch (err) {
    console.warn('⚠️ Mermaid render failed:', (err as Error).message);
    return false;
  }
}
