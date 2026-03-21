# Phase 2: Quality Gates - Research

**Researched:** 2026-03-21
**Domain:** Python CLI scripting — text parsing, regex, YAML/CSV data, exit-code conventions, pytest subprocess testing
**Confidence:** HIGH

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| CHECK-01 | Consistency checker: Python script scanning all `content/*.md` for contradictions (altitude mismatches, budget overruns, orphaned requirements, missing units) | Seven specific checks defined in AUTOMATION_PLAN.md A2; regex patterns and CSV/YAML parsing patterns documented below |
| CHECK-02 | Pre-submit checklist: milestone-aware checklist script (`--milestone idea_review` etc.) with non-zero exit on unresolved items | Milestone-to-checklist mapping defined in AUTOMATION_PLAN.md A3; exit-code pattern and argparse patterns documented below; COLLAB-02 (review markers) is a sub-requirement |
</phase_requirements>

---

## Summary

Phase 2 delivers two standalone Python CLI scripts that act as quality gates before every document build. Both scripts are pure Python (no external services, no API calls) and follow the same conventions as the Phase 1 scripts: `argparse` for CLI, `pathlib.Path` for all paths, `yaml.safe_load` for YAML, `sys.exit(1)` for failure.

`check_consistency.py` scans Markdown content files plus the budget CSVs and `mission_config.yaml` to detect seven categories of contradiction. It writes a `consistency_report.md` file (PASS/FAIL per check with line references) and exits non-zero if any check fails. `pre_submit_check.py` is a milestone-aware checklist that reads a hard-coded checklist per milestone from within the script, prints only the relevant items, and exits non-zero if any item is unresolved.

Both scripts must integrate cleanly into the existing test infrastructure (pytest, `subprocess.run`, `tmp_path`). The seven consistency checks span three data sources: Markdown text files (regex extraction), CSV budget files (numeric comparison against `mission_config.yaml`), and `requirements.yaml` (structural coverage analysis).

**Primary recommendation:** Implement both scripts as self-contained Python CLI tools following the build_doc.py/rtm_generator.py style exactly. No new dependencies are required — stdlib `re`, `csv`, `pathlib`, `argparse`, `sys`, plus the already-installed `pyyaml` cover everything.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| `re` (stdlib) | 3.10+ | Regex extraction of altitude, units, headings from Markdown | No dependency, sufficient for all text pattern matching needed |
| `csv` (stdlib) | 3.10+ | Parsing `mass_budget.csv` and `power_budget.csv` | No dependency, handles the simple CSV schema in use |
| `pathlib` | 3.10+ | All file path operations | Project convention (build_doc.py model) |
| `argparse` | 3.10+ | CLI argument parsing (`--content-dir`, `--config`, `--milestone`) | Project convention |
| `sys` | 3.10+ | `sys.exit(1)` for non-zero exit on failure | Project convention |
| `pyyaml` | already installed | Load `mission_config.yaml` and `requirements/requirements.yaml` | Already in project; used by all Phase 1 scripts |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `dataclasses` (stdlib) | 3.10+ | Typed result objects for check outcomes | Use for `CheckResult(name, status, detail, line_ref)` to keep report generation clean |
| `textwrap` (stdlib) | 3.10+ | Format report output neatly | Use in report writer only |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| stdlib `csv` | `pandas` | pandas already in project but is overkill for simple CSV row iteration; stdlib csv avoids an unnecessary import |
| regex on raw Markdown | A Markdown AST parser (e.g. `mistletoe`) | AST parsing is more robust but adds a new dependency and is unnecessary for the simple keyword/number extraction needed |

**Installation:** No new packages required. All dependencies are stdlib or already installed (`pyyaml`).

---

## Architecture Patterns

### Recommended Project Structure

```
scripts/
├── check_consistency.py    # CHECK-01: seven-check consistency scanner
├── pre_submit_check.py     # CHECK-02: milestone-aware checklist
tests/
├── conftest.py             # existing shared fixtures (tmp_config, tmp_prompts_dir)
├── test_check_consistency.py   # new — subprocess + tmp_path tests
└── test_pre_submit_check.py    # new — subprocess + tmp_path tests
```

No new directories needed. `consistency_report.md` is written to the working directory (or an explicit `--output` path).

### Pattern 1: Check-Result Object + Report Writer

