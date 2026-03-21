# ELEC-E4240 Satellite Systems 2026
**Mission Feasibility Study — Aalto University**

Maiju Alavuotunki · Alissa Lebedeva · Simon Bauer

---

## For Readers (Professor / TA)

This repository contains our team's mission feasibility study for the ELEC-E4240 Satellite Systems course, Aalto University 2026. The course theme is *Small Satellite Missions for European Resilience and Societal Security*.

The study follows the structure prescribed in the Statement of Work and is submitted as a PDF exported from a styled DOCX. The document is built from version-controlled Markdown source files using Pandoc with the course template as the reference document.

**Submission artefacts** are in `output/` as dated `.docx` files. The corresponding PDF is produced from the same source.

**AI tool usage** is documented in accordance with the course AI policy. A dedicated AI usage chapter is included in the final document, describing what was generated, how it was validated, and what was written by hand.

**Team document:** see the live Google Doc linked in the document header.

---

## For Engineers (Students)

### The idea

We are three students with jobs and no time to meet. The document is written through async iterations: students discuss and decide, AI writes and verifies, students read and approve.

```
Students decide something async    →  append to design_log.md
One student opens Claude Code      →  briefs Claude with the decision
Claude reads the repo + log        →  updates config, writes sections, runs tools, commits
Students pull and review           →  read the DOCX diff, leave next notes in design_log.md
```

This works because the toolchain separates **decisions** (human) from **execution** (AI). Students never write section text from scratch — they feed Claude the design choices and validate what comes back. When the mission concept changes, update `mission_config.yaml` and rebuild — all outputs stay consistent.

Feasibility study documents are iterative. Keeping everything in Google Docs means losing version control and making it painful to propagate changes. Markdown as source of truth means every change is a diff, every milestone is a git tag, and nothing is lost.

### How it works

```
mission_config.yaml          ← single source of truth for all parameters
      │
      ├─ prompts/*.md        ← fill with config values → paste into Claude
      │         │
      │    Claude output     ← paste back as content/*.md
      │
content/0*.md                ← your actual section text (version-controlled)
      │
build_doc.py                 ← pandoc assembles sections → styled DOCX
      │
output/mission_feasibility_YYYYMMDD.docx
```

### Way of working

**As driver** (the student running Claude Code this session):
1. `git pull`
2. Open Claude Code: *"Read design_log.md and the repo state. We decided [X]. Do [Y]."*
3. Review the diff and the built DOCX
4. `git push`

**As reviewer** (other teammates after a push):
1. `git pull && python scripts/build_doc.py`
2. Open `output/mission_feasibility_*.docx` and read
3. Add any corrections or next decisions to `design_log.md`

**Adding a decision to the log:**
```markdown
## 2026-03-25 — Payload selection
**Decision:** Go with multispectral imager, TRL 7, fits 6U mass budget
**Participants:** Maiju, Alissa
**Context:** SAR was too heavy at 2 kg; imager gives better TRL for this phase
**Action for AI:** Update mission_config.yaml payload_type, update Section 3 draft
**Status:** Pending
```

### Quick start

```bash
# 1. Install dependencies (Manjaro/Arch)
sudo pacman -S pandoc
pip install pyyaml pytest

# 2. Edit the mission concept
$EDITOR mission_config.yaml

# 3. Generate a section prompt, paste into Claude, paste output back
python scripts/generate_section.py --section motivation > /tmp/prompt.md
# → paste /tmp/prompt.md into Claude → paste Claude output into content/01_motivation.md

# 4. Build the document
python scripts/build_doc.py
# → output/mission_feasibility_YYYYMMDD.docx
```

### Repository layout

