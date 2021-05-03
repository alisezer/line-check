"""Data Models Tests"""

from lc.models import Task

def test_create_task():
    lines = "victoria,bakerloo"
    status = "scheduled"
    schedule_time = "2021-06-05T17:00:00"
    test_task = Task(lines=lines, status=status, schedule_time=schedule_time)
    assert test_task.lines == lines
    assert test_task.status == status
    assert test_task.schedule_time == schedule_time

def test_task_to_full_json():
    lines = "victoria,bakerloo"
    status = "scheduled"
    schedule_time = "2021-06-05T17:00:00"
    test_task = Task(lines=lines, status=status, schedule_time=schedule_time)
    test_json = test_task.to_full_json()

    assert test_json["lines"] == lines
    assert test_json["status"] == status
    assert test_json["schedule_time"] == schedule_time
    assert test_json["result"] is None
    assert test_json["id"] is None
    assert test_json["created_at"] is None
    assert test_json["updated_at"] is None

def test_task_to_half_json():
    lines = "victoria,bakerloo"
    status = "scheduled"
    schedule_time = "2021-06-05T17:00:00"
    test_task = Task(lines=lines, status=status, schedule_time=schedule_time)
    test_json = test_task.to_full_json()

    assert test_json["lines"] == lines
    assert test_json["status"] == status
    assert test_json["schedule_time"] == schedule_time
    assert test_json["result"] is None