from flask import Flask, render_template, request, Response
from pymongo import MongoClient
import datetime

app = Flask(__name__)

client = MongoClient('192.168.0.155', 27017, username='root', password='klimma1508')

db = client["weather"]
weatherDB = db["weather"]


@app.route('/', methods=('GET', 'POST'))
def index():
    return render_template('help.html')

#get weather data and save to mongoDB
@app.route('/send', methods=('GET', 'POST'))
def send():
    IO = None
    room = None
    dat = None
    date = datetime.datetime.now()

    date = str(date.year) + "." + str(date.month) + "." + str(date.day) + " " + str(date.hour) + ":" + str(date.minute) + ":" + str(date.second)

    get = request.get_json()

    if get:
        if "IO" in get:
            IO = get["IO"]

        if "ROOM" in get:
            room = get["ROOM"]

        if "SENSORS" in get:
            dat = get["SENSORS"]

    mydat = {"date": date, "IO": IO, "room": room, "sensors": dat}
    x = weatherDB.insert_one(mydat).inserted_id
    print(x)


    return Response(str(x), status=200, mimetype='application/text')


#read data from DB and send them as JSON according to request
@app.route('/read', methods=('GET', 'POST'))
def read():
    Type = request.args.get('type')# ID/Date/room/IO
    mode = request.args.get('mode')# single/multi
    IO = request.args.get('IO')
    value = request.args.get('value')
    x = ""

    if Type == "ID":
        if mode == "single":
            x = weatherDB.find({"_id": value})
        elif mode == "multi":
            x = weatherDB.find({"_id": {"$gt" : value.split("-")[0], "$lt" : value.split("-")[1]}})

    if Type == "date":
        return 0

    if Type == "room":
        return 0

    if Type == "IO":
        if mode == "single":
            x = weatherDB.find({"IO": str(value)})
        elif mode == "multi":
            x = "error, not allowed"


    result = "{"
    for y in x:
        result = result + str(y) + ","
    result = result[:-1] + "}"
    return Response(result, status=200, mimetype='application/json')


if __name__ == '__main__':
    app.run()