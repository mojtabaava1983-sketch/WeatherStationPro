from forecast.estimators import ForecastEstimator

def test_last_value():
    assert ForecastEstimator.last_value([1, None, 3]) == 3

def test_moving_average():
    assert ForecastEstimator.moving_average([1, 2, 3, 4], 2) == 3.5

def test_trend_forecast_rises():
    result = ForecastEstimator.trend_forecast([10, 12, 14], 2)
    assert result == [16.0, 18.0]
