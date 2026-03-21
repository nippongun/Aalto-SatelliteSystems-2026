# Satellite Feasibility Study — AI Automation Plan

**Project:** ELEC-E4240 Satellite Systems, Aalto 2026
**Goal:** Build a suite of local tools that generate, check, and format the feasibility study — all authored in Markdown, exported to DOCX using the course template.

---

## Core Pipeline: Markdown → DOCX

### The Problem
- Course requires submissions as PDFs from a structured DOCX template (Google Docs)
- AI-generated content is easiest to produce, version-control, and iterate in Markdown
- Manual copy-paste between Markdown and Google Docs is error-prone and slow

### The Solution: Pandoc + Reference Document
`pandoc` supports a `--reference-doc` flag that uses an existing `.docx` as a style template while injecting new content. This means:

1. Extract the course template structure from `2026 Statement of Work for Mission Feasibility Study.docx`
2. Create a `template.docx` stripped of content but keeping all heading styles, fonts, margins, and page setup
3. Write every section of the feasibility study as a `.md` file
4. Run `pandoc` to produce a correctly styled `.docx` → export to PDF

```bash
pandoc content/mission.md -o output/mission_feasibility.docx \
  --reference-doc=templates/reference_base.docx \
  --table-of-contents \
  --toc-depth=3
```

### File Structure
```
Aalto-SatelliteSystems-2026/
├── templates/
│   └── course_template.docx          # Full SoW styles + header/footer, no body content
├── content/
│   ├── 01_motivation.md
│   ├── 02_requirements.md
│   ├── 03_payload.md
│   ├── 04_mission_design.md
│   ├── 05_spacecraft_design.md
│   ├── 06_product_assurance.md
│   ├── 07_project_description.md
│   └── 08_permits.md
├── budgets/
│   ├── mass_budget.csv
│   ├── power_budget.csv
│   └── link_budget.csv
├── scripts/
│   ├── build_doc.py                  # Assembles all .md → .docx
│   ├── check_consistency.py          # Section consistency checker
│   ├── rtm_generator.py              # RTM from requirements YAML
│   ├── link_budget.py
│   ├── mass_power_budget.py
│   └── orbit_analysis.py
├── requirements/
│   └── requirements.yaml             # Single source of truth for requirements
├── KNOWLEDGE_BASE.md
├── AUTOMATION_PLAN.md
└── output/
    └── mission_feasibility.docx
```

### Template Extraction Steps
1. `templates/course_template.docx` is built by merging styles from the vault SoW DOCX into a pandoc-generated base using `lxml` (raw XML manipulation). It contains:
   - SoW `docDefaults`: Arial 11pt, 1.15× line spacing
   - SoW heading styles (H1–H6) with correct sizes and grey colour palette
   - SoW Title (26pt) and Subtitle (15pt grey)
   - All pandoc-specific styles (BodyText, Compact, BlockText, etc.) updated to Arial
   - SoW page header: "A!" logo (Arial Black) + course name + live-document hyperlink placeholder + horizontal rule
   - A4 portrait, 1-inch margins on all sides
   - Embedded Arial Black TTF font
   Result: zero body paragraphs, all styles and page layout intact.
2. Map Markdown heading levels to DOCX heading styles:
   - `#` → Heading 1
   - `##` → Heading 2
   - `###` → Heading 3
   - `**bold**` → Bold inline
   - Tables → Table style from template
3. Test round-trip: simple `test.md` → `pandoc` → inspect output styling

### Build Script (`scripts/build_doc.py`)
```bash
python scripts/build_doc.py
# Optional overrides:
# python scripts/build_doc.py --config path/to/config.yaml --output-dir path/to/out/
```
Cross-platform Python script. Reads `mission_config.yaml` for metadata, assembles `content/0*.md` in sorted order via `tempfile`, calls pandoc via `subprocess.run`. Works on Windows, Linux, macOS.

---

## A. Documentation Generation & Consistency

### A1. Section Prompt Templates
Each feasibility study section has a parameterized prompt template. Variables are injected from a central `mission_config.yaml`:

```yaml
# mission_config.yaml
mission_name: "TBD"
satellite_class: "CubeSat"
mass_kg: ~8
orbit_type: "LEO"
orbit_altitude_km: 550
inclination_deg: 97.6
mission_application: "TBD"
payload_type: "TBD"
```

Prompt template example for Section 1 (Motivation):
```
Given the following mission parameters: {mission_config}
Write the "Mission Motivation and Objectives" section of a satellite feasibility study.
Cover: problem statement, why a space solution is needed, mission goal (measurable),
product of the mission, success criteria (minimal/full/extended), and target orbit justification.
Output in Markdown. Use ## for subsections. All technical claims must include numbers and units.
```

