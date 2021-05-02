from flask import Blueprint, jsonify, request

from lc.models import Task
from lc.main import db

api = Blueprint('api', __name__)

@api.route('/tasks/', methods=['GET'])
def get_all_tasks():
    print("Querying all tasks")
    tasks = Task.query.all()
    output = {'tasks': [task.to_half_json() for task in tasks]}
    return jsonify(output)

@api.route('/tasks/<int:id>', methods=['GET'])
def get_single_task(id):
    print(f"Querying single task with {id}")
    task = Task.query.get_or_404(id)
    return jsonify(task.to_full_json())

@api.route('/tasks/', methods=['POST'])
def create_new_task():
    print("Creating new task")
    print(request.form.get("schedule_time"))
    print(request.form.get("lines"))
    return jsonify({'scuesss': True})

@api.route('/tasks/<int:id>', methods=['PUT'])
def edit_task(id):
    print("Editing existing task")
    # task = task.query.get_or_404(id)
    # task.schedule_time = request.json.get('line')
    # task.line = request.json.get('line')

    # db.session.add(task)
    # db.session.commit()

    tmp = {"tmp": True}
    return jsonify(tmp)
    # return jsonify(task.to_full_json())

"""curl -X POST -d "schedule_time=2021-06-05T17:00:00&lines=victoria" http://localhost:8000/v1/tasks"""