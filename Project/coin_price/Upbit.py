import requests
import json
from datetime import datetime
from datetime import timedelta
import pandas as pd
import numpy as np

class UpbitAPI:
    """Upbit 거래소에 조회 요청하기 위한 api
    
    """
    def __init__(self):
        print("This is Upbit API")
        
    def get_all_day_list(self):
        """거래소 설립일 2017-09-25 부터 일봉 전부 조회
        
        """
        today = datetime.today()
        url = "https://api.upbit.com/v1/candles/days"
        df_list=[]

        for j in range(6):
            if j==0:
                querystring = {"market":"KRW-BTC","count":"200",}
            else:
                cur = df_list[j-1].index[-1]
                cur = datetime.strptime(cur,'%Y-%m-%dT%H:%M:%S')
                next_to = cur - timedelta(days=1)
                querystring = {"market":"KRW-BTC","count":"200","to":next_to}

            response = requests.request("GET", url, params=querystring)
            d = json.loads(response.text)

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

            df_list.append(pd.DataFrame(list(zip(open_prices,closed_prices,high_prices,low_prices,volume)), index=timestamps, columns = ['open','close','high','low','volume']))
    
        df = pd.DataFrame()
        for i in range(len(df_list)):
            df = df.append(df_list[i])
        df=df.iloc[::-1]
        return df