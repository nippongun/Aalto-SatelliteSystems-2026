"""tests/test_check_consistency.py — Subprocess tests for scripts/check_consistency.py.

All seven CHECK-01 behaviors are tested here. Tests run check_consistency.py
as a subprocess, passing all paths explicitly via CLI args.
"""
import csv
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_config(tmp_path: Path, overrides: dict | None = None) -> Path:
    """Write a minimal mission_config.yaml into tmp_path and return its Path."""
    config = {
        "mission_name": "TestMission",
        "satellite_class": "CubeSat",
        "mass_kg": 8,
        "orbit_type": "LEO",
        "orbit_altitude_km": 550,
        "inclination_deg": 97.6,
        "mission_application": "TBD",
        "payload_type": "TBD",
        "frequency_GHz": 8.0,
        "tx_power_dBm": 30,
        "eps_power_W": 30,
        "ground_station": "Aalto",
        "authors": "Test Author",
        "google_doc_url": "https://example.com",
    }
    if overrides:
        config.update(overrides)
    config_path = tmp_path / "mission_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    return config_path


def write_requirements(tmp_path: Path, objectives: list) -> Path:
    """Write a minimal requirements.yaml into tmp_path and return its Path."""
    data = {"objectives": objectives}
    req_path = tmp_path / "requirements.yaml"
    with open(req_path, "w") as f:
        yaml.dump(data, f)
    return req_path


