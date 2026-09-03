from datetime import datetime, timedelta, timezone
import pytest
from data_analysis.engine import DataAnalysisEngine
from data_analysis.models import Observation

def obs(t, temp, quality=100):
    return Observation(t, {"temperature": temp}, quality=quality)

def test_summary_and_trend():
    start = datetime(2026,1,1,tzinfo=timezone.utc)
    data = [obs(start, 10), obs(start+timedelta(hours=1), 12), obs(start+timedelta(hours=2), 14)]
    result = DataAnalysisEngine().summarize(data, ["temperature"])
    assert result.results[0].mean == 12
    assert result.trends[0].direction == "rising"
    assert result.trends[0].change == 4

def test_quality_filter():
    start = datetime(2026,1,1,tzinfo=timezone.utc)
    data = [obs(start, 10, 50), obs(start+timedelta(minutes=1), 20, 90)]
    result = DataAnalysisEngine(minimum_quality=80).summarize(data, ["temperature"])
    assert result.results[0].count == 1

def test_invalid_quality():
    with pytest.raises(Exception):
        DataAnalysisEngine(minimum_quality=101)

def test_rolling_mean():
    start = datetime(2026,1,1,tzinfo=timezone.utc)
    data = [obs(start+timedelta(minutes=i), float(i)) for i in range(4)]
    result = DataAnalysisEngine.rolling_mean(data, "temperature", 2)
    assert [round(v,1) for _,v in result] == [0.5,1.5,2.5]
