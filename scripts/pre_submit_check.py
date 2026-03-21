#!/usr/bin/env python3
"""scripts/pre_submit_check.py — Milestone-aware pre-submission checklist.

Usage:
    python scripts/pre_submit_check.py --milestone idea_review
    python scripts/pre_submit_check.py --milestone concept_review

Exits non-zero always — the human must verify all items before submission.
"""
import argparse
import sys

CHECKLISTS = {
    "idea_review": [
        "Mission goal is measurable (has numbers and units)",
        "Target orbit altitude, inclination specified",
        "At least 3 objectives defined",
        "RTM has >=1 row per objective",
        "Success criteria present (minimal/full/extended)",
        "AI usage section present",
        "Document version and date in header",
        "All section files have review markers (<!-- reviewed: ... --> or <!-- ai-draft: ... -->)",
    ],
    "concept_review": [
        "Sections 1-5 drafted and student-reviewed",
        "Mass budget present with margins",
        "Power budget present with margins",
        "Link budget computed and inserted",
        "Payload trade-off matrix present",
        "RTM complete (all objectives covered)",
        "AI usage section present",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Pre-submission checklist")
    parser.add_argument(
        "--milestone",
        required=True,
        choices=list(CHECKLISTS.keys()),
        help="Milestone target: " + " | ".join(CHECKLISTS.keys()),
    )
    args = parser.parse_args()

    items = CHECKLISTS[args.milestone]
    print(f"\nPre-submit checklist: {args.milestone}\n")
    for item in items:
        print(f"  [ ] {item}")
    print(f"\n{len(items)} items to confirm before submission.")
    print("Resolve all items, then re-run build_doc.py.")
    sys.exit(1)


if __name__ == "__main__":
    main()
