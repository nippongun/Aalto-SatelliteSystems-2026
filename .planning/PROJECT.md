# Satellite Feasibility Study Toolchain

## What This Is

A portable Python + Pandoc toolchain that lets a team of up to 3 author the Aalto ELEC-E4240 satellite mission feasibility study entirely in Markdown, then build a correctly styled `.docx` submission using the course template. Includes engineering calculators (link budget, mass/power, orbit analysis), a requirements traceability matrix generator, parameterized section prompt templates for Claude, and a consistency checker that flags contradictions before every submission.

## Core Value

The Pandoc pipeline must work — without it, no other tool can produce course-ready output.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [x] PIPE-01 — Pandoc pipeline: `build_doc.py` converts assembled Markdown → styled `.docx` using course template as reference doc
- [x] PIPE-02 — Template: `course_template.docx` — full SoW styles (Arial, headings, title/subtitle), SoW header (A! logo + course name + live-doc link), A4 1-inch margins, embedded Arial Black font
- [x] PIPE-03 — `mission_config.yaml`: single source of truth for mission parameters (altitude, mass, frequency, etc.)
- [x] PIPE-04 — Section prompt library: `prompts/` folder with parameterized `.md` prompts per feasibility study section, filled from `mission_config.yaml` and output ready to paste into Claude
- [x] PIPE-05 — RTM generator: reads `requirements/requirements.yaml` and outputs a Markdown RTM table
- [ ] CHECK-01 — Consistency checker: Python script scanning all `content/*.md` for contradictions (altitude mismatches, budget overruns, orphaned requirements, missing units)
- [ ] CHECK-02 — Pre-submit checklist: milestone-aware checklist script (`--milestone idea_review` etc.)
- [ ] CALC-01 — Link budget calculator: Python CLI script, outputs Markdown table ready for document insertion
- [ ] CALC-02 — Mass + power budget tool: reads `budgets/*.csv`, computes margins, flags if system margin <10%, outputs Markdown tables
- [ ] CALC-03 — Orbital analysis tool: altitude + inclination → period, contact time, eclipse fraction, weekly downlink capacity
- [ ] TRADE-01 — Trade-off matrix generator: YAML-driven weighted scoring, outputs Markdown table
- [ ] QUAL-01 — Rubric self-assessment prompt: prompt template that grades a document section against the SoW criteria
- [ ] LOG-01 — AI usage log + chapter generator: `ai_usage_log.yaml` → auto-generates the required AI usage chapter
- [ ] ORCH-01 — Full milestone runner script: chains all tools for a given milestone target

### Collaboration

- [x] COLLAB-01 — Design log (`design_log.md`): running file where students capture async decisions and mission choices; AI reads it as context when drafting or updating sections
- [ ] COLLAB-02 — Section review markers: a lightweight way for students to mark a section as human-reviewed vs AI-drafted, surfaced in the pre-submit checklist

### Out of Scope

- Claude API integration in scripts — no automated API calls; Claude Code is used interactively by a student acting as driver
- GUI or web interface — CLI tools only
- Hardware simulation or MATLAB/Simulink integration — Python only

## Context

- **Course:** Aalto ELEC-E4240 Satellite Systems 2026. Theme: Small Satellite Missions for European Resilience and Societal Security
- **Deliverable format:** PDF from DOCX, submitted to MyCourses + Google Docs online version for instructor comments
- **Upcoming deadline:** Idea Review — 2026-03-26 (5 days). Must have: Pandoc pipeline + section prompts + mission_config.yaml + RTM generator
- **Mission concept:** Not yet defined. Tools must be parameterized so swapping `mission_config.yaml` regenerates all outputs
- **Course template:** `templates/course_template.docx` — SoW styles (Arial, headings H1–H6, Title/Subtitle), SoW header (A! logo + course name + live-doc link), page number footer, A4 1-inch margins, embedded Arial Black font. Pandoc reference-doc for all DOCX builds.
- **AI policy:** AI tools explicitly allowed; a dedicated AI usage chapter is required in the final document
- **Knowledge base:** `KNOWLEDGE_BASE.md` at repo root — full document structure, subsystem reference, deadlines
- **Automation plan:** `AUTOMATION_PLAN.md` at repo root — full technical design for all tools

## Constraints

- **Portability:** Must run on teammates' machines — provide `requirements.txt`, `README.md`, and clear setup instructions. Any evironment must work (Windows, Linux, macOS)
- **Dependencies:** `pandoc`, Python ≥3.10, `pyyaml`, `pandas`, `numpy`, `python-docx`, `sgp4` (optional)
- **Content generation:** Claude Code is used interactively as the AI driver — one student runs a session, briefs Claude with the design log, Claude writes/runs/commits. No automated API calls in scripts.
- **Timeline:** Idea Review in 5 days; Concept Review April 23; Detailed Design May 21; Presentation June 1–4
- **Document structure:** Must follow the SoW template section order exactly

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Pandoc + `--reference-doc` for DOCX generation | Preserves course template styles while keeping content in version-controlled Markdown | — Pending |
| Python CLI scripts (not Jupyter) for calculators | Outputs pipe into document build automatically; no notebook server needed | — Pending |
| Claude Code as interactive AI driver (not API) | One student runs a session, briefs Claude with design_log.md, Claude writes/runs/commits; human validates before push | — Confirmed |
| Single `mission_config.yaml` as source of truth | Mission concept not locked yet; parameterization means any concept can be swapped in | — Pending |
| `requirements.yaml` as structured requirements store | Enables RTM auto-generation and orphan detection | — Pending |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PIPE-01 | Phase 1 | Done |
| PIPE-02 | Phase 1 | Done |
| PIPE-03 | Phase 1 | Done |
| PIPE-04 | Phase 1 | Done |
| PIPE-05 | Phase 1 | Done |
| CHECK-01 | Phase 2 | Pending |
| CHECK-02 | Phase 2 | Pending |
| CALC-01 | Phase 3 | Pending |
| CALC-02 | Phase 3 | Pending |
| CALC-03 | Phase 3 | Pending |
| TRADE-01 | Phase 4 | Pending |
| QUAL-01 | Phase 4 | Pending |
| LOG-01 | Phase 4 | Pending |
| ORCH-01 | Phase 5 | Pending |
| COLLAB-01 | Phase 1 | Done |
| COLLAB-02 | Phase 2 | Pending |

---
*Last updated: 2026-03-21 — Phase 1 complete: pipeline working, course_template.docx has full SoW styling + header/footer*
