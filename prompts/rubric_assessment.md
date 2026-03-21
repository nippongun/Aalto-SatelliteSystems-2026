You are reviewing a satellite mission feasibility study against the Aalto ELEC-E4240 grading rubric.

Mission context:
- Mission name: {mission_name}
- Satellite class: {satellite_class}
- Orbit: {orbit_altitude_km} km, {inclination_deg}° ({orbit_type})
- Application: {mission_application}
- Payload: {payload_type}
- Milestone: {milestone}

Full document text to review:
---
[PASTE FULL DOCUMENT TEXT HERE]
---

Assess the full document against each criterion below. Score 1–5 (5 = excellent).

## Criterion 1 — Realism
Are all technical numbers physically plausible for a {satellite_class} at {orbit_altitude_km} km?
Check: orbital period, contact time, link margin, mass budget margins, power budget margins.
Flag any claim that lacks a reference, calculation, or citation.

## Criterion 2 — Completeness
Are all required sections from the SoW present?
Required for {milestone}:
- idea_review: Sections 1–2 (Motivation, Requirements), RTM, mission config defined
- concept_review: Sections 1–5, mass/power/data budgets, payload trade-off matrix
- preliminary_design: Sections 1–6, verification matrix, full RTM, link budget
- detailed_design: All 8 sections, all budgets finalized, Gantt chart, cost estimate, ≥5 risks
Flag any section that is missing or is still a placeholder.

## Criterion 3 — Internal Consistency
Do all cross-references agree?
- Altitude in text matches mission_config.yaml
- Mass budget total ≤ satellite_class envelope
- Power budget total ≤ EPS generation
- Link margin ≥ 3 dB
- Every RTM row traces to an objective
Flag specific contradictions with section references.

## Criterion 4 — Requirement Quality
Does every requirement have:
- A unique ID (REQ-XX)
- Measurable text (number + unit)
- A verification method (test / analysis / inspection / demonstration)
Flag any requirement that fails any of the three criteria.

## Criterion 5 — Figure and Table Quality
- Every figure is referenced in the text and has a caption
- Every table has a title and column headers
- No orphaned figures or unlabelled axes
Flag figures or tables that violate these rules.

## Criterion 6 — Writing Quality
Is the text concise, unambiguous, and at MSc report level?
Flag: passive constructions that obscure the subject, vague quantifiers ("large", "fast", "good"), claims stated as fact without citation.

---

Output format:

## Rubric Assessment — {milestone}

| Criterion | Score (1–5) | Key finding |
|-----------|-------------|-------------|
| Realism | X | ... |
| Completeness | X | ... |
| Internal consistency | X | ... |
| Requirement quality | X | ... |
| Figure/table quality | X | ... |
| Writing quality | X | ... |

**Overall estimated grade range:** X–Y / 13

## Issues to Fix (prioritized by impact on grade)
1. [Most critical]
2. ...

## Suggested Fixes
[Specific rewrites or additions for the top 3 issues]
