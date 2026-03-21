---
phase: 01-core-pipeline
plan: 03
subsystem: pipeline
tags: [yaml, python, prompt-engineering, format_map, mission-config]

# Dependency graph
requires:
  - phase: 01-01
    provides: pandoc scaffold and Wave 0 test infrastructure already in place

provides:
  - mission_config.yaml: single source of truth with 11 mission parameter keys
  - scripts/generate_section.py: CLI tool substituting config values into prompt templates
  - prompts/motivation.md: parameterized Claude prompt for Section 1 (Motivation and Objectives)
  - prompts/requirements_derivation.md: parameterized Claude prompt for Section 2 (Requirements Analysis)
  - prompts/payload_tradeoff.md: parameterized Claude prompt for Section 3 (Payload Selection)
  - prompts/ops_concept.md: parameterized Claude prompt for Section 4 (Operations Concept)
  - prompts/risk_analysis.md: parameterized Claude prompt for Risk Analysis
  - prompts/review_section.md: parameterized Claude prompt for section quality review

affects:
  - 01-04 (RTM generation uses mission_config.yaml and requirements.yaml)
  - All future report generation that uses prompt templates

# Tech tracking
tech-stack:
  added: [pyyaml, argparse, pathlib, str.format_map()]
  patterns:
    - "YAML config as single source of truth for all variable substitution"
    - "str.format_map() for {variable} placeholder substitution (not string.Template)"
    - "--prompts-dir argument to support pytest tmp_path fixtures"

key-files:
  created:
    - mission_config.yaml
    - scripts/generate_section.py
    - prompts/motivation.md
    - prompts/requirements_derivation.md
    - prompts/payload_tradeoff.md
    - prompts/ops_concept.md
    - prompts/risk_analysis.md
    - prompts/review_section.md
  modified: []

key-decisions:
  - "str.format_map() used for {variable} substitution — consistent with AUTOMATION_PLAN.md convention (not $variable Template)"
  - "KeyError on missing config key prints clear message and exits 1 — prevents silent failures"
  - "All TBD values kept in mission_config.yaml — mission concept undefined, parameterization enables any swap later"

patterns-established:
  - "Prompt template convention: use only keys present in mission_config.yaml to avoid KeyError"
  - "CLI convention: --prompts-dir overrides default to support test fixtures"
  - "Error handling: missing file or missing key always exits non-zero with descriptive stderr message"

requirements-completed:
  - PIPE-03
  - PIPE-04

# Metrics
duration: 3min
completed: 2026-03-21
---

# Phase 01 Plan 03: Mission Config and Prompt Library Summary

**mission_config.yaml with 11 mission parameters + generate_section.py CLI + 6 parameterized Claude prompt templates substituted via str.format_map()**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-21T11:33:41Z
- **Completed:** 2026-03-21T11:36:24Z
- **Tasks:** 2
- **Files modified:** 8

## Accomplishments
- Created mission_config.yaml as single source of truth for all 11 mission parameters (orbit_altitude_km, mission_name, satellite_class, etc.)
- Created scripts/generate_section.py: reads YAML config, loads prompt template, substitutes {variables} via format_map(), prints to stdout
- Created all six prompt template files in prompts/: motivation, requirements_derivation, payload_tradeoff, ops_concept, risk_analysis, review_section
- All prompts use only keys present in mission_config.yaml — no KeyError possible on real config
- All 3 pytest tests pass (test_config.py x2, test_generate_section.py x1)

## Task Commits

Each task was committed atomically:

1. **Task 1: Create mission_config.yaml** - `8b96761` (feat)
2. **Task 2: Create generate_section.py and all six prompts templates** - `6d28b03` (feat)

## Files Created/Modified
- `mission_config.yaml` - Single source of truth: 11 mission parameters, TBD values for undefined mission concept
- `scripts/generate_section.py` - CLI: --section, --config, --prompts-dir; format_map substitution; graceful error exits
- `prompts/motivation.md` - Section 1: Motivation and Objectives template (6 subsections required)
- `prompts/requirements_derivation.md` - Section 2: Requirements Analysis, YAML objectives/requirements format
- `prompts/payload_tradeoff.md` - Section 3: Payload Selection with trade-off scoring table
- `prompts/ops_concept.md` - Section 4: Operations Concept with mission phases and data flow
- `prompts/risk_analysis.md` - Risk matrix with likelihood/impact scoring
- `prompts/review_section.md` - Quality review against 5 criteria with structured output format

## Decisions Made
- str.format_map() used instead of string.Template for {variable} substitution — matches AUTOMATION_PLAN.md convention
- KeyError on missing config key prints "Missing config key in prompt template: {key}. Add it to {config_path}." and exits 1
- --prompts-dir argument added to generate_section.py to support pytest tmp_path fixture (tests/conftest.py creates tmp prompts dir)

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None.

## User Setup Required

None - no external service configuration required.

## Next Phase Readiness
- PIPE-03 and PIPE-04 complete: any team member can now run `python scripts/generate_section.py --section motivation` to get a ready-to-paste Claude prompt with mission parameters substituted
- Changing orbit_altitude_km in mission_config.yaml propagates to all sections automatically
- Ready for 01-04 if not already complete (RTM generation)
- Idea Review deadline 2026-03-26: prompt library operational

## Self-Check: PASSED

All created files confirmed present:
- mission_config.yaml: FOUND
- scripts/generate_section.py: FOUND
- prompts/motivation.md: FOUND
- prompts/requirements_derivation.md: FOUND
- prompts/payload_tradeoff.md: FOUND
- prompts/ops_concept.md: FOUND
- prompts/risk_analysis.md: FOUND
- prompts/review_section.md: FOUND
- .planning/phases/01-core-pipeline/01-03-SUMMARY.md: FOUND
- Commit 8b96761 (mission_config.yaml): FOUND
- Commit 6d28b03 (generate_section.py + prompts): FOUND

---
*Phase: 01-core-pipeline*
*Completed: 2026-03-21*
