"""Schedule Module Tests"""

from unittest.mock import MagicMock

from lc.constants import SCHEDULED_TASK_STATUS, SUCCEEDED_TASK_STATUS
from lc.models import Task
from lc import schedule
from lc.schedule import (
    check_schedule_for_tasks,
    update_task_with_results,
    run_scheduler
)


def test_check_schedule_for_tasks(test_client, test_db):
    # Setting this to last year to avoid freezing time
    ready_schedule_time = "2020-05-03T13:20:00"
    ready_lines = "central"

    # In 10 years this test will break
    not_ready_schedule_time = "2032-05-03T13:20:00"
    not_ready_lines = "victoria"

    test_task_ready = Task(
        lines=ready_lines,
        schedule_time=ready_schedule_time,
        status=SCHEDULED_TASK_STATUS
    )
    test_task_not_ready = Task(
        lines=not_ready_lines,
        schedule_time=not_ready_schedule_time,
        status=SCHEDULED_TASK_STATUS
    )
    test_db.session.add(test_task_ready)
    test_db.session.add(test_task_not_ready)
    test_db.session.commit()

    ready_tasks = check_schedule_for_tasks()

    assert len(ready_tasks) == 1
    assert ready_tasks[0].lines == ready_lines


def test_update_task_with_results(test_client, test_db):

    line = "central"
    fake_output = {"result": "big problems"}
    test_task = Task(lines=line, status=SCHEDULED_TASK_STATUS)

    def mock_line_request(*args, **kwargs):
        return fake_output

    schedule.retrieve_line_data = MagicMock(side_effect=mock_line_request)
    test_task = update_task_with_results(test_task)

    assert test_task.result == fake_output

def test_run_schduler(test_client, test_db):
    # Setting this to last year to avoid freezing time
    ready_schedule_time = "2020-05-03T13:20:00"
    ready_lines = "central"

    # In 10 years this test will break
    not_ready_schedule_time = "2032-05-03T13:20:00"
    not_ready_lines = "victoria"

    test_task_ready = Task(
        lines=ready_lines,
        schedule_time=ready_schedule_time,
        status=SCHEDULED_TASK_STATUS
    )
    test_task_not_ready = Task(
        lines=not_ready_lines,
        schedule_time=not_ready_schedule_time,
        status=SCHEDULED_TASK_STATUS
    )
    test_db.session.add(test_task_ready)
    test_db.session.add(test_task_not_ready)
    test_db.session.commit()

    fake_output = {"result": "big problems"}
    def mock_line_request(*args, **kwargs):
        return fake_output

    schedule.retrieve_line_data = MagicMock(side_effect=mock_line_request)

    run_scheduler()

    success = Task.query.filter(Task.status == SUCCEEDED_TASK_STATUS).all()
    assert len(success) == 1
    assert success[0].lines == ready_lines
    assert success[0].result == fake_output