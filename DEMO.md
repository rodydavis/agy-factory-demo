# Live Demo Guide: Becoming a Software Factory with Antigravity

This runbook walks through running the **Evergreen Commerce Software Factory** demo live on stage or in a recorded walkthrough, aligned 1-for-1 with the **Becoming a Software Factory with Antigravity** slides (`Slides 01–33`).

---

## 0. Pre-Flight Reset (30 Seconds Before Going Live)

Ensure the repository is at the clean `demo-baseline` snapshot where all 14 legacy/policy violations and the `2023`/`2024` Git history are intact:

```bash
git reset --hard demo-baseline
git clean -fd
```

Open these 4 files in tabs so you can show the "Before" state in seconds:
1. [`.agents/platform-targets.yaml`](.agents/platform-targets.yaml) — Your declarative support policy (`Node >= 20.12.0`, `Android minSdk 29 / targetSdk 35`, `iOS >= 17.0 / SDK 18.0`, `stale_threshold_days: 365`).
2. [`services/backend/src/hmac-signature-verifier.ts`](services/backend/src/hmac-signature-verifier.ts) — Last touched in `2023-03-15` (`1,314 days ago`), critical security code with **zero stability docs**.
3. [`apps/android/app/src/main/AndroidManifest.xml`](apps/android/app/src/main/AndroidManifest.xml) — Declares `.sync.OrderSyncService` (`dataSync`) and `.ShareReceiver` with an `<intent-filter>` **missing `android:exported`** (matching **Slide 28**).
4. [`apps/ios/PrivacyInfo.xcprivacy`](apps/ios/PrivacyInfo.xcprivacy) — Empty privacy manifest that will trigger Apple App Store rejection `ITMS-91053`.

---

## Act 1: Show the Multi-Year Git History & Baseline Audit (1 Minute)

Run these commands in the terminal (or ask Antigravity to run Act 1) to show the audience what the factory is about to discover:

```bash
# 1. Show authentic multi-year commit timestamps (2023, 2024, 2026)
git log --format="%h | %cs | %s"

# 2. Run the Git Code Freshness Scanner (> 365 days untouched)
python3 .agents/plugins/factory/skills/platform/scripts/freshness_scanner.py
```

**What to point out**:
- Four files haven't been updated since **March 15, 2023** (`1,314 days` old):
  - Three are true **Legacy Removal Candidates**: `legacy-csv-batch-2023.ts`, `Holiday2023Banner.kt`, and `LegacyStoreKit1Bridge.swift`.
  - One is **`hmac-signature-verifier.ts`**: it hasn't changed since 2023 because RFC 2104 HMAC-SHA256 verification is **critical, stable security code**—but because nobody documented it with `@stability stable-critical`, the scanner blocks it so no engineer or agent ever mistakes it for dead legacy code!

Now run the baseline policy audit:
```bash
python3 .agents/plugins/factory/skills/platform/scripts/verify_targets_hook.py --audit
```
- Shows **14 policy & security violations** across Node.js redundant dependencies, duplicated DRY functions, dead exports, Android Google Play API 35 rules, `.ShareReceiver` missing `android:exported`, and iOS App Store `ITMS-91053` rules.

---

## Act 2: Trigger the Full Software Factory Pipeline — Jidoka, Andon & Poka-Yoke (3 Minutes)

Paste this prompt into Antigravity (or click the first Suggested Prompt on the **`factory`** plugin card):

```markdown
Run the platform skill across Node.js, Android Jetpack Compose, and iOS SwiftUI:
1. Phase 1 (Intake): Have intake-scout check .agents/platform-targets.yaml, scan git code freshness, and correlate issues #101, #102, and #103.
2. Phase 2 (Parallel Worktree Workers): Dispatch node-backend-worker, android-compose-worker, and ios-swiftui-worker in parallel to subtract obsolete shims/dependencies, consolidate DRY code, document stable-critical modules, and upgrade to Android API 35 and iOS 18 SDK.
3. Phase 3 (Jidoka Inspectors): Run the 3 read-only Jidoka inspectors (commandExecutionPolicy: off). When android-play-and-compose-reviewer detects the .ShareReceiver <intent-filter> missing android:exported in AndroidManifest.xml, pull the Andon cord with the Google Play Pre-Submission Audit Report (STATUS: BLOCKED).
4. Phase 4 (Self-Correction & Poka-Yoke): Fix .ShareReceiver in AndroidManifest.xml AND apply a Poka-Yoke upgrade to .agents/plugins/factory/agents/android-compose-worker.md and .agents/plugins/factory/skills/platform/SKILL.md so the line never repeats this defect, then re-verify with verify_targets_hook.py --audit.
5. Phase 5 (Verified Output & Human Escalation): Generate FRESHNESS_REPORT.md and walkthrough.md, and escalate the decision on the 3 stale 2023 legacy removal candidates via ask_question.
```

### What Happens During Execution (Mapped to Slides 20, 25–31)

1. **Phase 1 — Intake & Research (`intake-scout`, `model: flash`)**:
   - Reads [`.agents/platform-targets.yaml`](.agents/platform-targets.yaml) and correlates `issues/101-*`, `102-*`, and `103-*`.
   - Identifies that while Node `22.9.0` supports `fs.globSync` natively, `min_supported: "20.12.0"` requires a fallback tagged with `/* @remove-when: node >= 22.0.0 */`.
