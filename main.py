# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime, os, time, calendar

from flask import Flask, render_template, request
from datetime import date #,timedelta

# [START gae_python37_datastore_store_and_fetch_times]
from google.cloud import datastore

datastore_client = datastore.Client()

# [END gae_python37_datastore_store_and_fetch_times]
app = Flask(__name__)

# [START gae_python37_datastore_store_and_fetch_times]


my_date = date.today()
dayName = calendar.day_name[my_date.weekday()]

A = (805, 850)
B = (855, 940)
C = (1020, 1105)
D = (1110, 1155)
E = (1250, 1335)
F = (1340, 1425)
G = (1430, 1515)

CC = (0,0)

if dayName == 'Monday':
    A = (805, 850)
    B = (855, 940)
    C = (1020, 1105)
    D = (1110, 1155)
    E = (1250, 1335)
    F = (1340, 1425)
    G = (1430, 1515)
elif dayName == 'Tuesday':
    B = (805, 850)
    C = (855, 940)
    A = (1020, 1105)
    D = (1110, 1155)
    F = (1250, 1335)
    G = (1340, 1425)
    E = (1430, 1515)
elif dayName == 'Wednesday':
    A = (805, 920)
    CC = (925, 1015)
    B = (1020, 1135)
    E = (1230, 1345)
    F = (1400, 1515)
elif dayName == 'Thursday':
    C = (910, 1025)
    D = (1100, 1215)
    G = (1400, 1515)
elif dayName == 'Friday':
    C = (805, 850)
    A = (855, 940)
    B = (1020, 1105)
    D = (1110, 1155)
    G = (1250, 1335)
    E = (1340, 1425)
    F = (1430, 1515)


def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times
# [END gae_python37_datastore_store_and_fetch_times]

# [START gae_python37_datastore_store_data_from_pi]
#ourTime = datetime.datetime.now() + timedelta(hours = 6, minutes = 0)
timeFull = 0
def storeScannedData(scannedData):
    entity = datastore.Entity(key=datastore_client.key('scan'))
    time = datetime.datetime.now()
    minute = time.minute
    hour = time.hour
    timeFull = str(hour) + str(minute)
    timeFull = int(timeFull)
    entity.update({
        'timestamp': str(timeFull),
        #readerId is the name of the key of the dictionary
        'readerId': scannedData['rID'], #rID should match match the name of variable posted by Pi
        'username': scannedData['username'], #username should match the name of variable posted by Pi
        'realnames': scannedData['realnames']
    })

    datastore_client.put(entity)


def fetchScannedData(limit):
    query = datastore_client.query(kind='scan')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times
# [END gae_python37_datastore_store_data_from_pi]

# [START gae_python37_datastore_render_times]
@app.route('/')
def root():
    # Store the current access time in Datastore.
    store_time(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    #times = fetch_times(10)
    scans = fetchScannedData(10)

    return render_template(
        'index.html', scans=scans, dayName=dayName,
        A=A, B=B, C=C, D=D, E=E, F=F, G=G)
# [END gae_python37_datastore_render_times]


# [START gae_python37_datastore_render_times]
@app.route('/rcvDataFromPi', methods=['POST'])
def rcvDataFromPi():
    # Store the current access time in Datastore.
    #store_time(datetime.datetime.now())
    storeScannedData(request.form) #Getting the dictionary sent from Pi

    return 'ok'
# [END gae_python37_datastore_render_times]

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
