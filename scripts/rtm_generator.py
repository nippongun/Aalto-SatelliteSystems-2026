#!/usr/bin/env python3
"""Generate a 4-column SoW RTM from requirements.yaml.

Usage:
    python scripts/rtm_generator.py
    python scripts/rtm_generator.py --requirements path/to/requirements.yaml

Output: Markdown table with columns:
    Objectives and Drivers | Requirements | Observation Requirements | Instrument Requirements

One row per leaf node (instrument_req if present, else obs_req, else req).
"""
import argparse
import pathlib
import sys

import yaml


def _cell(id_: str, text: str) -> str:
    return f"**{id_}** {text}"


def build_rtm_rows(objectives: list) -> list[tuple[str, str, str, str]]:
    rows = []
    for obj in objectives:
        obj_cell = _cell(obj["id"], obj["text"])
        for req in obj.get("requirements", []):
            req_cell = _cell(req["id"], req["text"])
            obs_reqs = req.get("observation_reqs", [])
            if not obs_reqs:
                rows.append((obj_cell, req_cell, "—", "—"))
                continue
            for obs in obs_reqs:
                obs_cell = _cell(obs["id"], obs["text"])
                instr_reqs = obs.get("instrument_reqs", [])
                if not instr_reqs:
                    rows.append((obj_cell, req_cell, obs_cell, "—"))
                else:
                    for instr in instr_reqs:
                        rows.append((obj_cell, req_cell, obs_cell, _cell(instr["id"], instr["text"])))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a 4-column SoW Markdown RTM from requirements.yaml"
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

    rows = build_rtm_rows(objectives)

    header = "| Objectives and Drivers | Requirements | Observation Requirements | Instrument Requirements |"
    sep    = "|------------------------|--------------|--------------------------|------------------------|"
    print(header)
    print(sep)
    for obj_c, req_c, obs_c, instr_c in rows:
        print(f"| {obj_c} | {req_c} | {obs_c} | {instr_c} |")


if __name__ == "__main__":
    main()
