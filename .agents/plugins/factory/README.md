# Evergreen Software Factory Plugin (`factory`)

A portable Antigravity Plugin implementing the **5-Step Software Factory Blueprint** from *Becoming a Software Factory with Antigravity*:

1. **Worker Primitives (`agents/*-worker.md`)** — Scoped specialist stations (`model: pro`, `commandExecutionPolicy: sandbox`) that execute concurrently in isolated Git worktrees.
2. **Reusable Factory Lines (`skills/*/SKILL.md`)**:
   - `platform` (`skills/platform/SKILL.md`) — 5-Phase multi-platform subtraction, modernization, Jidoka inspection (Andon cord), Poka-Yoke self-correction, and Git freshness orchestration pipeline.
   - `onboarding` (`skills/onboarding/SKILL.md`) — Interactive `/grill-me`-style onboarding interview using `ask_question` to generate `.agents/platform-targets.yaml`, scaffold custom platform skills/agents, and configure hooks.
3. **Read-Only Jidoka (自働化) Inspectors (`agents/*-reviewer.md`)** — Pure read-only audit stations (`commandExecutionPolicy: off`) that pull the **Andon cord (`STATUS: BLOCKED`)** on policy/security defects and trigger **Poka-Yoke** upgrades to worker prompts and skills:
   - `node-runtime-and-freshness-reviewer`
   - `android-play-and-compose-reviewer` (emits the **Google Play Pre-Submission Audit Report**)
   - `ios-appstore-and-swiftui-reviewer`
4. **Main Factory Agent (`agents/software-factory.md`)** — Top-level factory supervisor invocable via `$ agy --agent software-factory`.
5. **Automated Intake & Guardrail Hooks (`hooks.json`)**:
   - `target-guardrail` (`PreToolUse` on `run_command` `git commit`)
   - `factory-gate` (`PostToolUse` on `edit_file|write_file`)
