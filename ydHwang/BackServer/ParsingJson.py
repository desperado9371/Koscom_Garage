
# coding: utf-8

# In[37]:


import asyncio
import websockets
from websocket import create_connection
import math
import json
import pandas as pd
from datetime import datetime
import ta
import socket
import numpy as np
from backtestAPI import BacktestAPI

class Algo_Info:
    str_date =""
    end_date =""
    bns_tp=""
    name = []

class block:
    condition_min = ""
    condition_max = ""
    total_count = ""

# 지표값을 호출해서 리스트에 추가함
def Make_indicat(indi,prc_lst): 
    
    if indi['name'] == 'macd':
        prc_lst = macd(prc_lst,
                           int(indi['val']['n_slow']),
                           int(indi['val']['n_fast']),
                           int(indi['val']['n_sign']))    
    elif indi['name'] == 'obv':
        prc_lst = obv(prc_lst)
    elif indi['name'] == 'rsi':
        prc_lst = rsi(prc_lst,int(indi['val']['period']))
    elif indi['name'] == 'bollinger_band':
        prc_lst = bollinger_band(prc_lst,
                                 int(indi['val']['period']),
                                 int(indi['val']['ndev']))

    return prc_lst

def get_price_data( market='upbit', time_delta='1d'):
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
    
##지표 구현 부분########
def macd(Prc_history, n_slow=26, n_fast=12, n_sign=9):
    indicator_macd = ta.trend.MACD(Prc_history['close'],
                                   n_slow=n_slow,
                                   n_fast=n_fast,
                                   n_sign=n_sign)
    Prc_history['macd'] = indicator_macd.macd()
    Prc_history['macd_diff'] = indicator_macd.macd_diff()
    Prc_history['macd_signal'] = indicator_macd.macd_signal()
    return Prc_history

def rsi(df, n=14):
    indicator_rsi = ta.momentum.RSIIndicator(df['close'],
                                             n=n)
    df['rsi'] = indicator_rsi.rsi()
    return df

def bollinger_band(df, n=20, ndev=2):
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

def obv(df):
    indicator_obv = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume'])
    df['obv'] = indicator_obv.on_balance_volume()
    return df


#  ----- Chk_Meet_Condition 함수
#  ----- input 으로 들어온 값들의 
def Chk_Meet_Condition(Prc_history,group_algo,row,meet_condtion):
    print("Chk_Meet_Condition 시작:" )
    #print(str(Prc_history[group_algo[0]['name']][row]) + str(Prc_history[group_algo[2]['name']][row]))
    meet_condtion= int(meet_condtion)
    # (case1 지표끼리 비교시)
    if group_algo[0]['name'] !='num' and group_algo[2]['name'] !='num':
        if math.isnan(Prc_history[group_algo[0]['name']][row])!= True and math.isnan(Prc_history[group_algo[2]['name']][row])!= True:
            print('case1 지표끼리 비교시')
            chk = str(Prc_history[group_algo[0]['name']][row])+str(group_algo[1]['val'])+str(Prc_history[group_algo[2]['name']][row])
            print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    elif group_algo[0]['name'] !='num' and group_algo[2]['name'] =='num':
        print('case2 지표랑 뒷부분의 상수랑 비교시')
        # (case2 지표랑 뒷부분의 상수랑 비교시)
        if math.isnan(Prc_history[group_algo[0]['name']][row])!= True and math.isnan(int(group_algo[2]['val']))!= True:
            chk = str(Prc_history[group_algo[0]['name']][row])+str(group_algo[1]['val'])+str(group_algo[2]['val'])
            print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    elif group_algo[0]['name'] =='num' and group_algo[2]['name'] !='num':
        print('case3 앞의 상수랑 뒷부분의 지표랑 비교시')
        # (case3 앞의 상수랑 뒷부분의 지표랑 비교시)
        if math.isnan(int(group_algo[0]['val']))!= True and math.isnan(Prc_history[group_algo[2]['name']][row])!= True :
            chk = str(group_algo[0]['val'])+str(group_algo[1]['val'])+str(Prc_history[group_algo[2]['name']][row])
            print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    return meet_condtion
        
#  ----- Fet 함수
#  ----- 하루하루씩 알고리즘에 대입해서 충족하는지 확인함 확인후 모든 block 이 충족될경우 일자를 저장해서 리턴
def Fet_Algo(Prc_history, algo,bns_tp,hourday_tp):
    result_datelist = []
    #for row in range(60, 70):
    for row in range(len(Prc_history)):
        group_meet_condtion = 0  # 각 그룹의 충족갯수
        block_meet_condtion = 1  # 각 블록의 충족여부 (1:충족 0: 미충족) =기본으로 충족이라고 가정하고 시작
        # 알고리즘 확인후 각 일자별로 충족하는지 확인
        for pars in algo['algo']:
            if pars[0:5] == 'block':
                group_meet_condtion = 0  # 그룹 충족 갯수 초기화
                for search_group in algo['algo'][pars]:
                    # group 순회시작
                    if search_group[0:5] == 'group':
                        print(pars + "/" + search_group + " 시작!")
                        # 각 그룹의 지표 확인
                        for group_algo in algo['algo'][pars][search_group]:
                            # 알고리즘에 맞게 지표 세팅
                            Prc_history = Make_indicat(group_algo, Prc_history)
                        group_meet_condtion = Chk_Meet_Condition(Prc_history, algo['algo'][pars][search_group], row,
                                                                 group_meet_condtion)

                print("순회 완료 Min: " + str(algo['algo'][pars]['min']) + " Mix: " + str(
                    algo['algo'][pars]['max']))
                print("group 충족수:" + str(group_meet_condtion))
                # 알고리즘 그룹을 다 순환하고 끝난 경우 충족조건이 맞는지 확인
                if int(algo['algo'][pars]['min']) <= int(group_meet_condtion) and int(
                        algo['algo'][pars]['max']) >= int(group_meet_condtion):
                    print("충족!")
                    block_meet_condtion = 1
                else:
                    print("미충족!")
                    block_meet_condtion = 0

                # 이미 블록중에 미충족된 블록이 있는경우 더이상 순회할 필요가 없으므로 break
                if block_meet_condtion == 0:
                    print("미충족 block 존재 다음 알고리즘으로 PASS")
                    break
        if block_meet_condtion == 1:
            # 충족시 일자를 리스트에 추가
            print("이날 알고리즘은 완벽하게 충족")
            if hourday_tp == 'day':#일봉인 경우
                result_datelist.append([Prc_history['timestamp'][row][0:10], bns_tp])  # 일자에서 시간부분 잘라내기위해 [0:10] 적용
            else :#시간봉인경우
                result_datelist.append([Prc_history['timestamp'][row], bns_tp])

    print(result_datelist)
    return result_datelist

