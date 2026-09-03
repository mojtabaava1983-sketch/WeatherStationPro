from config.configuration import (
    Configuration, ConfigurationError, SettingDefinition
)


def test_defaults_are_available():
    cfg = Configuration()
    assert cfg.get("app.name") == "WeatherStationPro"
    assert cfg.get("app.timezone") == "UTC"


def test_override_preserves_other_defaults():
    cfg = Configuration({"app.environment": "production"})
    assert cfg.get("app.environment") == "production"
    assert cfg.get("logging.level") == "INFO"


def test_set_and_update():
    cfg = Configuration()
    cfg.set("runtime.interval_seconds", 60)
    cfg.update({"logging.level": "DEBUG", "runtime.enabled": False})
    assert cfg.get("runtime.interval_seconds") == 60
    assert cfg.get("logging.level") == "DEBUG"
    assert cfg.get("runtime.enabled") is False


def test_require_rejects_missing():
    cfg = Configuration(definitions=(
        SettingDefinition("required.setting", required=True),
    ))
    try:
        cfg.require("required.setting")
        assert False
    except ConfigurationError:
        pass


def test_secret_is_masked():
    cfg = Configuration(
        {"api.key": "secret-value"},
        definitions=(SettingDefinition("api.key", secret=True),),
    )
    assert cfg.get("api.key") == "secret-value"
    assert cfg.masked_dict()["api.key"] == "***"


def test_empty_name_rejected():
    cfg = Configuration()
    try:
        cfg.set("", 1)
        assert False
    except ConfigurationError:
        pass
