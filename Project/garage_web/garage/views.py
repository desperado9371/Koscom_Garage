from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
import numpy as np
import pandas as pd
from backtestAPI import BacktestAPI
import asyncio
from websocket import create_connection

# Create your views here.


# async def my_connect():
#     async with websockets.connect("ws://52.79.241.205:80/Cocos") as websocket:
#         await websocket.send("load|test_user|all")
#         data_rcv = await websocket.recv()
#         return data_rcv

@login_required
def test(request):
    backtestapi = BacktestAPI()

    upbit_min = pd.read_csv('upbit_krwbtc_1day.csv')
    upbit_min = upbit_min[-150:]
    upbit_min.reset_index(drop=True, inplace=True)
    upbit_min = backtestapi.macd(upbit_min)
    upbit_min = backtestapi.rsi(upbit_min)
    upbit_min = backtestapi.obv(upbit_min)

    timestamps = upbit_min['timestamp']
    opens = upbit_min['open']
    closes = upbit_min['close']
    highs = upbit_min['high']
    lows = upbit_min['low']




    for i in range(len(timestamps)):
        timestamps[i] = timestamps[i][:10]

    data = list()
    tooltips = list()
    for i in range(len(timestamps)):
        if i % 3 == 0:
            tooltips.append('stroke-width: 5;' +
                            'stroke-color: #1800c8')
        if i % 3 == 1:
            tooltips.append('stroke-width: 5;' +
                           'stroke-color: #1800c8')
        if i % 2 == 0:
            tooltips.append('')

    for i in range(len(timestamps)):
        temp = list()
        year = timestamps[i][:4]
        month = timestamps[i][5:7]
        day = timestamps[i][8:10]
        temp.append(year)
        temp.append(month)
        temp.append(day)
        temp.append(timestamps[i][:10])
        temp.append(lows[i])
        temp.append(opens[i])
        temp.append(closes[i])
        temp.append(highs[i])
        #temp.append(tooltips[i])
        data.append(temp)
    # print( upbit_min['close'][-30:].tolist())


################################################################
    #백테스트 수행 관련

    init_krw_bal = 500000000
    order_quantity = 1
    final_balance = 0
    final_profit = 0

    result = []
    # with open('Define_Algo2.json', 'r') as f:
    #     json_data = json.load(f)

    # ws = create_connection("ws://52.79.241.205:80/Cocos")
    # ws.send("load|test_user|all")
    # json_data = ws.recv()
    # json_data = eval(json_data)
    # json_data = eval(json_data['items'][0]['buy_algo'])

    with open('Define_Algo.json', 'r') as f:
        json_data_b = json.load(f)
    with open('Define_Algo2.json', 'r') as f:
        json_data_s = json.load(f)

    # json_data = json_data_b
    # market = json_data['algo']['market']
    # str_date = json_data['algo']['srt_date']
    # end_date = json_data['algo']['end_date']
    # bns_tp = json_data['algo']['buysell']
    # Prc_history = Get_DtPrc(market,str_date,end_date)

    Prc_history = pd.read_csv('upbit_krwbtc_1day.csv')
    Prc_history = Prc_history[-150:]
    Prc_history.reset_index(drop=True, inplace=True)

    # 시세데이터 get
    #     df = get_price_data('upbit','1d')
    #     print(df)
    # df = Set_Indicator(df,json_data)

    # result= Fet_Algo(Prc_history,json_data,bns_tp,json_data)
    result = Parsing_Main(Prc_history, json_data_b, json_data_s)
    trade_list = []
    final_balance = init_krw_bal
    final_increase = 0
    final_profit = 0
    if not result:
        print("해당 조건에 충족하는 주문일이 없습니다.")
    else:
        date_list = np.array(result).T[0]
        type_list = np.array(result).T[1]
        trade_list, final_balance, final_increase, final_profit = backtestapi.execute_backtest(init_krw_bal=init_krw_bal, order_quantity=order_quantity, date_list=date_list, type_list=type_list)
        final_increase = "%.2f" % final_increase
        final_profit = "%.2f" % final_profit

    bal_diff = int(final_balance-init_krw_bal)
    bal_diff = str(bal_diff)
    if len(bal_diff) > 6:
        if len(bal_diff)== 7 and bal_diff[0] == '-':
            bal_diff = bal_diff[0:-3] + ',' + bal_diff[-3:]
        else:
            bal_diff = bal_diff[0:-6]+','+bal_diff[-6:-3]+','+bal_diff[-3:]
    else:
        bal_diff = bal_diff[0:-3] + ',' + bal_diff[-3:]
