import requests 
import base64
import json
from flask import Blueprint, request
from util.utils import reply_json, captureFace, get_time_gap, get_current_time
from database.Working import Working
from database.Emotions import Emotions

emotions = Blueprint('emotions',__name__)

last_success_time = 0

class FaceRecog:
    def __init__(self):
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=wm8zkBBzjlenarSlfx481Y8Q&client_secret=OmOEawYr2Glc9cniKCd1AR4S2oqif9kr'
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
    
    captureFace()
    faceRe = FaceRecog()
    res = faceRe.recog("picture/image.jpg")
    if(not res):
        return reply_json(0)

    res = res.json()
    print(res)
    working_stat = Working.isWorking()
    if(res['result'] == None):
        if working_stat:
            time_gap = get_time_gap(last_success_time)
            if time_gap > 3*60:
                if Working.stop_working():
                    print(2)
                    return reply_json(2)
                else:
                    print('finish working failed.')
                    return reply_json(3)
        return reply_json(3)

    if not working_stat:
        last_success_time = get_current_time()
        working_stat = Working.begin_working()
        if not working_stat:
            print('already working')
    expression = res['result']['face_list'][0]['expression']['type']
    emotion = res['result']['face_list'][0]['emotion']['type']
    Emotions.add(Emotions(emotion))
    last_success_time = get_current_time()
    return reply_json(1,data={'expression':expression, 'emotion':emotion, 'begin_time':Working.isWorking().begin_time})

if __name__ == "__main__":
    faceRe = FaceRecog()
    faceRe.recog("picture/image.jpg")