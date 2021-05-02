'''API Endpoints'''

# from flask import Blueprint
from flask import jsonify, request

from lc.models import Call

# api = Blueprint('api', __name__)

# @api.route('/calls/', methods=['GET'])
def get_all_calls():
    calls = Call.query.all()
    return jsonify({
        'calls_here': [call.to_half_json() for call in calls]
    })

# @api.route('/calls/<int:id>')
def get_sigle_call(id):
    call = Call.query.get_or_404(id)
    return jsonify(call.to_full_json())

# @api.route('/calls/', methods=['POST'])
def create_new_call():
    schedule_time = request.json.get('schedule_time')
    line = request.json.get('line')
    print(schedule_time, line)

    return jsonify({'scuesss': True})

# @api.route('/calls/<int:id>', methods=['PUT'])
def edit_call(id):
    call = Call.query.get_or_404(id)
    call.schedule_time = request.json.get('line')
    call.line = request.json.get('line')

    db.session.add(call)
    db.session.commit()

    return jsonify(call.to_full_json())