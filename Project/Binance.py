from binance.client import Client
from datetime import datetime
import numpy as np
import pandas as pd
import ta

class BinanceAPI:
    """Binance 거래소에 조회 요청하기 위한 api
        
        
    """
    def __init__(self):
        print("This is Biance API")
        
    def api_connect(self):
        """api key 연동
        
            Returns : api key와 secret key를 통해 조회요청한 Client 객체
        
        """
        return Client('ng0Zhq6ea42X3QxMV2RAubZxs508gguTISRwM13lQFFPrDDTxRiqmq3pBvIcvJMy',
                      'vHZDWuQvPf4mcaDvzxwRbtIWDbWuCyFyyG59bCZeTW6A6sd98qbHfCsFDVDdN3wn')
    
    def get_all_coin_list(self):
        """해당 거래소에 상장된 전체 코인 목록을 조회
        
            Returns : 코인 목록을 list 형태로 반환
            
        """
        client = self.api_connect()
        coin_all_list = client.get_all_tickers()
        coin_list = []
        for coin in coin_all_list:
            coin_list.append(coin['symbol'])
        return coin_list
        
    def get_klines(self,coin_name='BTCUSDT', interval='1d', term='6m' ):
        """분봉조회 하는 함수
        
            Args:
                    coin_name : 코인 종류 ( 비트코인<->USD, BTCUSTD)
                    
                    interval : 조회 주기( 1분봉, 15분봉,1일봉 등)
                                    분-M, 시간-h, 일-d, 주-w
                                    ex>1분 : '15M'
                    
                    term: 조회 기간 ( 최근 1개월, 6개월, 1년 등)
                                월-m, 년-y
                                ex>6개월 : '6m'
                    
            Returns:
                    open, close, high, low, volume 이 포함되고 timestamp로 인덱스된 DataFrame
                    
        
        """
        # binance 서버와 통신하기위해 api key 셋팅
        client = self.api_connect()
        
        #조회 주기 및 기간 설정을 위한 변수
        request_interval = Client.KLINE_INTERVAL_1DAY
        request_term = "6 month ago UTC"
        
        #조회 주기 설정
        if interval == '1M':
            request_interval = Client.KLINE_INTERVAL_1MINUTE
        elif interval == '15M':
            request_inerval = Client.KLINE_INTERVAL_15MINUTE
        elif interval == '1h':
            request_inerval = Client.KLINE_INTERVAL_1HOUR
        elif interval == '6h':
            request_inerval = Client.KLINE_INTERVAL_6HOUR
        elif interval == '12h':
            request_inerval = Client.KLINE_INTERVAL_6HOUR
        elif interval == '1d':
            request_inerval = Client.KLINE_INTERVAL_1DAY
        elif interval == '1w':
            request_inerval = Client.KLINE_INTERVAL_1WEEK
        else:
            request_interval = Client.KLINE_INTERVAL_1DAY
        
        #조회 기간 설정
        if term =='1d':
            request_term = "1 day ago UTC"
        elif term == '1w':
            request_term = "1 week ago UTC"
        elif term == '1m':
            request_term = "1 month ago UTC"
        elif term =='6m':
            request_term = "6 month ago UTC"
        elif term =='1y':
            request_term = "1 year ago UTC"
        else:
            request_term = "6 month ago UTC"
        
        # 설정한 값으로 조회
        klines = client.get_historical_klines(coin_name, request_interval, request_term)
        
        #데이터 추출을 위한 변수
        unix_timestamps=[]
        timestamps = []
        closed_prices = []
        open_prices = []
        high_prices= []
        low_prices= []
        volume = []
        
        #시간 추출 unix time
        for kline in klines:
            unix_timestamps.append(kline[0])
        
        #시간 변환  datetime
        for unix_timestamp in unix_timestamps:
            timestamps.append(datetime.fromtimestamp(unix_timestamp/1000))

        # open,close,high,low,volume 추출
        for kline in klines:
            open_prices.append(float(kline[1]))
            high_prices.append(float(kline[2]))
            low_prices.append(float(kline[3]))
            closed_prices.append(float(kline[4]))
            volume .append(float(kline[5]))
        
        #dataframe으로 묶음
        df = pd.DataFrame(list(zip(timestamps, open_prices,closed_prices,high_prices,low_prices,volume)), columns = ['timestamp','open','close','high','low','volume'])
    
        #반환
        return df
    
    def get_klines_set_term(self, coin_name="BTCUSDT", interval='1d',kline_from='1 Dec, 2017', kline_to='1 Jan, 2018' ):
        
        client = self.api_connect()
        
        request_interval = Client.KLINE_INTERVAL_1MINUTE
        request_from = kline_from
        request_to = kline_to
        
        klines = client.get_historical_klines(coin_name, request_interval, request_from, request_to)
        
        #데이터 추출을 위한 변수
        unix_timestamps=[]
        timestamps = []
        closed_prices = []
        open_prices = []
        high_prices= []
        low_prices= []
        volume = []
        
        #시간 추출 unix time
        for kline in klines:
            unix_timestamps.append(kline[0])
        
        #시간 변환  datetime
        for unix_timestamp in unix_timestamps:
            timestamps.append(datetime.fromtimestamp(unix_timestamp/1000))

        # open,close,high,low,volume 추출
        for kline in klines:
            open_prices.append(float(kline[1]))
            high_prices.append(float(kline[2]))
            low_prices.append(float(kline[3]))
            closed_prices.append(float(kline[4]))
            volume .append(float(kline[5]))
        
        #dataframe으로 묶음
        df = pd.DataFrame(list(zip(timestamps,open_prices,closed_prices,high_prices,low_prices,volume)),  columns = ['timestamp','open','close','high','low','volume'])
    
        #반환
        return df
        