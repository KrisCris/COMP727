from flask import Blueprint, request

from util.utils import get_current_time, reply_json, get_time_gap
from database.Working import Working

working = Blueprint('working',__name__)

@working.route('/stop_working', methods=['POST'])
def stop_working():
    end_time = get_current_time()
    last_work = Working.query.order_by(Working.id.desc()).first()
    if last_work is not None:
        if last_work.end_time is not None:
            return reply_json(-2)
    last_work.end_time = end_time
    Working.add(last_work)
    return reply_json(1, data={'period':get_time_gap(last_work.begin_time)})


@working.route('/begin_working', methods=['POST'])
def begin_working():
    last_work = Working.query.order_by(Working.id.desc()).first()
    if last_work is not None:
        if last_work.end_time is None:
            return reply_json(-1)

    begin_time = get_current_time()
    work = Working(begin=begin_time)
    Working.add(work)

    return reply_json(1, data={'begin_time':begin_time})