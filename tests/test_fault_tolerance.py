import pytest
from config.fault_tolerance import (
    ConfigurationRecovery, ConfigurationRecoveryError
)

def test_success_does_not_use_fallback():
    calls = []
    result = ConfigurationRecovery(
        lambda: {"x": 1}, lambda: calls.append(1) or {}
    ).load()
    assert result.value == {"x": 1}
    assert result.recovered is False
    assert calls == []

def test_failed_load_uses_fallback():
    def bad():
        raise ValueError("corrupt settings")
    result = ConfigurationRecovery(
        bad, lambda: {"defaults": True}
    ).load()
    assert result.value == {"defaults": True}
    assert result.recovered is True
    assert "corrupt settings" in (result.error or "")

def test_failed_fallback_raises_controlled_error():
    def bad():
        raise OSError("load failed")
    def also_bad():
        raise RuntimeError("fallback failed")
    with pytest.raises(ConfigurationRecoveryError):
        ConfigurationRecovery(bad, also_bad).load()
