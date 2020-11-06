from database.db import db
from util.utils import get_current_time

class Working(db.Model):
    __tablename__ = 'working'

    id = db.Column(db.INTEGER, primary_key=True, unique=True, nullable=False, autoincrement=True)
    begin_time = db.Column(db.INTEGER)
    end_time = db.Column(db.INTEGER)

    def __init__(self, begin):
        self.begin_time = begin


    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()