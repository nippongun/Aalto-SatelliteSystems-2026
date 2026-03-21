# Satellite Feasibility Study Toolchain

## What This Is

A portable Python + Pandoc toolchain that lets a team of up to 3 author the Aalto ELEC-E4240 satellite mission feasibility study entirely in Markdown, then build a correctly styled `.docx` submission using the course template. Includes engineering calculators (link budget, mass/power, orbit analysis), a requirements traceability matrix generator, parameterized section prompt templates for Claude, and a consistency checker that flags contradictions before every submission.

## Core Value

The Pandoc pipeline must work — without it, no other tool can produce course-ready output.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] PIPE-01 — Pandoc pipeline: `build_doc.sh` converts assembled Markdown → styled `.docx` using course template as reference doc
- [ ] PIPE-02 — Template extraction: `course_template.docx` stripped of content, retaining all heading/paragraph styles
- [ ] PIPE-03 — `mission_config.yaml`: single source of truth for mission parameters (altitude, mass, frequency, etc.)
- [ ] PIPE-04 — Section prompt library: `prompts/` folder with parameterized `.md` prompts per feasibility study section, filled from `mission_config.yaml` and output ready to paste into Claude
- [ ] PIPE-05 — RTM generator: reads `requirements/requirements.yaml` and outputs a Markdown RTM table
- [ ] CHECK-01 — Consistency checker: Python script scanning all `content/*.md` for contradictions (altitude mismatches, budget overruns, orphaned requirements, missing units)
- [ ] CHECK-02 — Pre-submit checklist: milestone-aware checklist script (`--milestone idea_review` etc.)
- [ ] CALC-01 — Link budget calculator: Python CLI script, outputs Markdown table ready for document insertion
- [ ] CALC-02 — Mass + power budget tool: reads `budgets/*.csv`, computes margins, flags if system margin <10%, outputs Markdown tables
- [ ] CALC-03 — Orbital analysis tool: altitude + inclination → period, contact time, eclipse fraction, weekly downlink capacity
- [ ] TRADE-01 — Trade-off matrix generator: YAML-driven weighted scoring, outputs Markdown table
- [ ] QUAL-01 — Rubric self-assessment prompt: prompt template that grades a document section against the SoW criteria
- [ ] LOG-01 — AI usage log + chapter generator: `ai_usage_log.yaml` → auto-generates the required AI usage chapter
- [ ] ORCH-01 — Full milestone runner script: chains all tools for a given milestone target

### Out of Scope

- Claude API integration (automated content generation) — manual copy-paste workflow chosen; avoids API key dependency and keeps humans in the loop for validation
- GUI or web interface — CLI tools only
- Hardware simulation or MATLAB/Simulink integration — Python only

## Context

- **Course:** Aalto ELEC-E4240 Satellite Systems 2026. Theme: Small Satellite Missions for European Resilience and Societal Security
- **Deliverable format:** PDF from DOCX, submitted to MyCourses + Google Docs online version for instructor comments
- **Upcoming deadline:** Idea Review — 2026-03-26 (5 days). Must have: Pandoc pipeline + section prompts + mission_config.yaml + RTM generator
- **Mission concept:** Not yet defined. Tools must be parameterized so swapping `mission_config.yaml` regenerates all outputs
- **Course template:** `vault/2026 Statement of Work for Mission Feasibility Study.docx` — styles source
- **AI policy:** AI tools explicitly allowed; a dedicated AI usage chapter is required in the final document
- **Knowledge base:** `KNOWLEDGE_BASE.md` at repo root — full document structure, subsystem reference, deadlines
- **Automation plan:** `AUTOMATION_PLAN.md` at repo root — full technical design for all tools

## Constraints

- **Portability:** Must run on teammates' machines — provide `requirements.txt`, `README.md`, and clear setup instructions. Primary dev platform is Manjaro Linux.
- **Dependencies:** `pandoc`, Python ≥3.10, `pyyaml`, `pandas`, `numpy`, `python-docx`, `sgp4` (optional)
- **Content generation:** Section prompts are copy-paste-to-Claude only — no API calls
- **Timeline:** Idea Review in 5 days; Concept Review April 23; Detailed Design May 21; Presentation June 1–4
- **Document structure:** Must follow the SoW template section order exactly

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Pandoc + `--reference-doc` for DOCX generation | Preserves course template styles while keeping content in version-controlled Markdown | — Pending |
| Python CLI scripts (not Jupyter) for calculators | Outputs pipe into document build automatically; no notebook server needed | — Pending |
| Manual copy-paste for Claude prompts (not API) | No API key dependency; keeps human validation in the loop; required for AI usage chapter | — Pending |
| Single `mission_config.yaml` as source of truth | Mission concept not locked yet; parameterization means any concept can be swapped in | — Pending |
| `requirements.yaml` as structured requirements store | Enables RTM auto-generation and orphan detection | — Pending |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PIPE-01 | Phase 1 | Pending |
| PIPE-02 | Phase 1 | Pending |
| PIPE-03 | Phase 1 | Pending |
| PIPE-04 | Phase 1 | Pending |
| PIPE-05 | Phase 1 | Pending |
| CHECK-01 | Phase 2 | Pending |
| CHECK-02 | Phase 2 | Pending |
| CALC-01 | Phase 3 | Pending |
| CALC-02 | Phase 3 | Pending |
| CALC-03 | Phase 3 | Pending |
| TRADE-01 | Phase 4 | Pending |
| QUAL-01 | Phase 4 | Pending |
| LOG-01 | Phase 4 | Pending |
| ORCH-01 | Phase 5 | Pending |

---
*Last updated: 2026-03-21 — roadmap initialized, requirement IDs assigned*
