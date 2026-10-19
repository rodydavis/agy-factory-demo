#!/usr/bin/env python3
"""Deterministic Platform Target, Store Compliance & Freshness Guardrail Script.

Can be executed in two modes:
  1. `--audit`: Runs a full repository check against `.agents/platform-targets.yaml`
     and prints structured PASS / BLOCKED results for each platform & freshness rule.
  2. `--pre-tool-hook`: Reads Antigravity PreToolUse JSON from stdin; if the command
     is a `git commit` while violations exist (unless `ALLOW_LEGACY_SEED=1`), returns
     `{"decision": "deny", "reason": "..."}`.
"""

from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

from freshness_scanner import get_repo_root, scan_repository


def audit_repository(repo_root: Path) -> list[str]:
    violations: list[str] = []

    # 1. Node.js Backend Checks
    pkg_json_path = repo_root / "services/backend/package.json"
    if pkg_json_path.exists():
        pkg_data = json.loads(pkg_json_path.read_text(encoding="utf-8"))
        deps = pkg_data.get("dependencies", {})
        banned = {"node-fetch", "uuid", "rimraf", "chalk", "dotenv"}
        present_banned = sorted(banned.intersection(deps.keys()))
        if present_banned:
            violations.append(
                f"[Node.js Backend] Redundant npm packages still in package.json (replaceable by Node 20.12+ stdlib): {', '.join(present_banned)}"
            )

    catalog_sync = repo_root / "services/backend/src/catalog-sync.ts"
    report_exporter = repo_root / "services/backend/src/report-exporter.ts"
    if catalog_sync.exists() and report_exporter.exists():
        c_text = catalog_sync.read_text(encoding="utf-8")
        r_text = report_exporter.read_text(encoding="utf-8")
        if (
            "export function formatCurrencyWithTax" in c_text
            and "export function formatCurrencyWithTax" in r_text
        ):
            violations.append(
                "[Node.js DRY] formatCurrencyWithTax() and retryWithBackoff() are duplicated across catalog-sync.ts and report-exporter.ts"
            )
        if "legacyXmlReportExporter" in r_text or "deprecatedV1WebhookMapper" in r_text:
            violations.append(
                "[Node.js Dead Code] Unused exports legacyXmlReportExporter / deprecatedV1WebhookMapper still present in report-exporter.ts"
            )
        # Check Node 22-only APIs used without @remove-when guard while min_supported is 20.12.0
        for fpath, text in [("catalog-sync.ts", c_text), ("report-exporter.ts", r_text)]:
            if (
                "fs.globSync" in text or "Promise.withResolvers" in text
            ) and "@remove-when: node >= 22" not in text:
                violations.append(
                    f"[Node.js LTS Matrix] {fpath} uses Node 22+ API (fs.globSync / Promise.withResolvers) without a Node 20.12 fallback & '@remove-when: node >= 22.0.0' tag"
                )

    # 2. Git Code Freshness Check (Undocumented Critical Files > 365 days)
    freshness = scan_repository(repo_root, datetime.date(2026, 10, 19))
    for item in freshness["stale_files"]:
        if item["classification"] == "undocumented_critical_violation":
            violations.append(
                f"[Code Freshness] Critical file {item['file']} (last updated {item['last_updated']}, {item['age_days']}d ago) lacks '@stability stable-critical', '@last-verified', and '@invariants' header docs"
            )

    # 3. Android Jetpack Compose & Google Play API 35 Checks
    gradle_path = repo_root / "apps/android/app/build.gradle.kts"
    if gradle_path.exists():
        g_text = gradle_path.read_text(encoding="utf-8")
        if "targetSdk = 35" not in g_text:
            violations.append(
                "[Android Google Play] apps/android/app/build.gradle.kts must set targetSdk = 35"
            )
        if "accompanist-" in g_text:
            violations.append(
                "[Android Compose] Deprecated com.google.accompanist dependencies still present in build.gradle.kts"
            )

    sync_service = (
        repo_root
        / "apps/android/app/src/main/java/com/acme/evergreen/sync/OrderSyncService.kt"
    )
    if sync_service.exists():
        s_lines = [
            line for line in sync_service.read_text(encoding="utf-8").splitlines()
            if not line.strip().startswith("//")
        ]
        s_code = "\n".join(s_lines)
        if "override fun onTimeout" not in s_code:
            violations.append(
                "[Android 15 API 35 Crash Risk] OrderSyncService.kt (dataSync FGS) is missing mandatory override fun onTimeout(startId: Int, fgsType: Int)"
            )

    main_act = (
        repo_root / "apps/android/app/src/main/java/com/acme/evergreen/MainActivity.kt"
    )
    if main_act.exists():
        m_text = main_act.read_text(encoding="utf-8")
        if "enableEdgeToEdge()" not in m_text:
            violations.append(
                "[Android 15 Edge-to-Edge] MainActivity.kt is missing enableEdgeToEdge() in onCreate()"
            )
        if "VERSION_CODES.O" in m_text or "VERSION_CODES.Q" in m_text:
            violations.append(
                "[Android Subtraction] MainActivity.kt still contains obsolete SDK_INT checks <= minSdk (29)"
            )

    catalog_screen = (
        repo_root
        / "apps/android/app/src/main/java/com/acme/evergreen/ui/CatalogScreen.kt"
    )
    if catalog_screen.exists():
        cs_text = catalog_screen.read_text(encoding="utf-8")
        if "Scaffold { _ ->" in cs_text or "padding(innerPadding)" not in cs_text:
            violations.append(
                "[Android Compose Insets] CatalogScreen.kt ignores Scaffold innerPadding under Android 15 edge-to-edge mode"
            )

    # 4. iOS SwiftUI & App Store Connect ITMS-91053 Checks
    privacy_path = repo_root / "apps/ios/PrivacyInfo.xcprivacy"
    if privacy_path.exists():
        p_text = privacy_path.read_text(encoding="utf-8")
        if "CA92.1" not in p_text or "35F9.1" not in p_text:
            violations.append(
                "[iOS App Store ITMS-91053] apps/ios/PrivacyInfo.xcprivacy is missing required reason codes CA92.1 (UserDefaults) and 35F9.1 (SystemBootTime)"
            )

    ios_catalog = repo_root / "apps/ios/Sources/CatalogView.swift"
    if ios_catalog.exists():
        ic_text = ios_catalog.read_text(encoding="utf-8")
        if "#available(iOS 15" in ic_text or "#available(iOS 16" in ic_text:
            violations.append(
                "[iOS Subtraction] CatalogView.swift still contains obsolete #available(iOS 15/16) branches while min_os_version is 17.0"
            )
        if "NavigationView" in ic_text:
            violations.append(
                "[iOS SwiftUI] CatalogView.swift still uses deprecated NavigationView instead of NavigationStack"
            )
        if (
            "sidebarAdaptable" in ic_text
            and "@remove-when: ios >= 18.0" not in ic_text
        ):
            violations.append(
                "[iOS Version Matrix] CatalogView.swift uses iOS 18 .sidebarAdaptable without an #available(iOS 18.0, *) guard and '// @remove-when: ios >= 18.0' tag"
            )

    return violations


