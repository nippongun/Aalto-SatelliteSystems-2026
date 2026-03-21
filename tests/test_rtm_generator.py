import subprocess
import sys
import yaml
import pathlib


def test_rtm_output(tmp_path):
    """rtm_generator.py outputs a Markdown table with correct column headers."""
    req_data = {
        "objectives": [
            {
                "id": "OBJ-01",
                "text": "Detect GNSS jamming",
                "requirements": [
                    {"id": "REQ-01", "text": "The satellite shall detect jamming with SNR > 10 dB"}
                ],
            }
        ]
    }
    req_path = tmp_path / "requirements.yaml"
    with open(req_path, "w") as f:
        yaml.dump(req_data, f)

    result = subprocess.run(
        [sys.executable, "scripts/rtm_generator.py", "--requirements", str(req_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"rtm_generator.py failed: {result.stderr}"
    output = result.stdout
    assert "| Req ID |" in output, "Missing 'Req ID' column header"
    assert "REQ-01" in output, "Expected REQ-01 in output"
    assert "OBJ-01" in output, "Expected OBJ-01 (parent) in output"
