#!/usr/bin/env python3
"""scripts/check_consistency.py — Seven-check consistency scanner.

Reads Markdown content files, budget CSVs, mission_config.yaml, and
requirements.yaml to detect contradictions before every document build.

Usage:
    python scripts/check_consistency.py content/
    python scripts/check_consistency.py content/ --config mission_config.yaml
    python scripts/check_consistency.py content/ --config mission_config.yaml \\
        --requirements requirements/requirements.yaml \\
        --output consistency_report.md
    python scripts/check_consistency.py content/ --budget budgets/mass_budget.csv
"""
import argparse
import csv
import dataclasses
import pathlib
import re
import sys
from collections import defaultdict

import yaml

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

ALTITUDE_CONTEXT = re.compile(
    r"(?:orbit|altitude|LEO|apogee|perigee).*?(\d+(?:\.\d+)?)\s*km"
    r"|(\d+(?:\.\d+)?)\s*km.*?(?:orbit|altitude|LEO|apogee|perigee)",
    re.IGNORECASE,
)
UNIT_PATTERN = re.compile(
    r"\d+(?:\.\d+)?\s*(?:km|m|dB|W|kg|bps|MHz|GHz|°|deg|%|ms|s\b)"
)
AI_HEADING = re.compile(r"^#+\s+AI\s+usage", re.IGNORECASE | re.MULTILINE)


# ---------------------------------------------------------------------------
# Data type
# ---------------------------------------------------------------------------

@dataclasses.dataclass
class CheckResult:
    name: str
    status: str   # "PASS", "FAIL", or "WARNING"
    detail: str
    line_refs: list  # list of (filename_str, line_no_int) tuples


# ---------------------------------------------------------------------------
# Seven check functions
# ---------------------------------------------------------------------------

def check_altitude_consistent(content_dir: pathlib.Path, config: dict) -> CheckResult:
    """Check that all content files agree on orbit altitude km value."""
    altitude_hits: dict[str, list] = defaultdict(list)

    for md_file in sorted(content_dir.glob("*.md")):
        try:
            lines = md_file.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for lineno, line in enumerate(lines, start=1):
            for m in ALTITUDE_CONTEXT.finditer(line):
                value = m.group(1) or m.group(2)
                if value:
                    altitude_hits[value].append((md_file.name, lineno))

    if len(altitude_hits) > 1:
        sorted_values = sorted(altitude_hits.keys(), key=float)
        refs = []
        for val in sorted_values:
            refs.extend(altitude_hits[val])
        detail = (
            f"Multiple altitude values found: {', '.join(sorted_values)} km. "
            "All content files must agree on one altitude."
        )
        return CheckResult("Altitude consistency", "FAIL", detail, refs)

    return CheckResult("Altitude consistency", "PASS", "All altitude references are consistent.", [])


def check_mass_budget(config: dict, budget_path: pathlib.Path) -> CheckResult:
    """Check that total mass in CSV does not exceed config mass_kg."""
    if not budget_path.exists():
        return CheckResult(
            "Mass budget",
            "PASS",
            f"{budget_path.name} not found — skipped",
            [],
        )

    total = 0.0
    skipped_rows = 0
    refs = []
    try:
        with open(budget_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):  # row 1 is header
                try:
                    total += float(row["mass_kg"])
                    refs.append((budget_path.name, i))
                except (ValueError, KeyError):
                    skipped_rows += 1

    except OSError as exc:
        return CheckResult("Mass budget", "FAIL", f"Could not read {budget_path}: {exc}", [])

    limit = config.get("mass_kg", 0)
    skip_note = f" ({skipped_rows} TBD rows skipped)" if skipped_rows else ""
    if total > limit:
        return CheckResult(
            "Mass budget",
            "FAIL",
            f"Total mass {total:.2f} kg exceeds limit {limit} kg{skip_note}.",
            refs,
        )
    return CheckResult(
        "Mass budget",
        "PASS",
        f"Total mass {total:.2f} kg within limit {limit} kg{skip_note}.",
        refs,
    )


