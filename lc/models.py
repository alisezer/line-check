
from sqlalchemy.dialects.postgresql import JSON

from datetime import datetime
from lc.main import db


class Call(db.Model):
    __tablename__ = 'calls'
    id = db.Column(db.Integer, primary_key=True)
    line = db.Column(db.String(20))
    status = db.Column(db.String(20))
    schedule_time = db.Column(db.DateTime())
    result = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Call, self).__init__(**kwargs)

    def to_full_json(self):
        output = {
            "id": self.id,
            "line": self.line,
            "status": self.status,
            "schedule_time": self.schedule_time,
            "result": self.result,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return json_story

    def to_half_json(self):
        output = {
            "id": self.id,
            "line": self.line,
            "schedule_time": self.schedule_time,
            "status": self.status,
        }
        return output
