from flask import Flask

from api.surroundings import surroundings
from api.emotions import emotions
from api.working import working
from database.db import db

from util.constants import HOST, PORT, DEBUG, ENV
from util.constants import DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_PORT, DATABASE
import RPi.GPIO as GPIO
import time

# shit mountain
# end of shit mountain

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_PORT, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(surroundings, url_prefix='/surroundings')
app.register_blueprint(emotions, url_prefix='/emotions')
app.register_blueprint(working, url_prefix='/working')


if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    app.run(host=HOST, port=PORT, debug=DEBUG)