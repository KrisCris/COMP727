from util.constants import REPLY_CODES
from flask import jsonify
from picamera import PiCamera
from time import sleep

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