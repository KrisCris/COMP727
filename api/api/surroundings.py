from flask import Blueprint, request
import requests
from util.SC import SC
from database.Surroundings import Surroundings


from util.utils import reply_json, get_indoor_temp, get_outdoor_weather

surroundings = Blueprint('surroundings',__name__)

@surroundings.route('/indoor_weather', methods=['GET'])
def indoor_weather():
    result = get_indoor_temp()
    if result :
        if result[0] is not None and result[1] is not None:
            res = requests.get('https://api.thingspeak.com/update?'+SC['thingspeak']+'field3='+str(result[0])+'&field4='+str(result[1]))
            Surroundings(indoor_tmp=result[0], indoor_hmd=result[1]).add()
            return reply_json(code=1, data={'tmp':result[0],'hmd':result[1]})
    return reply_json(code=0,data=[])




@surroundings.route('/outdoor_weather', methods=['GET'])
def outdoor_weather():
    return reply_json(1, data=get_outdoor_weather())
    # metric/imperial C/F

@surroundings.route('/location', methods=['GET'])
def location():
    ip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
    r = requests.get('http://api.ipstack.com/'+ip+'?'+SC['location']).json()
    print(r)
    return reply_json(1, data=r)
    

    