import schedule
import time
import pandas as pd
import pandas_gbq
import requests
import json

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

        df = pd.DataFrame.from_dict(dict)

        try:
            pandas_gbq.to_gbq(df, 'sensehat.temperature', project_id='bigquerywouter', if_exists='append')
        except:
            print('An error has occurred: BigQuery insert did not go through...')
    
    else:
        print('An error has occurred with request.get.')

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)