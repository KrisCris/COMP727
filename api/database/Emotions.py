from database.db import db
from util.utils import get_current_time
import time

from database.Working import Working

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

    @staticmethod
    def get_depress_rate():
        last_work = Working.isWorking()
        if last_work is None:
            return None
        else:
            begin_time = last_work.begin_time
            entire = Emotions.query.filter(Emotions.time>begin_time).count()
            depress = Emotions.query \
                    .filter(Emotions.time>begin_time) \
                    .filter((Emotions.emotion == 'sad') | (Emotions.emotion == 'fear') | (Emotions.emotion == 'angry')).count()
            print(str(entire)+'\t'+str(depress))            
            return depress/entire if entire != 0 else 0

    @staticmethod
    def get_periodic_emotion():
        current = get_current_time()
        begin = [current-3600, current-3600*3,current-3600*6,current-3600*12]
        # map = {
        #     "angry": 1.00001,
        #     "fear": 2.00001,
        #     "sad": 3.00001,
        #     "neutral": 4.00001,
        #     "surprise": 5.00001,
        #     "happy": 6.00001
        # }
        map = {
            "angry": 1,
            "fear": 2,
            "sad": 3,
            "neutral": 4,
            "surprise": 5,
            "happy": 6
        }
        data = [{},{},{},{}]
        index = 0
        for t in begin:
            res = Emotions.query.order_by(Emotions.time.asc()).filter(Emotions.time>t).all()
            if res is not None:
                for r in res:
                    h = time.localtime(r.time).tm_hour
                    m = time.localtime(r.time).tm_min
                    h = str(int(h)) if h>=10 else '0'+str(int(h))
                    m = str(int(m)) if m>=10 else '0'+str(int(m))
                    tm = h+":"+m
                    data[index][tm] = map[r.emotion]
            index += 1
        return data
            