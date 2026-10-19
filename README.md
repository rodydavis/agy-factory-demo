# Evergreen Commerce — Multi-Platform Code Subtraction & Freshness Demo

**Evergreen Commerce** is a multi-platform reference monorepo (**Node.js Backend**, **Android Jetpack Compose**, and **iOS SwiftUI**) paired with the **`evergreen-factory` Antigravity Plugin** ([`.agents/plugins/evergreen-factory`](file:///Users/rodydavis/Documents/antigravity/keen-davinci/.agents/plugins/evergreen-factory)).

It demonstrates how an autonomous **Software Factory** continuously:
1. **Reads a Declarative Support Policy** ([`.agents/platform-targets.yaml`](file:///Users/rodydavis/Documents/antigravity/keen-davinci/.agents/platform-targets.yaml)) defining minimum Node.js LTS versions, Android `minSdk` / Google Play `targetSdk`, iOS `min_os_version` / App Store SDK targets, and Git staleness thresholds (`stale_threshold_days: 365`).
2. **Searches Upstream Documentation & Scans Git History**: Cross-references Node.js LTS built-ins, Google Play API 35 rules, and Apple App Store `ITMS-91053` privacy manifest requirements while scanning `git log` commit dates to distinguish **forgotten legacy code** from **battle-tested, critical code that changes infrequently** (`@stability stable-critical`).
3. **Executes Parallel Git Worktree Workers**: Evicts redundant third-party dependencies (`node-fetch`, `uuid`, `rimraf`, `chalk`, `dotenv`, `glob`, `accompanist-*`), deletes obsolete OS version checks (`SDK_INT <= 29`, `#available(iOS 15/16)`), consolidates duplicated (non-DRY) logic, removes dead code, and adopts modern platform APIs.
4. **Enforces Read-Only Reviewer Gates & Deterministic Hooks**: Blocks merges when a worker adopts an API newer than `min_supported` without a fallback (`@remove-when`), misses Android 15's mandatory `Service.onTimeout()` / `enableEdgeToEdge()`, misses iOS `PrivacyInfo.xcprivacy` required reason codes (`CA92.1`, `35F9.1`), or leaves a critical old module undocumented.
5. **Publishes a Codebase Freshness Report (`FRESHNESS_REPORT.md`)**: Surfaces stale legacy removal candidates, verifies `@stability stable-critical` headers on critical infrastructure, and tracks `@remove-when` annotations for the next version horizon.

---

## Repository Structure

```text
.
├── README.md                                      # Project overview & architecture
├── DEMO.md                                        # Step-by-step live demo presenter guide
├── GEMINI.md                                      # Workspace rules enforcing platform-targets.yaml
├── .agents/
│   ├── platform-targets.yaml                      # Declarative version targets & freshness policy
│   ├── plugins.json                               # Workspace plugin discovery registration
│   ├── skills.json                                # Workspace skill discovery registration
│   └── plugins/
│       └── evergreen-factory/                     # Portable Antigravity Plugin bundle
│           ├── plugin.json                        # Plugin manifest & starter prompts
│           ├── hooks.json                         # PreToolUse guardrail hook on git commit
│           ├── rules/AGENTS.md                    # Always-on plugin rules
│           ├── agents/                            # 1 Scout + 3 Worktree Workers + 3 Read-Only Reviewers
│           │   ├── intake-scout.md
│           │   ├── node-backend-worker.md
│           │   ├── android-compose-worker.md
│           │   ├── ios-swiftui-worker.md
│           │   ├── node-runtime-and-freshness-reviewer.md
│           │   ├── android-play-and-compose-reviewer.md
│           │   └── ios-appstore-and-swiftui-reviewer.md
│           └── skills/
│               └── evergreen-platform/
│                   ├── SKILL.md                   # 4-Phase orchestration SOP
│                   └── scripts/
│                       ├── freshness_scanner.py   # Git modification-age & @stability scanner
│                       └── verify_targets_hook.py # Deterministic policy & store compliance verifier
├── issues/                                        # Open backlog issues correlated during intake
│   ├── 101-node-backend-dependency-diet.md
│   ├── 102-android-play-api35-and-compose.md
│   └── 103-ios18-sdk-and-swiftui-cleanup.md
├── services/
│   └── backend/                                   # Target 1: Node.js TypeScript Backend
│       ├── package.json
│       ├── src/
│       │   ├── hmac-signature-verifier.ts         # Committed 2023-03-15 (Critical, undocumented stability)
│       │   ├── legacy-csv-batch-2023.ts           # Committed 2023-03-15 (Stale legacy removal candidate)
│       │   ├── catalog-sync.ts                    # Committed 2024-06-20 (Legacy npm shims + non-DRY helpers)
│       │   ├── report-exporter.ts                 # Committed 2024-06-20 (Legacy npm shims + dead exports)
│       │   └── webhook-handler.ts                 # Active webhook handler using hmac-signature-verifier
│       └── tests/
│           └── backend.test.ts                    # Runnable node:test suite
└── apps/
    ├── android/                                   # Target 2: Android Jetpack Compose Client
    │   ├── app/build.gradle.kts                   # minSdk = 29, targetSdk = 34 + deprecated Accompanist
    │   └── app/src/main/
    │       ├── AndroidManifest.xml                # Declares OrderSyncService (dataSync)
    │       └── java/com/acme/evergreen/
    │           ├── MainActivity.kt                # Obsolete SDK_INT <= 29 branches; missing enableEdgeToEdge()
    │           ├── ui/CatalogScreen.kt            # Deprecated SwipeRefresh; ignores Scaffold innerPadding
    │           ├── ui/Holiday2023Banner.kt        # Committed 2023-03-15 (Stale seasonal banner)
    │           └── sync/OrderSyncService.kt       # Missing Android 15 onTimeout(int, int) override
    └── ios/                                       # Target 3: iOS SwiftUI Client
        ├── PrivacyInfo.xcprivacy                  # Missing required reason codes CA92.1 & 35F9.1
        └── Sources/
            ├── CatalogView.swift                  # Obsolete #available(iOS 15/16) shims & NavigationView
            ├── OrderViewModel.swift               # Legacy ObservableObject/@Published boilerplate
            ├── DeviceTelemetry.swift              # Calls UserDefaults & systemUptime
            └── LegacyStoreKit1Bridge.swift        # Committed 2023-03-15 (Superseded StoreKit 1 wrapper)
```

---

## Quick Verification Commands

```bash
# 1. Inspect the multi-year Git commit history (2023, 2024, 2026)
git log --format="%h | %cs | %s"

# 2. Run the Node.js backend unit test suite
node --test services/backend/tests/backend.test.ts

# 3. Scan Git modification age (> 365 days) for legacy candidates vs undocumented critical code
python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/freshness_scanner.py

# 4. Audit all 13 seeded platform, DRY, dead-code, and mobile store policy violations
python3 .agents/plugins/evergreen-factory/skills/evergreen-platform/scripts/verify_targets_hook.py --audit

# 5. Reset the repository back to the pre-demo baseline anytime
git reset --hard demo-baseline
```

For step-by-step live presentation instructions and prompts, see **[DEMO.md](file:///Users/rodydavis/Documents/antigravity/keen-davinci/DEMO.md)**.
