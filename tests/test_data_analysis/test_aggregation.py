from datetime import datetime, timezone
from data_analysis.aggregation import ObservationAggregator
from data_analysis.models import Observation

def test_hourly_aggregation():
    t=datetime(2026,1,1,12,30,tzinfo=timezone.utc)
    data=[Observation(t, {"temperature": 10}), Observation(t, {"temperature": 14})]
    result=ObservationAggregator.by_hour(data,"temperature")
    key=list(result)[0]
    assert result[key]["mean"] == 12
    assert result[key]["count"] == 2
