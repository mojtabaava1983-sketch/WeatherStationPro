from weather_api.models import NormalizedObservation
def test_optional_fields():
    o=NormalizedObservation(pressure=1013.25)
    assert o.temperature is None and o.humidity is None
    assert o.to_dict()["Pressure"] == 1013.25
