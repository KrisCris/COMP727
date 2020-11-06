from flask import Flask

from api.surroundings import surroundings
from api.faceRecog import faceRecognize

from database.db import db

from util.constants import HOST, PORT, DEBUG, ENV
from util.constants import DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_PORT, DATABASE

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (
    DB_USERNAME, DB_PASSWORD, DB_ADDRESS, DB_PORT, DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(surroundings,url_prefix='/surroundings')
app.register_blueprint(faceRecognize, url_prefix='/faceRecognize')

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        db.create_all()

    app.run(host=HOST, port=PORT, debug=DEBUG)