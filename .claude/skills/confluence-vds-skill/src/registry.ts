import * as fs from 'fs';
import * as path from 'path';

export interface RegistryEntry {
  title: string;
  pageId: string;
  spaceKey: string;
  domain: string;
  url: string;
  sourceFile: string;
  lastPushed: string;
  version: number;
}

const REGISTRY_FILE = path.join(process.cwd(), '.confluence', 'pages.json');

export function loadRegistry(): RegistryEntry[] {
  if (!fs.existsSync(REGISTRY_FILE)) return [];
  try {
    return JSON.parse(fs.readFileSync(REGISTRY_FILE, 'utf-8'));
  } catch {
    return [];
  }
}

export function saveRegistry(entries: RegistryEntry[]): void {
  const dir = path.dirname(REGISTRY_FILE);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(REGISTRY_FILE, JSON.stringify(entries, null, 2));
}

export function addEntry(entry: RegistryEntry): void {
  const entries = loadRegistry();
  const idx = entries.findIndex(e => e.pageId === entry.pageId || (e.title === entry.title && e.domain === entry.domain));
  if (idx >= 0) {
    entries[idx] = entry;
  } else {
    entries.push(entry);
  }
  saveRegistry(entries);
}

export function findByTitle(title: string, domain?: string): RegistryEntry | undefined {
  const entries = loadRegistry();
  return entries.find(e => e.title === title && (!domain || e.domain === domain));
}

export function findByPageId(pageId: string): RegistryEntry | undefined {
  const entries = loadRegistry();
  return entries.find(e => e.pageId === pageId);
}
