---
name: onboarding
description: >-
  Interactive "grill-me"-style onboarding interview for the Evergreen Factory plugin.
  Auto-detects the repository's tech stack and Git commit age distribution, interviews
  the user via structured questions to establish version support windows, stdlib/DRY
  subtraction policies, and code freshness thresholds, generates .agents/platform-targets.yaml,
  and customizes or scaffolds platform skills, worker/reviewer subagents, and hooks.
---

# Evergreen Factory Agentic Onboarding (`grill-me` Flow)

Use this skill when onboarding a new or existing repository to the **Evergreen Platform, Code Subtraction & Freshness System**, or when the user asks to configure `.agents/platform-targets.yaml` and tailor the factory's skills and subagents to their project.

---

## Core Interview Philosophy

1. **Reconnaissance Before Questions**: Never ask the user what languages are in their repo if you can detect them in 2 seconds. Scan the workspace first so every question presents smart `(Recommended)` defaults tailored to their actual files.
2. **Structured Multi-Choice (`ask_question`)**: Use the `ask_question` tool to interview the user in **2 concise rounds** (2–3 questions per round) so they can configure their entire factory in under 60 seconds. Skip any question the user already answered in their prompt.
3. **Generate & Customize Concrete Artifacts**: At the end of the interview, write `.agents/platform-targets.yaml`, customize `skills/platform/SKILL.md` (and scaffold any new platform skills/subagents requested), configure `hooks.json`, and run an immediate baseline audit.

---

## Step 1: Automatic Codebase Reconnaissance

Before calling `ask_question`, quickly inspect the repository:
1. Check for platform manifests (`package.json`, `tsconfig.json`, `app/build.gradle.kts`, `PrivacyInfo.xcprivacy`, `Package.swift`, `pyproject.toml`, `go.mod`, `Cargo.toml`).
2. Run a quick Git history check (`git log --reverse --format="%cs" | head -n 1` and `git log -1 --format="%cs"`) to see the repository's age span.
3. Check whether `.agents/platform-targets.yaml` already exists.

Briefly share a 2-sentence summary of what you detected (e.g., *"Detected a multi-platform monorepo with Node.js Backend (`engines.node >= 20.12.0`), Android Jetpack Compose (`minSdk = 29, targetSdk = 34`), and iOS SwiftUI, with Git history dating back to `2023-03-15`."*), and immediately launch **Round 1**.

---

## Step 2: Round 1 Interview — Platforms, Support Windows & Subtraction Scope

Call `ask_question` with the following questions (adjusting the `(Recommended)` tags to match the detected stack):

1. **Question 1 (`is_multi_select: true`)**:
   - `question`: `"Which platform targets in this repository should the Evergreen Factory actively manage?"`
   - `options`:
     - `"(Recommended) Node.js / TypeScript Backend (LTS stdlib replacements & DRY cleanup)"`
     - `"(Recommended) Android Jetpack Compose (Google Play Target SDK 35 & Material 3 migration)"`
     - `"(Recommended) iOS SwiftUI (App Store iOS 18 SDK, PrivacyInfo.xcprivacy & @Observable)"`
     - `"Web Frontend (MDN Web Baseline APIs, CSS Anchor/Popover & polyfill removal)"`
     - `"Python / Go / Rust Backend Services"`
2. **Question 2 (`is_multi_select: false`)**:
   - `question`: `"What version support window should govern when legacy shims and polyfills are deleted?"`
   - `options`:
     - `"(Recommended) Current + 1 Previous LTS/Major Version (e.g., Node 20.12 & 22, iOS 17 & 18, Android API 29–35)"`
     - `"Conservative N-2 Window (Support last 2 major releases; keep more @remove-when fallbacks)"`
     - `"Aggressive Current-Only Window (Target latest LTS/OS only for maximum code deletion)"`
     - `"Custom version numbers per platform"`