def check_power_budget(config: dict, budget_path: pathlib.Path) -> CheckResult:
    """Check that total power draw does not exceed eps_power_W."""
    if "eps_power_W" not in config:
        return CheckResult(
            "Power budget",
            "WARNING",
            "eps_power_W not defined in mission_config.yaml — add it before this check is meaningful",
            [],
        )

    if not budget_path.exists():
        return CheckResult(
            "Power budget",
            "PASS",
            f"{budget_path.name} not found — skipped",
            [],
        )

    total = 0.0
    refs = []
    try:
        with open(budget_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, start=2):
                try:
                    total += float(row["power_W"])
                    refs.append((budget_path.name, i))
                except (ValueError, KeyError):
                    pass
    except OSError as exc:
        return CheckResult("Power budget", "FAIL", f"Could not read {budget_path}: {exc}", [])

    limit = config["eps_power_W"]
    if total > limit:
        return CheckResult(
            "Power budget",
            "FAIL",
            f"Total power {total:.2f} W exceeds EPS capacity {limit} W.",
            refs,
        )
    return CheckResult(
        "Power budget",
        "PASS",
        f"Total power {total:.2f} W within EPS capacity {limit} W.",
        refs,
    )


def check_requirement_units(req_data: dict) -> CheckResult:
    """Check that every requirement text contains at least one number+unit."""
    missing = []
    for obj in req_data.get("objectives", []):
        for req in obj.get("requirements", []):
            text = req.get("text", "")
            if not UNIT_PATTERN.search(text):
                missing.append(req.get("id", "unknown"))

    if missing:
        return CheckResult(
            "Requirement units",
            "FAIL",
            f"Requirements missing a measurable unit: {', '.join(missing)}",
            [],
        )
    return CheckResult(
        "Requirement units",
        "PASS",
        "All requirements contain a measurable unit.",
        [],
    )


def check_objective_coverage(req_data: dict) -> CheckResult:
    """Check that every objective has at least one requirement."""
    orphaned = []
    for obj in req_data.get("objectives", []):
        if not obj.get("requirements"):
            orphaned.append(obj.get("id", "unknown"))

    if orphaned:
        return CheckResult(
            "Objective coverage",
            "FAIL",
            f"Objectives with no requirements: {', '.join(orphaned)}",
            [],
        )
    return CheckResult(
        "Objective coverage",
        "PASS",
        "All objectives have at least one requirement.",
        [],
    )


def check_success_criteria(content_dir: pathlib.Path) -> CheckResult:
    """Check that 01_motivation.md contains minimal and full success criteria."""
    motivation_path = content_dir / "01_motivation.md"
    if not motivation_path.exists():
        return CheckResult(
            "Success criteria",
            "FAIL",
            "01_motivation.md not found in content directory.",
            [],
        )

    text = motivation_path.read_text(encoding="utf-8").lower()
    missing = []
    if "minimal success" not in text:
        missing.append('"minimal success"')
    if "full success" not in text:
        missing.append('"full success"')

    if missing:
        return CheckResult(
            "Success criteria",
            "FAIL",
            f"01_motivation.md is missing: {', '.join(missing)}.",
            [(motivation_path.name, 0)],
        )
    return CheckResult(
        "Success criteria",
        "PASS",
        "Both 'minimal success' and 'full success' criteria found in 01_motivation.md.",
        [],
    )


def check_requirement_verification(req_data: dict) -> CheckResult:
    """Check that every requirement has a verification_method field."""
    missing = []
    for obj in req_data.get("objectives", []):
        for req in obj.get("requirements", []):
            if not req.get("verification_method"):
                missing.append(req.get("id", "unknown"))

    if missing:
        return CheckResult(
            "Requirement verification methods",
            "FAIL",
            f"Requirements missing a verification_method: {', '.join(missing)}",
            [],
        )
    return CheckResult(
        "Requirement verification methods",
        "PASS",
        "All requirements have a verification_method.",
        [],
    )


def check_req_ids_in_product_assurance(
    req_data: dict, content_dir: pathlib.Path
) -> CheckResult:
    """Check that every REQ-XX id from requirements.yaml appears in 06_product_assurance.md."""
    assurance_path = content_dir / "06_product_assurance.md"
    if not assurance_path.exists():
        return CheckResult(
            "REQ traceability to product assurance",
            "WARNING",
            "06_product_assurance.md not found — skipped",
            [],
        )

    text = assurance_path.read_text(encoding="utf-8")
    req_ids = []
    for obj in req_data.get("objectives", []):
        for req in obj.get("requirements", []):
            req_id = req.get("id")
            if req_id:
                req_ids.append(req_id)

    if not req_ids:
        return CheckResult(
            "REQ traceability to product assurance",
            "WARNING",
            "No requirements found in requirements.yaml — skipped",
            [],
        )

    unverified = [rid for rid in req_ids if rid not in text]
    if unverified:
        return CheckResult(
            "REQ traceability to product assurance",
            "FAIL",
            f"Requirements not referenced in 06_product_assurance.md: {', '.join(unverified)}",
            [(assurance_path.name, 0)],
        )
    return CheckResult(
        "REQ traceability to product assurance",
        "PASS",
        f"All {len(req_ids)} requirement IDs found in 06_product_assurance.md.",
        [],
    )


