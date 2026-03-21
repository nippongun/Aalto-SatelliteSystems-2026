---
phase: 2
slug: quality-gates
status: draft
nyquist_compliant: false
wave_0_complete: false
created: 2026-03-21
---

# Phase 2 — Validation Strategy

> Per-phase validation contract for feedback sampling during execution.

---

## Test Infrastructure

| Property | Value |
|----------|-------|
| **Framework** | pytest (already installed, used in Phase 1) |
| **Config file** | none — pytest auto-discovers `tests/test_*.py` |
| **Quick run command** | `python -m pytest tests/test_check_consistency.py tests/test_pre_submit_check.py -x -q` |
| **Full suite command** | `python -m pytest tests/ -x -q` |
| **Estimated runtime** | ~5 seconds |

---

## Sampling Rate

- **After every task commit:** Run `python -m pytest tests/test_check_consistency.py tests/test_pre_submit_check.py -x -q`
- **After every plan wave:** Run `python -m pytest tests/ -x -q`
- **Before `/gsd:verify-work`:** Full suite must be green
- **Max feedback latency:** ~5 seconds

---

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|-----------|-------------------|-------------|--------|
| 2-01-01 | 02-01 | 0 | CHECK-01 | unit | `pytest tests/test_check_consistency.py -x -q` | ❌ W0 | ⬜ pending |
| 2-01-02 | 02-01 | 0 | CHECK-02 | unit | `pytest tests/test_pre_submit_check.py -x -q` | ❌ W0 | ⬜ pending |
| 2-01-03 | 02-01 | 1 | CHECK-01 | subprocess | `pytest tests/test_check_consistency.py::test_altitude_mismatch_fails -x` | ❌ W0 | ⬜ pending |
| 2-01-04 | 02-01 | 1 | CHECK-01 | subprocess | `pytest tests/test_check_consistency.py::test_altitude_consistent_passes -x` | ❌ W0 | ⬜ pending |
| 2-01-05 | 02-01 | 1 | CHECK-01 | subprocess | `pytest tests/test_check_consistency.py::test_mass_over_budget_fails -x` | ❌ W0 | ⬜ pending |
| 2-01-06 | 02-01 | 1 | CHECK-01 | subprocess | `pytest tests/test_check_consistency.py::test_requirement_units_fail -x` | ❌ W0 | ⬜ pending |
| 2-01-07 | 02-01 | 1 | CHECK-01 | subprocess | `pytest tests/test_check_consistency.py::test_tbd_csv_values_skipped -x` | ❌ W0 | ⬜ pending |
| 2-01-08 | 02-01 | 1 | CHECK-01 | subprocess | `pytest tests/test_check_consistency.py::test_missing_budget_skipped -x` | ❌ W0 | ⬜ pending |
| 2-01-09 | 02-01 | 1 | CHECK-01 | subprocess | `pytest tests/test_check_consistency.py::test_report_always_written -x` | ❌ W0 | ⬜ pending |
| 2-02-01 | 02-02 | 1 | CHECK-02 | subprocess | `pytest tests/test_pre_submit_check.py::test_idea_review_items -x` | ❌ W0 | ⬜ pending |
| 2-02-02 | 02-02 | 1 | CHECK-02 | subprocess | `pytest tests/test_pre_submit_check.py::test_exits_nonzero -x` | ❌ W0 | ⬜ pending |
| 2-02-03 | 02-02 | 1 | CHECK-02 | subprocess | `pytest tests/test_pre_submit_check.py::test_unknown_milestone -x` | ❌ W0 | ⬜ pending |
| 2-02-04 | 02-02 | 1 | COLLAB-02 | subprocess | `pytest tests/test_pre_submit_check.py::test_review_marker_item_present -x` | ❌ W0 | ⬜ pending |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

---

## Wave 0 Requirements

- [ ] `tests/test_check_consistency.py` — stubs for all 7 CHECK-01 checks
- [ ] `tests/test_pre_submit_check.py` — stubs for CHECK-02 + COLLAB-02 items

*Existing `tests/conftest.py` with `tmp_config` fixture is reusable — no new shared fixtures needed.*
*`budgets/mass_budget.csv` will be created in-test with `tmp_path` (no stub needed at repo level).*

---

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| Section review markers (`<!-- ai-draft -->` / `<!-- reviewed -->`) visible in content | COLLAB-02 | Convention only — no enforcement in v1 | Open any `content/*.md`, confirm markers are present where expected |

---

## Validation Sign-Off

- [ ] All tasks have `<automated>` verify or Wave 0 dependencies
- [ ] Sampling continuity: no 3 consecutive tasks without automated verify
- [ ] Wave 0 covers all MISSING references
- [ ] No watch-mode flags
- [ ] Feedback latency < 5s
- [ ] `nyquist_compliant: true` set in frontmatter

**Approval:** pending
