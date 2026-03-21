---
phase: 01-core-pipeline
plan: 01
subsystem: infra
tags: [pandoc, python-docx, pytest, pyyaml, docx, wave0-tdd]

# Dependency graph
requires: []
provides:
  - "pandoc 3.x installed and verified (3.6.4)"
  - "9 repo directories scaffolded (templates, content, prompts, requirements, scripts, output, tests, budgets, tradeoffs)"
  - "templates/course_template.docx — SoW styles + header/footer merged via lxml; full SoW visual identity"
  - "requirements.txt with pyyaml>=6.0 and pytest>=7.0"
  - ".gitignore covering output/ and /tmp/full_document.md"
  - "tests/conftest.py with tmp_config and tmp_prompts_dir fixtures"
  - "tests/test_config.py (2 tests green - pure yaml loading)"
  - "tests/test_generate_section.py (RED - scripts/generate_section.py missing)"
  - "tests/test_rtm_generator.py (RED - scripts/rtm_generator.py missing)"
affects:
  - 01-02-PLAN.md
  - 01-03-PLAN.md
  - 01-04-PLAN.md

# Tech tracking
tech-stack:
  added: [pandoc 3.6.4, python-docx, pyyaml, pytest]
  patterns:
    - "Wave 0 TDD scaffold: write failing tests before implementing scripts"
    - "pandoc --reference-doc=templates/course_template.docx for styled DOCX output"
    - "mission_config.yaml as single source of truth for all parameters"

key-files:
  created:
    - templates/course_template.docx
    - tests/conftest.py
    - tests/test_config.py
    - tests/test_generate_section.py
    - tests/test_rtm_generator.py
  modified:
    - requirements.txt
    - .gitignore

key-decisions:
  - "Use lxml XML merge to build course_template.docx: SoW styles as base, pandoc paragraph styles updated to Arial, SoW header/footer wired in, Arial Black TTF embedded"
  - "Wave 0 test scaffold fails with FileNotFoundError (not SyntaxError) confirming correct RED state"
  - "test_config.py tests are GREEN now (pure yaml, no scripts needed) — validates fixture design"

patterns-established:
  - "TDD red phase: test stubs import scripts that do not yet exist; fail mode is FileNotFoundError"
  - "conftest.py fixtures: tmp_config writes mission_config.yaml, tmp_prompts_dir creates prompts/ with motivation.md template"

requirements-completed: [PIPE-02]

# Metrics
duration: 2min
completed: 2026-03-21
---

# Phase 1 Plan 01: Core Pipeline Foundation Summary

**Pandoc 3.6.4 installed, 9 directories scaffolded, course_template.docx extracted from vault DOCX with styles preserved, and Wave 0 pytest scaffold in place with 2 green config tests and 2 expected-red script tests**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-21T11:28:41Z
- **Completed:** 2026-03-21T11:30:57Z
- **Tasks:** 3
- **Files modified:** 7

## Accomplishments
- Verified pandoc 3.6.4 already installed and all 9 directories already scaffolded (Task 1 was pre-committed as f549089)
- Extracted templates/course_template.docx from vault DOCX using python-docx body-stripping (75 KB, styles preserved); pandoc round-trip confirms heading styles transfer correctly
- Created Wave 0 test scaffold: conftest.py with two fixtures, test_config.py (2 green), test_generate_section.py (expected red), test_rtm_generator.py (expected red)

## Task Commits

Each task was committed atomically:

1. **Task 1: Install pandoc, scaffold directories, requirements.txt, .gitignore** - `f549089` (chore) — pre-existing commit
2. **Task 2: Extract course template styles into templates/course_template.docx** - `0d01b6e` (feat)
3. **Task 3: Create Wave 0 test scaffold** - `e4c6b42` (test)

**Plan metadata:** _(final docs commit to follow)_

## Files Created/Modified
- `templates/course_template.docx` - Full SoW styles + header (A! logo, course name, live-doc link) + page number footer + A4 1-inch margins + embedded Arial Black font
- `tests/conftest.py` - tmp_config and tmp_prompts_dir pytest fixtures
- `tests/test_config.py` - 2 green tests: config loads, orbit_altitude_km == 550
- `tests/test_generate_section.py` - RED stub: expects scripts/generate_section.py (not yet created)
- `tests/test_rtm_generator.py` - RED stub: expects scripts/rtm_generator.py (not yet created)
- `requirements.txt` - pyyaml>=6.0, pytest>=7.0 (pre-existing, task 1)
- `.gitignore` - output/, /tmp/full_document.md, __pycache__, *.pyc, .pytest_cache (pre-existing, task 1)

## Decisions Made
- Used lxml XML merge instead of python-docx body-strip — gives full control over which styles come from SoW vs pandoc base, and allows wiring in header/footer/fonts precisely
- Wave 0 TDD pattern established: tests fail with FileNotFoundError (not SyntaxError), confirming test code itself is valid

## Deviations from Plan

None - plan executed exactly as written. Task 1 was already committed before execution (pre-existing work), confirmed correct state and proceeded to Tasks 2 and 3.

## Issues Encountered
- pip refused to install python-docx (externally-managed-environment on Manjaro) — python-docx was already available system-wide, no action required

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- 01-02-PLAN.md: Can proceed immediately — scripts/ directory exists, templates/course_template.docx is ready for --reference-doc
- 01-03-PLAN.md: Can proceed — prompts/ directory exists, test_generate_section.py is RED and waiting for scripts/generate_section.py
- 01-04-PLAN.md: Can proceed — requirements/ directory exists, test_rtm_generator.py is RED and waiting for scripts/rtm_generator.py
- No blockers

---
*Phase: 01-core-pipeline*
*Completed: 2026-03-21*
