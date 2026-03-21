"""tests/test_pre_submit_check.py — Full test suite for scripts/pre_submit_check.py.

Tests CHECK-02 (milestone-aware checklist) and COLLAB-02 (review marker item).
"""
import subprocess
import sys

SCRIPT = "scripts/pre_submit_check.py"


def test_idea_review_items():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--milestone", "idea_review"],
        capture_output=True,
        text=True,
    )
    assert "mission goal" in result.stdout.lower()
    assert "target orbit" in result.stdout.lower()
    assert "success criteria" in result.stdout.lower()
    assert "ai usage" in result.stdout.lower()
    assert "review marker" in result.stdout.lower()


def test_exits_nonzero():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--milestone", "idea_review"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1


def test_unknown_milestone():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--milestone", "unknown_milestone"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_review_marker_item_present():
    result = subprocess.run(
        [sys.executable, SCRIPT, "--milestone", "idea_review"],
        capture_output=True,
        text=True,
    )
    stdout_lower = result.stdout.lower()
    assert "review" in stdout_lower
    assert "marker" in stdout_lower
