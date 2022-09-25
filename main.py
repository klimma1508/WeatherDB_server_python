from flask import Flask, render_template, request, url_for, redirect, Response, jsonify
from pymongo import MongoClient
import json
import datetime

app = Flask(__name__)

client = MongoClient('192.168.0.155', 27017, username='root', password='klimma1508')

db = client["weather"]
indoor = db["indoor"]
outdoor = db["outdoor"]


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('help.html')


@app.route('/send', methods=('GET', 'POST'))
def send():
    IO = None
    room = None
    dat = None
    date = datetime.datetime.now()

    get = request.get_json()

    if get:
        if "IO" in get:
            IO = get["IO"]

        if IO == "IN":
            room = get["ROOM"]

        if "SENSORS" in get:
            dat = get["SENSORS"]

    if IO == "IN":
        mydat ={ "date": date, "room": room, "sensors": dat }
        x = indoor.insert_one(mydat).inserted_id
        print(x)

    if IO == "OUT":
        mydat ={ "date": date, "sensors": dat }
        x = outdoor.insert_one(mydat).inserted_id
        print(x)

    return Response(str(x), status=200, mimetype='application/text')


@app.route('/send', methods=('GET', 'POST'))
def send():

    return return Response(str(x), status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()