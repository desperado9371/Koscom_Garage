import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime
import ta
import socket


class BacktestAPI:

    def __init__(self):
        print('backtest api')

    def backtest_listener(self, user_id='UserID', algo_id='test', initial_balance=100000000, from_date='20180101',
                          to_date='20191231', slippage=0.1, ):
        """ 장고에서 넘어오는 요청을 받고 백테스트 연산 후 결과 리턴해주는 함수

            Returns :
        """
        while True:
            HOST = '0.0.0.0'

            # 클라이언트 접속을 대기하는 포트 번호입니다.
            PORT = 9999

            # 소켓 객체를 생성합니다.
            # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용합니다.
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 포트 사용중이라 연결할 수 없다는
            # WinError 10048 에러 해결를 위해 필요합니다.
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용됩니다.
            # HOST는 hostname, ip address, 빈 문자열 ""이 될 수 있습니다.
            # 빈 문자열이면 모든 네트워크 인터페이스로부터의 접속을 허용합니다.
            # PORT는 1-65535 사이의 숫자를 사용할 수 있습니다.
            server_socket.bind((HOST, PORT))

            # 서버가 클라이언트의 접속을 허용하도록 합니다.
            server_socket.listen()
            # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓을 리턴합니다.
            client_socket, addr = server_socket.accept()
            # 접속한 클라이언트의 주소입니다.
            print('Connected by', addr)
            # 무한루프를 돌면서
            while True:
                # 클라이언트가 보낸 메시지를 수신하기 위해 대기합니다.
                data = client_socket.recv(1024)
                # 빈 문자열을 수신하면 루프를 중지합니다.
                if not data:
                    break
                # 수신받은 문자열을 출력합니다.
                request_str = data.decode()
                print('Received from', addr, data.decode())
                # 받은 문자열을 다시 클라이언트로 전송해줍니다.
                request = request_str.split('|')
                print(len(request))
                temp = "go back"
                df = self.get_price_data()
                df_str = df.to_json()
                client_socket.sendall(df_str.encode())

            # 소켓을 닫습니다.
            client_socket.close()
            server_socket.close()
            print('Connection Closed')

        price_data = []
        trade_data = []
        profit_list = []

        return price_data, trade_data, profit_list

    async def middleware_connect(self, user_id, algo_id):
        """
        미들웨어와 웹소켓방식으로 직접 통신하는 함수

        :param user_id:
        :param algo_id:
        :return:
        """
        async with websockets.connect("ws://15.164.231.112:80/Cocos") as websocket:
            msg = "load"
            msg = msg + "|" + user_id
            msg = msg + "|" + algo_id
            await websocket.send(msg)
            data_rcv = await websocket.recv()
            return data_rcv

    def algorithm_request(self, user_id, algo_id):
        """
        사용자 id와 알고리즘 id를 입력받아 DB로부터 알고리즘을 조회하는 함수

        param user_id:
        :param algo_id:
        :return:
        """

        data = asyncio.get_event_loop().run_until_complete(self.middleware_connect(user_id, algo_id))
        algo_json = eval(data)

        return algo_json

    def get_price_data(self, market='upbit', time_delta='1d'):
        """
        파일로 되어있는 시세 정보를 시장과 시간단위 를 입력받아서 읽어오는 함수

        :param market:
        :param time_delta:
        :return:
        """

        bitcoin_dt = pd.DataFrame()
        if market == 'upbit':
            if time_delta == '1d':
                bitcoin_dt = pd.read_csv('upbit_krwbtc_1day.csv')
            elif time_delta == '1m':
                bitcoin_dt = pd.read_csv('upbit_krwbtc_1min.csv')
        elif market == 'binance':
            if time_delta == '1d':
                bitcoin_dt = pd.read_csv('binance_btcusdt_1day.csv')
            elif time_delta == '1m':
                bitcoin_dt = pd.read_csv('binance_btcusdt_1min.csv')

        return bitcoin_dt

    def calculate_indicators(self, df):

        return df

    ##지표 구현 부분########
    def macd(self, df, n_slow=26, n_fast=12, n_sign=9):
        indicator_macd = ta.trend.MACD(df['close'],
                                       n_slow=n_slow,
                                       n_fast=n_fast,
                                       n_sign=n_sign)
        df['macd'] = indicator_macd.macd()
        df['macd_diff'] = indicator_macd.macd_diff()
        df['macd_signal'] = indicator_macd.macd_signal()
        return df

    def rsi(self, df, n=14):
        indicator_rsi = ta.momentum.RSIIndicator(df['close'],
                                                 n=n)
        df['rsi'] = indicator_rsi.rsi()
        return df

    def bollinger_band(self, df, n=20, ndev=2):
        indicator_bollinger = ta.volatility.BollingerBands(df['close'],
                                                           n=n,
                                                           ndev=ndev)
        df['bollinger_hband'] = indicator_bollinger.bollinger_hband()
        df['bollinger_hband_indicator'] = indicator_bollinger.bollinger_hband_indicator()
        df['bollinger_lband'] = indicator_bollinger.bollinger_lband()
        df['bollinger_lband_indicator'] = indicator_bollinger.bollinger_lband_indicator()
        df['bollinger_mband'] = indicator_bollinger.bollinger_mavg()
        df['bollinger_wband'] = indicator_bollinger.bollinger_wband()
        return df

    def obv(self, df):
        indicator_obv = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume'])
        df['obv'] = indicator_obv.on_balance_volume()
        return df

    ##################

    def sample_macd_stratege(self):
        """
        추세지표인 MACD를 이용하여 매수 매도 리스트 생성

        :return:
        """
        bitcoin_dt = pd.read_csv('upbit_krwbtc_1day.csv')
        df = bitcoin_dt
        macd = ta.trend.MACD(bitcoin_dt['close'])
        indicator_macd = ta.trend.MACD(df['close'])
        # Add Bollinger Bands features
        df['macd'] = indicator_macd.macd()
        df['macd_diff'] = indicator_macd.macd_diff()
        df['macd_signal'] = indicator_macd.macd_signal()
        date_list = []
        type_list = []

        for index, data in df.iterrows():
            if str(data['macd']) != 'nan':
                if df['macd'][index - 1] * data['macd'] < 0:
                    if data['macd'] < 0:
                        # print("sell : {},{}".format(data['macd'],data['timestamp']))
                        date_list.append(data['timestamp'][:10])
                        type_list.append("sell")
                    else:
                        # print("buy : {},{}".format(data['macd'],data['timestamp']))
                        date_list.append(data['timestamp'][:10])
                        type_list.append("buy")

        return date_list, type_list

    def get_trade_list(self):

        return

    def send_order(self, market='upbit',
                   order_type='buy',
                   quantity=1,
                   target_date="2018-10-11",
                   krw_balance=0.0,
                   btc_balance=0.0):
        """
        과거데이터에 주문을 실행하는 함수

        :param market:
        :param order_type:
        :param quantity:
        :param target_date:
        :param krw_balance:
        :param btc_balance:
        :return:
        """
        bitcoin_dt = pd.read_csv('upbit_krwbtc_1day.csv')

        target_date = datetime.strptime(target_date, "%Y-%m-%d")

        price = -1

        dt_index = 0

        for index, bitcoin in bitcoin_dt.iterrows():
            temp = datetime.strptime(bitcoin['timestamp'][:10], "%Y-%m-%d")
            if temp == target_date:
                price = float(bitcoin['close'])
                dt_index = index
                break;

        if order_type == 'buy':
            if (price * quantity) <= krw_balance:
                krw_balance = krw_balance - (price * quantity)
                btc_balance = btc_balance + quantity
                print("주문 성공 : 구매 ({}) -  btckrw:{} 수량:{} 원화잔고:{} 비트코인잔고:{} 평가금액 :{}".
                      format(bitcoin_dt['timestamp'][dt_index],
                             float(bitcoin['close']),
                             quantity,
                             krw_balance,
                             btc_balance,
                             krw_balance + (btc_balance) * float(bitcoin['close'])))
            else:
                print("주문실패 : 잔고부족 ({})".format(bitcoin_dt['timestamp'][dt_index]))

        elif order_type == 'sell':
            if quantity <= btc_balance:
                krw_balance = krw_balance + (price * quantity)
                btc_balance = btc_balance - quantity
                print("주문 성공 : 판매 ({}) -  btckrw:{} 수량:{} 원화잔고:{} 비트코인잔고:{} 평가금액: {}".
                      format(bitcoin_dt['timestamp'][dt_index],
                             float(bitcoin['close']),
                             quantity, krw_balance,
                             btc_balance,
                             krw_balance + (btc_balance) * float(bitcoin['close'])))
            else:
                print("주문실패 : 잔고부족 ({})".format(bitcoin_dt['timestamp'][dt_index]))

        return krw_balance, btc_balance

    def execute_backtest(self, init_krw_bal=100000000, init_btc_bal=0, order_quantity=5,
                         date_list=['2019-01-11', '2019-02-11', '2019-02-20', '2019-06-11', '2019-07-11', '2019-07-20'],
                         type_list=['buy', 'buy', 'buy', 'sell', 'sell', 'sell']):
        """
        백테스트를 실행하는 함수

        :param init_krw_bal:
        :param init_btc_bal:
        :param order_quantity:
        :param date_list:
        :param type_list:
        :return:
        """

        krw_bal = init_krw_bal
        btc_bal = init_btc_bal
        order_quantity = order_quantity

        date_list = date_list
        type_list = type_list
        list_len = len(date_list)

        print("현재 원화잔고 : {}\\".format(krw_bal))
        print("현재 비트코인잔고 : {}".format(btc_bal))

        for i in range(list_len):
            krw_bal, btc_bal = self.send_order(market='upbit',
                                               order_type=type_list[i],
                                               quantity=order_quantity,
                                               target_date=date_list[i],
                                               krw_balance=krw_bal,
                                               btc_balance=btc_bal)

        print("현재 원화잔고 : {}\\".format(krw_bal))
        print("현재 비트코인잔고 : {}".format(btc_bal))
        print("수익률 : {}%".format((krw_bal - init_krw_bal) / init_krw_bal * 100))

