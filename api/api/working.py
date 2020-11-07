from flask import Blueprint, request

from util.utils import get_current_time, reply_json, get_time_gap
from database.Working import Working

working = Blueprint('working',__name__)