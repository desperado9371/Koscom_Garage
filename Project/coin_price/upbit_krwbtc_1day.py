import requests
import json
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np
import time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

prev = pd.read_csv('/home/garage/workspace/price_update_crontab/upbit_krwbtc_1day.csv',index_col=False)
last_timestamp = prev.iloc[-1][0]

querystring = {"market":"KRW-BTC","count":"100"}
url = "https://api.upbit.com/v1/candles/days"
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

df= pd.DataFrame(list(zip(timestamps,open_prices,closed_prices,high_prices,low_prices,volume)),
                            columns = ['timestamp','open','close','high','low','volume'])
df = df.iloc[::-1]

index = 0
for i in range(len(df)):
    timestamp = str(df.iloc[i]['timestamp'])
    if timestamp >= last_timestamp:
        index = i
        break

df[index:]
next_df = prev[:-1:].append(df[index:])
next_df.to_csv('/home/garage/workspace/price_update_crontab/upbit_krwbtc_1day.csv',index=False)
