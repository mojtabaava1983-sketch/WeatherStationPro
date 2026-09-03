from datetime import date
from sunlight.solar import calculate_sun_times

def test_equatorial_day():
    sunrise, sunset, noon, polar_day, polar_night = calculate_sun_times(
        date(2026,3,20), 0, 0
    )
    assert sunrise is not None
    assert sunset is not None
    assert not polar_day
    assert not polar_night
