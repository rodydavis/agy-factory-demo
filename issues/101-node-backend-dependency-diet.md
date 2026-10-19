# Issue #101: Node.js Backend Dependency Diet & DRY Cleanup

- **Labels**: `backend`, `maintenance`, `dependencies`
- **Target**: `services/backend` (`node >= 20.12.0` / `22.9.0` LTS)

## Problem
`services/backend/package.json` still lists 6 legacy packages (`node-fetch`, `uuid`, `rimraf`, `glob`, `chalk`, `dotenv`) and custom wrapper shims in `catalog-sync.ts` and `report-exporter.ts` that have built-in equivalents in modern Node.js LTS. Additionally, `formatCurrencyWithTax` and `retryWithBackoff` are copy-pasted across both files, and several old exports and 2023 modules appear unused or undocumented.
