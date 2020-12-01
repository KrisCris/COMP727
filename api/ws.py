from flask import Flask
from database.db import db
from flask_sockets import Sockets
import time

from util.constants import WSP
from util.constants import DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_PORT, DATABASE
from util.utils import get_current_time, get_zero_clock
app = Flask(__name__)
sockets = Sockets(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_PORT, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@sockets.route('/mobile')
def echo_socket(ws):
    while not ws.closed:
        print('\n\n\n\n')
        db.session.commit()
        from database.Surroundings import Surroundings
        s = Surroundings.get_latest_indoor()
        tmp = s[0]
        hmd = s[1]

        from database.Working import Working
        worklist = Working.getTodayWorkRecords()
        worktime = 0
        working_data = {}
        if worklist is not None:
            for work in worklist:
                single_time = 0
                if work.end_time is None:
                    single_time = get_current_time()-work.begin_time
                else:
                    single_time = work.end_time - work.begin_time
                worktime += single_time
                print('s:'+str(single_time//60))
                relative_time = work.begin_time-get_zero_clock()
                beginH = relative_time // 3600
                beginM = (relative_time % 3600)//60
                beginH = str(int(beginH)) if beginH>=10 else '0'+str(int(beginH))
                beginM = str(int(beginM)) if beginM>=10 else '0'+str(int(beginM))
                t = beginH+':'+beginM
                single_time = single_time//60
                if single_time <= 1:
                    continue
                working_data[t] = single_time
            worktime = worktime/3600
        from database.Emotions import Emotions
        edata = Emotions.get_periodic_emotion()

        data = {'tmp':tmp, 'hmd':hmd, 'worktime':worktime, 'edata':edata, 'wdata':working_data}
        ws.send(str(data))  #发送数据
        # print(data)
        time.sleep(10)




if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', WSP), app, handler_class=WebSocketHandler)
    print('server start')
    server.serve_forever()
