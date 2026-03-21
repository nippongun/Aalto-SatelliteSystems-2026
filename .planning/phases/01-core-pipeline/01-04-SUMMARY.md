---
phase: 01-core-pipeline
plan: "04"
subsystem: requirements
tags: [yaml, rtm, requirements-traceability, pytest, argparse]

# Dependency graph
requires:
  - phase: 01-01
    provides: pandoc scaffold and test infrastructure (conftest.py, tests/ dir)

provides:
  - requirements/requirements.yaml — structured requirements store with 4-level nesting schema
  - scripts/rtm_generator.py — CLI tool producing Markdown RTM table from YAML
  - PIPE-05 automated verification: pytest tests/test_rtm_generator.py

affects: [02-section-generator, 03-document-assembly, idea-review-submission]

# Tech tracking
tech-stack:
  added: [pyyaml (already installed), argparse (stdlib), pathlib (stdlib)]
  patterns: [fail-loud KeyError on malformed YAML fields, argparse default path with --override flag]

key-files:
  created:
    - requirements/requirements.yaml
    - scripts/rtm_generator.py
  modified: []

key-decisions:
  - "Use req['id'] (not req.get('id')) — KeyError on malformed data is intentional fail-loud behavior"
  - "YAML schema supports full 4-level nesting (objectives→requirements→observation_reqs→instrument_reqs) from day 1, RTM generator only surfaces top 2 levels for now"
  - "{orbit_altitude_km} in REQ-03 is literal placeholder text, not a template variable — RTM outputs it verbatim"

patterns-established:
  - "argparse with sensible default path allows test to pass tmp file via --requirements flag"
  - "flatten_requirements() separates data logic from I/O — testable independently of subprocess"

requirements-completed: [PIPE-05]

# Metrics
duration: 1min
completed: 2026-03-21
---

# Phase 1 Plan 04: RTM Generator Summary

**YAML requirements store (4-level schema) and argparse-driven Markdown RTM generator — full pytest suite 4/4 green**

## Performance

- **Duration:** 1 min
- **Started:** 2026-03-21T11:34:05Z
- **Completed:** 2026-03-21T11:35:24Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments

- `requirements/requirements.yaml` with 2 objectives and 4 requirements, supporting full 4-level nesting schema from day 1
- `scripts/rtm_generator.py` CLI tool that reads YAML and prints a Markdown RTM table (header + separator + 4 data rows)
- Script fails loud: exits 1 with "Not found" on missing file; KeyError on malformed YAML entries
- All 4 pytest tests pass: test_config (2), test_generate_section (1), test_rtm_generator (1)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create requirements/requirements.yaml** - `f097f6a` (feat)
2. **Task 2: Create scripts/rtm_generator.py** - `72ec8f8` (feat)

## Files Created/Modified

- `requirements/requirements.yaml` — Nested requirements store with 2 objectives, 4 requirements, optional observation_reqs/instrument_reqs levels
- `scripts/rtm_generator.py` — CLI RTM generator: reads YAML via --requirements arg, outputs 3-column Markdown table, fail-loud on errors

## Decisions Made

- `req["id"]` over `req.get("id")` — silent None on malformed data is worse than a loud KeyError; fail early
- 4-level YAML schema established now even though RTM only flattens 2 levels — avoids schema migration later when observation/instrument reqs are added
- `--requirements` argparse flag with default path means tests can pass tmp file without monkeypatching

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness

- PIPE-05 complete: `python scripts/rtm_generator.py` produces complete Markdown RTM table ready for Idea Review (2026-03-26)
- Full Phase 1 PIPE test suite green (PIPE-01 through PIPE-05 verified by pytest)
- `requirements.yaml` uses TBD stubs — edit as mission concept is defined, RTM updates automatically

---
*Phase: 01-core-pipeline*
*Completed: 2026-03-21*
