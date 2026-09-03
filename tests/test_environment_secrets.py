import pytest
from config.environment_secrets import EnvironmentReader, SecretConfigurationError

def test_reads_environment_value():
    env={"WEATHER_API_KEY":"abc123"}
    r=EnvironmentReader(env)
    assert r.get("WEATHER_API_KEY")=="abc123"

def test_missing_optional_value_returns_none():
    assert EnvironmentReader({}).get("OPTIONAL") is None

def test_required_value_missing_raises():
    with pytest.raises(SecretConfigurationError):
        EnvironmentReader({}).require("WEATHER_API_KEY")

def test_required_value_empty_raises():
    with pytest.raises(SecretConfigurationError):
        EnvironmentReader({"WEATHER_API_KEY":""}).require("WEATHER_API_KEY")

def test_secret_value_is_masked_for_diagnostics():
    r=EnvironmentReader({"WEATHER_API_KEY":"abc123"})
    assert r.masked_get("WEATHER_API_KEY")=="***"
    assert r.get("WEATHER_API_KEY")=="abc123"
