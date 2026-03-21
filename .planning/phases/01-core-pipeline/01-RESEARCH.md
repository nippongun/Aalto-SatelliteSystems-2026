# Phase 1: Core Pipeline - Research

**Researched:** 2026-03-21
**Domain:** Pandoc DOCX generation, Python CLI scripting, YAML configuration, Markdown template systems
**Confidence:** HIGH (all key decisions pre-made; research confirms/refines implementation details)

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| PIPE-01 | `build_doc.sh` converts assembled Markdown to styled `.docx` using course template as `--reference-doc` | Pandoc `--reference-doc` confirmed; installation step required first |
| PIPE-02 | `course_template.docx` stripped of content, retaining all heading/paragraph styles | Template extraction procedure documented; critical pitfall identified (see below) |
| PIPE-03 | `mission_config.yaml` as single source of truth for mission parameters | PyYAML `safe_load()` pattern; `string.Template` or f-string substitution |
| PIPE-04 | `prompts/` folder with parameterized `.md` prompts per feasibility study section, filled from config, output ready to paste | `generate_section.py` argparse + PyYAML + string.Template pattern confirmed |
| PIPE-05 | Reads `requirements/requirements.yaml` and outputs a Markdown RTM table | PyYAML nested dict traversal; Python tabular Markdown output via f-strings |
</phase_requirements>

---

## Summary

Phase 1 builds the entire toolchain foundation. Every subsequent phase depends on the Pandoc pipeline (PIPE-01/02), the config system (PIPE-03), and the prompt generator (PIPE-04). The RTM generator (PIPE-05) is needed for the Idea Review submission on 2026-03-26.

All four architectural decisions are already locked: Pandoc + `--reference-doc`, Python CLI scripts only, `string.Template` substitution from a single YAML config, and nested YAML for requirements. Research confirms these are sound choices with well-understood implementation paths. The primary implementation risk is the reference-doc template extraction step: Pandoc's official docs recommend generating the base reference-doc from Pandoc itself rather than using the course file directly, then copying styles from the course template.

Pandoc is **not currently installed** on the dev machine. Installation is the first task of the phase and blocks everything else.

**Primary recommendation:** Install pandoc first (one pacman command), then follow the two-step template extraction (pandoc-generated base + LibreOffice style transfer from course file), then build scripts, config, and prompt library in dependency order.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| pandoc | 3.x (latest via pacman) | Markdown → DOCX conversion with style reference | Only tool that supports `--reference-doc` for DOCX; widely used in academic pipelines |
| pyyaml | 6.x | Parse `mission_config.yaml` and `requirements.yaml` | Standard Python YAML library; `safe_load()` is the correct API for untrusted YAML |
| Python | ≥3.10 (3.14.3 installed) | All scripting; confirmed installed | Required by PROJECT.md; already present |
| string.Template (stdlib) | stdlib | `$variable` substitution in prompt `.md` files | No additional dependency; `safe_substitute()` leaves unfilled vars intact — useful during authoring |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| argparse (stdlib) | stdlib | CLI interface for `generate_section.py` | Every Python CLI script in this project |
| pathlib (stdlib) | stdlib | File path handling | Prefer over `os.path` in Python ≥3.6 |
| python-docx | 1.x | Inspect/verify style names in generated DOCX | PIPE-02 verification step only; not needed at runtime |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| string.Template | Jinja2 | Jinja2 is more powerful but adds a dependency; `string.Template` is sufficient for `{var}` → value substitution in prompt files. Note: AUTOMATION_PLAN.md uses `{variable}` brace syntax — must use `str.format_map()` or replace with `$variable` for `string.Template` |
| PyYAML | ruamel.yaml | ruamel preserves comments on round-trip; not needed here — we only read, never write back |
| Flat Markdown section files | Single big `.md` | Flat section files (`content/0*.md`) allow per-section git diffs and per-section prompt generation; `cat content/0*.md` assembles them trivially |

**Installation:**
```bash
# Pandoc (Manjaro)
sudo pacman -S pandoc

# Python dependencies (Phase 1 only needs pyyaml)
pip install pyyaml

# Optional for DOCX style inspection
pip install python-docx
```

---

## Architecture Patterns

### Recommended Project Structure

