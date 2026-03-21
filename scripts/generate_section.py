#!/usr/bin/env python3
"""Generate a section prompt with mission parameters substituted from mission_config.yaml.

Usage:
    python scripts/generate_section.py --section motivation
    python scripts/generate_section.py --section motivation --config path/to/config.yaml
    python scripts/generate_section.py --section motivation --prompts-dir path/to/prompts/
"""
import argparse
import pathlib
import sys

import yaml


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a section prompt with mission parameters"
    )
    parser.add_argument(
        "--section", required=True, help="Section name (e.g. motivation)"
    )
    parser.add_argument(
        "--config",
        default="mission_config.yaml",
        help="Path to mission config YAML (default: mission_config.yaml)",
    )
    parser.add_argument(
        "--prompts-dir",
        default="prompts",
        help="Path to prompts directory (default: prompts/)",
    )
    args = parser.parse_args()

    config_path = pathlib.Path(args.config)
    prompt_path = pathlib.Path(args.prompts_dir) / f"{args.section}.md"

    if not config_path.exists():
        print(f"ERROR: Config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    if not prompt_path.exists():
        print(f"ERROR: Prompt not found: {prompt_path}", file=sys.stderr)
        prompts_parent = pathlib.Path(args.prompts_dir)
        if prompts_parent.exists():
            available = ", ".join(p.stem for p in prompts_parent.glob("*.md"))
        else:
            available = "(prompts directory not found)"
        print(
            f"Available sections: {available}",
            file=sys.stderr,
        )
        sys.exit(1)

    with open(config_path) as f:
        config = yaml.safe_load(f)

    template = prompt_path.read_text()

    try:
        output = template.format_map(config)
    except KeyError as e:
        print(
            f"ERROR: Missing config key in prompt template: {e}. Add it to {config_path}.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(output)


if __name__ == "__main__":
    main()
