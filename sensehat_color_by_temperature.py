import schedule
import time
import pandas as pd
import pandas_gbq
import requests
import json
from datetime import datetime, timedelta
from sense_hat import SenseHat

sense = SenseHat()
sense.clear()
sense.set_rotation(180)


df = pd.DataFrame({
            'timestamp': [],
            'pressure': [], 
            'temp_hum': [], 
            'tmp_press': [], 
            'humidity': []
        })

def job():
    response = requests.get('http://192.168.2.74:4444/api/temp')
    if response:
        print('Success!')

        result_json = json.loads(response.text.replace('\'','"'))

        dict = {
            'timestamp': [pd.Timestamp.now()],
            'pressure': [result_json['pressure']], 
            'temp_hum': [result_json['temp_hum']], 
            'tmp_press': [result_json['tmp_press']], 
            'humidity': [result_json['humidity']]
        }

        df_row = pd.DataFrame.from_dict(dict)

        global df
        df = df.append(df_row)
        df = df[df['timestamp']>(datetime.today() - timedelta(days=1))]
        df['rank_temp_press'] = df['tmp_press'].rank()

        set_sense_hat(df)
    
    else:
        print('An error has occurred with request.get.')

def set_sense_hat(df):
    count = len(df.index)
    rank = int(df['rank_temp_press'].loc[df['timestamp'] == df['timestamp'].max()].values[0])

    r = int(round(((rank-1)/max((count-1),1)) * 255)) # Red
    g = 0
    b = int(round((1-((rank-1)/max((count-1),1))) * 255)) # Blue

    sense.clear()
    sense.clear(r,g,b)


schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)