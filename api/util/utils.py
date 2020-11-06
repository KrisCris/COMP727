from util.constants import REPLY_CODES
from flask import jsonify
from picamera import PiCamera
from time import sleep
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
    return jsonify({
        'code': 400,
        'msg': 'Unknown code',
        'data': data
    })


def captureFace():
    camera = PiCamera()
    sleep(1)
    camera.capture('picture/image.jpg')
    camera.close()


def get_indoor_temp():
	import os
	ds18b20 = ''
	for i in os.listdir('/sys/bus/w1/devices'):
		if i != 'w1_bus_master1':
			ds18b20 = i
	location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'

	tfile = open(location)
	text = tfile.read()
	tfile.close()
	temp_data = float(text.split(" ")[-1][2:])/1000

	if temp_data != None:
		return '%0.1f' % temp_data
	else:
		return None


def get_outdoor_weather():
	ip = requests.get('http://ifconfig.me/ip', timeout=1).text.strip()
	location = requests.get('http://api.ipstack.com/'+ip+'?access_key=b9553ca98642d0f3a7e88f8ad16141a0').json()
	lon = str(location.get("longitude"))
	lat = str(location.get("latitude"))
	weather = requests.get('http://api.openweathermap.org/data/2.5/weather?appid=3c47f6b2f1a633f74b5b5452edd29ce9&units=metric&lat='+lat+'&lon='+lon).json()
	weather['weather'][0]['icon'] = "http://openweathermap.org/img/w/"+weather['weather'][0]['icon']+".png"
	return weather


def get_current_time():
    return int(time.time())


def get_time_gap(old):
    return int(time.time()) - old