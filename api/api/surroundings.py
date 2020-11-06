from flask import Blueprint, request
import requests

from util.utils import reply_json,get_indoor_temp

surroundings = Blueprint('surroundings',__name__)

@surroundings.route('/indoor_temp', methods=['GET'])
def indoor_temp():
    temp = get_indoor_temp()
    if temp is not None:
        return reply_json(code=1, data={'temp':temp})


@surroundings.route('/outdoor_weather', methods=['GET'])
def outdoor_weather():
    ip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
    location = requests.get('http://api.ipstack.com/'+ip+'?access_key=b9553ca98642d0f3a7e88f8ad16141a0').json()
    lon = str(location.get("longitude"))
    lat = str(location.get("latitude"))
    weather = requests.get('http://api.openweathermap.org/data/2.5/weather?appid=3c47f6b2f1a633f74b5b5452edd29ce9&units=metric&lat='+lat+'&lon='+lon).json()
    weather['weather'][0]['icon'] = "http://openweathermap.org/img/w/"+weather['weather'][0]['icon']+".png"
    return reply_json(1, data=weather)
    # metric/imperial C/F

@surroundings.route('/location', methods=['GET'])
def location():
    ip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
    r = requests.get('http://api.ipstack.com/'+ip+'?access_key=b9553ca98642d0f3a7e88f8ad16141a0').json()
    print(r)
    return reply_json(1, data=r)
    

    