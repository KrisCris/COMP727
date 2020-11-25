from database.db import db
from util.utils import get_current_time

class Emotions(db.Model):
    __tablename__ = 'emotions'

    id = db.Column(db.INTEGER, primary_key=True, unique=True, nullable=False, autoincrement=True)
    emotion = db.Column(db.VARCHAR(255))
    time = db.Column(db.INTEGER)

    def __init__(self, emotion):
        self.emotion = emotion
        self.time = get_current_time()


    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_last_timestamp():
        return Emotions.query.order_by(Emotions.id.desc()).first().time