def run_checker(tmp_path: Path, content_dir: Path, config_path: Path,
                req_path: Path | None = None, output_path: Path | None = None) -> subprocess.CompletedProcess:
    """Run check_consistency.py as a subprocess with explicit paths."""
    script = Path(__file__).parent.parent / "scripts" / "check_consistency.py"
    if output_path is None:
        output_path = tmp_path / "consistency_report.md"
    cmd = [
        sys.executable, str(script),
        str(content_dir),
        "--config", str(config_path),
        "--output", str(output_path),
    ]
    if req_path is not None:
        cmd += ["--requirements", str(req_path)]
    return subprocess.run(cmd, capture_output=True, text=True)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_altitude_mismatch_fails(tmp_path):
    """Two content files with different altitude values → non-zero exit, FAIL in report."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01.md").write_text("The orbit altitude is 550 km above the Earth.")
    (content_dir / "02.md").write_text("Operations at altitude 400 km ensure coverage.")

    config_path = write_config(tmp_path)
    report_path = tmp_path / "report.md"
    result = run_checker(tmp_path, content_dir, config_path, output_path=report_path)

    assert result.returncode != 0, (
        f"Expected non-zero exit for altitude mismatch.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert report_path.exists(), "Report file must always be written."
    report_text = report_path.read_text()
    assert "FAIL" in report_text, f"Expected 'FAIL' in report.\nReport:\n{report_text}"


def test_altitude_consistent_passes(tmp_path):
    """Two content files with same altitude value → exit 0, PASS in report."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01.md").write_text("The orbit altitude is 550 km.\nMinimal success: basic comms. Full success: all ops.")
    (content_dir / "02.md").write_text("Operations at altitude 550 km ensure full coverage.\n## AI usage\nUsed AI for drafting.")

    config_path = write_config(tmp_path)

    # Write requirements with units so requirement_units check passes
    objectives = [
        {
            "id": "OBJ-01",
            "text": "Test objective",
            "requirements": [
                {"id": "REQ-01", "text": "The satellite shall transmit at 1 Mbps data rate."},
            ],
        }
    ]
    req_path = write_requirements(tmp_path, objectives)
    report_path = tmp_path / "report.md"
    result = run_checker(tmp_path, content_dir, config_path, req_path=req_path, output_path=report_path)

    assert result.returncode == 0, (
        f"Expected exit 0 for consistent altitude.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert report_path.exists(), "Report file must always be written."
    report_text = report_path.read_text()
    assert "PASS" in report_text, f"Expected 'PASS' in report.\nReport:\n{report_text}"


def test_mass_over_budget_fails(tmp_path):
    """mass_budget.csv total > mass_kg in config → non-zero exit, FAIL in report."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01.md").write_text("Orbit altitude 550 km mission.\nMinimal success: ops. Full success: all.\n## AI usage\nUsed AI.")

    config_path = write_config(tmp_path, {"mass_kg": 8})

    budgets_dir = tmp_path / "budgets"
    budgets_dir.mkdir()
    budget_path = budgets_dir / "mass_budget.csv"
    with open(budget_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["subsystem", "mass_kg"])
        writer.writeheader()
        writer.writerow({"subsystem": "OBC", "mass_kg": "5"})
        writer.writerow({"subsystem": "EPS", "mass_kg": "5"})  # total=10, limit=8

    report_path = tmp_path / "report.md"
    cmd = [
        sys.executable,
        str(Path(__file__).parent.parent / "scripts" / "check_consistency.py"),
        str(content_dir),
        "--config", str(config_path),
        "--budget", str(budget_path),
        "--output", str(report_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode != 0, (
        f"Expected non-zero exit for mass overrun.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert report_path.exists(), "Report file must always be written."
    report_text = report_path.read_text()
    assert "FAIL" in report_text, f"Expected 'FAIL' in report.\nReport:\n{report_text}"


def test_requirement_units_fail(tmp_path):
    """Requirement text with no number+unit → non-zero exit, FAIL in report."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01.md").write_text("Orbit altitude 550 km.\nMinimal success: ops. Full success: all.\n## AI usage\nUsed AI.")

    config_path = write_config(tmp_path)

    # Requirement with no number+unit pattern
    objectives = [
        {
            "id": "OBJ-01",
            "text": "Test objective",
            "requirements": [
                {"id": "REQ-01", "text": "The satellite shall detect signals and transmit data."},
            ],
        }
    ]
    req_path = write_requirements(tmp_path, objectives)
    report_path = tmp_path / "report.md"
    result = run_checker(tmp_path, content_dir, config_path, req_path=req_path, output_path=report_path)

    assert result.returncode != 0, (
        f"Expected non-zero exit for missing units.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert report_path.exists(), "Report file must always be written."
    report_text = report_path.read_text()
    assert "FAIL" in report_text, f"Expected 'FAIL' in report.\nReport:\n{report_text}"


def test_tbd_csv_values_skipped(tmp_path):
    """mass_budget.csv with TBD mass_kg rows → no crash, report written."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01.md").write_text("Orbit altitude 550 km.\nMinimal success: ops. Full success: all.\n## AI usage\nUsed AI.")

    config_path = write_config(tmp_path, {"mass_kg": 8})

    budgets_dir = tmp_path / "budgets"
    budgets_dir.mkdir()
    budget_path = budgets_dir / "mass_budget.csv"
    with open(budget_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["subsystem", "mass_kg"])
        writer.writeheader()
        writer.writerow({"subsystem": "OBC", "mass_kg": "1"})    # numeric: 1 kg
        writer.writerow({"subsystem": "EPS", "mass_kg": "TBD"})  # TBD: should be skipped

    report_path = tmp_path / "report.md"
    cmd = [
        sys.executable,
        str(Path(__file__).parent.parent / "scripts" / "check_consistency.py"),
        str(content_dir),
        "--config", str(config_path),
        "--budget", str(budget_path),
        "--output", str(report_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    # Must not crash (no Python traceback)
    assert "Traceback" not in result.stderr, (
        f"Script crashed with traceback:\n{result.stderr}"
    )
    assert report_path.exists(), "Report file must always be written even with TBD rows."


def test_missing_budget_skipped(tmp_path):
    """No mass_budget.csv in tmp_path → exit 0, report written with skip note."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01.md").write_text("Orbit altitude 550 km.\nMinimal success: ops. Full success: all.\n## AI usage\nUsed AI.")

    config_path = write_config(tmp_path)

    # Write valid requirements
    objectives = [
        {
            "id": "OBJ-01",
            "text": "Test objective",
            "requirements": [
                {"id": "REQ-01", "text": "The satellite shall transmit at 1 Mbps data rate."},
            ],
        }
    ]
    req_path = write_requirements(tmp_path, objectives)
    report_path = tmp_path / "report.md"

    # Do NOT create mass_budget.csv — budget_path arg points to nonexistent file
    nonexistent_budget = tmp_path / "budgets" / "mass_budget.csv"
    cmd = [
        sys.executable,
        str(Path(__file__).parent.parent / "scripts" / "check_consistency.py"),
        str(content_dir),
        "--config", str(config_path),
        "--requirements", str(req_path),
        "--budget", str(nonexistent_budget),
        "--output", str(report_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    assert result.returncode == 0, (
        f"Expected exit 0 when budget missing.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
    assert report_path.exists(), "Report must be written even when budget is missing."


def test_report_always_written(tmp_path):
    """All checks pass → report file exists at --output path."""
    content_dir = tmp_path / "content"
    content_dir.mkdir()
    (content_dir / "01.md").write_text(
        "The orbit altitude is 550 km.\n"
        "Minimal success: basic comms operational.\n"
        "Full success: all mission objectives achieved.\n"
        "## AI usage\nUsed AI for drafting this section.\n"
    )

    config_path = write_config(tmp_path)

    objectives = [
        {
            "id": "OBJ-01",
            "text": "Test objective",
            "requirements": [
                {"id": "REQ-01", "text": "The satellite shall transmit at 1 Mbps data rate."},
            ],
        }
    ]
    req_path = write_requirements(tmp_path, objectives)
    report_path = tmp_path / "report.md"
    result = run_checker(tmp_path, content_dir, config_path, req_path=req_path, output_path=report_path)

    assert report_path.exists(), (
        f"Report file must always be written.\nstdout: {result.stdout}\nstderr: {result.stderr}"
    )
