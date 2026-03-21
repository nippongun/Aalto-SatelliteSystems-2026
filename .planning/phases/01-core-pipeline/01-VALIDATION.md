---
phase: 1
slug: core-pipeline
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-21
---

# Phase 1 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest 7.x (Wave 0 installs) |
| **Config file** | `pytest.ini` or `pyproject.toml` — Wave 0 creates |
| **Quick run command** | `pytest tests/ -x -q` |
| **Full suite command** | `pytest tests/ -v` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `pytest tests/ -x -q`
- **After every plan wave:** Run `pytest tests/ -v`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** 5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 1-01-01 | 01 | 0 | PIPE-02 | smoke | `test -f templates/course_template.docx` | ❌ W0 | ⬜ pending |
| 1-01-02 | 02 | 1 | PIPE-01 | smoke | `bash scripts/build_doc.sh && test -f output/mission_feasibility_*.docx` | ❌ W0 | ⬜ pending |
| 1-01-03 | 03 | 1 | PIPE-03, PIPE-04 | unit | `pytest tests/test_config.py tests/test_generate_section.py -x -q` | ❌ W0 | ⬜ pending |
| 1-01-04 | 04 | 1 | PIPE-05 | unit | `pytest tests/test_rtm_generator.py -x -q` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/conftest.py` — shared fixtures (tmp `mission_config.yaml`, tmp `prompts/` dir)
- [ ] `tests/test_config.py` — covers PIPE-03 (config loads, value propagates)
- [ ] `tests/test_generate_section.py` — covers PIPE-04 (substitution produces non-empty output)
- [ ] `tests/test_rtm_generator.py` — covers PIPE-05 (RTM table has correct columns)
- [ ] `pip install pytest` — framework not yet installed

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Heading styles in output `.docx` match course template visually | PIPE-01, PIPE-02 | Visual inspection required; no automated DOCX style comparison tool in stack | Open `output/mission_feasibility_*.docx` and course template side-by-side in LibreOffice; verify Heading 1, Heading 2, Normal paragraph fonts/sizes match |
| Pandoc installed and correct version | PIPE-01 | System dependency, not testable in pytest | Run `pandoc --version`; confirm 3.x |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
