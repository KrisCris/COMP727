from flask import Blueprint, request
import requests

from util.utils import reply_json, get_indoor_temp, get_outdoor_weather

surroundings = Blueprint('surroundings',__name__)

@surroundings.route('/indoor_weather', methods=['GET'])
def indoor_weather():
    tmp = float(get_indoor_temp())
    hmd = 60
    if tmp is not None and hmd is not None:
        return reply_json(code=1, data={'tmp':tmp,'hmd':hmd})


@surroundings.route('/outdoor_weather', methods=['GET'])
def outdoor_weather():
    return reply_json(1, data=get_outdoor_weather())
    # metric/imperial C/F

@surroundings.route('/location', methods=['GET'])
def location():
    ip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
    r = requests.get('http://api.ipstack.com/'+ip+'?access_key=b9553ca98642d0f3a7e88f8ad16141a0').json()
    print(r)
    return reply_json(1, data=r)
    

    