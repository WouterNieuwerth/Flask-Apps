#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:30:12 2019

@author: wouternieuwerth
"""

import eventlet
import socketio
from sense_hat import SenseHat
import time

sense = SenseHat()

sense.set_rotation(180)

# create a Socket.IO server
sio = socketio.Server()

# wrap with a WSGI application
app = socketio.WSGIApp(sio)

output = {
    'pressure': sense.get_pressure(),
    'temp_hum': sense.get_temperature_from_humidity(),
    'tmp_press': sense.get_temperature_from_pressure(),
    'humidity': sense.get_humidity()
}

def emitOutput():
    sio.emit('senseData', {'data' : output})
    
while True:
    emitOutput()
    time.sleep(1)

@sio.event
def connect(sid, environ):
    print('connect ', sid)

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)