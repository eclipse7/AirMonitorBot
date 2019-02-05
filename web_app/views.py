from datetime import datetime, timedelta

import flask
from flask import request
from flask import session as flask_session

from web_app import app
from web_app.types import collection
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
    if content:
        try:
            data = {
                'device_id': int(content['device_id'], 16),
                'date': datetime.now(),
                'temp': float(content['temp']),
                'hum': float(content['hum']),
                'ppm': int(content['ppm']),
                'pressure': float(content['pressure']),
                'bmp180_temp': float(content['bmp180_temp'])
            }
            print(data)
            response = collection.insert_one(data).inserted_id
            return flask.Response(status=200)

        except Exception:
            return flask.Response(status=400)