**What:** Each of the seven consistency checks returns a small result object. A separate function collects all results and writes `consistency_report.md`. The main function calls each check in sequence, collects results, writes the report, and exits non-zero if any check failed.

**When to use:** Any time a script runs multiple named checks and needs a structured report.

**Example:**

```python
# Source: project convention derived from rtm_generator.py style

import dataclasses

@dataclasses.dataclass
class CheckResult:
    name: str           # human-readable check name
    status: str         # "PASS" or "FAIL"
    detail: str         # explanation or "OK"
    line_refs: list     # list of (file, line_number) pairs where issue was found

def run_all_checks(content_dir, config, req_data) -> list:
    results = []
    results.append(check_altitude_consistent(content_dir, config))
    results.append(check_mass_budget(config))
    results.append(check_power_budget(config))
    results.append(check_requirement_units(req_data))
    results.append(check_objective_coverage(req_data))
    results.append(check_success_criteria(content_dir))
    results.append(check_ai_usage_section(content_dir))
    return results

def write_report(results: list, output_path) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# Consistency Report\n\n")
        for r in results:
            icon = "PASS" if r.status == "PASS" else "FAIL"
            f.write(f"## {icon}: {r.name}\n\n{r.detail}\n\n")
            for file, line in r.line_refs:
                f.write(f"- `{file}` line {line}\n")
            f.write("\n")

def main():
    # ... argparse ...
    results = run_all_checks(content_dir, config, req_data)
    write_report(results, "consistency_report.md")
    if any(r.status == "FAIL" for r in results):
        sys.exit(1)
```

### Pattern 2: Regex Extraction from Markdown for Number Checks

**What:** Read all `content/*.md` files, use `re.findall` to extract all altitude numbers, compare unique values. Same pattern for success-criteria keyword check and AI usage heading check.

**When to use:** Any check that scans free-form Markdown text for a specific pattern.

**Example:**

```python
# Source: AUTOMATION_PLAN.md A2 specification

import re

ALTITUDE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*km", re.IGNORECASE)

def check_altitude_consistent(content_dir, config) -> CheckResult:
    """Flag if more than one unique altitude value appears across all .md files."""
    all_altitudes = {}  # value -> [(file, line_no)]
    for md_file in sorted(content_dir.glob("*.md")):
        for line_no, line in enumerate(md_file.read_text(encoding="utf-8").splitlines(), 1):
            for match in ALTITUDE_PATTERN.finditer(line):
                val = float(match.group(1))
                all_altitudes.setdefault(val, []).append((md_file.name, line_no))

    config_alt = float(config.get("orbit_altitude_km", 0))
    unique = set(all_altitudes.keys())
    if len(unique) <= 1:
        return CheckResult("Altitude consistent", "PASS", "OK", [])
    else:
        detail = f"Multiple altitude values found: {sorted(unique)} km (config: {config_alt} km)"
        refs = [ref for refs in all_altitudes.values() for ref in refs]
        return CheckResult("Altitude consistent", "FAIL", detail, refs)
```

**CRITICAL DESIGN NOTE:** The altitude regex `r"(\d+(?:\.\d+)?)\s*km"` will match any number followed by "km". This is intentionally broad. The planner must decide whether to limit scope to specific context (e.g., only lines containing "altitude" or "orbit") to reduce false positives from unrelated km values (e.g., ground station distances). A narrower regex like `r"orbit.*?(\d+(?:\.\d+)?)\s*km|altitude.*?(\d+(?:\.\d+)?)\s*km"` is safer.

### Pattern 3: CSV vs Config Numeric Comparison

**What:** Load the budget CSV using stdlib `csv.DictReader`, sum the target column, compare against the corresponding value in `mission_config.yaml`. Flag if over budget.

**When to use:** Mass budget check (total mass vs `mass_kg`) and power budget check (peak power vs derived EPS capacity).

**Example:**

