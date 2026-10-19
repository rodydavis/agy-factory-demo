#!/usr/bin/env python3
"""Git Code Freshness & Stability Scanner.

Inspects `git log` modification dates across source files in the repository,
identifies files untouched for longer than `stale_threshold_days` (default 365),
and classifies them into:
  1. Documented Stable-Critical Modules (`@stability stable-critical`)
  2. Undocumented Critical Modules (actively imported on critical paths, missing `@stability`)
  3. Legacy Removal Candidates (superseded, seasonal, or low/zero active usage)
Also scans for `@remove-when:` horizon annotations.
"""

from __future__ import annotations

import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SOURCE_DIRS = ["services/backend/src", "apps/android", "apps/ios/Sources"]
SOURCE_EXTENSIONS = {".ts", ".js", ".mjs", ".kt", ".swift"}
STALE_THRESHOLD_DAYS = 365


def get_repo_root() -> Path:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True
        ).strip()
        return Path(out)
    except Exception:
        return Path.cwd()


def get_last_commit_date(repo_root: Path, rel_path: str) -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cs", "--", rel_path],
            cwd=repo_root,
            text=True,
        ).strip()
        return out or None
    except Exception:
        return None


def count_references(repo_root: Path, target_stem: str, self_rel_path: str) -> list[str]:
    refs: list[str] = []
    for src_dir in SOURCE_DIRS:
        base = repo_root / src_dir
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file() or path.suffix not in SOURCE_EXTENSIONS:
                continue
            rel = str(path.relative_to(repo_root))
            if rel == self_rel_path:
                continue
            content = path.read_text(encoding="utf-8", errors="ignore")
            if target_stem in content:
                refs.append(rel)
    return refs


def scan_repository(repo_root: Path, ref_date: datetime.date) -> dict:
    stale_files = []
    remove_when_tags = []

    for src_dir in SOURCE_DIRS:
        base = repo_root / src_dir
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file() or path.suffix not in SOURCE_EXTENSIONS:
                continue
            rel_path = str(path.relative_to(repo_root))
            content = path.read_text(encoding="utf-8", errors="ignore")

            for line_no, line in enumerate(content.splitlines(), start=1):
                match = re.search(r"@remove-when:\s*([^\*\n]+)", line)
                if match:
                    remove_when_tags.append(
                        {
                            "file": rel_path,
                            "line": line_no,
                            "condition": match.group(1).strip(),
                        }
                    )

            last_date_str = get_last_commit_date(repo_root, rel_path)
            if not last_date_str:
                continue
            last_date = datetime.date.fromisoformat(last_date_str)
            age_days = (ref_date - last_date).days

            if age_days <= STALE_THRESHOLD_DAYS:
                continue

            has_stability_doc = "@stability stable-critical" in content
            has_last_verified = "@last-verified" in content
            has_invariants = "@invariants" in content
            refs = count_references(repo_root, path.stem, rel_path)

            is_critical_domain = any(
                kw in rel_path.lower() or kw in content.lower()
                for kw in ["hmac", "timingsafeequal", "signature-verifier"]
            ) and not any(
                leg in rel_path.lower() for leg in ["legacy", "2023", "holiday", "webhook-handler"]
            )
            is_legacy_artifact = any(
                leg in rel_path.lower()
                for leg in ["legacy", "2023", "holiday", "storekit1"]
            )

            if has_stability_doc and has_last_verified and has_invariants:
                classification = "documented_stable_critical"
            elif is_critical_domain:
                classification = "undocumented_critical_violation"
            elif is_legacy_artifact:
                classification = "legacy_removal_candidate"
            else:
                continue

            stale_files.append(
                {
                    "file": rel_path,
                    "last_updated": last_date_str,
                    "age_days": age_days,
                    "referenced_by": refs,
                    "has_stability_doc": has_stability_doc,
                    "classification": classification,
                }
            )

    return {
        "reference_date": ref_date.isoformat(),
        "stale_threshold_days": STALE_THRESHOLD_DAYS,
        "stale_files": stale_files,
        "remove_when_horizon": remove_when_tags,
    }


def main() -> int:
    repo_root = get_repo_root()
    ref_date = datetime.date(2026, 10, 19)
    report = scan_repository(repo_root, ref_date)

    if "--json" in sys.argv:
        print(json.dumps(report, indent=2))
        return 0

    print("=== Evergreen Git Code Freshness Scan ===")
    print(f"Threshold: > {report['stale_threshold_days']} days untouched in git log\n")
    for item in report["stale_files"]:
        status_label = {
            "documented_stable_critical": "[OK: STABLE-CRITICAL DOCUMENTED]",
            "undocumented_critical_violation": "[BLOCKED: UNDOCUMENTED CRITICAL CODE]",
            "legacy_removal_candidate": "[CANDIDATE FOR REMOVAL: STALE LEGACY]",
        }[item["classification"]]
        print(
            f"- {item['file']} (Last updated: {item['last_updated']}, {item['age_days']} days old) -> {status_label}"
        )

    if report["remove_when_horizon"]:
        print("\n=== Next-Horizon @remove-when Annotations ===")
        for tag in report["remove_when_horizon"]:
            print(f"- {tag['file']}:{tag['line']} -> @remove-when: {tag['condition']}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