#########################################################


    # date_list = ['2019-01-11', '2019-02-11', '2019-02-20', '2019-06-11', '2019-07-11', '2019-07-20']
    # type_list = ['buy', 'buy', 'buy', 'sell', 'sell', 'sell']
    # wl_list = ['', '', '', 'win', 'lose', 'win']
    # daily_prof_list = ['0.1%', '0.3%', '1.0%', '0.5%', '0.6%', '1.2%']
    # accum_prof_list = ['1.1%', '2.1%', '2.0%', '1.1%', '2.2%', '3.3%']
    # balance_list = ['12345', '12346', '12345', '12344', '12346', '12347']
    # trade_list = []
    #
    # for i in range(len(date_list)):
    #     tmp = []
    #     tmp.append(date_list[i])
    #     tmp.append(type_list[i])
    #     tmp.append(wl_list[i])
    #     tmp.append(daily_prof_list[i])
    #     tmp.append(accum_prof_list[i])
    #     tmp.append(balance_list[i])
    #     trade_list.append(tmp)
    # print(trade_list)

    start_date = Prc_history['timestamp'][0][:10]
    end_date = Prc_history['timestamp'][len(Prc_history)-1][:10]
    trade_num = len(trade_list)

    return render(request, 'garage/test.html', {'data': upbit_min['close'][-30:].tolist(),
                                                'labels': upbit_min['timestamp'][-30:].tolist(),
                                                'trades': trade_list,
                                                'datas': data,
                                                'init_bal': init_krw_bal,
                                                'fin_bal': int(final_balance),
                                                'bal_diff': bal_diff,
                                                'fin_prf': final_profit,
                                                'fin_inc': final_increase,
                                                'st_date': start_date,
                                                'end_date': end_date,
                                                'trade_num': trade_num})

def home(request):
    """
    index페이지 로드

    :param request:
    :return:
    """
    return render(request, 'garage/index.html', {})


def mypage(request):


    return render(request, 'garage/mypage.html',{})

@csrf_exempt
def login(request):
    """
    로그인 페이지 로드
    :paramrequest:
    :return:
    """

    # post요청이 있을시 로그인 체크
    if request.method == "POST":
        # auth에 id 와 pw 전달하여 로그인 시도
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)

        # 로그인 성공시
        if user is not None:
            # 로그인 세션 생성
            auth.login(request, user)
            response = redirect('/')
            response.set_cookie('username', username)
            # print("login as "+username)
            return response
        # 로그인 실패
        else:
            print("login fail")
            return render(request, 'garage/login.html', { 'error':'username or password is incorrect!'})

    # 첫 로드시 바로 페이지 반환
    return render(request, 'garage/login.html', {})


@csrf_exempt
def signup(request):
    """
    회원가입 페이지 로드
    :param request:
    :return:
    """
    # post 요청이 있을 시
    if request.method == "POST":
        # 입력한 두개의 패스워드가 같으면
        if request.POST["password1"] == request.POST["password2"]:
            # DB에 신규유저 추가
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            # 해당 유저로 로그인 처리
            auth.login(request, user)
            response = redirect('/')
            response.set_cookie('username', request.POST["username"])
            # print("login as "+username)
            return response
        return render(request, 'garage/signup.html', {})

    # 첫 로드시 바로 페이지 반환
    return render(request, 'garage/signup.html', {})


def logout(request):
    """
    로그아웃 후 메인페이지로 복귀
    :param request:
    :return:
    """
    # 쿠키 삭제 및 세션 종료 후 메인페이지로 복귀
    response = redirect('/')
    response.delete_cookie('username')
    auth.logout(request)
    return response

