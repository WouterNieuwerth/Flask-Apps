#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 23:20:01 2019

@author: wouternieuwerth
"""

from flask import Flask
from sense_hat import SenseHat
sense = SenseHat()

sense.set_rotation(180)

app = Flask(__name__)

@app.route('/api/temp')
def temp():
    output = {
            'pressure': sense.get_pressure(),
            'temp_hum': sense.get_temperature_from_humidity(),
            'tmp_press': sense.get_temperature_from_pressure(),
            'humidity': sense.get_humidity()
            }
    return output

if __name__ == '__main__':
    app.run(debug=True)