Run via `scripts/generate_section.py --section motivation --config mission_config.yaml`

### A2. Internal Consistency Checker (`scripts/check_consistency.py`)
Reads all `.md` content files and flags:

| Check | Method |
|-------|--------|
| Orbit altitude consistent across all sections | Regex extract all altitude numbers, flag if >1 unique value |
| Mass budget total ≤ system dry mass | Parse mass_budget.csv, compare to system mass in config |
| Power budget peak ≤ EPS generation | Parse power_budget.csv, compare to EPS capacity in config |
| Every requirement has a number and unit | Regex: requirements lines without `[0-9]+\s*(km|m|dB|W|kg|bps|°)` |
| Every objective maps to ≥1 requirement | Parse requirements.yaml, check RTM coverage |
| Success criteria present in Section 1 | Check for "minimal success" and "full success" keywords |
| AI usage chapter present | Check for section heading matching "AI usage" |

Run before every submission: `python scripts/check_consistency.py content/`
Output: `consistency_report.md` with PASS/FAIL per check and line references.

### A3. Pre-submission Checklist (`scripts/pre_submit_check.py`)
Milestone-aware checklist. Pass `--milestone idea_review` to get the right subset:

```
[ ] Mission goal is measurable (has numbers and units)
[ ] Target orbit altitude, inclination specified
[ ] At least 3 objectives defined
[ ] RTM has ≥1 row per objective
[ ] Mass budget present with margins
[ ] Power budget present with margins
[ ] All figures have captions
[ ] References cited for all factual claims
[ ] AI usage section present
[ ] Document version and date in header
```

### A4. Section Completeness Linter
Checks that required subsections from the SoW template are present in the Markdown:

```python
REQUIRED_SECTIONS = {
    "idea_review": [
        "Mission motivation", "Problem to be solved", "Mission goal",
        "Product of the mission", "Success criteria", "Target orbit"
    ],
    "concept_review": [
        "Requirement analysis", "Payload selection", "Mission overview",
        "Spacecraft architecture", "Mass budget", "Power budget"
    ],
    # ... etc
}
```

---

## B. Engineering Calculations

### B1. Link Budget Calculator (`scripts/link_budget.py`)
Self-contained Python script. Inputs via CLI or YAML config:

```python
# Computes: FSPL, received power, SNR, Eb/N0, link margin
# Inputs: frequency_GHz, altitude_km, tx_power_dBm, tx_gain_dBi,
#         rx_gain_dBi, rx_noise_temp_K, data_rate_bps, required_Eb_N0_dB
# Outputs: link_budget.md table + pass/fail on link margin
```

Outputs a Markdown table that drops directly into `content/05_spacecraft_design.md`.

### B2. Mass & Power Budget Tool (`scripts/mass_power_budget.py`)
- Reads `budgets/mass_budget.csv` and `budgets/power_budget.csv`
- Computes totals, margins, system-level margin
- Flags if any subsystem exceeds allocation or system margin <10%
- Outputs formatted Markdown tables ready for document insertion

CSV format:
```csv
subsystem,mass_kg,margin_kg
Structure,0.8,0.08
OBC,0.12,0.012
EPS,0.35,0.035
COM,0.15,0.015
ADCS,0.18,0.018
Payload,TBD,TBD
```

### B3. Orbital Analysis Tool (`scripts/orbit_analysis.py`)
Uses `sgp4` or analytical formulas for LEO parameters:

| Output Parameter | Formula / Source |
|-----------------|-----------------|
| Orbital period | Kepler's third law |
| Orbital velocity | v = √(μ/r) |
| Ground track speed | Project v onto ground |
| Eclipse fraction | Geometry, altitude, inclination |
| Daily ground station contacts | Elevation mask + orbit geometry |
| Contact time per pass | Cone geometry |
| Weekly downlink capacity | contact_time × effective_data_rate |
| Revisit time (for imaging) | Repeat ground track period |

Output: `orbit_summary.md` table for document insertion.

### B4. Data Budget Calculator
Links orbit analysis → link budget → payload data volume:

```
payload_data_rate_bps × duty_cycle → data_generated_per_orbit_MB
contact_time_per_day × effective_link_rate → downlink_capacity_per_day_MB
downlink_capacity / data_generated → buffer_days (must be < orbit lifetime)
```

Flags if data generated > data downloadable (mission bottleneck).

---

## C. Trade-off Analysis

