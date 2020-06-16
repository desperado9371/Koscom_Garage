
# coding: utf-8

# In[25]:


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
    if indi['name'] == 'macd' or indi['name'] == 'macd_signal' or indi['name'] == 'macd_diff':
        prc_lst = macd(prc_lst,
                       int(indi['val']['n_slow']),
                       int(indi['val']['n_fast']),
                       int(indi['val']['n_sign']))
    elif indi['name'] == 'obv':
        prc_lst = obv(prc_lst)
    elif indi['name'] == 'roc':
        prc_lst = roc(prc_lst, n = int(indi['val']['period']))
    elif indi['name'] == 'rsi':
        prc_lst = rsi(prc_lst, n = int(indi['val']['period']))
    elif indi['name'] == 'tsi':
        prc_lst = tsi(prc_lst, r = int(indi['val']['high']), s = int(indi['val']['low']))
    elif indi['name'] == 'ao':
        prc_lst = ao(prc_lst, s = int(indi['val']['short']), len = int(indi['val']['long']))
    elif indi['name'] == 'kama':
        prc_lst = kama(prc_lst, n = int(indi['val']['ration']))
    elif indi['name'] == 'stoch':
        prc_lst = stoch(prc_lst, n = int(indi['val']['period']))
    #volume
    elif indi['name'] == 'adi':
        prc_lst = adi(prc_lst)
    elif indi['name'] == 'obv':
        prc_lst = obv(prc_lst)
    elif indi['name'] == 'cmf':
        prc_lst = cmf(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'eom':
        prc_lst = eom(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'fi':
        prc_lst = fi(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'mfi':
        prc_lst = mfi(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'nvi':
        prc_lst = nvi(prc_lst)
    elif indi['name'] == 'vpt':
        prc_lst = vpt(prc_lst)
    elif indi['name'] == 'vwap':
        prc_lst = vwap(prc_lst, n=int(indi['val']['period']))
    #Volatility
    elif indi['name'] == 'atr':
        prc_lst = atr(prc_lst,int(indi['val']['period']))
    elif indi['name'] == 'bollinger_hband':
        prc_lst = bollinger_hband(prc_lst,int(indi['val']['period']))
    elif indi['name'] == 'bollinger_lband':
        prc_lst = bollinger_lband(prc_lst, int(indi['val']['period']))
    elif indi['name'] == 'bollinger_mband':
        prc_lst = bollinger_mband(prc_lst,int(indi['val']['period']))
    elif indi['name'] == 'bollinger_wband':
        prc_lst = bollinger_wband(prc_lst, int(indi['val']['period']))
    elif indi['name'] == 'donchian_channel_hband':
        prc_lst = donchian_channel_hband(prc_lst,int(indi['val']['period']))
    elif indi['name'] == 'donchian_channel_lband':
        prc_lst = donchian_channel_lband(prc_lst,int(indi['val']['period']))
    #Trend
    elif indi['name'] == 'adx':
        prc_lst = adx(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'adx_neg':
        prc_lst = adx_neg(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'aroon_down':
        prc_lst = aroon_down(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'aroon_up':
        prc_lst = aroon_up(prc_lst, n=int(indi['val']['period']))  
    elif indi['name'] == 'aroon_indicator':
        prc_lst = aroon_indicator(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'cci':
        prc_lst = cci(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'dpo':
        prc_lst = dpo(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'ema':
        prc_lst = ema(prc_lst, n=int(indi['val']['period']))  
    elif indi['name'] == 'mi':
        prc_lst = mi(prc_lst, n=int(indi['val']['short']),n2=int(indi['val']['long']))
    elif indi['name'] == 'sma':
        prc_lst = sma(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'trix':
        prc_lst = trix(prc_lst, n=int(indi['val']['period']))    
    elif indi['name'] == 'vortex_indicator_diff':
        prc_lst = vortex_indicator_diff(prc_lst, n=int(indi['val']['period']))
    elif indi['name'] == 'vortex_indicator_neg':
        prc_lst = vortex_indicator_neg(prc_lst, n=int(indi['val']['period']))    
    elif indi['name'] == 'vortex_indicator_pos':
        prc_lst = vortex_indicator_pos(prc_lst, n=int(indi['val']['period']))

        #정의되어있지 않으면 그냥 PASS

    return prc_lst

    
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


## Momentum지표 추가 구현 부분########
def roc(df,n=12):
    indicator_roc = ta.momentum.ROCIndicator(df['close'],n=n)
    df['roc'] = indicator_roc.roc()
    return df

def rsi(df, n=14):
    indicator_rsi = ta.momentum.RSIIndicator(df['close'],n=n)
    df['rsi'] = indicator_rsi.rsi()
    return df

def tsi(df,r=25,s=13):
    indicator_tsi = ta.momentum.TSIIndicator(df['close'],r=r,s=s)
    df['tsi'] = indicator_tsi.tsi()
    return df

def ao(df,s=5,len=34):
    indicator_ao = ta.momentum.AwesomeOscillatorIndicator(df['high'],df['low'],s=s,len=len)
    df['ao'] = indicator_ao.ao()
    return df

def kama(df,n=10,pow1=2, pow2=30):
    indicator_kama = ta.momentum.KAMAIndicator(df['close'],n=n,pow1=pow1,pow2=pow2)
    df['kama'] = indicator_kama.kama()
    return df

def stoch(df,n=14, d_n=3 ):
    indicator_stoch = ta.momentum.StochasticOscillator(df['high'],df['low'],df['close'],n=n,d_n=d_n)
    df['stoch'] = indicator_stoch.stoch()
    return df

## Volume 지표 추가 구현 부분########
def adi(df):
    indicator_adi = ta.volume.AccDistIndexIndicator(high=df['high'], low=df['low'], close=df['close'], volume =df['volume'])
    df['adi'] = indicator_adi.acc_dist_index()
    return df

def obv(df):
    indicator_obv = ta.volume.OnBalanceVolumeIndicator(df['close'], df['volume'])
    df['obv'] = indicator_obv.on_balance_volume()
    return df

def cmf(df,n=20):
    indicator_cmf = ta.volume.ChaikinMoneyFlowIndicator(high=df['high'], low=df['low'], close=df['close'], volume =df['volume'],n=n)
    df['cmf'] = indicator_cmf.chaikin_money_flow()
    return df

def eom(df,n=14):
    indicator_eom = ta.volume.EaseOfMovementIndicator(high=df['high'], low=df['low'], volume =df['volume'],n=n)
    df['eom'] = indicator_eom.ease_of_movement()
    return df

def fi(df,n=13):
    indicator_fi = ta.volume.ForceIndexIndicator(close=df['close'], volume=df['volume'],n=n)
    df['fi'] = indicator_fi.force_index()
    return df

def mfi(df,n=14):
    indicator_mfi = ta.momentum.MFIIndicator(high=df['high'], low=df['low'], close=df['close'], volume =df['volume'],n=n)
    df['mfi'] = indicator_mfi.money_flow_index()
    return df

def nvi(df):
    indicator_nvi = ta.volume.NegativeVolumeIndexIndicator(close=df['close'], volume =df['volume'])
    df['nvi'] = indicator_nvi.negative_volume_index()
    return df

def vpt(df):
    indicator_vpt = ta.volume.VolumePriceTrendIndicator(close=df['close'], volume =df['volume'])
    df['vpt'] = indicator_vpt.volume_price_trend()
    return df

def vwap(df,n=14):
    indicator_vwap = ta.volume.VolumeWeightedAveragePrice(high=df['high'], low=df['low'], close=df['close'], volume =df['volume'],n=n)
    df['vwap'] = indicator_vwap.volume_weighted_average_price()
    return df

## Volatility 지표 추가 구현 부분########
def atr(df,n=14):
    indicator_atr = ta.volatility.AverageTrueRange(high=df['high'], low=df['low'], close=df['close'],n=n)
    df['atr'] = indicator_atr.average_true_range()
    return df

def bollinger_hband(df, n=20, ndev=2):
    indicator_bollinger = ta.volatility.BollingerBands(df['close'],n=n, ndev=ndev)
    df['bollinger_hband'] = indicator_bollinger.bollinger_hband()
    return df

def bollinger_lband(df, n=20, ndev=2):
    indicator_bollinger = ta.volatility.BollingerBands(df['close'], n=n, ndev=ndev)
    df['bollinger_lband'] = indicator_bollinger.bollinger_hband()
    return df

def bollinger_mband(df, n=20, ndev=2):
    indicator_bollinger = ta.volatility.BollingerBands(df['close'], n=n, ndev=ndev)
    df['bollinger_mband'] = indicator_bollinger.bollinger_hband()
    return df

def bollinger_wband(df, n=20, ndev=2):
    indicator_bollinger = ta.volatility.BollingerBands(df['close'], n=n, ndev=ndev)
    df['bollinger_wband'] = indicator_bollinger.bollinger_hband()
    return df

def donchian_channel_hband(df,n=20):
    indicator_donchian_channel = ta.volatility.DonchianChannel(close=df['close'],n=n)
    df['donchian_channel_hband'] = indicator_donchian_channel.donchian_channel_hband()
    return df

def donchian_channel_lband(df,n=20):
    indicator_donchian_channel = ta.volatility.DonchianChannel(close=df['close'],n=n)
    df['donchian_channel_lband'] = indicator_donchian_channel.donchian_channel_lband()
    return df

## Trend 지표 추가 구현 부분########
def adx(df,n=14):
    indicator_adx = ta.trend.ADXIndicator(high=df['high'], low=df['low'], close=df['close'],n=n)
    df['adx'] = indicator_adx.adx()
    return df

def adx_neg(df,n=14):
    indicator_adx = ta.trend.ADXIndicator(high=df['high'], low=df['low'], close=df['close'],n=n)
    df['adx_neg'] = indicator_adx.adx_neg()
    return df

def aroon_down(df,n=25):
    indicator_aroon = ta.trend.AroonIndicator(close=df['close'],n=n)
    df['aroon_down'] = indicator_aroon.aroon_down()
    return df

def aroon_up(df,n=25):
    indicator_aroon = ta.trend.AroonIndicator(close=df['close'],n=n)
    df['aroon_up'] = indicator_aroon.aroon_up()
    return df

def aroon_indicator(df,n=25):
    indicator_aroon = ta.trend.AroonIndicator(close=df['close'],n=n)
    df['aroon_indicator'] = indicator_aroon.aroon_indicator()
    return df

def cci(df,n=20):
    indicator_cci = ta.trend.CCIIndicator(high=df['high'], low=df['low'], close=df['close'],n=n,c=0.015)
    df['cci'] = indicator_cci.cci()
    return df

def dpo(df,n=20):
    indicator_dpo = ta.trend.DPOIndicator(close=df['close'],n=n)
    df['dpo'] = indicator_dpo.dpo()
    return df

def ema(df,n=14):
    indicator_ema = ta.trend.EMAIndicator(close=df['close'],n=n)
    df['ema'] = indicator_ema.ema_indicator()
    return df

def mi(df,n=9,n2=25):
    indicator_mi = ta.trend.MassIndex(high=df['high'],low=df['low'],n=n,n2=n2)
    df['mi'] = indicator_mi.mass_index()
    return df

def sma(df,n=14):
    indicator_sma = ta.trend.SMAIndicator(close=df['close'],n=n)
    df['sma'] = indicator_sma.sma_indicator()
    return df

def trix(df,n=15):
    indicator_trix = ta.trend.TRIXIndicator(close=df['close'],n=n)
    df['trix'] = indicator_trix.trix()
    return df

def vortex_indicator_diff(df,n=14):
    indicator_vi = ta.trend.VortexIndicator(high=df['high'], low=df['low'], close=df['close'],n=n)
    df['vortex_indicator_diff'] = indicator_vi.vortex_indicator_diff()
    return df

def vortex_indicator_neg(df,n=14):
    indicator_vi = ta.trend.VortexIndicator(high=df['high'], low=df['low'], close=df['close'],n=n)
    df['vortex_indicator_neg'] = indicator_vi.vortex_indicator_neg()
    return df

def vortex_indicator_pos(df,n=14):
    indicator_vi = ta.trend.VortexIndicator(high=df['high'], low=df['low'], close=df['close'],n=n)
    df['vortex_indicator_pos'] = indicator_vi.vortex_indicator_pos()
    return df


#  ----- Chk_Meet_Condition 함수
#  ----- input 으로 들어온 값들의 
def Chk_Meet_Condition(Prc_history,group_algo,row,meet_condtion):
    # print("Chk_Meet_Condition 시작:" )
    # print(str(Prc_history[group_algo[0]['name']][row]) + str(Prc_history[group_algo[2]['name']][row]))
    meet_condtion= int(meet_condtion)
    # (case1 지표끼리 비교시)
    if group_algo[0]['name'] !='num' and group_algo[2]['name'] !='num':
        if math.isnan(Prc_history[group_algo[0]['name']][row])!= True and math.isnan(Prc_history[group_algo[2]['name']][row])!= True:
            # print('case1 지표끼리 비교시')
            chk = str(Prc_history[group_algo[0]['name']][row])+str(group_algo[1]['val'])+str(Prc_history[group_algo[2]['name']][row])
            # print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    elif group_algo[0]['name'] !='num' and group_algo[2]['name'] =='num':
        # print('case2 지표랑 뒷부분의 상수랑 비교시')
        # (case2 지표랑 뒷부분의 상수랑 비교시)
        if math.isnan(Prc_history[group_algo[0]['name']][row])!= True and math.isnan(int(group_algo[2]['val']))!= True:
            chk = str(Prc_history[group_algo[0]['name']][row])+str(group_algo[1]['val'])+str(group_algo[2]['val'])
            # print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    elif group_algo[0]['name'] =='num' and group_algo[2]['name'] !='num':
        # print('case3 앞의 상수랑 뒷부분의 지표랑 비교시')
        # (case3 앞의 상수랑 뒷부분의 지표랑 비교시)
        if math.isnan(int(group_algo[0]['val']))!= True and math.isnan(Prc_history[group_algo[2]['name']][row])!= True :
            chk = str(group_algo[0]['val'])+str(group_algo[1]['val'])+str(Prc_history[group_algo[2]['name']][row])
            # print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    return meet_condtion
        
#  ----- Fet 함수
#  ----- 하루하루씩 알고리즘에 대입해서 충족하는지 확인함 확인후 모든 block 이 충족될경우 일자를 저장해서 리턴
def Fet_Algo(Prc_history, algo,bns_tp,hourday_tp):
    result_datelist = []

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
                        # print(pars + "/" + search_group + " 시작!")
                        # 각 그룹의 지표 확인
                        for group_algo in algo['algo'][pars][search_group]:
                            # 알고리즘에 맞게 지표 세팅
                            Prc_history = Make_indicat(group_algo, Prc_history)
                        # print(Prc_history)
                        group_meet_condtion = Chk_Meet_Condition(Prc_history, algo['algo'][pars][search_group], row,
                                                                 group_meet_condtion)

                # print("순회 완료 Min: " + str(algo['algo'][pars]['min']) + " Mix: " + str(
                #     algo['algo'][pars]['max']))
                # print("group 충족수:" + str(group_meet_condtion))
                # 알고리즘 그룹을 다 순환하고 끝난 경우 충족조건이 맞는지 확인
                if int(algo['algo'][pars]['min']) <= int(group_meet_condtion) and int(
                        algo['algo'][pars]['max']) >= int(group_meet_condtion):
                    # print("충족!")
                    block_meet_condtion = 1
                else:
                    # print("미충족!")
                    block_meet_condtion = 0

                # 이미 블록중에 미충족된 블록이 있는경우 더이상 순회할 필요가 없으므로 break
                if block_meet_condtion == 0:
                    # print("미충족 block 존재 다음 알고리즘으로 PASS")
                    break
        if block_meet_condtion == 1:
            # 충족시 일자를 리스트에 추가
            # print("이날 알고리즘은 완벽하게 충족")
            if hourday_tp == 'day':#일봉인 경우
                result_datelist.append([Prc_history['timestamp'][row][0:10], bns_tp])  # 일자에서 시간부분 잘라내기위해 [0:10] 적용
            else :#시간봉인경우
                result_datelist.append([Prc_history['timestamp'][row], bns_tp])

    # print(result_datelist)
    return result_datelist

#일봉 기준 시세 가져오기
def Get_DtPrc(market='upbit',str_date='0',end_date='99999999'):
    # print('market: '+market+' str_date: '+str_date+' end_date: '+end_date)
    
    ws = create_connection('ws://13.124.102.83:80/BackServer_Day')
    order_packet = 'load'+'|'+market+'|'+str_date+'|'+end_date
    # print(order_packet)
    if ws.connected:
        ws.send(order_packet)
        # print()
        result = ws.recv()
        # print(f"client received:{result}")
        ws.close()
    if not result :
        print("DB에서 값을 못받아왔습니다. 패킷 확인하세요")
    else:
        json_data=json.loads(result)    
        dataframe_result = pd.DataFrame(list(json_data),columns=['timestamp','open','close','high','low','volume'])

    return dataframe_result

#시간봉 기준 시세 가져오기
def Get_HrPrc(market='upbit',str_date='0',end_date='99999999', srt_time = '00', end_time='24'):
    # print('market: '+market+' str_date: '+str_date+' end_date: '+end_date)
    # print('srt_time: '+srt_time+' end_time: '+end_time)
    
    ws = create_connection('ws://13.124.102.83:80/BackServer_Hr')
    order_packet = 'load'+'|'+market+'|'+str_date+'|'+end_date+'|'+srt_time+'|'+end_time
    # print(order_packet)
    if ws.connected:
        ws.send(order_packet)
        # print()
        result = ws.recv()
        # print(f"client received:{result}")
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
        
#     Prc_history = stoch(Prc_history)
#     print(Prc_history)
#임시
    # print('매수전략 시작')
    if buy_strategy =='':
        print("매수전략 없음")
    else :
        buy_result = Fet_Algo(Prc_history,buy_strategy,'buy',hourday_tp)
    
    if sell_strategy =='':
        print("매도전략 없음")
    else :
        sell_result = Fet_Algo(Prc_history,sell_strategy,'sell',hourday_tp)
    
    # print('매수리스트')
    # print(buy_result)
    # print('매도리스트')
    # print(sell_result)
    # print('최종리스트')
    buy_result.extend(sell_result)
    final_result=sorted(buy_result)
    # print(final_result)
    return final_result
    
    
if __name__ == '__main__':
    data = []
    result = []
    with open('Define_Algo_bb.json', 'r') as f:
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
    # 6번째 파라미터 = srt_time시작시간
    # 7번째 파라미터 = end_time종료시간
    # 8번째 파라미터 = hourday_tp 시간봉/일봉
    result = Parsing_Main(json_data,json_data,market,srt_date,end_date,srt_time,end_time,hourday_tp)
    
    


        
        



# import backtestAPI