```python
# Source: AUTOMATION_PLAN.md A2 + budget CSV schema in AUTOMATION_PLAN.md B2

import csv

def check_mass_budget(config) -> CheckResult:
    """Flag if total mass in mass_budget.csv exceeds system dry mass in mission_config.yaml."""
    budget_path = pathlib.Path("budgets/mass_budget.csv")
    if not budget_path.exists():
        return CheckResult("Mass budget", "PASS", "budgets/mass_budget.csv not found — skipped", [])

    system_mass = float(config.get("mass_kg", 0))
    total = 0.0
    rows_with_issues = []

    with open(budget_path, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row_no, row in enumerate(reader, 2):  # 2: header is row 1
            try:
                total += float(row["mass_kg"])
            except (ValueError, KeyError):
                rows_with_issues.append(("mass_budget.csv", row_no))  # TBD or malformed

    if total > system_mass:
        detail = f"Total mass {total:.3f} kg exceeds system dry mass {system_mass} kg"
        return CheckResult("Mass budget", "FAIL", detail, [("budgets/mass_budget.csv", 0)])
    return CheckResult("Mass budget", "PASS", f"Total {total:.3f} kg ≤ {system_mass} kg OK", [])
```

**IMPORTANT:** The CSV currently has `TBD` values for some subsystems (e.g., Payload). The check must skip non-numeric rows gracefully — not crash. Skip `TBD` rows and note that the check is partial.

### Pattern 4: Milestone-Aware Checklist with Inline Dict

**What:** `pre_submit_check.py` contains a hard-coded dict mapping milestone names to lists of checklist items. Each item is a string. The script accepts `--milestone`, looks up the checklist, prints it, then checks resolution markers or always exits non-zero (forcing manual review).

**When to use:** CHECK-02 / `pre_submit_check.py`.

**Example:**

```python
# Source: AUTOMATION_PLAN.md A3 specification

CHECKLISTS = {
    "idea_review": [
        "Mission goal is measurable (has numbers and units)",
        "Target orbit altitude, inclination specified",
        "At least 3 objectives defined",
        "RTM has >=1 row per objective",
        "Success criteria present (minimal/full/extended)",
        "AI usage section present",
        "Document version and date in header",
        "All section files have review markers (<!-- reviewed: ... --> or <!-- ai-draft: ... -->)",
    ],
    "concept_review": [
        "Sections 1-5 drafted and student-reviewed",
        "Mass budget present with margins",
        "Power budget present with margins",
        "Link budget computed and inserted",
        "Payload trade-off matrix present",
        "RTM complete (all objectives covered)",
        "AI usage section present",
    ],
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--milestone", required=True, choices=list(CHECKLISTS.keys()),
                        help="Milestone target: idea_review | concept_review")
    args = parser.parse_args()

    checklist = CHECKLISTS[args.milestone]
    print(f"Pre-submit checklist for: {args.milestone}\n")
    for item in checklist:
        print(f"  [ ] {item}")
    print("\nAll items must be confirmed before submission.")
    print("This script always exits non-zero — resolve all items then re-run build.")
    sys.exit(1)  # Always fail until a --auto-check mode exists
```

**Design decision for planner:** The v1 implementation always exits non-zero (no automated resolution checking beyond what check_consistency.py already does). This satisfies the success criterion "exits non-zero when any item is unresolved" because unresolved is the default state. A future enhancement could add `--auto-check` to auto-verify some items (e.g., AI usage section presence). The planner should plan for the simple v1 first.

### Pattern 5: YAML Coverage Check (Objectives → Requirements)

**What:** Load `requirements.yaml`, confirm every objective has at least one requirement. Optionally cross-check that every `REQ-XX` ID mentioned in `requirements.yaml` appears somewhere in the content Markdown.

**When to use:** CHECK-01 check 5 (objective-to-requirement coverage).

**Example:**

```python
def check_objective_coverage(req_data) -> CheckResult:
    """Every objective must have at least one requirement."""
    orphaned = []
    for obj in req_data.get("objectives", []):
        if not obj.get("requirements"):
            orphaned.append(obj["id"])
    if orphaned:
        detail = f"Objectives with no requirements: {orphaned}"
        return CheckResult("Objective coverage", "FAIL", detail, [])
    return CheckResult("Objective coverage", "PASS", "All objectives have >=1 requirement", [])
```

### Pattern 6: Section Heading / Keyword Presence Check

**What:** Read assembled Markdown files, check for presence of required keywords or headings using `str.lower()` + `in` check.

**When to use:** Check 6 (success criteria keywords) and Check 7 (AI usage section).

**Example:**

