import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

// Legacy rimraf / uuid / chalk shims simulating external packages in package.json
const chalkYellow = (text: string) => `\x1b[33m${text}\x1b[39m`;
const uuidv4 = () =>
  'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (crypto.randomBytes(1)[0] % 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });

function legacyRimrafSync(targetDir: string): void {
  if (!fs.existsSync(targetDir)) return;
  for (const entry of fs.readdirSync(targetDir)) {
    const fullPath = path.join(targetDir, entry);
    if (fs.lstatSync(fullPath).isDirectory()) {
      legacyRimrafSync(fullPath);
    } else {
      fs.unlinkSync(fullPath);
    }
  }
  fs.rmdirSync(targetDir);
}

// NON-DRY VIOLATION: Exact duplicate of formatCurrencyWithTax in catalog-sync.ts
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

// NON-DRY VIOLATION: Exact duplicate of retryWithBackoff in catalog-sync.ts
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

export function cleanAndExportReport(
  outputDir: string,
  revenueCents: number
): { reportId: string; totalFormatted: string } {
  // Dead legacy Node 14 branch
  if (process.env.NODE_LEGACY_V14 === 'true') {
    console.warn('Running Node 14 compatibility mode');
  }

  legacyRimrafSync(outputDir);
  fs.mkdirSync(outputDir, { recursive: true });

  const reportId = uuidv4();
  const totalFormatted = formatCurrencyWithTax(revenueCents, 0.0825);
  console.log(chalkYellow(`[ReportExporter] Generated report ${reportId}: ${totalFormatted}`));

  return { reportId, totalFormatted };
}

// DEAD CODE EXPORT #1: Unused anywhere in the repository
export function legacyXmlReportExporter(items: Array<{ id: string; cents: number }>): string {
  return `<report>${items.map((i) => `<item id="${i.id}">${i.cents}</item>`).join('')}</report>`;
}

// DEAD CODE EXPORT #2: Unused anywhere in the repository
export function deprecatedV1WebhookMapper(payload: Record<string, unknown>): string {
  return JSON.stringify({ v1: true, data: payload });
}
