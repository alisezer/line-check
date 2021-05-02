
from sqlalchemy.dialects.postgresql import JSON

from datetime import datetime
from lc.main import db


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    lines = db.Column(db.String(20))
    status = db.Column(db.String(20))
    schedule_time = db.Column(db.DateTime())
    result = db.Column(JSON, nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now)

    def __init__(self, **kwargs):
        super(Task, self).__init__(**kwargs)

    def to_full_json(self):
        output = {
            "id": self.id,
            "lines": self.lines,
            "status": self.status,
            "schedule_time": self.schedule_time,
            "result": self.result,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return output

    def to_half_json(self):
        output = {
            "id": self.id,
            "lines": self.lines,
            "schedule_time": self.schedule_time,
            "status": self.status,
        }
        return output
