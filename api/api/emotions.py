import requests
import base64
import json
import time
from flask import Blueprint, request
from util.utils import reply_json, captureFace, get_time_gap, get_current_time, get_weighted_value
from database.Working import Working
from database.Emotions import Emotions
from util.SC import SC

emotions = Blueprint('emotions', __name__)

class FaceRecog:
    def __init__(self):
        # client_id is AK， client_secret is SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&' + SC[
            'baidu_face']
        response = requests.get(host)
        if (response):
            res = response.json()
            self.access_token = res['access_token']
        else:
            print("error")

    def recog(self, path):
        with open(path, "rb") as f:  # to binary
            base64_data = base64.b64encode(f.read())  # base64 encode
            request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
            request_body = {
                "image": base64_data.decode(),
                "image_type": "BASE64",
                "face_field": "expression,emotion",
                "face_type": "LIVE"
            }
            jsonData = json.dumps(request_body)
            request_url = request_url + "?access_token=" + self.access_token
            headers = {'content-type': 'application/json'}
            response = requests.post(request_url,
                                     data=jsonData,
                                     headers=headers)
            return response


@emotions.route('/getEmotion', methods=['GET'])
def getEmotion():
    # init working stat determination
    last_face_time = Emotions.get_last_timestamp()
    current_time = get_current_time()
    face_check_gap = current_time - last_face_time
    working_stat = Working.isWorking()

    # a expression map that help convert what in database to what in iot platform
    map = {
        "angry": 1,
        "fear": 2,
        "sad": 3,
        "neutral": 4,
        "surprise": 5,
        "happy": 6
    }

    # guess the most possible user emotion
    prob = [0, 0, 0, 0, 0, 0]

    res = [None, None, None]
    count = 0
    for i in range(5):
        if count >= 3:
            break
        captureFace()
        faceRe = FaceRecog()
        if not res:
            continue
        res[count] = faceRe.recog("picture/image.jpg").json()
        count += 1

    if count == 0:
        return reply_json(0)

    # detect multiple frames of user photo, once detect a face, hasFace +=1
    hasFace = 0
    for i in range(count):
        if res[i]['result'] != None and res[i]['result']['face_num'] > 0 and res[i]['result']['face_list'][0]['face_probability']>=0.92:
            hasFace += 1
            ex = res[i]['result']['face_list'][0]['expression']['type']
            exp = res[i]['result']['face_list'][0]['expression']['probability']
            e = res[i]['result']['face_list'][0]['emotion']['type']
            p = res[i]['result']['face_list'][0]['emotion']['probability']
            if ex == 'smile' or ex == 'laugh':
                if exp >= 0.5:
                    if e != 'happy':
                        e = 'happy'
                        p = exp
            # print(res[i])
            if e in map:
                prob[map[e] - 1] += get_weighted_value(p)
            else:
                prob[3] += get_weighted_value(p)

    # find the most possible emotion_id among multiple results
    emotion = 0
    init = 0.8
    if hasFace > 0:
        for i in range(len(prob)):
            if prob[i] > init:
                init = prob[i]
                emotion = i + 1
        if emotion == 0:
            emotion = 4
    if emotion != 0:
        print("emotion = " + list(map.keys())[emotion - 1] + "\t" + str(max(prob)))

    # stop last work, since user haveleft for more than 2 mins
    if working_stat and face_check_gap > 2*60:
        begin_time = working_stat.begin_time

        # stop too fast, delete
        if last_face_time - begin_time < 2*60:
            Working.delete(working_stat)
        else:
            if begin_time > last_face_time:
                print('ERROR!!!!!!!!!!!!!!!!work time larger than face time !!!!!!!!!!!!!!!!!!!!!!!')
                Working.stop_working(time=(begin_time+60*20))
            else:
                Working.stop_working(time=last_face_time)
        return reply_json(2)

    # if no face detected, means idle
    if hasFace < 1:
        res = requests.get('https://api.thingspeak.com/update?' +
                           SC['thingspeak'] + 'field5=0')
        return reply_json(3)

    # if user haven't start working, then start work, since at least 1 face has been detected
    if not working_stat:
        working_stat = Working.begin_working()

    # put the expression data into database, now last face time should be current time
    Emotions.add(Emotions(list(map.keys())[emotion - 1],time=current_time))
    res = requests.get('https://api.thingspeak.com/update?' +
                       SC['thingspeak'] + 'field1=' + str(emotion) +
                       '&field5=1')

    # init pressure evaluation
    shouldRest = False
    rate = Emotions.get_depress_rate()
    begin_time = working_stat.begin_time
    work_duration = current_time - begin_time

    # if more than 20% of the expression captured are negative and user have worked more than 40mins, he/she should take a rest
    if rate > 0.1 and work_duration > 60*40:
        shouldRest = True
    
    # successfully detected face - working;
    return reply_json(1,
                      data={
                          'emotion': list(map.keys())[emotion - 1],
                          'begin_time': begin_time,
                          'shouldRest':shouldRest
                      })


@emotions.route('/playSong', methods=['GET'])
def playSong():
    from util.buzzer import play_mario
    play_mario()
    return reply_json(1)


if __name__ == "__main__":
    faceRe = FaceRecog()
    faceRe.recog("picture/image.jpg")
