from datetime import timedelta

import flask
from flask import request
from flask import session as flask_session

from web_app import app
from web_app.types import *
from config import APP_SECRET_KEY

app.secret_key = APP_SECRET_KEY


@app.before_request
def function_session():
    flask_session.modified = True
    flask_session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)


@app.route('/device', methods=['POST'])
def new_data():
    content = request.get_json()
    # print(content)

    if content:
        try:
            session = Session()
            device = Device()
            device.date = datetime.now()
            device.device_id = int(content['device_id'], 16)
            device.temp = float(content['temp'])
            device.hum = float(content['hum'])
            device.ppm = int(content['ppm'])
            session.add(device)
            session.commit()
            return flask.Response(status=200)

        except Exception:
            Session.rollback()
            return flask.Response(status=400)