@login_required
def algomaker(request):
    """
    알고리즘 제작(cocos) 페이지 로드
    :param request:
    return:
    """
    username = ""
    if request.COOKIES.get('username') is not None:
        print("cookie found!")
        print(request.COOKIES.get('username'))
        username = request.COOKIES.get('username')
    return render(request, 'garage/cocos_algo.html', {'username': username})


def loading(request):
    check = 1;
    return render(request, 'garage/loading.html',{'check': check})


def charttest(request):
    upbit_min = pd.read_csv('upbit_krwbtc_1day.csv')
    backtestapi = BacktestAPI()
    upbit_min = backtestapi.macd(upbit_min)
    upbit_min = backtestapi.rsi(upbit_min)
    upbit_min = upbit_min[-400:]
    upbit_min.reset_index(drop=True, inplace=True)

    timestamps = upbit_min['timestamp']
    closes = upbit_min['close']
    macds = upbit_min['macd']
    rsis = upbit_min['rsi']

    for i in range(len(timestamps)):
        timestamps[i] = timestamps[i][:10]

    data = list()

    for i in range(len(timestamps)):
        temp=[]
        year = timestamps[i][:4]
        month = timestamps[i][5:7]
        day = timestamps[i][8:10]
        temp.append(year)
        temp.append(month)
        temp.append(day)
        temp.append(closes[i])
        if i % 3 == 0:
            temp.append("buy")
        else:
            temp.append("null")
        # temp.append(macds[i])
        # temp.append(rsis[i])
        data.append(temp)


    return render(request, 'garage/chart_test.html', {'data':data})

def backtest(request):

    upbit_min = pd.read_csv('upbit_krwbtc_1day.csv')

    timestamps = upbit_min['timestamp']
    opens = upbit_min['open']
    closes = upbit_min['close']
    highs = upbit_min['high']
    lows = upbit_min['low']

    for i in range(len(timestamps)):
        timestamps[i] = timestamps[i][:10]

    data = list()
    temp = list()
    tooltips = list()
    for i in range(len(timestamps)):
        if i % 3 == 0:
            tooltips.append('stroke-width: 5;' +
                            'stroke-color: #1800c8')
        if i % 3 == 1:
            tooltips.append('stroke-width: 5;' +
                           'stroke-color: #1800c8')
        if i % 2 == 0:
            tooltips.append('')

    for i in range(len(timestamps)):
        temp.append(timestamps[i])
        temp.append(lows[i])
        temp.append(opens[i])
        temp.append(closes[i])
        temp.append(highs[i])
        #temp.append(tooltips[i])
        data.append(temp)
        temp = list()
    print( data[:4])
    # print( upbit_min['close'][-30:].tolist())

    return render(request, 'garage/backtest.html', {'data': upbit_min['close'][-30:].tolist(),
                                                   'labels': upbit_min['timestamp'][-30:].tolist(),
                                                    'datas': data[-100:]})


import asyncio
# from websocket import create_connection
import math
import json
import pandas as pd
from datetime import datetime
import ta
import socket
import numpy as np
from backtestAPI import BacktestAPI


class Algo_Info:
    str_date = ""
    end_date = ""
    bns_tp = ""
    name = []


class block:
    condition_min = ""
    condition_max = ""
    total_count = ""


# 지표값을 호출해서 리스트에 추가함
def Make_indicat(indi, prc_lst):
    if indi['name'] == 'macd':
        prc_lst = macd(prc_lst,
                       int(indi['val']['n_slow']),
                       int(indi['val']['n_fast']),
                       int(indi['val']['n_sign']))
    elif indi['name'] == 'obv':
        prc_lst = obv(prc_lst)
    elif indi['name'] == 'rsi':
        prc_lst = rsi(prc_lst, int(indi['val']['period']))
    elif indi['name'] == 'bollinger_band':
        prc_lst = bollinger_band(prc_lst,
                                 int(indi['val']['period']),
                                 int(indi['val']['ndev']))

    return prc_lst


