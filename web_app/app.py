from datetime import datetime

import flask
from flask import Flask, request

from bot.types import collection
from config import APP_SECRET_KEY

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY


@app.route("/")
def hello():
    return "<h1>Air Monitor!</h1>"


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
                'bmp180_temp': float(content['bmp180_temp']),
                'gas_res': float(content['gas_res'])
            }
            print(data)
            response = collection.insert_one(data).inserted_id
            return flask.Response(status=200)

        except Exception:
            return flask.Response(status=400)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=1883)
