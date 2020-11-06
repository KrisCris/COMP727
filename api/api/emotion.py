from flask import Blueprint, request
import requests

emotion = Blueprint('emotion',__name__)

@emotion.route('/emotion', methods=['POST'])
def emotion():
    pass