```python
def check_success_criteria(content_dir) -> CheckResult:
    """Section 1 must contain 'minimal success' and 'full success' keywords."""
    section1 = content_dir / "01_motivation.md"
    if not section1.exists():
        return CheckResult("Success criteria", "FAIL", "01_motivation.md not found", [])
    text = section1.read_text(encoding="utf-8").lower()
    missing = []
    for keyword in ["minimal success", "full success"]:
        if keyword not in text:
            missing.append(keyword)
    if missing:
        return CheckResult("Success criteria", "FAIL",
                           f"Missing keywords: {missing}", [("01_motivation.md", 0)])
    return CheckResult("Success criteria", "PASS", "Keywords present", [])

def check_ai_usage_section(content_dir) -> CheckResult:
    """Any content file must contain a heading matching 'AI usage' (case-insensitive)."""
    AI_HEADING = re.compile(r"^#+\s+AI\s+usage", re.IGNORECASE | re.MULTILINE)
    for md_file in content_dir.glob("*.md"):
        if AI_HEADING.search(md_file.read_text(encoding="utf-8")):
            return CheckResult("AI usage section", "PASS", f"Found in {md_file.name}", [])
    return CheckResult("AI usage section", "FAIL", "No AI usage heading found in any content file", [])
```

### Pattern 7: Requirement Units Check

**What:** Iterate over all requirements in `requirements.yaml`, check that the text contains at least one number+unit pair using regex. Flag requirements with no measurable value.

**When to use:** CHECK-01 check 4 (requirement units).

**Example:**

```python
UNIT_PATTERN = re.compile(r"\d+(?:\.\d+)?\s*(?:km|m|dB|W|kg|bps|MHz|GHz|°|deg|%|ms|s\b)")

def check_requirement_units(req_data) -> CheckResult:
    """Every requirement text must contain at least one number+unit pair."""
    missing = []
    for obj in req_data.get("objectives", []):
        for req in obj.get("requirements", []):
            if not UNIT_PATTERN.search(req["text"]):
                missing.append(req["id"])
    if missing:
        detail = f"Requirements missing measurable units: {missing}"
        return CheckResult("Requirement units", "FAIL", detail, [("requirements/requirements.yaml", 0)])
    return CheckResult("Requirement units", "PASS", "All requirements have number+unit", [])
```

### Anti-Patterns to Avoid

- **Crashing on TBD values:** Both budget CSVs have `TBD` placeholder values. Any numeric comparison must catch `ValueError` on `float()` conversion and skip gracefully.
- **Hardcoding paths inside check functions:** All paths must flow from CLI args → main → check functions as parameters. The test suite injects `tmp_path` equivalents.
- **Writing report to the same directory as content:** The report output path should default to the current working directory, not inside `content/`. Use `--output` arg or a sensible default.
- **Exiting immediately on first failure:** Collect all results before writing the report, then exit. Never call `sys.exit(1)` inside a check function.
- **Missing power budget config key:** `mission_config.yaml` currently has no `eps_power_W` key. The power budget check must handle a missing key gracefully (skip or emit a WARNING, not crash).

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| YAML loading | Custom YAML parser | `yaml.safe_load` | Already used throughout project; handles nested structures |
| CSV parsing | `str.split(",")` on each line | `csv.DictReader` | Handles quoted fields, missing columns, and empty rows correctly |
| Argparse | `sys.argv` manual parsing | `argparse` | Project convention; `--help` is free |
| Number regex | String scanning char-by-char | `re.compile` + `findall`/`finditer` | Handles floats, ranges, whitespace variants |

**Key insight:** All data sources (YAML, CSV, Markdown text) are already established and small. No performance optimization is needed — correctness and clear error messages matter more than speed.

---

## Common Pitfalls

### Pitfall 1: Power Budget Config Key Missing

**What goes wrong:** `check_power_budget()` calls `config.get("eps_power_W")` but this key does not exist in `mission_config.yaml`. The check crashes or silently passes.

**Why it happens:** The power budget check was designed against a future config schema that hasn't been finalized.

**How to avoid:** Check for the key's existence before doing the comparison. If missing, emit a WARNING result (not FAIL, not PASS) that says "eps_power_W not defined in mission_config.yaml — add it before this check is meaningful".

**Warning signs:** `config.get("eps_power_W")` returns `None`, `float(None)` raises `TypeError`.

### Pitfall 2: TBD Values in Budget CSVs Cause Crashes

**What goes wrong:** `float(row["mass_kg"])` raises `ValueError` for rows where `mass_kg = "TBD"` (e.g., Payload row).

**Why it happens:** The budget CSV template uses "TBD" for components not yet specified.

