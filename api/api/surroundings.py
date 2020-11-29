from flask import Blueprint, request, Response
import requests
from util.SC import SC
from database.Surroundings import Surroundings

from util.utils import reply_json, get_indoor_temp, get_outdoor_weather, get_local_ip, gen_qrcode

surroundings = Blueprint('surroundings', __name__)



@surroundings.route('/indoor_weather', methods=['GET'])
def indoor_weather():
    result = get_indoor_temp()
    if result:
        if result[0] is not None and result[1] is not None:
            res = requests.get('https://api.thingspeak.com/update?' +
                               SC['thingspeak'] + 'field3=' + str(result[0]) +
                               '&field4=' + str(result[1]))
            Surroundings(indoor_tmp=result[0], indoor_hmd=result[1]).add()
            return reply_json(code=1,
                              data={
                                  'tmp': result[0],
                                  'hmd': result[1]
                              })
    return reply_json(code=0, data=[])


@surroundings.route('/outdoor_weather', methods=['GET'])
def outdoor_weather():
    weather_info = get_outdoor_weather()
    id = weather_info['weather'][0]['id']
    max = int(weather_info['main']['temp_max'])
    min = int(weather_info['main']['temp_min'])
    first = int(id / 100)
    weather_name = ''
    if first == 2:
        weather_name = 'thunder'
    elif first == 3 or first == 5:
        weather_name = 'rainy'
    elif first == 6:
        weather_name = 'snowy'
    elif first == 7:
        weather_name = 'smogy'
    elif id == 800:
        weather_name = 'sunny'
    elif first == 8:
        weather_name = 'cloudy'
    return reply_json(1,
                      data={
                          'weather': weather_name,
                          'max': max,
                          'min': min
                      })
    # metric/imperial C/F


@surroundings.route('/location', methods=['GET'])
def location():
    ip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
    r = requests.get('http://api.ipstack.com/' + ip + '?' +
                     SC['location']).json()
    print(r)
    return reply_json(1, data=r)


@surroundings.route('/ip_qr',methods=['GET'])
def ip_qr():
    ip = get_local_ip()
    qr = gen_qrcode(ip)
    return Response(qr, mimetype="image/jpeg")