### C1. Payload Trade-off Matrix Generator (`scripts/tradeoff.py`)
Input: `tradeoffs/payload_options.yaml`

```yaml
options:
  - name: "Multispectral imager"
    mass_kg: 0.5
    power_W: 5
    data_rate_Mbps: 50
    TRL: 7
    cost_kEUR: 80
    performance_score: 8  # 1-10, mission-specific
  - name: "SAR"
    mass_kg: 2.0
    power_W: 30
    ...
criteria_weights:
  mass: 0.2
  power: 0.2
  data_rate: 0.1
  TRL: 0.3
  cost: 0.1
  performance: 0.1
```

Output: scored trade-off table in Markdown, with winner highlighted.

### C2. Subsystem Trade-off Trees
One YAML file per subsystem (ADCS, COM, EPS, OBC, Structure).
Each lists standard options with key parameters pulled from Aalto course notes and COTS databases.
Script generates the trade-off section for the document automatically.

### C3. COTS Component Lookup
Prompt template: given mission requirements, query satsearch.co-style lookup or search NASA SST SoA PDF for matching components. Returns candidate list with mass/power/cost/TRL for input to trade-off matrix.

---

## D. Review & Quality

### D1. Grading Rubric Self-Assessment
Before each submission, feed the full document to Claude with the grading rubric:

```
Assess the following feasibility study section against these criteria:
- Realism: Are all numbers physically plausible? Are claims backed by calculation?
- Completeness: Are all required subsections present per the SoW?
- Internal consistency: Do all cross-references (budgets, orbits, requirements) agree?
- Figure quality: Is each figure referenced in the text and does it have a caption?
- Requirement quality: Does each requirement have a number, unit, and verification method?

Return: score estimate per criterion (1-5), specific weaknesses, suggested fixes.
```

### D2. Instructor Comment Integration
Workflow for each review cycle:
1. Export instructor comments from Google Docs as text
2. Feed to Claude: "Map each comment to the relevant section. For each, suggest a fix. Output as a task list."
3. Apply fixes to `.md` source files
4. Run consistency checker
5. Re-build DOCX

### D3. Version Control & Diff
- Each milestone produces a tagged git commit: `git tag idea-review-2026-03-26`
- Before submission: `git diff HEAD~1 -- content/` shows exactly what changed
- Diff is included in the document version history section

### D4. AI Usage Documentation Generator
A `scripts/log_ai_usage.py` script that:
- Reads a `ai_usage_log.yaml` (append to this every session)
- Generates the required "AI Usage" chapter automatically
- Includes: what was generated, what was validated, how validation was done

```yaml
# ai_usage_log.yaml
- date: 2026-03-21
  tool: Claude (Sonnet 4.6)
  section: KNOWLEDGE_BASE.md
  usage: "Summarized course PDFs and SoW document"
  validation: "Cross-checked against original PDFs"
```

---

## E. Workflow Orchestration

### E1. Milestone Workflow
Each milestone has a dedicated runner: `scripts/milestone.sh --target idea_review`

Steps executed automatically:
1. Pull latest `mission_config.yaml`
2. Generate any missing sections via Claude prompt templates
3. Run consistency checker → fix flagged issues
4. Run pre-submit checklist → confirm all boxes
5. Run rubric self-assessment → review score
6. Build DOCX from Markdown
7. Git commit and tag
8. Open output DOCX for final review

### E2. Mission Config as Single Source of Truth
`mission_config.yaml` is the root parameter file. Every tool reads from it.
Changing the orbit altitude in one place → all budgets, link calculations, and generated text update on next build.

This makes mission trade-offs fast: change altitude from 550km to 400km → rebuild → see all impacts immediately.

### E3. Requirements as YAML (`requirements/requirements.yaml`)
All requirements stored in structured YAML:

```yaml
objectives:
  - id: OBJ-01
    text: "Detect GNSS jamming signals over European territory"
    requirements:
      - id: REQ-01
        text: "The satellite shall detect GNSS jamming with SNR > X dB"
        observation_reqs:
          - id: OBS-01
            text: "GNSS signal shall be sampled at ≥ Y MHz bandwidth"
            instrument_reqs:
              - id: INS-01
                text: "Receiver sensitivity shall be ≤ Z dBm"
```

From this single file:
- `rtm_generator.py` outputs the full RTM table in Markdown
- Consistency checker verifies all IDs are referenced in the document
- Orphaned requirements (no parent) are flagged automatically

### E4. Prompt Library (`prompts/`)
A folder of reusable `.md` prompt templates, one per document section and tool.
Parameterized with `{variable}` placeholders, filled by `scripts/generate_section.py`.

