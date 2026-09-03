from config.configuration import SettingDefinition
from config.configuration_integration import IntegratedConfiguration
from config.settings_storage import JsonSettingsStorage

def test_load_defaults_and_save(tmp_path):
    storage=JsonSettingsStorage(tmp_path/"settings.json")
    app=IntegratedConfiguration.load(storage)
    assert app.get("app.name")=="WeatherStationPro"
    app.set("app.environment","production")
    app.save()

    restored=IntegratedConfiguration.load(storage)
    assert restored.get("app.environment")=="production"

def test_required_setting_blocks_save(tmp_path):
    storage=JsonSettingsStorage(tmp_path/"settings.json")
    definitions=(SettingDefinition("required.api", required=True),)
    app=IntegratedConfiguration.load(storage, definitions)
    try:
        app.save()
        assert False
    except ValueError:
        pass
