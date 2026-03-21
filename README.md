# ELEC-E4240 Satellite Systems 2026
**Mission Feasibility Study — Aalto University**

Maiju Alavuotunki · Alissa Lebedeva · Simon Bauer

---

## What this repo does

This repository is an AI-assisted authoring system for a satellite mission feasibility study. It separates **decisions** (made by the team) from **execution** (handled by AI and scripts). The team logs design choices; the AI drafts sections, runs calculations, checks consistency, and builds the submission DOCX. Students read, verify, and approve before anything is committed.

The document source lives in version-controlled Markdown. A Pandoc pipeline assembles sections into a correctly styled DOCX matching the Aalto course template. When a mission parameter changes, update `mission_config.yaml` and rebuild — all outputs update consistently.

```
mission_config.yaml        ← single source of truth for all mission parameters
      │
      ├─ prompts/*.md       ← prompt templates, filled with config values
      │        │
      │   AI output         ← paste response into content/*.md
      │
content/0*.md              ← versioned section text
      │
scripts/build_doc.py       ← pandoc assembles sections → styled DOCX
      │
output/mission_feasibility_YYYYMMDD.docx
```

---

## For Readers (Professor / TA)

This repository contains the team's mission feasibility study for the ELEC-E4240 Satellite Systems course, Aalto University 2026. The course theme is *Small Satellite Missions for European Resilience and Societal Security*.

The study follows the structure prescribed in the Statement of Work and is submitted as a PDF exported from a styled DOCX. The document is built from version-controlled Markdown source files using Pandoc with the course template as the reference document.

**Submission artefacts** are in `output/` as dated `.docx` files. The corresponding PDF is produced from the same source.

**AI tool usage** is documented in accordance with the course AI policy. A dedicated AI usage chapter is included in the final document, describing what was generated, how it was validated, and what was written by hand.

**Team document:** see the live Google Doc linked in the document header.

---

## Getting started

### Prerequisites

