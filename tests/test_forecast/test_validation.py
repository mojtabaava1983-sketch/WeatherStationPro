from datetime import datetime, timezone
from forecast.engine import ForecastEngine
from forecast.models import ForecastRequest
from forecast.validation import validate_series

def test_forecast_series_validates():
    start = datetime(2026,1,1,tzinfo=timezone.utc)
    series = ForecastEngine().forecast(
        ForecastRequest(1, "temperature", 7, 24),
        [10, 12, 14],
        last_observation_at=start,
    )
    assert validate_series(series) == []
