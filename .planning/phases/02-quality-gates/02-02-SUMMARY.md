---
phase: 02-quality-gates
plan: "02"
subsystem: testing
tags: [python, argparse, subprocess, checklist, pre-submit, milestone-gate]

# Dependency graph
requires:
  - phase: 02-01
    provides: test stubs for pre_submit_check.py (skipped), check_consistency.py implementation
provides:
  - scripts/pre_submit_check.py — milestone-aware checklist printer with CHECKLISTS dict, always exits 1
  - tests/test_pre_submit_check.py — full subprocess test suite, 4 tests passing (no skips)
affects: [future milestone submissions, COLLAB-02 review marker enforcement, idea_review gate]

# Tech tracking
tech-stack:
  added: []
  patterns: [argparse choices= for enum-like CLI validation, subprocess.run for script integration tests, always-exit-1 as human-verification gate pattern]

key-files:
  created:
    - scripts/pre_submit_check.py
  modified:
    - tests/test_pre_submit_check.py

key-decisions:
  - "argparse choices= handles unknown milestone validation automatically — no custom error code needed; argparse exits 2 on invalid choice"
  - "Always exits 1 (not 0) to enforce human review — computer cannot verify checklist compliance"
  - "Review marker item in idea_review CHECKLISTS covers COLLAB-02 requirement via substring match"

patterns-established:
  - "Milestone gate pattern: print checklist, exit 1 — forces human to read and confirm before proceeding"
  - "Subprocess test pattern: sys.executable + script path + args — platform-independent, no import side effects"

requirements-completed: [CHECK-02]

# Metrics
duration: 5min
completed: 2026-03-21
---

# Phase 02 Plan 02: Pre-Submit Checklist Summary

**Milestone-aware pre-submission checklist (pre_submit_check.py) with argparse --milestone, CHECKLISTS dict for idea_review/concept_review, always-exit-1 gate, and 4-test subprocess suite replacing skipped stubs**

## Performance

- **Duration:** ~5 min
- **Started:** 2026-03-21T14:10:00Z
- **Completed:** 2026-03-21T14:11:12Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Created `scripts/pre_submit_check.py` with CHECKLISTS dict (8 idea_review items, 7 concept_review items)
- argparse `--milestone` with `choices=` enforces valid milestone names automatically (exits 2 on invalid)
- Script always exits 1 — enforces human review gate before any submission
- Replaced 4 skipped test stubs with full subprocess assertions; all 4 pass, full suite 18 passed

## Task Commits

Each task was committed atomically:

1. **Task 1: Implement scripts/pre_submit_check.py** - `0a836f7` (feat)
2. **Task 2: Replace test stubs with full assertions** - `ed1b821` (test)

## Files Created/Modified
- `scripts/pre_submit_check.py` - Milestone-aware checklist printer; CHECKLISTS dict, argparse --milestone, always exits 1
- `tests/test_pre_submit_check.py` - Full subprocess test suite; 4 tests covering items, exit code, unknown milestone, review marker

## Decisions Made
- argparse `choices=` handles unknown milestone validation — no additional custom code needed (argparse exits 2)
- Always-exit-1 is intentional: human must verify checklist, computer cannot confirm compliance
- Review marker item text satisfies COLLAB-02 via case-insensitive substring checks for "review" and "marker"

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- CHECK-02 and COLLAB-02 requirements fulfilled
- Phase 02 quality gates complete: check_consistency.py + pre_submit_check.py both operational
- Full test suite (18 tests) green — ready for Phase 03 or Idea Review submission

---
*Phase: 02-quality-gates*
*Completed: 2026-03-21*
