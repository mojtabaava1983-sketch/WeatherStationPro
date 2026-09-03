from datetime import datetime, timezone
import pytest
from forecast.engine import ForecastEngine
from forecast.models import ForecastRequest

def test_seven_day_forecast():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    engine = ForecastEngine()
    request = ForecastRequest(1, "temperature", 7, 24)
    series = engine.forecast(request, [10, 12, 14, 16], last_observation_at=start)
    assert len(series.points) == 7
    assert series.method == "linear_trend_baseline"
    assert series.points[0].value == 18.0

def test_ten_day_forecast():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    engine = ForecastEngine()
    request = ForecastRequest(1, "temperature", 10, 24)
    series = engine.forecast(request, [10, 11, 12], last_observation_at=start)
    assert len(series.points) == 10

def test_insufficient_history():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    engine = ForecastEngine(minimum_history=3)
    request = ForecastRequest(1, "temperature", 7, 24)
    with pytest.raises(Exception):
        engine.forecast(request, [10, 11], last_observation_at=start)
