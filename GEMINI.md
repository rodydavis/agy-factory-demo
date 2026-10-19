# Evergreen Commerce Workspace Rules

This repository is managed by the **Evergreen Platform, Code Subtraction & Freshness System** (`.agents/plugins/factory`).

## Mandatory Architectural Policies

1. **Declarative Support Targets**: Always consult [`.agents/platform-targets.yaml`](.agents/platform-targets.yaml) before removing version guards, replacing third-party packages with standard library APIs, or adopting new OS/runtime features.
2. **Progressive Guarding (`@remove-when`)**: Any API or modifier introduced in a version newer than `min_supported` / `min_os_version` / `min_sdk` MUST include a runtime or availability fallback annotated with `@remove-when: <platform> >= <version>`.
3. **Code Freshness & Intentional Stability**:
   - Files untouched in `git log` for longer than `stale_threshold_days` (`365` days) must be triaged as either **Legacy Removal Candidates** or **Protected Stable-Critical Modules**.
   - Critical modules that change infrequently (e.g., cryptographic verification, billing math, core state machines) MUST carry `@stability stable-critical`, `@last-verified YYYY-MM-DD`, and `@invariants` documentation in their file header.
4. **Read-Only Reviewer Verification**: No multi-platform modernization or subtraction change is complete until audited by the read-only reviewer subagents (`node-runtime-and-freshness-reviewer`, `android-play-and-compose-reviewer`, `ios-appstore-and-swiftui-reviewer`) and verified by `verify_targets_hook.py`.
