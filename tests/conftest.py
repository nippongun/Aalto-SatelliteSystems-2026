import pytest
import yaml
import pathlib


@pytest.fixture
def tmp_config(tmp_path):
    """Write a minimal mission_config.yaml and return its Path."""
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
        "ground_station": "Aalto",
        "authors": "Test Author",
        "google_doc_url": "https://example.com",
    }
    config_path = tmp_path / "mission_config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    return config_path


@pytest.fixture
def tmp_prompts_dir(tmp_path):
    """Create a minimal prompts/ directory with a motivation.md template."""
    prompts_dir = tmp_path / "prompts"
    prompts_dir.mkdir()
    motivation = prompts_dir / "motivation.md"
    motivation.write_text(
        "Mission: {mission_name}\nOrbit: {orbit_altitude_km} km\nWrite the motivation section."
    )
    return prompts_dir
