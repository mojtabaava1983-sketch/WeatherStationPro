import pytest
from config.provider_settings import ProviderSettings, ProviderSettingsError

def valid():
    return ProviderSettings("OpenWeather","https://api.example.test",
                             api_key_env="WEATHER_API_KEY")

def test_valid_provider_settings():
    p=valid()
    p.validate()
    assert p.enabled is True

def test_api_key_is_referenced_by_environment_name():
    p=valid()
    assert p.api_key_env=="WEATHER_API_KEY"

def test_empty_name_rejected():
    with pytest.raises(ProviderSettingsError):
        ProviderSettings("", "https://api.example.test").validate()

def test_empty_url_rejected():
    with pytest.raises(ProviderSettingsError):
        ProviderSettings("X", "").validate()

def test_invalid_timeout_rejected():
    with pytest.raises(ProviderSettingsError):
        ProviderSettings("X","https://api.example.test",timeout_seconds=0).validate()

def test_negative_retry_rejected():
    with pytest.raises(ProviderSettingsError):
        ProviderSettings("X","https://api.example.test",retry_count=-1).validate()

def test_invalid_rate_limit_rejected():
    with pytest.raises(ProviderSettingsError):
        ProviderSettings("X","https://api.example.test",rate_limit_per_minute=0).validate()
