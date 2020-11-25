import requests 
import base64
import json
import time
from flask import Blueprint, request
from util.utils import reply_json, captureFace, get_time_gap, get_current_time, get_weighted_value
from database.Working import Working
from database.Emotions import Emotions
from util.SC import SC

emotions = Blueprint('emotions',__name__)

last_success_time = 0

class FaceRecog:
    def __init__(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&'+ SC['baidu_face']
        response = requests.get(host)
        if(response):
            res = response.json()
            self.access_token = res['access_token']
        else:
            print("error")
    
    def recog(self,path):
        with open(path,"rb") as f:#转为二进制格式
            base64_data = base64.b64encode(f.read())#使用base64进行加密
            request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
            request_body = {
                "image":base64_data.decode(),
                "image_type":"BASE64",
                "face_field": "expression,emotion",
                "face_type":"LIVE"
            }
            jsonData = json.dumps(request_body)
            request_url = request_url + "?access_token=" + self.access_token
            headers = {'content-type': 'application/json'}
            response = requests.post(request_url, data=jsonData, headers=headers)
            return response

@emotions.route('/getEmotion',methods=['GET'])
def getEmotion():
    global last_success_time

    if last_success_time == 0 and Working.isWorking():
        t = Emotions.get_last_timestamp()
        if get_time_gap(t) > 120:
            Working.stop_working(time=t)
        else:
            last_success_time = t
    
    map = {
        "angry":1, 
        "fear":2,
        "sad":3, 
        "neutral":4,
        "surprise":5,
        "happy":6
    }

    prob = [0,0,0,0,0,0]

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
        print(res[count])
        count += 1
        time.sleep(0.5)

    if count == 0:
        return reply_json(0)

    hasFace = 0
    for i in range(count):
        if res[i]['result'] != None and res[i]['result']['face_num']>0:
            hasFace += 1
            e = res[i]['result']['face_list'][0]['emotion']['type']
            p = res[i]['result']['face_list'][0]['emotion']['probability']
            if p < 0.2:
                break
            if e in map:
                prob[map[e]-1] += get_weighted_value(p)
            else:
                prob[3] += get_weighted_value(0.5)

    emotion = 0
    init = 0.8
    if hasFace > 0:
        for i in range(len(prob)):
            if prob[i] > init:
                init = prob[i]
                emotion = i + 1
        if emotion == 0:
            emotion = 4

    print("emotion = "+list(map.keys())[emotion-1]+"\t"+str(max(prob)))

    working_stat = Working.isWorking()
    if working_stat and last_success_time == 0:
        Working.stop_working()
        working_stat = Working.isWorking()
    if not hasFace > 0:
        if working_stat:
            time_gap = get_time_gap(last_success_time)
            if time_gap > 120:
                if Working.stop_working():
                    return reply_json(2)
                else:
                    print('finish working failed.')
                    return reply_json(3)
        res = requests.get('https://api.thingspeak.com/update?'+SC['thingspeak']+'field5=0')
        return reply_json(3)

    if not working_stat:
        last_success_time = get_current_time()
        working_stat = Working.begin_working()
        if not working_stat:
            print('already working')

    Emotions.add(Emotions(list(map.keys())[emotion-1]))
    last_success_time = get_current_time()

    res = requests.get('https://api.thingspeak.com/update?'+SC['thingspeak']+'field1='+str(emotion)+'&field5=1')
    return reply_json(1,data={'emotion':list(map.keys())[emotion-1], 'begin_time':Working.isWorking().begin_time})

if __name__ == "__main__":
    faceRe = FaceRecog()
    faceRe.recog("picture/image.jpg")