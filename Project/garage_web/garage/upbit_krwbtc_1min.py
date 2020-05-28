import requests
import json
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

prev = pd.read_csv('/home/garage/workspace/price_update_crontab/upbit_krwbtc_1min.csv',index_col=False)
last_timestamp = prev.iloc[-1][0]

url = "https://api.upbit.com/v1/candles/minutes/1"

today = datetime.today()
date_from = today.strftime('%Y-%m-%d %H:%M:%S')

for k in range(1):
    df_list=[]
    cur = 0
    for j in range(10):

        if j==0:
            next_to = datetime.strptime(date_from,'%Y-%m-%d %H:%M:%S')
            next_to = next_to - timedelta(minutes=540)
            querystring = {"market":"KRW-BTC","count":"200","to":next_to}
        else:
            cur = df_list[-1].iloc[-1][0]
            cur = datetime.strptime(cur,'%Y-%m-%dT%H:%M:%S')
            next_to = cur - timedelta(minutes=540)
    #         print(j)
            if j%100==0:
                print(cur)
    #         print(next_to)
            querystring = {"market":"KRW-BTC","count":"200","to":next_to}

        response = requests.request("GET", url, params=querystring, verify=False)
        d = json.loads(response.text)

        if len(d) == 1:
            print("req err")

        unix_timestamps=[]
        timestamps = []
        closed_prices = []
        open_prices = []
        high_prices= []
        low_prices= []
        volume = []

        for i in range(len(d)):
            timestamps.append(d[i]['candle_date_time_kst'])
            closed_prices.append(d[i]['trade_price'])
            open_prices.append(d[i]['opening_price'])
            high_prices.append(d[i]['high_price'])
            low_prices.append(d[i]['low_price'])
            volume.append(d[i]['candle_acc_trade_volume'])

        df_list.append(pd.DataFrame(list(zip(timestamps,open_prices,closed_prices,high_prices,low_prices,volume)),
                                    columns = ['timestamp','open','close','high','low','volume']))
        if j%10==0:
            time.sleep(1)

new_df = pd.DataFrame()

df_list = df_list[::-1]
for df in df_list:
    new_df = new_df.append(df.iloc[::-1])
            
index = 0
for i in range(len(new_df)):
    if new_df.iloc[i]['timestamp'] == last_timestamp:
        index = i
        break

next_df = prev[:-1:].append(new_df[index:])
next_df.to_csv('/home/garage/workspace/price_update_crontab/upbit_krwbtc_1min.csv',index=False)
