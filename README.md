# Evergreen Commerce — Becoming a Software Factory with Antigravity

**Evergreen Commerce** is the companion reference monorepo (**Node.js Backend**, **Android Jetpack Compose**, and **iOS SwiftUI**) for the talk **"Becoming a Software Factory with Antigravity"**, powered by the portable **`factory` Antigravity Plugin** ([`.agents/plugins/factory`](.agents/plugins/factory)).

It demonstrates the **5-Step Software Factory Blueprint** and **Taiichi Ohno's 4 Steps of Jidoka (自働化)** in action:
1. **Step 1 — Worker Primitives (`.agents/plugins/factory/agents/*-worker.md`)**: Scoped specialist stations (`model: pro`, `commandExecutionPolicy: sandbox`) that execute concurrently across isolated Git worktrees to evict redundant dependencies (`node-fetch`, `uuid`, `rimraf`, `chalk`, `dotenv`, `glob`, `accompanist-*`), delete obsolete OS version branches (`SDK_INT <= 29`, `#available(iOS 15/16)`), consolidate duplicated DRY logic, and document `@stability stable-critical` security modules.
2. **Step 2 — Reusable Factory Lines (`.agents/plugins/factory/skills/*/SKILL.md`)**: Standard Operating Procedures (`platform` and `onboarding`) that codify worktree-to-worktree handoffs, declarative version policies ([`.agents/platform-targets.yaml`](.agents/platform-targets.yaml)), and required output artifacts.
3. **Step 3 — Read-Only Jidoka Inspectors (`commandExecutionPolicy: off`)**: Pure read-only audit stations (`node-runtime-and-freshness-reviewer`, `android-play-and-compose-reviewer`, `ios-appstore-and-swiftui-reviewer`) that **detect abnormalities immediately** and **pull the Andon (アンドン) cord (`STATUS: BLOCKED`)** when a worker misses a store policy or security rule (such as `.ShareReceiver` missing `android:exported` in `AndroidManifest.xml`).
4. **Step 4 — Self-Correcting Lines (Poka-Yoke ポカヨケ) & Portable Plugin (`plugin.json`)**: When a Jidoka inspector halts the line, the factory not only fixes the code in the worktree — it **upgrades its own `.agents/plugins/factory/agents/` worker prompt and `skills/platform/SKILL.md`** so the assembly line never repeats that defect on future runs.
5. **Step 5 — Automated Intake, Verified Output & Human Escalation**: Guarded by `PreToolUse` / `PostToolUse` hooks in `hooks.json`, the factory produces `FRESHNESS_REPORT.md` + `walkthrough.md` and escalates true architectural tradeoffs (such as deleting vs. archiving 2023 legacy modules) to the human via Remote Control / `ask_question`.

---

## Quick Start

```bash
git clone https://github.com/rodydavis/agy-factory-demo.git
cd agy-factory-demo
```

Open the workspace in **Antigravity** (or run `$ agy --agent software-factory`) and follow the live runbook in **[DEMO.md](DEMO.md)**:
- **Act 1 — Multi-Year Git History & Baseline Audit**: Inspect the `2023` / `2024` / `2026` commit history, run `freshness_scanner.py` (`> 365 days` untouched), and run `verify_targets_hook.py --audit` to view all **14 seeded policy, security & store compliance violations**.
- **Act 2 — Full Software Factory Pipeline (with Live Jidoka Andon Halt & Poka-Yoke Upgrade)**: Dispatch `intake-scout`, the 3 parallel worktree workers, and the 3 read-only Jidoka inspectors (`commandExecutionPolicy: off`). Watch `android-play-and-compose-reviewer` pull the **Andon cord** (`Google Play Pre-Submission Audit Report: ❌ BLOCKED` on `.ShareReceiver`), fix the manifest, and apply a **Poka-Yoke upgrade** to `android-compose-worker.md`.
- **Act 3 — Final Verification, `FRESHNESS_REPORT.md` & Human Escalation**: Confirm all 14 checks pass (`STATUS: PASS`), inspect the Poka-Yoke diff in `.agents/plugins/factory/`, review `FRESHNESS_REPORT.md`, and handle the human escalation on the 3 stale `2023-03-15` legacy candidates.
- **Bonus — Interactive `/grill-me` Style Onboarding (`onboarding`)**: Interview the user via structured multi-choice questions to customize `.agents/platform-targets.yaml` and scaffold custom skills/subagents.

---

## Repository Structure

```text
.
├── README.md                                      # Project overview & 5-Step Factory Blueprint
├── DEMO.md                                        # Step-by-step live demo presenter guide
├── GEMINI.md                                      # Workspace rules enforcing platform-targets.yaml
├── LICENSE                                        # Apache 2.0 License
├── .agents/
│   ├── platform-targets.yaml                      # Declarative version targets & freshness policy
│   ├── plugins.json                               # Workspace plugin discovery registration
│   ├── skills.json                                # Workspace skill discovery registration
│   └── plugins/
│       └── factory/                               # Portable Antigravity Plugin bundle
│           ├── plugin.json                        # Plugin manifest & starter prompts
│           ├── hooks.json                         # PreToolUse & PostToolUse guardrail hooks
│           ├── rules/AGENTS.md                    # Always-on plugin rules
│           ├── agents/                            # Main Agent + Scout + 3 Workers + 3 Jidoka Inspectors
│           │   ├── software-factory.md            # Main Factory Agent ($ agy --agent software-factory)
│           │   ├── intake-scout.md                # Research & Git freshness scout (model: flash)
│           │   ├── node-backend-worker.md         # Worktree Worker 1 (commandExecutionPolicy: sandbox)
│           │   ├── android-compose-worker.md      # Worktree Worker 2 (commandExecutionPolicy: sandbox)
│           │   ├── ios-swiftui-worker.md          # Worktree Worker 3 (commandExecutionPolicy: sandbox)
│           │   ├── node-runtime-and-freshness-reviewer.md # Jidoka Inspector 1 (commandExecutionPolicy: off)
│           │   ├── android-play-and-compose-reviewer.md   # Jidoka Inspector 2 (commandExecutionPolicy: off)
│           │   └── ios-appstore-and-swiftui-reviewer.md   # Jidoka Inspector 3 (commandExecutionPolicy: off)
│           └── skills/
│               ├── onboarding/
│               │   └── SKILL.md                   # Interactive /grill-me style onboarding & skill generator
│               └── platform/
│                   ├── SKILL.md                   # 5-Phase orchestration SOP (with Andon + Poka-Yoke)
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
    │       ├── AndroidManifest.xml                # OrderSyncService (dataSync) + .ShareReceiver missing exported
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
python3 .agents/plugins/factory/skills/platform/scripts/freshness_scanner.py

# 4. Audit all 14 seeded platform, DRY, dead-code, and mobile store policy violations
python3 .agents/plugins/factory/skills/platform/scripts/verify_targets_hook.py --audit

# 5. Reset the repository back to the pre-demo baseline anytime
git reset --hard demo-baseline && git clean -fd
```

For step-by-step live presentation instructions and prompts, see **[DEMO.md](DEMO.md)**.
