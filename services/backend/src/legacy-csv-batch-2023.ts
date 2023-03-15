import fs from 'node:fs';

export interface LegacyCsvRow {
  sku: string;
  title: string;
  priceCents: number;
}

export function parseLegacyFtpCatalogCsv(csvFilePath: string): LegacyCsvRow[] {
  const raw = fs.readFileSync(csvFilePath, 'utf8');
  const lines = raw.trim().split('\n').slice(1);
  return lines.map((line) => {
    const [sku, title, priceStr] = line.split(',');
    return {
      sku: sku.trim(),
      title: title.trim(),
      priceCents: Number.parseInt(priceStr, 10) || 0,
    };
  });
}
