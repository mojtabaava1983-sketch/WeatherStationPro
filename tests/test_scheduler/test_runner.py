import pytest
from scheduler.runner import SchedulerRunner
from scheduler.scheduler import Scheduler
def test_runner_validation():
    with pytest.raises(ValueError): SchedulerRunner(Scheduler(),0)
