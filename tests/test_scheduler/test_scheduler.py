from datetime import datetime, timezone, timedelta
import pytest
from scheduler.clock import FixedClock
from scheduler.models import Job, Schedule
from scheduler.scheduler import Scheduler
def test_immediate_job():
    now=datetime(2026,1,1,tzinfo=timezone.utc); clock=FixedClock(now); state=[]
    s=Scheduler(clock=clock); s.add_job(Job("weather",lambda:state.append(1),Schedule.minutes(10),run_immediately=True))
    assert s.tick()==[]; s.start(); r=s.tick()
    assert r[0].success and state==[1]
def test_interval_job():
    now=datetime(2026,1,1,tzinfo=timezone.utc); clock=FixedClock(now); state=[]
    s=Scheduler(clock=clock); s.add_job(Job("weather",lambda:state.append(1),Schedule.minutes(5))); s.start()
    assert s.tick()==[]; clock.set(now+timedelta(minutes=5)); assert len(s.tick())==1
    assert state==[1]
def test_duplicate():
    s=Scheduler(); s.add_job(Job("same",lambda:None,Schedule.seconds(1)))
    with pytest.raises(Exception): s.add_job(Job("same",lambda:None,Schedule.seconds(1)))
