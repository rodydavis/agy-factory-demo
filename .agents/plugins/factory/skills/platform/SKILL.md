---
name: platform
description: >-
  Orchestrates the 5-Phase Software Factory assembly line across Node.js Backend, Android
  Jetpack Compose, and iOS SwiftUI. Searches upstream docs, runs the Git code freshness
  scanner (> 365 days), dispatches parallel Git worktree workers, enforces read-only Jidoka
  inspector gates (Andon cord), applies Poka-Yoke self-correction to skills/worker prompts,
  and generates FRESHNESS_REPORT.md + walkthrough.md with human escalation on legacy candidates.
---

# Software Factory Line: Platform Modernization, Subtraction & Freshness (`platform`)

Follow this 5-phase Software Factory workflow whenever asked to run a platform sweep, modernize SDKs, subtract legacy shims/dependencies, or audit code freshness.

## Phase 1: Automated Intake & Git Freshness Scan

1. Read [`.agents/platform-targets.yaml`](.agents/platform-targets.yaml) to load the active support window (`node_backend`, `android_compose`, `ios_swiftui`, and `code_freshness.stale_threshold_days`).
2. Run the Git Code Freshness Scanner to inspect commit timestamps across all source files:
   ```bash
   python3 .agents/plugins/factory/skills/platform/scripts/freshness_scanner.py
   ```
3. Run the baseline target audit to see current policy and store compliance gaps:
   ```bash
   python3 .agents/plugins/factory/skills/platform/scripts/verify_targets_hook.py --audit
   ```
4. Invoke `intake-scout` (or perform web search via `search_web`) to cross-reference Node.js 20.12/22 LTS built-in APIs, Android 15 (API 35) foreground service & edge-to-edge rules, and Apple iOS 18 App Store `PrivacyInfo.xcprivacy` required reason codes against `issues/*.md`.

## Phase 2: Parallel Git Worktree Builders

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

## Phase 3: Read-Only Jidoka Inspectors (`commandExecutionPolicy: off`) & Andon Cord

Invoke the three read-only Jidoka audit stations (`node-runtime-and-freshness-reviewer`, `android-play-and-compose-reviewer`, `ios-appstore-and-swiftui-reviewer`) and run:
```bash
python3 .agents/plugins/factory/skills/platform/scripts/verify_targets_hook.py --audit
```
- **Jidoka Step 1 & 2 — Detect & Stop the Line (Andon Cord)**: When any Jidoka inspector returns `STATUS: BLOCKED` (such as `android-play-and-compose-reviewer` flagging `❌ Security Blocker: .ShareReceiver contains an <intent-filter> without an explicit android:exported declaration` in the **Google Play Pre-Submission Audit Report**), **halt the line immediately** so defective code never moves downstream.

## Phase 4: Self-Correcting Line — Fix & Poka-Yoke (ポカヨケ) Upgrade

Whenever a Jidoka inspector pulls the Andon cord in Phase 3, execute both steps of Taiichi Ohno's remediation loop:
1. **Jidoka Step 3 — Correct the Condition (Fix in Worktree)**:
   - Patch the immediate defect in the source tree (e.g., add `android:exported="false"` to `<receiver android:name=".ShareReceiver">` in `apps/android/app/src/main/AndroidManifest.xml`).
2. **Jidoka Step 4 — Poka-Yoke (Mistake-Proof the Line)**:
   - Instead of only patching the output code, **upgrade the worker prompt (`.agents/plugins/factory/agents/android-compose-worker.md`) and this skill (`.agents/plugins/factory/skills/platform/SKILL.md`)** to explicitly require verifying `android:exported` on all `<activity>`, `<service>`, and `<receiver>` components with `<intent-filter>` in `AndroidManifest.xml`.
   - Re-run `verify_targets_hook.py --audit` and confirm `STATUS: PASS`.

## Phase 5: Verified Output (`FRESHNESS_REPORT.md` + `walkthrough.md`) & Human Escalation

1. Generate `FRESHNESS_REPORT.md` at the repository root and `walkthrough.md` in the conversation artifact directory containing:
   - **Net Codebase Impact** (lines removed, dependencies evicted, DRY functions unified, store compliance status).
   - **Jidoka & Poka-Yoke Audit Log** (what defect pulled the Andon cord, how it was fixed, and which `.agents/` worker/skill files were upgraded).
   - **Git Code Freshness Audit** (`> 365 days` untouched files split into **A. Legacy Candidates Recommended for Removal** vs **B. Critical Infrequently-Changed Code with `@stability stable-critical` Documentation**).
   - **"Next Horizon" Recommendations Table** listing every `@remove-when` annotation in the repo and the exact future version bump in `.agents/platform-targets.yaml` that will unlock its removal.
2. **Human Escalation (`ask_question` / Remote Control)**:
   - For the 3 confirmed stale `2023-03-15` legacy removal candidates (`legacy-csv-batch-2023.ts`, `Holiday2023Banner.kt`, `LegacyStoreKit1Bridge.swift`), escalate the final architectural decision (Delete now vs. Keep for manual review) via `ask_question`.
