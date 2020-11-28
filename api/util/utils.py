from util.constants import REPLY_CODES
from util.SC import SC
from flask import jsonify
from picamera import PiCamera
import time
import requests


def reply_json(code, msg=None, data=None):
    if data is None:
        data = []
    if code in REPLY_CODES:
        return jsonify({
            'code': code,
            'msg': REPLY_CODES[code] if msg is None else msg,
            'data': data
        })
    return jsonify({'code': 400, 'msg': 'Unknown code', 'data': data})


def captureFace():
    camera = PiCamera()
    time.sleep(1)
    camera.capture('picture/image.jpg')
    camera.close()


def get_indoor_temp():
    # import os
    # ds18b20 = ''
    # for i in os.listdir('/sys/bus/w1/devices'):
    # 	if i != 'w1_bus_master1':
    # 		ds18b20 = i
    # location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'

    # tfile = open(location)
    # text = tfile.read()
    # tfile.close()
    # temp_data = float(text.split(" ")[-1][2:])/1000

    # if temp_data != None:
    # 	return '%0.1f' % temp_data
    # else:
    # 	return None

    import util.dht11 as dht11

    # read data using pin 14
    instance = dht11.DHT11(pin=22)
    result = instance.read()

    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print(result.humidity)
        return [result.temperature, result.humidity]
    else:
        print("Error: %d" % result.error_code)
        return False


def get_outdoor_weather():
    ip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
    location = requests.get('http://api.ipstack.com/' + ip + '?' +
                            SC['location']).json()
    lon = str(location.get("longitude"))
    lat = str(location.get("latitude"))
    weather = requests.get('http://api.openweathermap.org/data/2.5/weather?' +
                           SC['weather'] + '&units=metric&lat=' + lat +
                           '&lon=' + lon).json()
    weather['weather'][0][
        'icon'] = "http://openweathermap.org/img/w/" + weather['weather'][0][
            'icon'] + ".png"
    return weather


def get_current_time():
    return int(time.time())


def get_time_gap(old):
    return int(time.time()) - old


def get_weighted_value(ori):
    if ori >= 0.9:
        ori = ori * 3 / 2
    elif ori >= 0.7:
        ori = ori * 6 / 5
    elif ori >= 0.5:
        ori = ori * 5 / 6
    else:
        ori = ori / 2
    return ori

def get_zero_clock():
    t = time.localtime(time.time())
    time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t),'%Y-%m-%d %H:%M:%S'))
    return time1
