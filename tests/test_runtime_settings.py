import pytest
from config.runtime_settings import RuntimeSettings, RuntimeSettingsError

def test_defaults_are_valid():
    RuntimeSettings().validate()

def test_to_dict_contains_runtime_controls():
    d=RuntimeSettings().to_dict()
    assert d["request_timeout_seconds"]==15.0
    assert d["retry_count"]==2

@pytest.mark.parametrize("field", [
    "request_timeout_seconds","acquisition_interval_seconds"
])
def test_positive_duration_required(field):
    with pytest.raises(RuntimeSettingsError):
        RuntimeSettings(**{field:0}).validate()

def test_negative_retry_rejected():
    with pytest.raises(RuntimeSettingsError):
        RuntimeSettings(retry_count=-1).validate()

def test_negative_backoff_rejected():
    with pytest.raises(RuntimeSettingsError):
        RuntimeSettings(retry_backoff_seconds=-1).validate()

def test_invalid_log_level_rejected():
    with pytest.raises(RuntimeSettingsError):
        RuntimeSettings(logging_level="TRACE").validate()