def check_ai_usage_section(content_dir: pathlib.Path) -> CheckResult:
    """Check that at least one content file has an AI usage heading."""
    for md_file in sorted(content_dir.glob("*.md")):
        try:
            text = md_file.read_text(encoding="utf-8")
        except OSError:
            continue
        if AI_HEADING.search(text):
            return CheckResult(
                "AI usage section",
                "PASS",
                f"AI usage heading found in {md_file.name}.",
                [(md_file.name, 0)],
            )

    return CheckResult(
        "AI usage section",
        "FAIL",
        'No content file contains a heading matching "# AI usage" (case-insensitive).',
        [],
    )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_all_checks(
    content_dir: pathlib.Path,
    config: dict,
    req_data: dict,
    mass_budget_path: pathlib.Path,
    power_budget_path: pathlib.Path,
) -> list[CheckResult]:
    """Run all nine checks and return a list of CheckResult objects."""
    return [
        check_altitude_consistent(content_dir, config),
        check_mass_budget(config, mass_budget_path),
        check_power_budget(config, power_budget_path),
        check_requirement_units(req_data),
        check_objective_coverage(req_data),
        check_requirement_verification(req_data),
        check_req_ids_in_product_assurance(req_data, content_dir),
        check_success_criteria(content_dir),
        check_ai_usage_section(content_dir),
    ]


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(results: list[CheckResult], output_path: pathlib.Path) -> None:
    """Write a Markdown consistency report to output_path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Consistency Report\n"]
    for result in results:
        lines.append(f"## {result.status}: {result.name}\n")
        lines.append(f"{result.detail}\n")
        if result.line_refs:
            for fname, lineno in result.line_refs:
                ref = f"{fname}:{lineno}" if lineno else fname
                lines.append(f"- {ref}")
            lines.append("")
        lines.append("")
    output_path.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    repo_root = pathlib.Path(__file__).parent.parent

    parser = argparse.ArgumentParser(
        description="Run seven consistency checks on mission content files."
    )
    parser.add_argument(
        "content_dir",
        nargs="?",
        default=str(repo_root / "content"),
        help="Directory containing *.md content files (default: content/)",
    )
    parser.add_argument(
        "--config",
        default=str(repo_root / "mission_config.yaml"),
        help="Path to mission_config.yaml",
    )
    parser.add_argument(
        "--requirements",
        default=str(repo_root / "requirements" / "requirements.yaml"),
        help="Path to requirements.yaml",
    )
    parser.add_argument(
        "--budget",
        default=None,
        help="Path to mass_budget.csv (default: budgets/mass_budget.csv relative to repo root)",
    )
    parser.add_argument(
        "--power-budget",
        default=None,
        help="Path to power_budget.csv (default: budgets/power_budget.csv relative to repo root)",
    )
    parser.add_argument(
        "--output",
        default=str(repo_root / "consistency_report.md"),
        help="Path to write the consistency report Markdown",
    )
    args = parser.parse_args()

    content_dir = pathlib.Path(args.content_dir)
    config_path = pathlib.Path(args.config)
    req_path = pathlib.Path(args.requirements)
    output_path = pathlib.Path(args.output)

    mass_budget_path = (
        pathlib.Path(args.budget)
        if args.budget is not None
        else repo_root / "budgets" / "mass_budget.csv"
    )
    power_budget_path = (
        pathlib.Path(args.power_budget)
        if args.power_budget is not None
        else repo_root / "budgets" / "power_budget.csv"
    )

    # Load config
    if not config_path.exists():
        print(f"ERROR: Config not found at {config_path}", file=sys.stderr)
        sys.exit(2)
    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f) or {}

    # Load requirements (empty structure if missing)
    req_data: dict = {"objectives": []}
    if req_path.exists():
        with open(req_path, encoding="utf-8") as f:
            loaded = yaml.safe_load(f)
            if isinstance(loaded, dict):
                req_data = loaded

    results = run_all_checks(
        content_dir=content_dir,
        config=config,
        req_data=req_data,
        mass_budget_path=mass_budget_path,
        power_budget_path=power_budget_path,
    )

    write_report(results, output_path)
    print(f"Consistency report written to: {output_path}")

    any_fail = any(r.status == "FAIL" for r in results)
    if any_fail:
        for r in results:
            if r.status == "FAIL":
                print(f"FAIL: {r.name} — {r.detail}", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
