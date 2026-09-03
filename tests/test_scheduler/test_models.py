from datetime import timedelta
import pytest
from scheduler.models import Schedule, Job
def test_schedule_helpers():
    assert Schedule.minutes(5).interval == timedelta(minutes=5)
    assert Schedule.hours(1).interval == timedelta(hours=1)
def test_invalid_schedule():
    with pytest.raises(ValueError): Schedule(timedelta(seconds=0))
def test_invalid_job():
    with pytest.raises(ValueError): Job("", lambda:None, Schedule.seconds(1))
