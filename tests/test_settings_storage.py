import json
import pytest
from config.settings_storage import JsonSettingsStorage, SettingsStorageError

def test_missing_file_loads_as_empty(tmp_path):
    s=JsonSettingsStorage(tmp_path/"settings.json")
    assert s.load()=={}

def test_save_and_load_round_trip(tmp_path):
    p=tmp_path/"settings.json"
    s=JsonSettingsStorage(p)
    values={"app":{"name":"WeatherStationPro"},"runtime":{"enabled":True}}
    s.save(values)
    assert s.load()==values

def test_save_creates_parent_directory(tmp_path):
    p=tmp_path/"nested"/"settings.json"
    JsonSettingsStorage(p).save({"x":1})
    assert p.exists()

def test_invalid_root_is_rejected(tmp_path):
    p=tmp_path/"settings.json"
    p.write_text(json.dumps(["bad"]),encoding="utf-8")
    with pytest.raises(SettingsStorageError):
        JsonSettingsStorage(p).load()

def test_corrupt_json_is_rejected(tmp_path):
    p=tmp_path/"settings.json"
    p.write_text("{bad",encoding="utf-8")
    with pytest.raises(SettingsStorageError):
        JsonSettingsStorage(p).load()
