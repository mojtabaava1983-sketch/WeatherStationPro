import pytest
from forecast.models import ForecastRequest

def test_request_accepts_7_days():
    r = ForecastRequest(1, "temperature", 7, 24)
    assert r.horizon_days == 7

def test_request_rejects_more_than_10_days():
    with pytest.raises(ValueError):
        ForecastRequest(1, "temperature", 11, 24)
