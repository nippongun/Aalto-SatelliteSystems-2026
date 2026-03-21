import subprocess
import sys
import pathlib


def test_substitution(tmp_config, tmp_prompts_dir):
    """generate_section.py substitutes {mission_name} and {orbit_altitude_km} from config."""
    result = subprocess.run(
        [
            sys.executable,
            "scripts/generate_section.py",
            "--section", "motivation",
            "--config", str(tmp_config),
            "--prompts-dir", str(tmp_prompts_dir),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"generate_section.py failed: {result.stderr}"
    output = result.stdout
    assert len(output.strip()) > 0, "Output is empty"
    assert "{mission_name}" not in output, "Variable {mission_name} was not substituted"
    assert "TestMission" in output, "Expected substituted value 'TestMission' in output"
