<!-- ai-draft: 2026-04-19, reviewed and approved by Simon -->

# AI Usage

## Role of AI in This Project

This project uses AI (Claude Code, Anthropic) to create, format, and maintain documentation throughout the mission feasibility study. AI assists the team in achieving design goals faster and with greater precision, while the students retain full responsibility for all engineering and design decisions.

The workflow is structured as follows: students discuss and design the satellite at a high level, owning the conceptual and engineering decisions. The AI logs these decisions, drafts document sections, and runs automated verification checks. All output is reviewed and approved by the students before it enters the document. This makes the students the designers of the system while delegating the mechanical work of documentation, formatting, and consistency checking to the AI.

System requirements are stored as structured data in a YAML file (`requirements/requirements.yaml`). This approach treats requirements as immutable, traceable facts rather than free-form prose. The AI generates the Requirements Traceability Matrix (RTM) directly from this file, ensuring the RTM is always consistent with the source requirements and cannot drift due to copy-paste errors.

The AI fulfils four roles in this project:

- **Documentation creation** — drafting section content from team decisions logged in `design_log.md`
- **Documentation maintenance** — updating budgets, requirements, and cross-references as the design evolves
- **Verification assistance** — running automated consistency checks, flagging margin violations, and identifying missing or orphaned requirements before each submission
- **Error detection** — cross-checking team decisions against course standards and engineering constraints, surfacing potential issues for student review

The students validate all AI output by reviewing drafts, confirming requirement wording, checking calculations against known values, and approving commits. For each session, the AI logs its activity in `ai_usage_log.yaml`, which feeds this chapter automatically. The full repository and session history are available at: https://github.com/nippongun/Aalto-SatelliteSystems-2026

## Session Log

| Date | Tool | Sections touched | Activity |
|------|------|-----------------|----------|
| 2026-03-21 | Claude Code (claude-sonnet-4-6) | Repository scaffold | Toolchain setup, knowledge base, workflow documentation |
| 2026-03-23 | Claude Code (claude-sonnet-4-6) | mission_config.yaml, design_log.md | Logged team mission concept decisions; populated mission parameters |
| 2026-04-19 | Claude Code (claude-sonnet-4-6) | KNOWLEDGE_BASE.md, requirements.yaml, design_log.md, 08_permits.md, 09_ai_usage.md | Concept Review prep: compliance requirements added, permits section drafted, payload classification corrected, SMART requirement flags raised |