```
Aalto-SatelliteSystems-2026/
├── templates/
│   └── course_template.docx      # Styles-only, no content (PIPE-02)
├── content/
│   ├── 01_motivation.md          # Idea Review sections
│   ├── 02_requirements.md
│   ├── 03_payload.md
│   ├── 04_mission_design.md
│   ├── 05_spacecraft_design.md
│   ├── 06_product_assurance.md
│   ├── 07_project_description.md
│   └── 08_permits.md
├── prompts/
│   ├── motivation.md             # Parameterized prompt templates (PIPE-04)
│   ├── requirements_derivation.md
│   ├── payload_tradeoff.md
│   ├── ops_concept.md
│   ├── risk_analysis.md
│   └── review_section.md
├── requirements/
│   └── requirements.yaml         # Nested requirements structure (PIPE-05)
├── scripts/
│   ├── build_doc.sh              # Pandoc pipeline (PIPE-01)
│   ├── generate_section.py       # Prompt generator (PIPE-04)
│   └── rtm_generator.py          # RTM table output (PIPE-05)
├── output/                       # Generated DOCX files (git-ignored)
├── mission_config.yaml           # Single config source of truth (PIPE-03)
└── requirements.txt              # Python dependencies
```

### Pattern 1: Pandoc Reference-Doc DOCX Build

**What:** Shell script assembles sorted Markdown section files and passes them to pandoc with `--reference-doc` pointing to the style-only template.

**When to use:** Every time content changes; run before any submission.

**Critical detail:** Pandoc uses the reference-doc's _style definitions_, not its content. The reference-doc must contain every style name that pandoc will produce (Heading 1, Heading 2, Normal, Table, etc.). If a style is missing from the reference-doc, pandoc falls back to its built-in default — headings will lose course formatting.

```bash
#!/bin/bash
# scripts/build_doc.sh
set -euo pipefail
cat content/0*.md > /tmp/full_document.md
pandoc /tmp/full_document.md \
  -o "output/mission_feasibility_$(date +%Y%m%d).docx" \
  --reference-doc=templates/course_template.docx \
  --toc --toc-depth=3 \
  --from markdown+tables+pipe_tables
echo "Built: output/mission_feasibility_$(date +%Y%m%d).docx"
```

### Pattern 2: Two-Step Reference-Doc Template Extraction (PIPE-02)

**What:** The course `.docx` cannot be used directly as a reference-doc. Pandoc's docs state the reference-doc should be a Pandoc-generated file with styles edited in, not an arbitrary DOCX.

**Recommended procedure:**
1. Generate pandoc's default reference: `pandoc -o templates/reference_base.docx --print-default-data-file reference.docx`
2. Open `vault/2026 Statement of Work for Mission Feasibility Study.docx` in LibreOffice → note heading fonts, sizes, margins
3. Open `templates/reference_base.docx` in LibreOffice → apply matching styles (Heading 1, Heading 2, Normal) → save as `templates/course_template.docx`
4. Test: run a simple `pandoc test.md -o test.docx --reference-doc=templates/course_template.docx` and verify headings

