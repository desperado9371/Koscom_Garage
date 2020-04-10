import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime
import ta


def backtest_listener(user_id='UserID', algo_id='test', initial_balance=100000000, from_date='20180101', to_date='20191231', slippage=0.1, ):
    """ 장고에서 넘어오는 요청을 받고 백테스트 연산 후 결과 리턴해주는 함수

        Returns :
    """
    price_data = []
    trade_data = []
    profit_list = []

    return price_data, trade_data, profit_list


async def middleware_connect(user_id, algo_id):
    """
    미들웨어와 웹소켓방식으로 직접 통신하는 함수

    :param user_id:
    :param algo_id:
    :return:
    """
    async with websockets.connect("ws://54.180.86.151:80/Cocos") as websocket:
        msg = "load"
        msg = msg + "|" + user_id
        msg = msg + "|" + algo_id
        await websocket.send(msg)
        data_rcv = await websocket.recv()
        return data_rcv


def algorithm_request(user_id, algo_id):
    """
    사용자 id와 알고리즘 id를 입력받아 DB로부터 알고리즘을 조회하는 함수

    param user_id:
    :param algo_id:
    :return:
    """
    algorithm = ""
    data = asyncio.get_event_loop().run_until_complete(middleware_connect(user_id, algo_id))
    algo_json = json.loads(data)

    return algorithm


def get_price_data(market='upbit', time_delta='1d'):
    """
    파일로 되어있는 시세 정보를 시장과 시간단위 를 입력받아서 읽어오는 함수

    :param market:
    :param time_delta:
    :return:
    """

    bitcoin_dt = pd.DataFrame
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


def calculate_indicators():

    return


def macd():
    """
    추세지표인 MACD를 계산하는 함수

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
    date_list=[]
    type_list=[]

    for index, data in df.iterrows():
        if str(data['macd']) != 'nan':
            if df['macd'][index-1] * data['macd'] < 0:
                if data['macd']<0:
                    #print("sell : {},{}".format(data['macd'],data['timestamp']))
                    date_list.append(data['timestamp'][:10])
                    type_list.append("sell")
                else:
                    #print("buy : {},{}".format(data['macd'],data['timestamp']))
                    date_list.append(data['timestamp'][:10])
                    type_list.append("buy")

    return date_list, type_list


def get_trade_list():

    return


def execute_backtest(init_krw_bal = 100000000, init_btc_bal = 0, order_quantity = 5,
                    date_list=['2019-01-11','2019-02-11','2019-02-20','2019-06-11','2019-07-11','2019-07-20'],
                    type_list=['buy','buy','buy','sell','sell','sell'] ):
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

    date_list= date_list
    type_list= type_list
    list_len = len(date_list)

    print("현재 원화잔고 : {}\\".format(krw_bal))
    print("현재 비트코인잔고 : {}".format(btc_bal))

    for i in range(list_len):
        krw_bal, btc_bal = send_order(market='upbit',
                                      order_type=type_list[i],
                                      quantity= order_quantity,
                                      target_date=date_list[i],
                                      krw_balance = krw_bal,
                                      btc_balance=btc_bal)

    print("현재 원화잔고 : {}\\".format(krw_bal))
    print("현재 비트코인잔고 : {}".format(btc_bal))
    print("수익률 : {}%".format( (krw_bal-init_krw_bal)/init_krw_bal*100))


def send_order(market='upbit', order_type='buy', quantity=1, target_date="2018-10-11", krw_balance=0.0,
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