#일봉 기준 시세 가져오기
def Get_DtPrc(market='upbit',str_date='0',end_date='99999999'):
    print('market: '+market+' str_date: '+str_date+' end_date: '+end_date)
    
    ws = create_connection('ws://52.79.241.205:80/BackServer_Day')
    order_packet = 'load'+'|'+market+'|'+str_date+'|'+end_date
    print(order_packet)
    if ws.connected:
        ws.send(order_packet)
        print()
        result = ws.recv()
        print(f"client received:{result}")
        ws.close()
    if not result :
        print("DB에서 값을 못받아왔습니다. 패킷 확인하세요")
    else:
        json_data=json.loads(result)    
        dataframe_result = pd.DataFrame(list(json_data),columns=['timestamp','open','close','high','low','volume'])

    return dataframe_result

#시간봉 기준 시세 가져오기
def Get_HrPrc(market='upbit',str_date='0',end_date='99999999', srt_time = '00', end_time='24'):
    print('market: '+market+' str_date: '+str_date+' end_date: '+end_date)
    print('srt_time: '+srt_time+' end_time: '+end_time)
    
    ws = create_connection('ws://52.79.241.205:80/BackServer_Hr')
    order_packet = 'load'+'|'+market+'|'+str_date+'|'+end_date+'|'+srt_time+'|'+end_time
    print(order_packet)
    if ws.connected:
        ws.send(order_packet)
        print()
        result = ws.recv()
        print(f"client received:{result}")
        ws.close()
    if not result :
        print("DB에서 값을 못받아왔습니다. 패킷 확인하세요")
    else:
        json_data=json.loads(result)    
        dataframe_result = pd.DataFrame(list(json_data),columns=['timestamp','time','open','close','high','low','volume'])

    return dataframe_result

# 1. 일봉/시간봉에 따라 시세 가져옴
# 2. 매수전략 충족리스트 받아옴
# 3. 매도전략 충족리스트 받아옴
def Parsing_Main(buy_strategy='',sell_strategy = '',market='upbit',srt_date='00000000',end_date='99999999',srt_time='00',end_time='23',hourday_tp='day'):  
    buy_result = []
    sell_result = []
    final_result= []
    
    # 기간시세 가져옴
    if hourday_tp =='day':#일봉일 경우    
        Prc_history = Get_DtPrc(market,srt_date,end_date)
    else : #시간봉일 경우 
        Prc_history = Get_HrPrc(market,srt_date,end_date,srt_time,end_time)
        Prc_history['timestamp'] = Prc_history[['timestamp','time']].apply(lambda x:'T'.join(x),axis=1)
    
    print(Prc_history)
    print('매수전략 시작')
    if buy_strategy =='':
        print("매수전략 없음")
    else :
        buy_result = Fet_Algo(Prc_history,buy_strategy,'buy',hourday_tp)
    
    if sell_strategy =='':
        print("매도전략 없음")
    else :
        sell_result = Fet_Algo(Prc_history,sell_strategy,'sell',hourday_tp)
    
    print('매수리스트')
    print(buy_result)
    print('매도리스트')
    print(sell_result)
    print('최종리스트')
    buy_result.extend(sell_result)
    final_result=sorted(buy_result)
    print(final_result)
    return final_result
    
    
if __name__ == '__main__':
    data = []
    result = []
    with open('Define_Algo.json', 'r') as f:
        json_data = json.load(f)
    market = json_data['algo']['market']
    hourday_tp = json_data['algo']['hourday']
    srt_date = json_data['algo']['srt_date']
    end_date = json_data['algo']['end_date']
    srt_time = json_data['algo']['srt_time']
    end_time = json_data['algo']['end_time']
    bns_tp = json_data['algo']['buysell']
    

    # Parsing 함수
    # 1번째 파라미터 = buy_strategy: 매수전략
    # 2번째 파라미터 = sell_strategy: 매도전략
    # 3번째 파라미터 = marcket 거래소
    # 4번째 파라미터 = srt_date 시작일
    # 5번째 파라미터 = end_date 종료일
    # 6번째 파라미터 = srt_time 시작시간
    # 6번째 파라미터 = srt_time 종료시간
    # 6번째 파라미터 = srt_time 시간봉/일봉
    result = Parsing_Main(json_data,json_data,market,srt_date,end_date,srt_time,end_time,hourday_tp)
    
    


        
        



# import backtestAPI
