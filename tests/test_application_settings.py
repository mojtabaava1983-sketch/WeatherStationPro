import pytest
from config.application_settings import ApplicationSettings, ApplicationSettingsError

def test_defaults_are_valid():
    s=ApplicationSettings()
    s.validate()
    assert s.application_name=="WeatherStationPro"

def test_to_dict_and_from_dict_round_trip():
    s=ApplicationSettings(environment="production", logging_level="WARNING", data_retention_days=90)
    restored=ApplicationSettings.from_dict(s.to_dict())
    assert restored==s

@pytest.mark.parametrize("level",["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
def test_valid_log_levels(level):
    ApplicationSettings(logging_level=level).validate()

def test_invalid_log_level():
    with pytest.raises(ApplicationSettingsError):
        ApplicationSettings(logging_level="TRACE").validate()

def test_negative_retention_rejected():
    with pytest.raises(ApplicationSettingsError):
        ApplicationSettings(data_retention_days=-1).validate()

def test_empty_timezone_rejected():
    with pytest.raises(ApplicationSettingsError):
        ApplicationSettings(timezone="").validate()