| Tool | Install |
|------|---------|
| Python ≥ 3.10 | [python.org](https://www.python.org/downloads/) |
| Pandoc | [pandoc.org/installing](https://pandoc.org/installing.html) |
| Git | [git-scm.com](https://git-scm.com/) |
| An AI agent | Claude Code recommended — see [Working with AI](#working-with-ai) |

```bash
# Install Python dependencies (all platforms)
pip install pyyaml pytest

# Verify pandoc is available
pandoc --version
```

### First run

```bash
# 1. Clone and enter the repo
git clone <repo-url> && cd Aalto-SatelliteSystems-2026

# 2. Define the mission concept
$EDITOR mission_config.yaml

# 3. Generate a section prompt and draft with AI
python scripts/generate_section.py --section motivation
# → copy the output into your AI agent → save response to content/01_motivation.md

# 4. Build the document
python scripts/build_doc.py
# → output/mission_feasibility_YYYYMMDD.docx

# 5. Run quality checks
python scripts/check_consistency.py content/
python -m pytest tests/ -q
```

---

## How to use this repo

### The workflow

The work happens in async sessions. One team member acts as **driver** per session; others review and leave notes.

**As driver:**
1. `git pull`
2. Open your AI agent, brief it with recent decisions (see [Prompting guide](#prompting-guide))
3. AI updates config, drafts sections, runs checks
4. Review the DOCX diff — read and approve before committing
5. `git push`

**As reviewer** (after a push):
1. `git pull && python scripts/build_doc.py`
2. Open `output/mission_feasibility_*.docx`
3. Add corrections or next decisions to `design_log.md`

### Logging decisions

Every design decision goes into `design_log.md` before the AI acts on it. The AI reads this file at the start of every session and picks up all `Status: Pending` entries.

```markdown
## 2026-03-25 — Payload selection
**Decision:** Go with multispectral imager, TRL 7, fits 6U mass budget
**Participants:** [student names]
**Context:** SAR was too heavy at 2 kg; imager gives better TRL for this phase
**Action for AI:** Update mission_config.yaml payload_type, update Section 3 draft
**Status:** Pending
```

Once the AI acts on an entry, it marks it `Status: Done`.

### Do's and Don'ts

**Do:**
- Log every design decision in `design_log.md` *before* asking the AI to act on it
- Update `mission_config.yaml` whenever a mission parameter changes — never hardcode values elsewhere
- Run `python scripts/check_consistency.py content/` before every commit
- Build the DOCX and read it before committing — the diff is your review
- Validate AI-generated numbers against course PDFs and engineering judgement
- Mark `design_log.md` entries `Status: Done` once actioned
- Tag each milestone: `git tag idea-review-2026-03-26`

**Don't:**
- Let the AI make design decisions — orbit selection, payload choice, risk thresholds are yours
- Commit without reading the diff and built DOCX
- Modify anything in `vault/` — it is read-only course material
- Commit files in `output/` — they are gitignored and regenerated from source
- Accept AI-generated component specs or physical constants without cross-checking
- Write section text directly in `content/*.md` without a corresponding `design_log.md` entry — future sessions will have no context for the change

---

## Working with AI

### Recommended tool

**Claude Code** (Anthropic) is recommended. It reads the full repo context, runs scripts directly, edits files, and follows the conventions in `AGENT.md`. Any capable AI coding agent or chat assistant can be used — the prompts in `prompts/` work with any model that understands Markdown and YAML.

For chat-based workflows (ChatGPT, Gemini, etc.): generate the prompt with `python scripts/generate_section.py --section <name>`, paste it into the chat, and save the response to the appropriate `content/` file.

For agentic workflows (Claude Code, Cursor, Copilot Workspace): point the agent at the repo root and brief it with `design_log.md` as the primary input.

### Prompting guide

**Session start — always begin with context:**
```
Read design_log.md and the current repo state.

Since last session we decided:
- [Decision 1, one sentence]
- [Decision 2, one sentence]

Please: [specific action]
```

**Asking for a section draft:**
```
Run python scripts/generate_section.py --section motivation to get the prompt.
Draft content/01_motivation.md from it. Mark the file <!-- ai-draft: YYYY-MM-DD -->.
```

**Asking for a budget update:**
```
We selected [payload]. Its mass is X kg and peak power is Y W.
Update budgets/mass_budget.csv and budgets/power_budget.csv.
Run check_consistency.py and tell me if any margin is violated.
```

**Asking for a requirements update:**
```
Add a new objective: [text]. Derive 2–3 requirements with measurable units and verification methods.
Update requirements/requirements.yaml, regenerate the RTM, and paste the table into content/02_requirements.md.
```

**Asking for a quality review:**
```
Review content/03_payload.md using prompts/review_section.md as the rubric.
Score each criterion and list the top 3 issues to fix.
```

**Asking for a pre-submission check:**
```
Run python scripts/pre_submit_check.py --milestone idea_review.
Then run check_consistency.py and tell me which items are still failing.
```

**Things AI should never decide without you:**
- Which orbit, altitude, or inclination to use
- Which payload to select
- Which requirements to include or exclude
- Risk likelihood and impact scores
- Any number that goes into a budget without a source

### AI capabilities

#### Available now

| Capability | How to use |
|------------|------------|
| Draft Section 1 — Mission Motivation | `python scripts/generate_section.py --section motivation` → paste into AI |
| Draft Section 2 — Requirements derivation | `python scripts/generate_section.py --section requirements_derivation` → paste into AI |
| Draft Section 3 — Payload trade-off | `python scripts/generate_section.py --section payload_tradeoff` → paste into AI |
| Draft Section 4 — Operations concept | `python scripts/generate_section.py --section ops_concept` → paste into AI |
| Draft Section 7 — Risk analysis | `python scripts/generate_section.py --section risk_analysis` → paste into AI |
| Per-section quality review | `python scripts/generate_section.py --section review_section` → paste section text + prompt into AI |
| Full-document rubric assessment | Use `prompts/rubric_assessment.md` — paste full document text |
| AI usage chapter generation | Use `prompts/ai_usage_chapter.md` — reads from `ai_usage_log.yaml` |
| Consistency checking | `python scripts/check_consistency.py content/` |
| Pre-submission checklist | `python scripts/pre_submit_check.py --milestone <name>` |
| RTM generation | `python scripts/rtm_generator.py` |
| Document build | `python scripts/build_doc.py` |

#### Planned

| Capability | Script | Status |
|------------|--------|--------|
| Link budget calculator | `scripts/link_budget.py` | Planned |
| Mass/power budget tool with margin reporting | `scripts/mass_power_budget.py` | Planned |
| Orbital analysis (contact time, revisit, eclipse) | `scripts/orbit_analysis.py` | Planned |
| Payload/subsystem trade-off matrix generator | `scripts/tradeoff.py` | Planned |
| AI usage chapter auto-generator | `scripts/log_ai_usage.py` | Planned |
| Section completeness linter | `scripts/section_linter.py` | Planned |

---

## Repository layout

```
mission_config.yaml          Single source of truth — edit this first
ai_usage_log.yaml            Session AI usage log — append each session
design_log.md                Team decisions — AI reads this at session start
requirements.txt             Python dependencies

content/                     Section Markdown files, assembled in numeric order
  01_motivation.md             Mission Motivation and Objectives
  02_requirements.md           Requirement Analysis + RTM
  03_payload.md                Payload Selection
  04_mission_design.md         Mission and Spacecraft Design Overview
  05_spacecraft_design.md      Spacecraft Design + budgets
  06_product_assurance.md      Product Assurance Plan
  07_project_description.md    Project Description + risk register
  08_permits.md                Permits and Licences

prompts/                     AI prompt templates (filled from mission_config.yaml)
  motivation.md                Section 1
  requirements_derivation.md   Section 2
  payload_tradeoff.md          Section 3
  ops_concept.md               Section 4 (ConOps)
  risk_analysis.md             Section 7
  review_section.md            Per-section quality review
  rubric_assessment.md         Full-document grading rubric
  ai_usage_chapter.md          AI usage chapter generation

scripts/
  build_doc.py               Pandoc pipeline: content/*.md → styled DOCX
  generate_section.py        Fills prompt templates with mission_config values
  rtm_generator.py           Generates RTM table from requirements.yaml
  check_consistency.py       Nine-check consistency scanner (run before every commit)
  pre_submit_check.py        Milestone-aware pre-submission checklist

requirements/
  requirements.yaml          Structured requirements (objectives → reqs → verification)

budgets/
  mass_budget.csv            Mass budget by subsystem
  power_budget.csv           Power budget by subsystem and mode
  link_budget.csv            Link budget parameters
  cost_estimate.csv          Cost estimate by category

tradeoffs/
  payload_options.yaml       Payload trade-off input (options + scoring criteria)

templates/
  course_template.docx       Pandoc reference-doc with full SoW styling (do not regenerate)

tests/                       Pytest suite — run before every commit
output/                      Built DOCX files (gitignored — regenerate with build_doc.py)
vault/                       Course PDFs and original SoW DOCX (read-only — do not modify)
.planning/                   Phase plans, roadmap, and execution state
```

---

## Milestones

| Milestone | Deadline | Minimum required |
|-----------|----------|-----------------|
| Idea Review | 2026-03-26 | Sections 1–2, RTM, mission config defined |
| Concept Review | 2026-04-23 | Sections 1–5, mass/power/link budgets, payload trade-off |
| Preliminary Design | 2026-05-07 | Sections 1–6, full RTM with verification methods, orbit analysis |
| Detailed Design | 2026-05-21 | All 8 sections, all budgets, Gantt chart, cost estimate, ≥5 risks |
| Presentation | 2026-06-01–04 | Final submission, slides |

Run `python scripts/pre_submit_check.py --milestone <name>` to see the full checklist for each milestone.

---

## For AI Agents

Read `AGENT.md` for the full session protocol, constraints, file authority, and scope of work. The key points:

- Read `design_log.md` at the start of every session — all `Status: Pending` entries are work to pick up
- `mission_config.yaml` owns all mission parameters — never hardcode values in scripts or content
- `requirements/requirements.yaml` owns all requirements — reference by ID in content, never duplicate text
- `output/` is gitignored — never commit built DOCX files
- `vault/` is read-only — never modify course PDFs or the original SoW
- Run `python scripts/check_consistency.py content/` and `python -m pytest tests/ -q` before committing any content or budget change
- Do not make mission design choices — ask if the intent is unclear

### Key conventions

- Prompt templates use `{variable}` substitution via `str.format_map()` — consistent across all prompts
- Content files are numbered `01_` through `08_` — pandoc assembles them in glob order via `content/0*.md`
- Every requirement needs: a unique ID, measurable text (number + unit), and a `verification_method`
- Section review markers: `<!-- ai-draft: YYYY-MM-DD -->` or `<!-- reviewed: YYYY-MM-DD -->`
- `course_template.docx` was built by XML-merging SoW styles into a pandoc base — do not regenerate it with python-docx body-stripping (loses header, footer, font embedding)

### Updating the header link

Change `google_doc_url` in `mission_config.yaml`, then run:

```python
python3 -c "
import zipfile, yaml
from lxml import etree
url = yaml.safe_load(open('mission_config.yaml'))['google_doc_url']
PKG = 'http://schemas.openxmlformats.org/package/2006/relationships'
with zipfile.ZipFile('templates/course_template.docx') as z:
    files = {n: z.read(n) for n in z.namelist()}
root = etree.fromstring(files['word/_rels/header1.xml.rels'])
for r in root.findall(f'{{{PKG}}}Relationship'):
    if 'hyperlink' in r.get('Type',''): r.set('Target', url)
files['word/_rels/header1.xml.rels'] = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)
with zipfile.ZipFile('templates/course_template.docx','w') as z:
    [z.writestr(n,d) for n,d in files.items()]
print('Header link updated to', url)
"
```
