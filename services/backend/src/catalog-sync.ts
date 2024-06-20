import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { parseLegacyFtpCatalogCsv } from './legacy-csv-batch-2023.ts';

// Legacy npm wrapper shims simulating pre-Node 20.12/22 external packages
// (chalk, uuid, dotenv, glob, node-fetch) listed in package.json
const chalkGreen = (text: string) => `\x1b[32m${text}\x1b[39m`;
const uuidv4 = () =>
  'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (crypto.randomBytes(1)[0] % 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });

export function loadLegacyDotenv(envFilePath: string): void {
  if (!fs.existsSync(envFilePath)) return;
  const content = fs.readFileSync(envFilePath, 'utf8');
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eqIdx = trimmed.indexOf('=');
    if (eqIdx > 0) {
      const key = trimmed.slice(0, eqIdx).trim();
      const val = trimmed.slice(eqIdx + 1).trim();
      process.env[key] = val;
    }
  }
}

export function legacyGlobJsonFiles(dirPath: string): string[] {
  if (!fs.existsSync(dirPath)) return [];
  return fs
    .readdirSync(dirPath)
    .filter((file) => file.endsWith('.json'))
    .map((file) => path.join(dirPath, file));
}

// NON-DRY VIOLATION: Exact duplicate of formatCurrencyWithTax in report-exporter.ts
export function formatCurrencyWithTax(
  amountCents: number,
  taxRate: number,
  currency: string = 'USD'
): string {
  if (amountCents < 0) {
    throw new Error('Amount cannot be negative');
  }
  const subtotal = amountCents / 100;
  const taxAmount = subtotal * taxRate;
  const total = Math.round((subtotal + taxAmount) * 100) / 100;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(total);
}

// NON-DRY VIOLATION: Exact duplicate of retryWithBackoff in report-exporter.ts
export async function retryWithBackoff<T>(
  operation: () => Promise<T>,
  maxAttempts: number = 3,
  baseDelayMs: number = 50
): Promise<T> {
  let attempt = 0;
  let lastError: unknown;
  while (attempt < maxAttempts) {
    try {
      return await operation();
    } catch (err) {
      lastError = err;
      attempt += 1;
      if (attempt >= maxAttempts) break;
      const delay = baseDelayMs * Math.pow(2, attempt - 1);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }
  throw lastError;
}

export async function syncCatalogBatch(
  catalogDir: string,
  useLegacyCsvFlag: boolean = false
): Promise<{ batchId: string; count: number; formattedSample: string }> {
  loadLegacyDotenv('.env');
  const batchId = uuidv4();

  if (useLegacyCsvFlag) {
    const rows = parseLegacyFtpCatalogCsv(path.join(catalogDir, 'legacy.csv'));
    return {
      batchId,
      count: rows.length,
      formattedSample: formatCurrencyWithTax(rows[0]?.priceCents ?? 0, 0.0825),
    };
  }

  const files = legacyGlobJsonFiles(catalogDir);
  console.log(chalkGreen(`[CatalogSync] Syncing ${files.length} files in batch ${batchId}`));

  return {
    batchId,
    count: files.length,
    formattedSample: formatCurrencyWithTax(1999, 0.0825),
  };
}