**How to avoid:** Wrap `float()` calls in try/except. Skip TBD rows and note in the report that the check is partial.

**Warning signs:** `ValueError: could not convert string to float: 'TBD'`

### Pitfall 3: Altitude Regex Matches Irrelevant km Values

**What goes wrong:** The `\d+\s*km` pattern matches "300 km baseline" or "50 km ground station range" — values unrelated to orbital altitude — causing false FAIL.

**Why it happens:** The pattern is too broad for free-form Markdown.

**How to avoid:** Scope the regex to lines that mention orbit-related context words: `orbit`, `altitude`, `LEO`, `apogee`, `perigee`. Alternatively, only extract the first numeric km value in the document (a pragmatic heuristic).

**Warning signs:** FAIL on altitude check when all orbit-specific values agree.

### Pitfall 4: Budget CSV File Not Yet Created

**What goes wrong:** `check_mass_budget()` tries to open `budgets/mass_budget.csv` which does not exist yet (budgets/ directory is empty in Phase 1).

**Why it happens:** Phase 3 creates the budget files. Phase 2 runs before Phase 3.

**How to avoid:** Check file existence first. If file doesn't exist, return PASS with a note "file not found — skipped" rather than FAIL. The consistency checker should be non-blocking for optional files.

**Warning signs:** `FileNotFoundError` on `open(budget_path)`.

### Pitfall 5: Subprocess Tests Must Run from Repo Root

**What goes wrong:** Tests call `subprocess.run([sys.executable, "scripts/check_consistency.py", ...])` but the CWD is wrong, so the script can't find default paths.

**Why it happens:** `tmp_path` fixtures change the effective test directory.

**How to avoid:** Always pass explicit `--config` and `--content-dir` args in tests (no relying on defaults). This is what the Phase 1 tests do — follow the same pattern exactly.

**Warning signs:** `FileNotFoundError: requirements/requirements.yaml` in test output.

### Pitfall 6: Report Always Written Even When All Checks Pass

**What goes wrong:** Script exits 0 but doesn't write the report, so the caller can't tell what was checked.

**Why it happens:** Logic bug — report writing inside the `if any(FAIL)` branch.

**How to avoid:** Always write `consistency_report.md`. Exit code indicates pass/fail; the report is always produced.

---

## Code Examples

### CLI Skeleton (consistent with project style)

```python
#!/usr/bin/env python3
"""scripts/check_consistency.py — Scan content files for internal contradictions.

Usage:
    python scripts/check_consistency.py
    python scripts/check_consistency.py content/
    python scripts/check_consistency.py --content-dir content/ --config mission_config.yaml
"""
import argparse
import pathlib
import sys
import yaml

def main() -> None:
    repo_root = pathlib.Path(__file__).parent.parent
    parser = argparse.ArgumentParser(description="Check content consistency")
    parser.add_argument("content_dir", nargs="?",
                        default=str(repo_root / "content"),
                        help="Directory containing *.md content files")
    parser.add_argument("--config", default=str(repo_root / "mission_config.yaml"),
                        help="Path to mission_config.yaml")
    parser.add_argument("--requirements", default=str(repo_root / "requirements" / "requirements.yaml"),
                        help="Path to requirements.yaml")
    parser.add_argument("--output", default="consistency_report.md",
                        help="Output report file path")
    args = parser.parse_args()

    content_dir = pathlib.Path(args.content_dir)
    config_path = pathlib.Path(args.config)
    req_path = pathlib.Path(args.requirements)

    if not config_path.exists():
        print(f"ERROR: Config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    req_data = {}
    if req_path.exists():
        with open(req_path, encoding="utf-8") as f:
            req_data = yaml.safe_load(f) or {}

    results = run_all_checks(content_dir, config, req_data)
    write_report(results, pathlib.Path(args.output))

    any_fail = any(r.status == "FAIL" for r in results)
    print(f"Report: {args.output}")
    print(f"Result: {'FAIL' if any_fail else 'PASS'}")
    sys.exit(1 if any_fail else 0)
```

### Test Pattern (consistent with Phase 1 test style)