```
mission_config.yaml          Mission parameters (edit this first)
requirements.txt             Python dependencies

content/                     Section Markdown files (01–08, numeric order)
prompts/                     Parameterized Claude prompt templates per section
requirements/
  requirements.yaml          Structured requirements (objectives → reqs → obs)
scripts/
  build_doc.py               Pandoc pipeline: content/*.md → styled DOCX
  generate_section.py        Fills prompt templates with mission_config values
  rtm_generator.py           Generates RTM table from requirements.yaml
templates/
  course_template.docx       Pandoc reference-doc with full SoW styling
budgets/                     Mass, power, link budget CSVs (Phase 3)
tradeoffs/                   Payload/subsystem trade-off YAML files (Phase 4)
tests/                       Pytest suite
output/                      Built DOCX files (git-ignored)
vault/                       Course PDFs and original SoW DOCX (read-only)
.planning/                   GSD planning documents (roadmap, phase plans, state)
```

### Milestones

| Milestone | Deadline | Required |
|-----------|----------|---------|
| Idea Review | 2026-03-26 | Sections 1–2 drafted, RTM, mission config defined |
| Concept Review | 2026-04-23 | Sections 1–5, mass/power budgets, link budget |
| Detailed Design | 2026-05-21 | Full document, all budgets, trade-off matrices |
| Presentation | 2026-06-01–04 | Final submission |

### Updating the header link

The document header contains a "Link to your live document" hyperlink. To update it, change `google_doc_url` in `mission_config.yaml` and run:

```bash
python3 -c "
import zipfile, shutil, yaml
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

---

## For Agents (Claude / AI)

### What this repo is

A Python + Pandoc toolchain for authoring an Aalto satellite mission feasibility study in Markdown and building a correctly styled DOCX submission. The document must follow the structure in `vault/2026 Statement of Work for Mission Feasibility Study.docx` exactly.

### Current state (2026-03-21)

Phase 1 (Core Pipeline) is complete. The pipeline is working end-to-end:
- `python scripts/build_doc.py` produces a correctly styled DOCX from `content/*.md`
- `templates/course_template.docx` has full SoW styling (Arial, heading palette, header, page numbers, A4 margins)
- `mission_config.yaml` is the parameter source; values are TBD pending mission concept definition
- `scripts/generate_section.py` and `scripts/rtm_generator.py` are implemented and tested

Phases 2–5 (quality gates, engineering calculators, trade-off tools, orchestration) are planned in `.planning/ROADMAP.md`.

### Design log

`design_log.md` at the repo root is the primary input channel from students to AI. At the start of every session, read it. Any entry with `Status: Pending` is work to pick up. Mark entries `Status: Done` once actioned.

### Key conventions

- **One truth, one file:** all mission parameters live in `mission_config.yaml`. Scripts read it; never hardcode values.
- **Prompt substitution uses `str.format_map()`** with `{variable}` syntax — consistent across all prompt templates.
- **Content files are numbered** `01_` through `08_` — pandoc assembles them in glob order via `content/0*.md`.
- **`requirements.yaml` uses plain values** (no `{variable}` placeholders) — it is not a template.
- **Styles are in `course_template.docx`** — do not add inline formatting to Markdown; use heading levels and let pandoc map them.
- **`output/` is git-ignored** — never commit built DOCX files.
- **`vault/` is read-only** — do not modify course PDFs or the original SoW.

### Planning system

This repo uses GSD (Get Shit Done) for planning. See `.planning/` for:
- `PROJECT.md` — requirements, decisions, traceability
- `ROADMAP.md` — phase breakdown and progress
- `STATE.md` — current position, accumulated decisions, blockers

When making changes that affect the pipeline, template, or conventions, update `STATE.md` (decisions section) and `PROJECT.md` (requirement status) to keep them current.

### Template notes

`templates/course_template.docx` was built by XML-merging the SoW's `word/styles.xml` and `word/theme/theme1.xml` into a pandoc-generated base using `lxml`, then adding the SoW header and a page number footer. The pandoc-specific paragraph styles (BodyText, Compact, BlockText, etc.) are preserved and updated to Arial to match the SoW default font. Do not regenerate this file with python-docx body-stripping — that approach loses the header, footer, and font embedding.
