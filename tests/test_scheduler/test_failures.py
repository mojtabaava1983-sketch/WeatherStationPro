from datetime import datetime, timezone
from scheduler.clock import FixedClock
from scheduler.models import Job, Schedule
from scheduler.scheduler import Scheduler
def test_failure_does_not_stop_scheduler():
    clock=FixedClock(datetime(2026,1,1,tzinfo=timezone.utc)); s=Scheduler(clock=clock)
    def broken(): raise RuntimeError("boom")
    s.add_job(Job("broken",broken,Schedule.seconds(1),run_immediately=True)); s.start()
    r=s.tick()[0]
    assert not r.success and r.error=="boom" and s.running
