---
name: evergreen-platform
description: >-
  Orchestrates the Evergreen Platform, Code Subtraction & Freshness System across Node.js
  Backend, Android Jetpack Compose, and iOS SwiftUI. Searches upstream docs, runs the Git
  code freshness scanner (> 365 days), dispatches parallel Git worktree workers to remove
  obsolete shims/packages and consolidate DRY code, enforces read-only reviewer gates,
  and generates FRESHNESS_REPORT.md.
---

# Evergreen Platform, Code Subtraction & Freshness Skill

Follow this 4-phase workflow whenever asked to run an evergreen sweep, modernize platforms, subtract legacy shims/dependencies, or audit code freshness.

## Phase 1: Multi-Source Intake & Git Freshness Scan

1. Read [`.agents/platform-targets.yaml`](file:///Users/rodydavis/Documents/antigravity/keen-davinci/.agents/platform-targets.yaml) to load the active support window (`node_backend`, `android_compose`, `ios_swiftui`, and `code_freshness.stale_threshold_days`).
2. Run the Git Code Freshness Scanner to inspect commit timestamps across all source files:
   ```bash
   python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/freshness_scanner.py
   ```
3. Run the baseline target audit to see current policy and store compliance gaps:
   ```bash
   python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/verify_targets_hook.py --audit
   ```
4. Invoke `intake-scout` (or perform web search via `search_web`) to cross-reference Node.js 20.12/22 LTS built-in APIs, Android 15 (API 35) foreground service & edge-to-edge rules, and Apple iOS 18 App Store `PrivacyInfo.xcprivacy` required reason codes against `issues/*.md`.

## Phase 2: Parallel Worktree Builders

Invoke the three platform workers concurrently in isolated workspaces (`Workspace: "share"`):
- **`node-backend-worker`** (`services/backend/**`):
  - Evict redundant npm dependencies (`node-fetch`, `uuid`, `rimraf`, `chalk`, `dotenv`, `glob`) in favor of built-in Node APIs (`fetch`, `crypto.randomUUID`, `fs.rmSync`, `util.styleText`, `process.loadEnvFile`, `fs.globSync` with a Node 20.12 fallback annotated `/* @remove-when: node >= 22.0.0 */`).
  - Consolidate duplicated `formatCurrencyWithTax` and `retryWithBackoff` into `services/backend/src/shared/utils.ts` and remove dead exports (`legacyXmlReportExporter`, `deprecatedV1WebhookMapper`).
  - Add `@stability stable-critical`, `@last-verified`, and `@invariants` header documentation to `services/backend/src/hmac-signature-verifier.ts`.
- **`android-compose-worker`** (`apps/android/**`):
  - Remove obsolete `Build.VERSION.SDK_INT` checks for API levels `<= 29`, remove deprecated `accompanist-*` dependencies, and delete dead code (`legacySqliteMigration2021`, `LegacyXmlReceiptBridge`).
  - Upgrade `targetSdk = 35`, call `enableEdgeToEdge()`, consume `Scaffold` `innerPadding` in `CatalogScreen.kt`, and implement `override fun onTimeout(startId: Int, fgsType: Int)` in `OrderSyncService.kt`.
- **`ios-swiftui-worker`** (`apps/ios/**`):
  - Remove `#available(iOS 15.0, *)` and `#available(iOS 16.0, *)` branches, delete dead `LegacyReceiptView`, migrate `OrderViewModel` to `@Observable`, replace `NavigationView`/`.foregroundColor()`/`.cornerRadius()`, guard iOS 18 `.tabViewStyle(.sidebarAdaptable)` with `// @remove-when: ios >= 18.0`, and add `CA92.1` & `35F9.1` to `PrivacyInfo.xcprivacy`.

## Phase 3: Read-Only Reviewer Gate

Invoke the three read-only reviewers (`node-runtime-and-freshness-reviewer`, `android-play-and-compose-reviewer`, `ios-appstore-and-swiftui-reviewer`) and run:
```bash
python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/verify_targets_hook.py --audit
```
If any reviewer or check reports `BLOCKED`, remediate the violation before proceeding.

## Phase 4: Generate `FRESHNESS_REPORT.md`

Generate `FRESHNESS_REPORT.md` at the repository root containing:
1. **Net Codebase Impact** (lines removed, dependencies evicted, DRY functions unified, store compliance status).
2. **Git Code Freshness Audit** (`> 365 days` untouched files split into **A. Legacy Candidates Recommended for Removal** vs **B. Critical Infrequently-Changed Code with `@stability stable-critical` Documentation**).
3. **"Next Horizon" Recommendations Table** listing every `@remove-when` annotation in the repo and the exact future version bump in `.agents/platform-targets.yaml` that will unlock its removal.
