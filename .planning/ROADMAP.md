# Roadmap: Satellite Feasibility Study Toolchain

## Overview

Five phases deliver a complete Python + Pandoc toolchain for the Aalto ELEC-E4240 satellite mission feasibility study. Phase 1 is deadline-gated (Idea Review: 2026-03-26) and delivers the core pipeline plus mission config and RTM. Phases 2-5 build quality gates, engineering calculators, trade-off and review tools, and finally the milestone orchestration script that ties the whole workflow together.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Core Pipeline** - Pandoc build pipeline, mission config, prompt templates, and RTM generator — required for Idea Review (2026-03-26)
- [ ] **Phase 2: Quality Gates** - Consistency checker and milestone-aware pre-submit checklist
- [ ] **Phase 3: Engineering Calculators** - Link budget, mass/power budget, and orbital analysis tools
- [ ] **Phase 4: Trade-off and Review Tools** - Trade-off matrix generator, rubric self-assessment prompt, and AI usage log generator
- [ ] **Phase 5: Workflow Orchestration** - Full milestone runner script that chains all tools end-to-end

## Phase Details

### Phase 1: Core Pipeline
**Goal**: Authors can write section content in Markdown and produce a correctly styled `.docx` submission ready for the Idea Review deadline
**Depends on**: Nothing (first phase)
**Requirements**: PIPE-01, PIPE-02, PIPE-03, PIPE-04, PIPE-05
**Success Criteria** (what must be TRUE):
  1. Running `build_doc.sh` on assembled Markdown content produces a `.docx` whose heading styles match the course template (`course_template.docx`)
  2. `mission_config.yaml` exists with all mission parameters; changing a value (e.g. altitude) and rebuilding propagates the change into the generated document output
  3. Every feasibility study section has a corresponding parameterized prompt file in `prompts/`; running `generate_section.py --section motivation --config mission_config.yaml` prints a ready-to-paste Claude prompt with mission values substituted
  4. Running `rtm_generator.py` against `requirements/requirements.yaml` produces a complete Markdown RTM table with columns for requirement ID, text, and parent objective
**Plans**: 4 plans

Plans:
- [x] 01-01-PLAN.md — Install pandoc, scaffold directories, extract course template styles, create Wave 0 test infrastructure
- [ ] 01-02-PLAN.md — Write `scripts/build_doc.sh` and stub `content/0*.md` section files; verify Pandoc round-trip
- [ ] 01-03-PLAN.md — Create `mission_config.yaml` and `scripts/generate_section.py`; write all `prompts/*.md` templates
- [ ] 01-04-PLAN.md — Create `requirements/requirements.yaml` schema and `scripts/rtm_generator.py`; verify RTM table output

### Phase 2: Quality Gates
**Goal**: Every submission passes automated consistency and completeness checks before the document is built
**Depends on**: Phase 1
**Requirements**: CHECK-01, CHECK-02
**Success Criteria** (what must be TRUE):
  1. Running `check_consistency.py content/` produces a `consistency_report.md` that correctly flags a deliberately introduced altitude mismatch across two section files as FAIL, and reports PASS when values agree
  2. Running `pre_submit_check.py --milestone idea_review` prints only the checklist items relevant to that milestone and exits non-zero when any item is unresolved
  3. The consistency checker flags a mass budget CSV where total mass exceeds the system dry mass value in `mission_config.yaml`
**Plans**: TBD

Plans:
- [ ] 02-01: Implement `scripts/check_consistency.py` with all seven checks (altitude, mass, power, requirement units, objective-to-requirement coverage, success criteria presence, AI usage section presence)
- [ ] 02-02: Implement `scripts/pre_submit_check.py` with milestone-aware checklist; test against `idea_review`, `concept_review` targets

### Phase 3: Engineering Calculators
**Goal**: Authors can run Python CLI scripts to compute link budget, mass/power margins, and orbital parameters, and paste the resulting Markdown tables directly into content sections
**Depends on**: Phase 1
**Requirements**: CALC-01, CALC-02, CALC-03
**Success Criteria** (what must be TRUE):
  1. Running `link_budget.py` with frequency, altitude, TX power, and gain arguments prints a Markdown table including free-space path loss, received power, SNR, and link margin, and exits non-zero if link margin is negative
  2. Running `mass_power_budget.py` against `budgets/mass_budget.csv` and `budgets/power_budget.csv` prints formatted Markdown tables with totals and margins, and prints a warning if any subsystem margin is below 10%
  3. Running `orbit_analysis.py` with altitude and inclination arguments prints a Markdown summary table including orbital period, eclipse fraction, daily contact time, and weekly downlink capacity
**Plans**: TBD

Plans:
- [ ] 03-01: Implement `scripts/link_budget.py` with CLI interface; create `budgets/link_budget.csv` template
- [ ] 03-02: Implement `scripts/mass_power_budget.py`; create `budgets/mass_budget.csv` and `budgets/power_budget.csv` templates with correct CSV schema
- [ ] 03-03: Implement `scripts/orbit_analysis.py` using analytical formulas (Kepler + geometry); validate against known LEO parameters

### Phase 4: Trade-off and Review Tools
**Goal**: Authors can generate scored trade-off tables from YAML, run a rubric self-assessment prompt, and auto-generate the AI usage chapter
**Depends on**: Phase 1
**Requirements**: TRADE-01, QUAL-01, LOG-01
**Success Criteria** (what must be TRUE):
  1. Running `tradeoff.py` against a `tradeoffs/payload_options.yaml` file with at least two options and defined criteria weights produces a Markdown table with weighted scores, ranked options, and a highlighted winner
  2. `prompts/rubric_assessment.md` exists and contains the full self-assessment prompt; running `generate_section.py --section rubric_assessment` substitutes in the current section text and outputs a ready-to-paste prompt
  3. Running `log_ai_usage.py` against `ai_usage_log.yaml` produces a correctly structured AI usage Markdown chapter that can be inserted directly into the document
**Plans**: TBD

Plans:
- [ ] 04-01: Implement `scripts/tradeoff.py` with YAML-driven weighted scoring; create `tradeoffs/payload_options.yaml` template
- [ ] 04-02: Write `prompts/rubric_assessment.md` and `prompts/ai_usage_chapter.md`; implement `scripts/log_ai_usage.py` and create `ai_usage_log.yaml` schema

### Phase 5: Workflow Orchestration
**Goal**: A single script chains all tools for any given milestone, from config pull through consistency check to DOCX build and git tag
**Depends on**: Phases 2, 3, 4
**Requirements**: ORCH-01
**Success Criteria** (what must be TRUE):
  1. Running `scripts/milestone.sh --target idea_review` executes the full sequence (consistency check, pre-submit check, DOCX build) and halts with a clear error message if any step fails
  2. A successful run of `milestone.sh` produces a git commit tagged with the milestone name (e.g. `idea-review-2026-03-26`) and the output `.docx` file is present in `output/`
  3. Running with an unknown `--target` value prints a usage message listing all valid milestone targets
**Plans**: TBD

Plans:
- [ ] 05-01: Write `scripts/milestone.sh` with step-chaining, failure-halt logic, and git commit + tag step; test against `idea_review` target
- [ ] 05-02: Add `requirements.txt`, `README.md` with setup instructions (Manjaro + portable); validate full workflow on clean directory

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Core Pipeline | 3/4 | In Progress|  |
| 2. Quality Gates | 0/2 | Not started | - |
| 3. Engineering Calculators | 0/3 | Not started | - |
| 4. Trade-off and Review Tools | 0/2 | Not started | - |
| 5. Workflow Orchestration | 0/2 | Not started | - |
