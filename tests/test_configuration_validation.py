from config.configuration import SettingDefinition
from config.configuration_validation import (
    ConfigurationValidator, ConfigurationValidationError
)

def test_valid_defaults_have_no_issues():
    v=ConfigurationValidator([
        SettingDefinition("app.name","WeatherStationPro"),
        SettingDefinition("runtime.enabled",True),
    ])
    assert v.validate({})==[]

def test_required_missing_is_reported():
    v=ConfigurationValidator([
        SettingDefinition("api.key",required=True),
    ])
    issues=v.validate({})
    assert len(issues)==1
    assert issues[0].name=="api.key"

def test_empty_required_is_reported():
    v=ConfigurationValidator([
        SettingDefinition("api.key",required=True),
    ])
    assert v.validate({"api.key":""})

def test_optional_none_is_allowed():
    v=ConfigurationValidator([
        SettingDefinition("optional.value",default=None),
    ])
    assert v.validate({"optional.value":None})==[]

def test_validate_or_raise():
    v=ConfigurationValidator([SettingDefinition("x",required=True)])
    try:
        v.validate_or_raise({})
        assert False
    except ConfigurationValidationError as exc:
        assert exc.issues[0].name=="x"