def handle_pre_tool_hook(repo_root: Path) -> int:
    raw = sys.stdin.read().strip()
    if not raw:
        print(json.dumps({"decision": "allow"}))
        return 0

    try:
        payload = json.loads(raw)
    except Exception:
        print(json.dumps({"decision": "allow"}))
        return 0

    cmd = payload.get("toolCall", {}).get("args", {}).get("CommandLine", "")
    if "git commit" not in cmd or "ALLOW_LEGACY_SEED=1" in cmd:
        print(json.dumps({"decision": "allow"}))
        return 0

    violations = audit_repository(repo_root)
    if violations:
        print(
            json.dumps(
                {
                    "decision": "deny",
                    "reason": "Evergreen Factory Target & Store Policy Guardrail blocked commit:\n- "
                    + "\n- ".join(violations),
                }
            )
        )
        return 0

    print(json.dumps({"decision": "allow"}))
    return 0


def main() -> int:
    repo_root = get_repo_root()
    if "--pre-tool-hook" in sys.argv:
        return handle_pre_tool_hook(repo_root)

    violations = audit_repository(repo_root)
    if not violations:
        print("STATUS: PASS — All Node.js LTS, Android API 35, iOS 18 App Store, DRY, and Code Freshness checks passed!")
        return 0

    print(f"STATUS: BLOCKED ({len(violations)} policy violations detected):")
    for idx, v in enumerate(violations, start=1):
        print(f"  {idx}. {v}")
    return 1 if "--strict" in sys.argv else 0


if __name__ == "__main__":
    raise SystemExit(main())
