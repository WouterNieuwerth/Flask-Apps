#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:30:12 2019

@author: wouternieuwerth
"""

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import threading
from sense_hat import SenseHat
sense = SenseHat()

sense.set_rotation(180)

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'paper motion'
socketio = SocketIO(app)

@app.route('/')
def home():
    return 'test homepage /'

@app.route('/api/temp')
def temp():
    output = {
        'pressure': sense.get_pressure(),
        'temp_hum': sense.get_temperature_from_humidity(),
        'tmp_press': sense.get_temperature_from_pressure(),
        'humidity': sense.get_humidity()
    }
    return str(output)

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')
    
@socketio.on('incoming')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

def timer():
    threading.Timer(5.0, timer).start()
    output = {
        'pressure': sense.get_pressure(),
        'temp_hum': sense.get_temperature_from_humidity(),
        'tmp_press': sense.get_temperature_from_pressure(),
        'humidity': sense.get_humidity()
    }
    socketio.emit('senseHat', {'data': output})
    #print('ticker')

timer()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')