# Live Demo Guide: Evergreen Platform, Code Subtraction & Freshness System

This runbook walks through running the **Evergreen Commerce** demo live on stage or in a recorded walkthrough.

---

## 0. Pre-Flight Reset (30 Seconds Before Going Live)

Ensure the repository is at the clean `demo-baseline` snapshot where all 13 legacy/policy violations and the `2023`/`2024` Git history are intact:

```bash
git reset --hard demo-baseline
git clean -fd
```

Open these 4 files in tabs so you can show the "Before" state in seconds:
1. [`.agents/platform-targets.yaml`](file:///Users/rodydavis/Documents/antigravity/keen-davinci/.agents/platform-targets.yaml) — Your declarative support policy (`Node >= 20.12.0`, `Android minSdk 29 / targetSdk 35`, `iOS >= 17.0 / SDK 18.0`, `stale_threshold_days: 365`).
2. [`services/backend/src/hmac-signature-verifier.ts`](file:///Users/rodydavis/Documents/antigravity/keen-davinci/services/backend/src/hmac-signature-verifier.ts) — Last touched in `2023-03-15` (`1,314 days ago`), critical security code with **zero stability docs**.
3. [`apps/android/app/src/main/java/com/acme/evergreen/sync/OrderSyncService.kt`](file:///Users/rodydavis/Documents/antigravity/keen-davinci/apps/android/app/src/main/java/com/acme/evergreen/sync/OrderSyncService.kt) — Android `dataSync` foreground service missing Android 15's mandatory `onTimeout` override.
4. [`apps/ios/PrivacyInfo.xcprivacy`](file:///Users/rodydavis/Documents/antigravity/keen-davinci/apps/ios/PrivacyInfo.xcprivacy) — Empty privacy manifest that will trigger Apple App Store rejection `ITMS-91053`.

---

## Act 1: Show the Multi-Year Git History & Baseline Audit (1 Minute)

Run these commands in the terminal to show the audience what the factory is about to discover:

```bash
# 1. Show authentic multi-year commit timestamps (2023, 2024, 2026)
git log --format="%h | %cs | %s"

# 2. Run the Git Code Freshness Scanner (> 365 days untouched)
python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/freshness_scanner.py
```

**What to point out**:
- Four files haven't been updated since **March 15, 2023** (`1,314 days` old):
  - Three are true **Legacy Removal Candidates**: `legacy-csv-batch-2023.ts`, `Holiday2023Banner.kt`, and `LegacyStoreKit1Bridge.swift`.
  - One is **`hmac-signature-verifier.ts`**: it hasn't changed since 2023 because RFC 2104 HMAC-SHA256 verification is **critical, stable security code**—but because nobody documented it with `@stability stable-critical`, the scanner blocks it so no engineer or agent ever mistakes it for dead legacy code!

Now run the baseline policy audit:
```bash
python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/verify_targets_hook.py --audit
```
- Shows **13 policy violations** across Node.js redundant dependencies, duplicated DRY functions, dead exports, Android Google Play API 35 rules, and iOS App Store `ITMS-91053` rules.

---

## Act 2: Trigger the Full Evergreen Factory Pipeline (3 Minutes)

Paste this prompt into Antigravity (or click the first Suggested Prompt on the **`evergreen-factory`** plugin card):

```markdown
Run the evergreen-platform skill across Node.js, Android Jetpack Compose, and iOS SwiftUI:
1. Have intake-scout check our .agents/platform-targets.yaml policy, scan git code freshness, and correlate issues #101, #102, and #103.
2. Dispatch node-backend-worker, android-compose-worker, and ios-swiftui-worker in parallel to subtract obsolete shims/dependencies, consolidate DRY code, document stable-critical modules, and upgrade to Android API 35 and iOS 18 SDK.
3. Run the 3 read-only reviewers and verify_targets_hook.py --audit to catch any version-matrix or store-policy violations.
4. Generate FRESHNESS_REPORT.md with the before/after breakdown and Next-Horizon @remove-when table.
```

### What Happens During Execution

1. **Phase 1 — Intake & Research (`intake-scout`)**:
   - Reads [`.agents/platform-targets.yaml`](file:///Users/rodydavis/Documents/antigravity/keen-davinci/.agents/platform-targets.yaml) and correlates `issues/101-*`, `102-*`, and `103-*`.
   - Identifies that while Node `22.9.0` supports `fs.globSync` natively, `min_supported: "20.12.0"` requires a fallback tagged with `/* @remove-when: node >= 22.0.0 */`.
2. **Phase 2 — Parallel Platform Workers**:
   - **`node-backend-worker`**:
     - Evicts `node-fetch`, `uuid`, `rimraf`, `chalk`, `dotenv`, and `glob` from `services/backend/package.json` in favor of native Node APIs (`fetch`, `crypto.randomUUID()`, `fs.rmSync`, `util.styleText`, `process.loadEnvFile()`, and `fs.globSync` with a Node 20.12 fallback tagged `/* @remove-when: node >= 22.0.0 */`).
     - Extracts duplicated `formatCurrencyWithTax()` and `retryWithBackoff()` into `services/backend/src/shared/utils.ts` and deletes dead exports (`legacyXmlReportExporter`, `deprecatedV1WebhookMapper`).
     - Adds `@stability stable-critical`, `@last-verified`, and `@invariants` documentation to `hmac-signature-verifier.ts`.
   - **`android-compose-worker`**:
     - Removes obsolete `SDK_INT <= 29` branches, removes `accompanist-*` dependencies, replaces `SwipeRefresh` with Material 3 `PullToRefreshBox`, deletes dead code, bumps `targetSdk = 35`, adds `enableEdgeToEdge()`, applies `Scaffold` `innerPadding`, and adds `override fun onTimeout(startId: Int, fgsType: Int)` to `OrderSyncService.kt`.
   - **`ios-swiftui-worker`**:
     - Removes `#available(iOS 15/16)` branches, deletes `LegacyReceiptView`, migrates `OrderViewModel` to `@Observable`, upgrades `NavigationView` to `NavigationStack`, guards `.tabViewStyle(.sidebarAdaptable)` with `#available(iOS 18.0, *)` + `// @remove-when: ios >= 18.0`, and populates `PrivacyInfo.xcprivacy` with `CA92.1` and `35F9.1`.
3. **Phase 3 — Read-Only Reviewer & Hook Verification**:
   - The three read-only reviewers (`node-runtime-and-freshness-reviewer`, `android-play-and-compose-reviewer`, `ios-appstore-and-swiftui-reviewer`) audit the changes without write permissions.
   - `verify_targets_hook.py --audit` confirms all 13 violations are resolved (`STATUS: PASS`).

---

## Act 3: Inspect the Final Results & `FRESHNESS_REPORT.md` (1 Minute)

Run the verification commands after the factory finishes:

```bash
# 1. Confirm all Node.js unit tests pass after stdlib migration & DRY extraction
node --test services/backend/tests/backend.test.ts

# 2. Confirm all 13 policy & store compliance checks pass
python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/verify_targets_hook.py --audit

# 3. Inspect the updated Git Freshness & @remove-when horizon output
python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/freshness_scanner.py
```

Open the generated **`FRESHNESS_REPORT.md`** to show:
- **Legacy Candidates Recommended for Removal** (`legacy-csv-batch-2023.ts`, `Holiday2023Banner.kt`, `LegacyStoreKit1Bridge.swift` — untouched since `2023-03-15`).
- **Protected Stable-Critical Modules** (`hmac-signature-verifier.ts` — untouched since `2023-03-15`, now documented with `@stability stable-critical` and `@invariants`).
- **Next-Horizon Removal Table** (`@remove-when: node >= 22.0.0` and `@remove-when: ios >= 18.0` ready to be automatically deleted as soon as `.agents/platform-targets.yaml` advances).

---

## Bonus Demo: Show the Pre-Commit Hook Blocking a Bad Commit Live

Want to show the deterministic `hooks.json` guardrail (`PreToolUse`) in action by itself?
1. Reset to `demo-baseline`:
   ```bash
   git reset --hard demo-baseline
   ```
2. Ask the agent:
   ```markdown
   Stage a trivial comment in README.md and run git commit -m "test commit"
   ```
3. Watch `.agents/plugins/evergreen-factory/hooks.json` intercept `run_command` (`git commit`) via `verify_targets_hook.py --pre-tool-hook` and **hard-block the commit** with the exact list of 13 platform, store-policy, and freshness violations!
