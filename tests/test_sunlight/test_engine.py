from datetime import date
import pytest
from sunlight.engine import SunlightEngine

def test_coordinates_validation():
    engine = SunlightEngine()
    with pytest.raises(Exception):
        engine.calculate(date(2026,1,1), 91, 0)

def test_known_location_returns_events():
    result = SunlightEngine().calculate(date(2026,6,21), 40.7128, -74.0060)
    assert result.sunrise_utc is not None
    assert result.sunset_utc is not None
    assert result.sunrise_utc < result.sunset_utc

def test_range():
    result = SunlightEngine().calculate_range(date(2026,1,1), 3, 35.7, 51.4)
    assert len(result) == 3
