#!/usr/bin/env python3
"""Generate a Markdown Requirements Traceability Matrix (RTM) from requirements.yaml.

Usage:
    python scripts/rtm_generator.py
    python scripts/rtm_generator.py --requirements path/to/requirements.yaml

Output: Markdown table with columns: Req ID | Requirement Text | Parent Objective
"""
import argparse
import pathlib
import sys

import yaml


def flatten_requirements(objectives: list) -> list:
    """Flatten nested objectives/requirements to (req_id, req_text, parent_obj_id) rows.

    Only flattens the first level of requirements under each objective.
    observation_reqs and instrument_reqs are preserved in the YAML but not yet
    included in the RTM output (extend this function in a future phase if needed).
    """
    rows = []
    for obj in objectives:
        obj_id = obj["id"]   # KeyError if malformed — intentional, fail loud
        for req in obj.get("requirements", []):
            rows.append((req["id"], req["text"], obj_id))   # KeyError if malformed
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown RTM table from requirements.yaml"
    )
    parser.add_argument(
        "--requirements",
        default="requirements/requirements.yaml",
        help="Path to requirements YAML file (default: requirements/requirements.yaml)",
    )
    args = parser.parse_args()

    req_path = pathlib.Path(args.requirements)
    if not req_path.exists():
        print(f"ERROR: Not found: {req_path}", file=sys.stderr)
        sys.exit(1)

    with open(req_path) as f:
        data = yaml.safe_load(f)

    objectives = data.get("objectives", [])
    if not objectives:
        print("WARNING: No objectives found in requirements YAML", file=sys.stderr)

    rows = flatten_requirements(objectives)

    # Markdown table output
    print("| Req ID | Requirement Text | Parent Objective |")
    print("|--------|-----------------|-----------------|")
    for req_id, req_text, parent_id in rows:
        print(f"| {req_id} | {req_text} | {parent_id} |")


if __name__ == "__main__":
    main()