Prompts available:
- `prompts/motivation.md`
- `prompts/requirements_derivation.md`
- `prompts/payload_tradeoff.md`
- `prompts/ops_concept.md`
- `prompts/risk_analysis.md`
- `prompts/review_section.md` (quality check)
- `prompts/rubric_assessment.md`
- `prompts/ai_usage_chapter.md`

---

## F. Async Collaboration & Human-in-the-Loop

### The model

Three students, no scheduled meetings, all have jobs. The document is produced through rapid async iterations:

```
Students discuss & decide          (WhatsApp / async)
        │
        ▼
Student captures decision          → design_log.md
        │
        ▼
Student opens Claude Code          → briefs Claude: "read the design log, here's what we decided"
        │
        ▼
Claude reads repo context          → design_log.md, mission_config.yaml, content/, requirements/
        │
        ▼
Claude does the work               → updates config, writes/revises sections, runs tools, commits
        │
        ▼
Student reviews output             → reads built DOCX, scans git diff
        │
        ▼
Teammates pull & read              → leave notes in design_log.md or fix inline
        │
        └──────────────────────────► next iteration
```

The student acting as driver in a Claude Code session is the human-in-the-loop. They brief Claude, approve the output, and commit. Other teammates review asynchronously via git and leave their input in `design_log.md` for the next session.

### F1. Design log (`design_log.md`)

A running plain-text log at the repo root. Students append entries when decisions are made. Claude reads it at the start of each session for context.

Entry format:
```markdown
## YYYY-MM-DD — <topic>
**Decision:** <what was decided>
**Participants:** <who was involved>
**Context:** <why, what alternatives were considered>
**Action for AI:** <what Claude should do with this>
**Status:** Pending / Done
```

Rules:
- Append only — never edit or delete old entries
- Mark `Status: Done` once Claude has acted on an entry
- Short is fine: one sentence decisions are valid
- If a decision changes a config value, say which key

Claude reads `design_log.md` at the start of every session. Any entry with `Status: Pending` is work to be picked up.

### F2. Student roles in a session

One student acts as **driver** per session:
1. Pull latest from git
2. Open Claude Code in the repo root
3. Say: *"Read the design log and the current state of the repo. Here's what we decided since last session: [summary]. Do X."*
4. Review what Claude produces (diff + built DOCX)
5. Commit and push

Other students are **reviewers**:
1. Pull after driver pushes
2. Read the DOCX or the diff
3. Add notes or corrections to `design_log.md` for the next session

### F3. What AI does vs what students decide

| Students decide | AI does |
|-----------------|---------|
| Mission concept and application | Write section drafts from prompts |
| Payload choice | Run trade-off calculations |
| Orbit parameters | Compute orbital analysis, link budget |
| Requirements wording | Format into requirements.yaml, generate RTM |
| Which sections need rewriting | Rewrite them given the feedback |
| Final approval before submission | Run consistency checker, pre-submit checklist, build DOCX, git tag |

Students **never** write section text from scratch — they feed decisions and Claude drafts. Students **always** read and approve before committing.

### F4. Section review status

Each content file can carry a review header comment:

```markdown
<!-- reviewed: Simon 2026-03-25 -->
# Mission Motivation and Objectives
...
```

The pre-submit checklist (CHECK-02) will flag any section without a reviewed marker as unverified before submission.

---

## Implementation Priority

| Priority | Tool | Why First |
|----------|------|-----------|
| 1 | Markdown → DOCX pipeline | Unblocks everything else |
| 2 | `mission_config.yaml` + section templates | Needed before Idea Review (Mar 26) |
| 3 | `requirements.yaml` + RTM generator | Required at every milestone |
| 4 | Mass + power budget calculator | Required at Concept Review (Apr 23) |
| 5 | Consistency checker | Quality gate before every submission |
| 6 | Link budget calculator | Builds on HW1 work already done |
| 7 | Orbit analysis tool | Needed for Concept Review |
| 8 | Trade-off matrix generator | Payload selection chapter |
| 9 | Rubric self-assessment prompt | Polish before each submission |
| 10 | Full milestone workflow script | Ties everything together |

---

## Dependencies

```
pandoc        # DOCX generation
python >= 3.10
  pyyaml      # Config and requirements parsing
  pandas      # Budget CSV handling
  numpy       # Orbital mechanics math
  python-docx # DOCX inspection/style extraction
  sgp4        # Orbital propagation (optional, for contact time)
```

Install: `pip install pyyaml pandas numpy python-docx sgp4`
Pandoc: `sudo pacman -S pandoc` (Manjaro)