**Why not use course template directly:** Pandoc 3.x has known issues where heading styles from non-Pandoc-generated DOCX files are dropped or ignored (GitHub issue #10282). Starting from pandoc's own reference base avoids this.

### Pattern 3: YAML Config + String Substitution (PIPE-03/04)

**What:** `generate_section.py` reads `mission_config.yaml`, loads the named prompt template, substitutes `$variable` placeholders, and prints the result.

**Substitution syntax decision:** The AUTOMATION_PLAN.md uses `{variable}` brace syntax in prompt examples. Two options:
- `str.format_map(config_dict)` — uses `{variable}` syntax, stdlib, one line
- `string.Template(text).safe_substitute(config_dict)` — uses `$variable` syntax, stdlib, more robust (does not raise on missing keys)

**Recommendation:** Use `str.format_map()` with the `{variable}` syntax already planned in AUTOMATION_PLAN.md. Simpler, consistent with existing design.

```python
# scripts/generate_section.py
import argparse, yaml, pathlib, sys

def main():
    parser = argparse.ArgumentParser(description="Generate a section prompt with mission parameters")
    parser.add_argument("--section", required=True, help="Section name (e.g. motivation)")
    parser.add_argument("--config", default="mission_config.yaml", help="Path to mission config YAML")
    args = parser.parse_args()

    config_path = pathlib.Path(args.config)
    prompt_path = pathlib.Path("prompts") / f"{args.section}.md"

    if not config_path.exists():
        sys.exit(f"Config not found: {config_path}")
    if not prompt_path.exists():
        sys.exit(f"Prompt not found: {prompt_path}")

    with open(config_path) as f:
        config = yaml.safe_load(f)

    template = prompt_path.read_text()
    # Substitute {variable} placeholders; KeyError on unknown key is intentional
    try:
        output = template.format_map(config)
    except KeyError as e:
        sys.exit(f"Missing config key in prompt template: {e}")

    print(output)

if __name__ == "__main__":
    main()
```

### Pattern 4: YAML Requirements → Markdown RTM Table (PIPE-05)

**What:** `rtm_generator.py` reads the nested YAML requirements tree and outputs a flat Markdown table with columns: Req ID | Text | Parent Objective.

**YAML schema (from AUTOMATION_PLAN.md):**
```yaml
objectives:
  - id: OBJ-01
    text: "Detect GNSS jamming signals over European territory"
    requirements:
      - id: REQ-01
        text: "The satellite shall detect GNSS jamming with SNR > X dB"
```

**Output pattern:**
```python
# scripts/rtm_generator.py
import yaml, pathlib, sys

def main():
    req_path = pathlib.Path("requirements/requirements.yaml")
    if not req_path.exists():
        sys.exit(f"Not found: {req_path}")

    with open(req_path) as f:
        data = yaml.safe_load(f)

    rows = []
    for obj in data.get("objectives", []):
        for req in obj.get("requirements", []):
            rows.append((req["id"], req["text"], obj["id"]))

    # Markdown table
    header = "| Req ID | Requirement Text | Parent Objective |"
    sep    = "|--------|-----------------|-----------------|"
    print(header)
    print(sep)
    for rid, text, parent in rows:
        print(f"| {rid} | {text} | {parent} |")

if __name__ == "__main__":
    main()
```

### Anti-Patterns to Avoid

- **Using the course DOCX directly as `--reference-doc` without testing:** Pandoc may silently ignore styles from non-Pandoc-generated files. Always test the round-trip before writing content.
- **Globbing `content/*.md` without sort:** Shell glob order is filesystem-dependent. Use `content/0*.md` (numeric prefix) or explicitly sort to ensure section order is deterministic.
- **`yaml.load()` without Loader:** Always use `yaml.safe_load()`. Plain `yaml.load()` is deprecated and throws a warning in PyYAML 6.x.
- **Hardcoding section names in `generate_section.py`:** The `--section` argument should map directly to a filename in `prompts/`. No lookup table needed — this makes adding new sections trivial.
- **Putting generated DOCX files in git:** Add `output/` and `/tmp/full_document.md` to `.gitignore`. Only source files (`.md`, `.yaml`, `.sh`, `.py`) should be versioned.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| DOCX style application | Custom XML manipulation | Pandoc `--reference-doc` | OOXML internals are complex; Pandoc handles all heading/table/list mapping correctly |
| YAML parsing | Custom string splitter | `yaml.safe_load()` | Handles multi-line strings, anchors, quoted values; edge cases are not obvious |
| CLI argument parsing | `sys.argv` indexing | `argparse` | Help text, type coercion, error messages for free; standard Python idiom |
| Markdown table generation | Custom string padding | f-string rows with `|` separators | Markdown tables don't require aligned columns; simple f-strings are sufficient and readable |

**Key insight:** The entire Phase 1 stack is stdlib + pandoc + pyyaml. No heavy frameworks needed. This keeps the toolchain portable and the `requirements.txt` minimal.

---

## Common Pitfalls

### Pitfall 1: Pandoc Version Mismatch Between Teammates

**What goes wrong:** Teammate installs older pandoc (2.x) from a different package manager; heading style mapping differs from 3.x.
**Why it happens:** Pandoc 3.x changed some default style names.
**How to avoid:** Pin the pandoc version in README.md. For Manjaro: `sudo pacman -S pandoc` installs the current community repo version; document it. Check with `pandoc --version`.
**Warning signs:** Headings render as plain paragraphs or "Heading 1" style not found warnings in LibreOffice.

### Pitfall 2: Template Extraction Loses Styles

**What goes wrong:** Opening the course DOCX, deleting content, and saving does not preserve all styles — LibreOffice may strip unused styles.
**Why it happens:** Word processors prune styles marked as "unused" on save.
**How to avoid:** After deleting content, add one line of text using each heading level (Heading 1, Heading 2, Heading 3, Normal) before saving. Then delete that placeholder text in a second save, or leave a single placeholder heading.
**Warning signs:** `pandoc test.md -o test.docx --reference-doc=templates/course_template.docx` produces output where headings look like body text.

### Pitfall 3: `{variable}` KeyError Halts Prompt Generation

**What goes wrong:** A prompt template references `{mission_application}` but `mission_config.yaml` doesn't have that key yet (mission concept TBD).
**Why it happens:** `str.format_map()` raises `KeyError` on missing keys.
**How to avoid:** Either use `string.Template.safe_substitute()` (leaves `$var` in place if not found) or ensure all keys referenced in any prompt exist in the config (even as `"TBD"` values).
**Warning signs:** `generate_section.py` exits with KeyError.

### Pitfall 4: RTM Generator Silently Skips Malformed Requirements

**What goes wrong:** A requirement entry in YAML is missing the `id` or `text` key; `rtm_generator.py` produces a partial table with no error.
**Why it happens:** `dict.get()` returns `None` silently.
**How to avoid:** Use `req["id"]` (raises KeyError) rather than `req.get("id")`. Let the script fail loudly on malformed data — better to know early.
**Warning signs:** RTM output has blank cells or fewer rows than expected.

### Pitfall 5: Pandoc Not Installed (Confirmed Blocker)

**What goes wrong:** `build_doc.sh` fails immediately: `command not found: pandoc`.
**Why it happens:** Pandoc is not currently installed on the dev machine (verified: `which pandoc` returns nothing).
**How to avoid:** Plan 01-01 MUST include `sudo pacman -S pandoc` as step 0. This is the first executable action of the phase and cannot be deferred.
**Warning signs:** This is known; it is not a warning sign, it is a confirmed fact.

---

## Code Examples

### mission_config.yaml Schema (PIPE-03)

```yaml
# mission_config.yaml — Single source of truth for all mission parameters
mission_name: "TBD"
satellite_class: "CubeSat"
mass_kg: 8
orbit_type: "LEO"
orbit_altitude_km: 550
inclination_deg: 97.6
mission_application: "TBD"
payload_type: "TBD"
frequency_GHz: 8.0
tx_power_dBm: 30
ground_station: "Aalto"
```

### Prompt Template Format (PIPE-04)

```markdown
<!-- prompts/motivation.md -->
Given the following mission parameters:
- Mission name: {mission_name}
- Satellite class: {satellite_class}
- Target orbit: {orbit_altitude_km} km, {inclination_deg}° inclination
- Mission application: {mission_application}
- Payload: {payload_type}

Write the "Mission Motivation and Objectives" section of a satellite feasibility study.
Cover: problem statement, why a space solution is needed, mission goal (measurable),
product of the mission, success criteria (minimal/full/extended), and target orbit justification.
Output in Markdown. Use ## for subsections. All technical claims must include numbers and units.
```

### requirements.yaml Schema (PIPE-05)

```yaml
objectives:
  - id: OBJ-01
    text: "Detect GNSS jamming signals over European territory"
    requirements:
      - id: REQ-01
        text: "The satellite shall detect GNSS jamming with SNR > 10 dB"
      - id: REQ-02
        text: "The satellite shall cover European territory with revisit time < 12 hours"
  - id: OBJ-02
    text: "Transmit collected data to ground within 24 hours of acquisition"
    requirements:
      - id: REQ-03
        text: "The downlink data rate shall be ≥ 1 Mbps"
```

### Pandoc Round-Trip Verification Command

```bash
# Quick test after template extraction — run this before writing any real content
echo "# Heading 1\n## Heading 2\nNormal paragraph text.\n\n| Col A | Col B |\n|-------|-------|\n| val1 | val2 |" \
  | pandoc -f markdown -o /tmp/style_test.docx --reference-doc=templates/course_template.docx
# Open /tmp/style_test.docx in LibreOffice and verify Heading 1/2 match course template
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Use source DOCX as reference-doc directly | Generate reference-doc from pandoc, then apply styles | Pandoc 3.x (#10282) | Must use two-step template extraction |
| `yaml.load()` | `yaml.safe_load()` | PyYAML 5.1 | `yaml.load()` now raises warning; always use `safe_load()` |
| `sys.argv` for CLI | `argparse` | Python 3.2 (best practice since) | Canonical approach; all scripts should use it |

**Deprecated/outdated:**
- `yaml.load(f)` without Loader argument: triggers DeprecationWarning in PyYAML 6.x. Use `yaml.safe_load(f)`.
- Pandoc 2.x flag `--reference-docx` (old name): renamed to `--reference-doc` in Pandoc 3.x.

---

## Open Questions

1. **Template Style Fidelity**
   - What we know: Course template is a `.docx` file in `vault/`; Pandoc recommends starting from its own generated base
   - What's unclear: Whether the course template's heading fonts/sizes are standard enough to reproduce accurately in LibreOffice without a reference scan
   - Recommendation: Plan 01-01 explicitly includes a human verification step: open both files side-by-side and confirm Heading 1/2/3 fonts match before proceeding

2. **Prompt Variable Coverage**
   - What we know: AUTOMATION_PLAN.md lists 8 prompt files; `mission_config.yaml` has ~10 keys
   - What's unclear: Which prompt files need which config keys — some may reference keys not yet in the config schema
   - Recommendation: Plan 01-03 should draft all prompt files first, then audit which config keys are needed, then finalize `mission_config.yaml` schema

3. **RTM Depth**
   - What we know: AUTOMATION_PLAN.md shows 4 levels (objectives → mission reqs → observation reqs → instrument reqs)
   - What's unclear: The Idea Review only requires objectives and top-level requirements. Should the YAML schema support all 4 levels now or start flat?
   - Recommendation: Implement the full nested schema from day 1 (as in AUTOMATION_PLAN.md) but `rtm_generator.py` only needs to flatten to Req ID | Text | Parent for now. Extending later is trivial.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | None detected — Wave 0 must install pytest |
| Config file | None — see Wave 0 |
| Quick run command | `pytest tests/ -x -q` |
| Full suite command | `pytest tests/ -v` |

### Phase Requirements to Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| PIPE-01 | `build_doc.sh` produces a `.docx` file | smoke | `bash scripts/build_doc.sh && test -f output/mission_feasibility_*.docx` | Wave 0 |
| PIPE-02 | `templates/course_template.docx` exists and is non-empty | smoke | `test -f templates/course_template.docx` | Wave 0 |
| PIPE-03 | `mission_config.yaml` loads without error; changing altitude propagates | unit | `pytest tests/test_config.py::test_config_loads -x` | Wave 0 |
| PIPE-04 | `generate_section.py --section motivation` prints non-empty output with substituted values | unit | `pytest tests/test_generate_section.py::test_substitution -x` | Wave 0 |
| PIPE-05 | `rtm_generator.py` produces Markdown table with correct columns | unit | `pytest tests/test_rtm_generator.py::test_rtm_output -x` | Wave 0 |

### Sampling Rate

- **Per task commit:** `pytest tests/ -x -q`
- **Per wave merge:** `pytest tests/ -v`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_config.py` — covers PIPE-03
- [ ] `tests/test_generate_section.py` — covers PIPE-04
- [ ] `tests/test_rtm_generator.py` — covers PIPE-05
- [ ] `tests/conftest.py` — shared fixtures (tmp mission_config.yaml, tmp prompts dir)
- [ ] Framework install: `pip install pytest`

---

## Sources

### Primary (HIGH confidence)

- Pandoc MANUAL.html (https://pandoc.org/MANUAL.html) — `--reference-doc` behavior, style inheritance, TOC flags
- PyYAML documentation (https://pyyaml.org/wiki/PyYAMLDocumentation) — `safe_load()` API
- Python stdlib argparse docs (https://docs.python.org/3/library/argparse.html) — CLI pattern
- Python stdlib string.Template (https://docs.python.org/3/library/string.html) — `safe_substitute()` behavior

### Secondary (MEDIUM confidence)

- Pandoc GitHub issue #10282 (https://github.com/jgm/pandoc/issues/10282) — heading style loss in Pandoc 3.5 with non-Pandoc reference docs; confirms two-step template approach
- "Write in Markdown, Deliver as DOCX" (https://rnwest.engineer/auto-generate-docx-with-pandoc/) — practitioner pattern for reference-doc workflow
- R Markdown Cookbook §8.1 (https://bookdown.org/yihui/rmarkdown-cookbook/word-template.html) — confirms "start from pandoc-generated base, then edit styles" best practice

### Tertiary (LOW confidence)

- WebSearch results on PyYAML nested dict patterns — consistent with official docs; no novel findings

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all libraries are stdlib or single-purpose tools with stable APIs; pandoc and pyyaml are both mature
- Architecture: HIGH — directly derived from AUTOMATION_PLAN.md with one confirmed refinement (two-step template extraction)
- Pitfalls: HIGH (pandoc not installed: confirmed fact; template extraction risk: confirmed from GitHub issue); MEDIUM (runtime KeyError in substitution: logical inference from Python semantics)

**Research date:** 2026-03-21
**Valid until:** 2026-09-21 (pandoc API is stable; pyyaml API is stable; 6-month horizon reasonable)