3. **Question 3 (`is_multi_select: true`)**:
   - `question`: `"Which proactive code-subtraction and hygiene workflows should we enable?"`
   - `options`:
     - `"(Recommended) Evict redundant 3rd-party packages replaceable by native stdlib (node-fetch, uuid, rimraf, chalk, dotenv, accompanist)"`
     - `"(Recommended) Remove obsolete OS/runtime version branches (SDK_INT <= minSdk, #available <= min_os_version)"`
     - `"(Recommended) Consolidate duplicated (non-DRY) functions (>= 12 lines across 2+ files) into shared modules"`
     - `"(Recommended) Delete unreferenced dead exports, unused Compose/SwiftUI views, and stale flags"`

Wait for the user's response before proceeding to Round 2.

---

## Step 3: Round 2 Interview — Git Code Freshness, Critical Stability & Guardrail Hooks

Call `ask_question` to finalize the freshness and compliance rules:

1. **Question 1 (`is_multi_select: false`)**:
   - `question`: `"How should the Git Code Freshness scanner triage old files that haven't been updated recently?"`
   - `options`:
     - `"(Recommended) Flag files untouched > 365 days as Removal Candidates unless documented with @stability stable-critical"`
     - `"Flag files untouched > 180 days (6 months) with strict @stability stable-critical enforcement"`
     - `"Flag files untouched > 730 days (2 years) for conservative legacy triage"`
2. **Question 2 (`is_multi_select: true`)**:
   - `question`: `"Which read-only reviewer gates and pre-commit hooks should block merges on violations?"`
   - `options`:
     - `"(Recommended) Runtime & Version Matrix Reviewer (Enforces @remove-when fallbacks on newer APIs)"`
     - `"(Recommended) Google Play API 35 Reviewer (Enforces dataSync Service.onTimeout & Compose edge-to-edge insets)"`
     - `"(Recommended) Apple App Store ITMS-91053 Reviewer (Enforces PrivacyInfo.xcprivacy required reason codes)"`
     - `"(Recommended) PreToolUse git commit Hook (Runs verify_targets_hook.py before every commit)"`
3. **Question 3 (`is_multi_select: false`)**:
   - `question`: `"Would you like to scaffold any additional custom skills for your team's workflow?"`
   - `options`:
     - `"(Recommended) Keep the core platform orchestration skill and customize it for our selected stack"`
     - `"Also scaffold a dedicated dependabot-last-mile skill for fixing breaking dependency upgrades"`
     - `"Also scaffold a web-baseline-modernizer skill for MDN Web Baseline & CSS migrations"`

---

## Step 4: Generate Config & Customize Skills, Agents, and Hooks

Once the user completes Round 2, immediately execute these customizations:

1. **Write `.agents/platform-targets.yaml`**:
   - Populate `policy`, `code_freshness` (`stale_threshold_days`, `required_annotations`: `@stability stable-critical`, `@last-verified`, `@invariants`), and each selected platform section (`node_backend`, `android_compose`, `ios_swiftui`, `web_baseline`, etc.) reflecting the user's exact answers.
2. **Customize `skills/platform/SKILL.md` & Subagents**:
   - Update `.agents/plugins/factory/skills/platform/SKILL.md` so Phase 2 and Phase 3 match the user's enabled platforms and DRY/dead-code rules.
   - If the user requested an additional skill in Round 2 Question 3 (such as `dependabot-last-mile` or `web-baseline-modernizer`), scaffold `.agents/plugins/factory/skills/<skill-name>/SKILL.md` and its corresponding worker/reviewer subagent in `.agents/plugins/factory/agents/`.
3. **Configure `.agents/plugins/factory/hooks.json` & `verify_targets_hook.py`**:
   - Enable or disable the `PreToolUse` hook in `hooks.json` based on the user's selection, and align `STALE_THRESHOLD_DAYS` in `freshness_scanner.py` with their chosen threshold.
4. **Run Initial Baseline Audit & Present Summary**:
   - Execute `freshness_scanner.py` and `verify_targets_hook.py --audit` via `run_command` and present a concise onboarding summary showing:
     - Link to the generated [`.agents/platform-targets.yaml`](.agents/platform-targets.yaml)
     - Any customized or newly created skills/subagents
     - The initial list of detected violations and stale files ready for the first `platform` run.
