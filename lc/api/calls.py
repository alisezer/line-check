
from flask import jsonify, request

from lc.models import Call
from lc.api import api
from lc.main import db

@api.route('/calls/', methods=['GET'])
def get_all_calls():
    print("Querying all calls")
    calls = Call.query.all()
    output = {'calls': [call.to_half_json() for call in calls]}
    return jsonify(output)

@api.route('/calls/<int:id>', methods=['GET'])
def get_single_call(id):
    print(f"Querying single call with {id}")
    call = Call.query.get_or_404(id)
    return jsonify(call.to_full_json())

@api.route('/calls/', methods=['POST'])
def create_new_call():
    print("Creating new call")
    print(request.form.get("schedule_time"))
    print(request.form.get("lines"))
    return jsonify({'scuesss': True})

@api.route('/calls/<int:id>', methods=['PUT'])
def edit_call(id):
    print("Editing existing call")
    # call = Call.query.get_or_404(id)
    # call.schedule_time = request.json.get('line')
    # call.line = request.json.get('line')

    # db.session.add(call)
    # db.session.commit()

    tmp = {"tmp": True}
    return jsonify(tmp)
    # return jsonify(call.to_full_json())

"""curl -X POST -d "schedule_time=2021-06-05T17:00:00&lines=victoria" http://localhost:8000/v1/tasks"""