def get_price_data(market='upbit', time_delta='1d'):
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
def Chk_Meet_Condition(Prc_history, group_algo, row, meet_condtion):
    # print("Chk_Meet_Condition 시작:")
    # print(str(Prc_history[group_algo[0]['name']][row]) + str(Prc_history[group_algo[2]['name']][row]))
    meet_condtion = int(meet_condtion)
    # (case1 지표끼리 비교시)
    if group_algo[0]['name'] != 'num' and group_algo[2]['name'] != 'num':
        if math.isnan(Prc_history[group_algo[0]['name']][row]) != True and math.isnan(
                Prc_history[group_algo[2]['name']][row]) != True:
            # print('case1 지표끼리 비교시')
            chk = str(Prc_history[group_algo[0]['name']][row]) + str(group_algo[1]['val']) + str(
                Prc_history[group_algo[2]['name']][row])
            # print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    elif group_algo[0]['name'] != 'num' and group_algo[2]['name'] == 'num':
        # print('case2 지표랑 뒷부분의 상수랑 비교시')
        # (case2 지표랑 뒷부분의 상수랑 비교시)
        if math.isnan(Prc_history[group_algo[0]['name']][row]) != True and math.isnan(
                int(group_algo[2]['val'])) != True:
            chk = str(Prc_history[group_algo[0]['name']][row]) + str(group_algo[1]['val']) + str(group_algo[2]['val'])
            # print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    elif group_algo[0]['name'] == 'num' and group_algo[2]['name'] != 'num':
        # print('case3 앞의 상수랑 뒷부분의 지표랑 비교시')
        # (case3 앞의 상수랑 뒷부분의 지표랑 비교시)
        if math.isnan(int(group_algo[0]['val'])) != True and math.isnan(
                Prc_history[group_algo[2]['name']][row]) != True:
            chk = str(group_algo[0]['val']) + str(group_algo[1]['val']) + str(Prc_history[group_algo[2]['name']][row])
            # print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    return meet_condtion


#  ----- Fet 함수
#  ----- 하루하루씩 알고리즘에 대입해서 충족하는지 확인함 확인후 모든 block 이 충족될경우 일자를 저장해서 리턴
def Fet_Algo(Prc_history, algo, bns_tp):
    result_datelist = []
    # for row in range(60, 70):
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
                        group_meet_condtion = Chk_Meet_Condition(Prc_history, algo['algo'][pars][search_group], row,
                                                                 group_meet_condtion)

                # print("순회 완료 Min: " + str(algo['algo'][pars]['min']) + " Mix: " + str(algo['algo'][pars]['max']))
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
            result_datelist.append([Prc_history['timestamp'][row][0:10], bns_tp])  # 일자에서 시간부분 잘라내기위해 [0:10] 적용

    # print(result_datelist)
    return result_datelist


def Get_DtPrc(market='upbit', str_date='0', end_date='99999999'):
    # print('market: ' + market + ' str_date: ' + str_date + ' end_date: ' + end_date)

    ws = create_connection('ws://52.79.241.205:80/BackServer')
    order_packet = 'load' + '|' + market + '|' + str_date + '|' + end_date
    # print(order_packet)
    if ws.connected:
        ws.send(order_packet)
        # print()
        result = ws.recv()
        # print(f"client received:{result}")
        ws.close()
    if not result:
        print("DB에서 값을 못받아왔습니다. 패킷 확인하세요")
    else:
        json_data = json.loads(result)
        dataframe_result = pd.DataFrame(list(json_data),
                                        columns=['timestamp', 'open', 'close', 'high', 'low', 'volume'])

    return dataframe_result


def Parsing_Main(Prc_history, buy_strategy='', sell_strategy=''):
    buy_result = []
    sell_result = []
    final_result = []
    # print('매수전략 시작')
    if buy_strategy == '':
        print("매수전략 없음")
    else:
        buy_result = Fet_Algo(Prc_history, buy_strategy, 'buy')

    if sell_strategy == '':
        print("매도전략 없음")
    else:
        sell_result = Fet_Algo(Prc_history, sell_strategy, 'sell')

    # print('매수리스트')
    # print(buy_result)
    # print('매도리스트')
    # print(sell_result)
    # print('최종리스트')
    buy_result.extend(sell_result)
    final_result = sorted(buy_result)
    # print(final_result)
    return final_result


