# Evergreen Factory Plugin (`evergreen-factory`)

An Antigravity Plugin that automates platform modernization, proactive code/dependency subtraction, DRY consolidation, App Store / Google Play compliance checks, and Git modification-age freshness audits.

## Included Components

- **Skill**: `evergreen-platform` (`skills/evergreen-platform/SKILL.md`)
- **Subagents (`agents/*.md`)**:
  - `intake-scout` (Web search + Git freshness scanner + issue triage)
  - `node-backend-worker` (Node.js LTS stdlib migrations, DRY extraction, dead-code removal)
  - `android-compose-worker` (Google Play API 35, Material 3 Compose, `SDK_INT` cleanup)
  - `ios-swiftui-worker` (App Store iOS 18 SDK, `PrivacyInfo.xcprivacy`, `@Observable` migration)
  - `node-runtime-and-freshness-reviewer` (Read-only reviewer)
  - `android-play-and-compose-reviewer` (Read-only reviewer)
  - `ios-appstore-and-swiftui-reviewer` (Read-only reviewer)
- **Hook**: `evergreen-target-guardrail` (`hooks.json` -> `scripts/verify_targets_hook.py`)
- **Rules**: `rules/AGENTS.md`
