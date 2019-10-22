#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:30:12 2019

@author: wouternieuwerth
"""

from flask import Flask
import socketio
from sense_hat import SenseHat
import time

sense = SenseHat()

sense.set_rotation(180)

flapp = Flask(__name__)

# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio, flapp)

output = {
    'pressure': sense.get_pressure(),
    'temp_hum': sense.get_temperature_from_humidity(),
    'tmp_press': sense.get_temperature_from_pressure(),
    'humidity': sense.get_humidity()
}

@app.route('/api/temp')
def temp():
    return str(output)

def emitOutput():
    sio.emit('senseData', {'data' : output})
    
while True:
    emitOutput()
    time.sleep(1)

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0')