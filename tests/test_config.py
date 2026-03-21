import yaml
import pathlib


def test_config_loads(tmp_config):
    """mission_config.yaml loads without error and returns a dict."""
    with open(tmp_config) as f:
        config = yaml.safe_load(f)
    assert isinstance(config, dict)
    assert "orbit_altitude_km" in config


def test_config_value_present(tmp_config):
    """orbit_altitude_km value matches what was written."""
    with open(tmp_config) as f:
        config = yaml.safe_load(f)
    assert config["orbit_altitude_km"] == 550
