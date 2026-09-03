from release import DEFAULT_MANIFEST, version_string

def test_default_manifest_is_valid():
    assert DEFAULT_MANIFEST.validate() == []

def test_all_twelve_modules_are_present():
    ids = [item.module_id for item in DEFAULT_MANIFEST.modules]
    assert ids == [f"M{i:02d}" for i in range(1, 13)]

def test_version_string():
    assert "WeatherStation Pro" in version_string()
