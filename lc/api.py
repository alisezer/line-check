from datetime import datetime
import logging

from flask import Blueprint, jsonify, request

from lc.utils import check_line_name_validity
from lc.models import Task
from lc.main import db
from lc.constants import SCHEDULED_TASK_STATUS

logger = logging.getLogger(__name__)
api = Blueprint('api', __name__)

@api.route('/tasks/', methods=['GET'])
def get_all_tasks():
    logger.info("Querying all tasks")
    tasks = Task.query.all()
    output = {'tasks': [task.to_half_json() for task in tasks]}
    return jsonify(output)

@api.route('/tasks/<int:id>', methods=['GET'])
def get_single_task(id):
    logger.info(f"Querying single task with {id}")
    task = Task.query.get(id)
    if task:
        output = task.to_full_json()
    else:
        output = {"failure": f"Task with ID {id} cannot be found"}
    return jsonify(output)

@api.route('/tasks/', methods=['POST'])
def create_new_task():
    logger.info("Creating new task")
    lines = request.form.get("lines")
    line_validity = check_line_name_validity(lines)

    if line_validity:
        schedule_time = request.form.get("schedule_time", datetime.now())
        task = Task(
            lines=lines,
            schedule_time=schedule_time,
            status=SCHEDULED_TASK_STATUS
        )
        db.session.add(task)
        db.session.commit()
        output = {
            "success": "Task has been created",
            "task": task.to_full_json()
        }
    else:
        output = {"failure": "Incorrect line name"}

    return jsonify(output)

@api.route('/tasks/<int:id>', methods=['PUT'])
def edit_task(id):
    logger.info(f"Editing existing task with ID {id}")
    output = {}

    task = Task.query.get(id)
    if task:
        lines = request.form.get("lines")
        if lines:
            line_validity = check_line_name_validity(lines)
            if line_validity:
                task.lines = lines
            else:
                output["failure"] = "Line name couldn't be updated because of incorrect naming"

        schedule_time = request.form.get("schedule_time")
        if schedule_time:
            task.schedule_time = schedule_time

        if lines or schedule_time:
            task.updated_at = datetime.now()
            db.session.add(task)
            db.session.commit()
        output["task"] = task.to_full_json()
    else:
        output = {"failure": f"Task with ID {id} cannot be found"}
    return jsonify(output)
