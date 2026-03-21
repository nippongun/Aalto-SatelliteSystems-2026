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
        "Mass budget present with real numbers and margins",
        "Power budget present with real numbers and margins",
        "Link budget computed and inserted",
        "Payload trade-off matrix present (>=3 options scored)",
        "RTM complete (all objectives covered)",
        "All requirement IDs present in section 6 (product assurance)",
        "AI usage section present",
    ],
    "preliminary_design": [
        "Sections 1-6 drafted and student-reviewed",
        "Mass budget finalized with subsystem breakdown and system margin",
        "Power budget finalized per operating mode (nominal/safe/comms)",
        "Link budget verified (margin >= 3 dB)",
        "Data budget: downlink capacity >= data generated per orbit",
        "Orbit analysis complete (contact time, revisit time, eclipse fraction)",
        "Payload selection justified with scored trade-off matrix",
        "RTM complete with verification methods for every requirement",
        "Product assurance: model philosophy and test matrix defined",
        "Risk register has >= 5 risks with likelihood, impact, mitigation",
        "AI usage section present and up to date",
        "All section files have reviewed markers (<!-- reviewed: ... -->)",
    ],
    "detailed_design": [
        "All 8 sections complete and student-reviewed",
        "Mass budget finalized — system margin >= 20%",
        "Power budget finalized — all subsystem margins >= 10%",
        "Link budget verified — margin >= 3 dB",
        "Cost estimate present (launch + labour + materials, range 0.5–10 MEUR)",
        "Gantt chart present covering feasibility → PDR → CDR → AIT → launch → ops",
        "Risk register has >= 5 risks",
        "All RTM cells populated — no TBD entries",
        "All requirements have verification method (test/analysis/inspection/demonstration)",
        "Verification matrix in section 6 references every REQ-XX",
        "All figures have captions and are referenced in text",
        "All tables have titles and column headers",
        "Permits and licences section complete (Finnish law, RF licence, debris plan)",
        "AI usage chapter complete with validation methodology",
        "check_consistency.py exits 0 with no FAILs",
        "All tests pass: python -m pytest tests/ -x -q",
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
