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

    @staticmethod
    def stop_working():
        end_time = get_current_time()
        last_work = Working.isWorking()
        if last_work is not None:
            last_work.end_time = end_time
            Working.add(last_work)
            print('end working')
            return last_work
        else:
            return None

    @staticmethod
    def begin_working():
        last_work = Working.isWorking()
        if last_work is None:
            begin_time = get_current_time()
            work = Working(begin=begin_time)
            Working.add(work)
            print('begin working')
            return work
        else:
            return None

    @staticmethod
    def isWorking():
        last_work = Working.query.order_by(Working.id.desc()).first()
        if last_work is not None:
            if last_work.end_time is None:
                return last_work
            else:
                return None
        else:
            return None