# Evergreen Factory Plugin Rules

When operating on any repository with `.agents/platform-targets.yaml`:

1. Never delete a runtime shim, polyfill, or OS availability branch unless the replacement API is supported across the entire `[min_supported, current]` window defined in `.agents/platform-targets.yaml`.
2. When adopting an API newer than `min_supported` (such as Node 22 `Promise.withResolvers` or `fs.globSync` while `min_supported` is `20.12.0`, or iOS 18 `.tabViewStyle(.sidebarAdaptable)` while `min_os_version` is `17.0`), always provide a fallback annotated with `@remove-when: <platform> >= <version>`.
3. Any critical source file untouched in `git log` for more than `stale_threshold_days` must include `@stability stable-critical`, `@last-verified`, and `@invariants` in its header comments so it is never mistaken for dead legacy code.
4. Always run `python3 .agents/plugins/factory/skills/platform/scripts/verify_targets_hook.py --audit` after completing platform worker changes.
