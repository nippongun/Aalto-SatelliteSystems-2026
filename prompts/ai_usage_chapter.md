Generate the "AI Usage" chapter for a satellite mission feasibility study.

This chapter is required by the Aalto ELEC-E4240 AI usage policy.
It must describe: what AI tools were used, what was generated, how outputs were validated, and a critical analysis of reliability.

AI usage log entries:
---
{ai_usage_log}
---

Mission context:
- Mission name: {mission_name}
- Satellite class: {satellite_class}

Write the chapter in Markdown. Use ## for subsections.

Cover:
1. **Overview of AI tools used** — which tools, version, dates
2. **What was generated** — list by section: what AI drafted, what was written by hand
3. **Validation methodology** — for each type of AI output (calculations, text, requirements), how was it verified?
   - Calculations: cross-checked against analytical formulas or reference values
   - Requirements text: reviewed by team, compared to SoW
   - Section drafts: read and edited by at least one student before commit
4. **Critical analysis** — where did AI produce plausible but incorrect outputs? How were errors caught?
5. **Limitations** — what AI cannot reliably do in this context (e.g., provide real component specs without hallucination risk)

Tone: factual, academic. This chapter is graded on honesty and analytical depth, not on how much AI was used.
Output in Markdown. All factual claims about AI tools must be verifiable from the log entries above.
