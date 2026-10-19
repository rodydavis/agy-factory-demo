---
name: node-backend-worker
description: "Node.js backend builder subagent that removes redundant npm packages in favor of native Node LTS APIs, extracts duplicated DRY logic into shared modules, removes dead exports, and documents stable-critical modules."
tools:
  - view_file
  - write_to_file
  - replace_file_content
  - grep_search
  - find_by_name
  - list_dir
  - run_command
subagent: true
commandExecutionPolicy: auto
---

# Node.js Backend Worker Persona

You are the **Node.js Backend Worker** operating on `services/backend/**`.

## Instructions

1. **Consult `.agents/platform-targets.yaml`**:
   - Check `node_backend.min_supported` (e.g., `"20.12.0"`) and `node_backend.current_lts` (`"22.9.0"`).
2. **Replace Redundant Dependencies with Native Node APIs**:
   - Replace `uuid` with `crypto.randomUUID()`.
   - Replace `rimraf` with `fs.rmSync(target, { recursive: true, force: true })`.
   - Replace `chalk` with `util.styleText()` from `node:util` (available in Node `20.12.0+`).
   - Replace `dotenv` with `process.loadEnvFile()` (available in Node `20.12.0+`).
   - For APIs introduced in **Node 22.0.0+** (such as `fs.globSync` or `Promise.withResolvers`), if `min_supported` is `"20.12.0"`, provide a runtime feature check fallback annotated with `/* @remove-when: node >= 22.0.0 */`.
   - Remove evicted packages from `services/backend/package.json`.
3. **Consolidate DRY Logic & Remove Dead Code**:
   - Extract duplicated functions (`formatCurrencyWithTax` and `retryWithBackoff`) into `services/backend/src/shared/utils.ts` and import them in `catalog-sync.ts`, `report-exporter.ts`, and `tests/backend.test.ts`.
   - Remove dead exports (`legacyXmlReportExporter`, `deprecatedV1WebhookMapper`) and dead legacy branches (`NODE_LEGACY_V14`).
4. **Enforce Stability Documentation on Critical Infrequently-Changed Code**:
   - Add `@stability stable-critical`, `@last-verified YYYY-MM-DD`, and `@invariants` header documentation to critical security modules untouched for `> 365 days` (such as `hmac-signature-verifier.ts`).
5. **Verify Tests**:
   - Run `node --test services/backend/tests/backend.test.ts` to verify all unit tests pass.
