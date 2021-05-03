"""Schedule Logic"""

from datetime import datetime
import logging

from lc.data_retrieval import retrieve_line_data
from lc.models import Task
from lc.main import db
from lc.constants import SCHEDULED_TASK_STATUS, SUCCEEDED_TASK_STATUS, FAILED_TASK_STATUS

logger = logging.getLogger(__name__)

def check_schedule_for_tasks():
    logger.info("Checking for ready tasks")
    ready_tasks = Task.query.filter(
        Task.status == SCHEDULED_TASK_STATUS
        ).filter(
            Task.schedule_time < datetime.now()
            ).all()
    return ready_tasks


def update_task_with_results(task):
    logger.info(f"Running task with ID {task.id}")
    try:
        lines = task.lines
        result = retrieve_line_data(lines)
        task.result = result
        task.status = SUCCEEDED_TASK_STATUS
    except Exception as e:
        task.status = FAILED_TASK_STATUS
        task.result = {"failure": e}
    finally:
        task.updated_at = datetime.now()
        db.session.add(task)
        db.session.commit()
    return task


def run_scheduler():
    logger.info("Running scheduler")
    ready_tasks = check_schedule_for_tasks()
    if ready_tasks:
        logger.info(f"{len(ready_tasks)} are ready to be run")
        for task in ready_tasks:
            update_task_with_results(task)
    return