2. **Phase 2 — Parallel Git Worktree Workers (`commandExecutionPolicy: sandbox`)**:
   - **`node-backend-worker`**: Evicts `node-fetch`, `uuid`, `rimraf`, `chalk`, `dotenv`, and `glob` from `package.json`, extracts duplicated `formatCurrencyWithTax()` and `retryWithBackoff()` into `services/backend/src/shared/utils.ts`, deletes dead exports, and documents `hmac-signature-verifier.ts` with `@stability stable-critical`.
   - **`android-compose-worker`**: Removes obsolete `SDK_INT <= 29` branches, removes `accompanist-*` dependencies, replaces `SwipeRefresh` with Material 3 `PullToRefreshBox`, bumps `targetSdk = 35`, adds `enableEdgeToEdge()`, applies `Scaffold` `innerPadding`, and implements `OrderSyncService.onTimeout(int, int)`. *(Note: Because Issue #102 didn't mention `.ShareReceiver`, `AndroidManifest.xml` still has `.ShareReceiver` without `android:exported`!)*
   - **`ios-swiftui-worker`**: Removes `#available(iOS 15/16)` branches, deletes `LegacyReceiptView`, migrates `OrderViewModel` to `@Observable`, upgrades `NavigationView` to `NavigationStack`, guards `.tabViewStyle(.sidebarAdaptable)` with `// @remove-when: ios >= 18.0`, and populates `PrivacyInfo.xcprivacy` with `CA92.1` and `35F9.1`.
3. **Phase 3 — Read-Only Jidoka Inspectors (`commandExecutionPolicy: off`) Pull the Andon Cord (`Slides 20 & 28`)**:
   - `node-runtime-and-freshness-reviewer` and `ios-appstore-and-swiftui-reviewer` report `STATUS: PASS`.
   - **`android-play-and-compose-reviewer`** outputs the **Google Play Pre-Submission Audit Report** from **Slide 28** and **pulls the Andon cord (`Audit Status: ❌ BLOCKED`)**:
     - `❌ Security Blocker: .ShareReceiver contains an <intent-filter> without an explicit android:exported declaration.`
4. **Phase 4 — Self-Correcting Line: Fix + Poka-Yoke Upgrade (`Slides 20 & 31`)**:
   - **Step 3 of Jidoka (Correct the Condition)**: Adds `android:exported="false"` to `.ShareReceiver` in `AndroidManifest.xml`.
   - **Step 4 of Jidoka (Poka-Yoke — Mistake-Proof the Line)**: Updates `.agents/plugins/factory/agents/android-compose-worker.md` and `.agents/plugins/factory/skills/platform/SKILL.md` so the worker station permanently checks `<intent-filter>` `android:exported` on every future run!
   - Re-runs `verify_targets_hook.py --audit` $\rightarrow$ **`STATUS: PASS`** across all 14 checks!
5. **Phase 5 — Verified Output (`FRESHNESS_REPORT.md` + `walkthrough.md`) & Human Escalation (`Slide 31`)**:
   - Writes `FRESHNESS_REPORT.md` and `walkthrough.md`, then pauses cleanly via `ask_question` to let the human decide whether to delete or keep the 3 stale `2023-03-15` legacy removal candidates (`legacy-csv-batch-2023.ts`, `Holiday2023Banner.kt`, `LegacyStoreKit1Bridge.swift`).

---

## Act 3: Inspect the Final Results, Poka-Yoke Diff & `FRESHNESS_REPORT.md` (1 Minute)

Run the verification commands after the factory finishes:

```bash
# 1. Confirm all Node.js unit tests pass after stdlib migration & DRY extraction
node --test services/backend/tests/backend.test.ts

# 2. Confirm all 14 policy, security & store compliance checks pass
python3 .agents/plugins/factory/skills/platform/scripts/verify_targets_hook.py --audit

# 3. Inspect the updated Git Freshness & @remove-when horizon output
python3 .agents/plugins/factory/skills/platform/scripts/freshness_scanner.py

# 4. Show how the factory upgraded its own worker prompt (Poka-Yoke!)
git diff .agents/plugins/factory/agents/android-compose-worker.md
```

---

## Bonus Demo 1: Show the Pre-Commit Hook Blocking a Bad Commit Live (`Slide 17`)

1. Reset to `demo-baseline`:
   ```bash
   git reset --hard demo-baseline
   ```
2. Ask the agent:
   ```markdown
   Stage a trivial comment in README.md and run git commit -m "test commit"
   ```
3. Watch `.agents/plugins/factory/hooks.json` intercept `run_command` (`git commit`) via `verify_targets_hook.py --pre-tool-hook` and **hard-block the commit** with the exact list of 14 platform, security, store-policy, and freshness violations!

---

## Bonus Demo 2: Interactive `/grill-me` Style Onboarding (`onboarding`)

Paste this prompt into Antigravity:

```markdown
Run onboarding to interview me, configure .agents/platform-targets.yaml, and customize our factory skills.
```