```python
# tests/test_check_consistency.py
import subprocess, sys, pathlib, yaml

def write_config(tmp_path, overrides=None):
    config = {"mission_name": "Test", "mass_kg": 8, "orbit_altitude_km": 550, ...}
    if overrides:
        config.update(overrides)
    p = tmp_path / "mission_config.yaml"
    p.write_text(yaml.dump(config))
    return p

def test_altitude_mismatch_fails(tmp_path):
    """Altitude mismatch across two content files causes FAIL."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01_motivation.md").write_text(
        "The orbit altitude is 550 km above Earth.")
    (content_dir / "02_requirements.md").write_text(
        "Operations at altitude 400 km are required.")
    config = write_config(tmp_path)
    result = subprocess.run(
        [sys.executable, "scripts/check_consistency.py", str(content_dir),
         "--config", str(config), "--output", str(tmp_path / "report.md")],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    report = (tmp_path / "report.md").read_text()
    assert "FAIL" in report

def test_mass_over_budget_fails(tmp_path):
    """Mass CSV total exceeding mission_config mass_kg causes FAIL."""
    # ... create a mass_budget.csv where total > mass_kg, assert FAIL
```

### pre_submit_check.py CLI skeleton

```python
#!/usr/bin/env python3
"""scripts/pre_submit_check.py — Milestone-aware pre-submission checklist.

Usage:
    python scripts/pre_submit_check.py --milestone idea_review
    python scripts/pre_submit_check.py --milestone concept_review
"""
import argparse, sys

CHECKLISTS = {
    "idea_review": [...],
    "concept_review": [...],
}

def main():
    parser = argparse.ArgumentParser(description="Pre-submission checklist")
    parser.add_argument("--milestone", required=True, choices=list(CHECKLISTS.keys()))
    args = parser.parse_args()

    items = CHECKLISTS[args.milestone]
    print(f"\nPre-submit checklist: {args.milestone}\n")
    for item in items:
        print(f"  [ ] {item}")
    print(f"\n{len(items)} items to confirm before submission.")
    sys.exit(1)

if __name__ == "__main__":
    main()
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual DOCX review for consistency | Automated regex scanning of Markdown source | Phase 2 | Catches mismatches before pandoc build |
| Ad-hoc mental checklist per milestone | Script-enforced milestone checklist with non-zero exit | Phase 2 | Blocks doc build until human confirms all items |

**Deprecated/outdated:** None — this is new tooling with no legacy to replace.

---

## Open Questions

1. **Power budget config key name**
   - What we know: `mission_config.yaml` has `mass_kg` but no EPS power capacity key
   - What's unclear: Should it be `eps_power_W`, `power_generation_W`, or something else?
   - Recommendation: Planner should add `eps_power_W` to `mission_config.yaml` in Wave 0 of Plan 02-01, and document the key name in a comment. The check_consistency.py power check references this key.

2. **Altitude regex scope**
   - What we know: The broad `\d+\s*km` pattern will match non-orbital km references
   - What's unclear: Whether current and near-future content files will have enough non-altitude km references to cause false positives
   - Recommendation: Use a context-scoped regex (lines containing "orbit", "altitude", "LEO") in v1; broaden only if needed.

3. **pre_submit_check.py resolution detection**
   - What we know: Success criterion says "exits non-zero when any item is unresolved" — v1 always exits non-zero
   - What's unclear: Whether auto-checking some items (e.g., AI usage section presence by calling check_consistency.py) is in scope for this phase
   - Recommendation: V1 always exits non-zero. Auto-checking is a Phase 5 concern (ORCH-01 chains all tools). Keep pre_submit_check.py simple for Phase 2.

4. **review marker format**
   - What we know: AGENT.md specifies `<!-- reviewed: YYYY-MM-DD -->` and `<!-- ai-draft: YYYY-MM-DD, awaiting student review -->` as review marker formats. COLLAB-02 is a sub-requirement of CHECK-02.
   - What's unclear: Whether the pre-submit checklist should auto-detect these markers or just remind the user to check
   - Recommendation: V1 prints a checklist item "All sections have review markers (reviewed: or ai-draft:)" as a manual check item. Auto-detection can be added if time permits.

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (already installed, used in Phase 1) |
| Config file | none — pytest auto-discovers `tests/test_*.py` |
| Quick run command | `python -m pytest tests/test_check_consistency.py tests/test_pre_submit_check.py -x -q` |
| Full suite command | `python -m pytest tests/ -x -q` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| CHECK-01 | Altitude mismatch across two .md files → FAIL | subprocess | `pytest tests/test_check_consistency.py::test_altitude_mismatch_fails -x` | Wave 0 |
| CHECK-01 | Matching altitudes → PASS | subprocess | `pytest tests/test_check_consistency.py::test_altitude_consistent_passes -x` | Wave 0 |
| CHECK-01 | Mass CSV total > config mass_kg → FAIL | subprocess | `pytest tests/test_check_consistency.py::test_mass_over_budget_fails -x` | Wave 0 |
| CHECK-01 | Missing units in requirement → FAIL | subprocess | `pytest tests/test_check_consistency.py::test_requirement_units_fail -x` | Wave 0 |
| CHECK-01 | TBD values in CSV skipped gracefully (no crash) | subprocess | `pytest tests/test_check_consistency.py::test_tbd_csv_values_skipped -x` | Wave 0 |
| CHECK-01 | Missing budget CSV → PASS (skipped, not crash) | subprocess | `pytest tests/test_check_consistency.py::test_missing_budget_skipped -x` | Wave 0 |
| CHECK-01 | Report always written (even on PASS) | subprocess | `pytest tests/test_check_consistency.py::test_report_always_written -x` | Wave 0 |
| CHECK-02 | `--milestone idea_review` prints only idea_review items | subprocess | `pytest tests/test_pre_submit_check.py::test_idea_review_items -x` | Wave 0 |
| CHECK-02 | `--milestone idea_review` exits non-zero | subprocess | `pytest tests/test_pre_submit_check.py::test_exits_nonzero -x` | Wave 0 |
| CHECK-02 | Unknown `--milestone` value → error, non-zero exit | subprocess | `pytest tests/test_pre_submit_check.py::test_unknown_milestone -x` | Wave 0 |
| COLLAB-02 | Review marker check item appears in idea_review checklist | subprocess | `pytest tests/test_pre_submit_check.py::test_review_marker_item_present -x` | Wave 0 |

### Sampling Rate

- **Per task commit:** `python -m pytest tests/test_check_consistency.py tests/test_pre_submit_check.py -x -q`
- **Per wave merge:** `python -m pytest tests/ -x -q`
- **Phase gate:** Full suite green before `/gsd:verify-work`

### Wave 0 Gaps

- [ ] `tests/test_check_consistency.py` — covers CHECK-01 (all 7 checks)
- [ ] `tests/test_pre_submit_check.py` — covers CHECK-02
- [ ] `budgets/mass_budget.csv` — needed for CHECK-01 mass budget test fixture; create a minimal stub in Wave 0 or generate in-test with `tmp_path`

*(Existing `tests/conftest.py` with `tmp_config` fixture is reusable — no new shared fixtures needed)*

---

## Sources

### Primary (HIGH confidence)

- `AUTOMATION_PLAN.md` sections A2 (consistency checker), A3 (pre-submit checklist) — full specification of all 7 checks, regex patterns, CSV schema, milestone checklist items
- `scripts/build_doc.py` — authoritative model for CLI structure, argparse, pathlib, sys.exit conventions
- `scripts/rtm_generator.py` — authoritative model for YAML loading, fail-loud KeyError pattern
- `scripts/generate_section.py` — authoritative model for error messages, argparse defaults, format_map
- `tests/conftest.py`, `tests/test_rtm_generator.py`, `tests/test_build_doc.py` — authoritative test patterns for subprocess + tmp_path style
- `mission_config.yaml` — exact config key names for altitude (`orbit_altitude_km`), mass (`mass_kg`)
- `requirements/requirements.yaml` — exact YAML schema for objectives/requirements
- `AGENT.md` — hard constraints (cross-platform pathlib, no API calls, no hardcoded params), review marker format, pre-commit protocol

### Secondary (MEDIUM confidence)

- Python stdlib `re`, `csv`, `dataclasses`, `argparse` documentation — patterns are well-established

### Tertiary (LOW confidence)

- None — all findings are grounded in project source files and stdlib documentation.

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — all dependencies already in project; stdlib only
- Architecture: HIGH — patterns derived directly from existing Phase 1 scripts in repo
- Pitfalls: HIGH — derived from actual config schema inspection (missing `eps_power_W`) and actual CSV schema inspection (TBD values)
- Test map: HIGH — follows exact same subprocess + tmp_path pattern as Phase 1 tests

**Research date:** 2026-03-21
**Valid until:** 2026-05-21 (stable stdlib patterns; checklist items may need updating if course SoW changes)
