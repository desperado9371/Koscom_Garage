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
import json
from backtestAPI import BacktestAPI
import asyncio
from websocket import create_connection
import ParsingJson

# Create your views here.

# async def my_connect():
#     async with websockets.connect("ws://52.79.241.205:80/Cocos") as websocket:
#         await websocket.send("load|test_user|all")
#         data_rcv = await websocket.recv()
#         return data_rcv

@login_required
def test(request):
    backtestapi = BacktestAPI()

################################################################
    # 백테스트 수행 관련

    init_krw_bal = 500000000
    order_quantity = 0.25
    final_balance = 0
    final_profit = 0

    result = []
    with open('Define_Algo.json', 'r') as f:
        json_data1 = json.load(f)
    with open('Define_Algo2.json', 'r') as f:
        json_data2 = json.load(f)

    # username = request.COOKIES.get('username')
    # ws = create_connection("ws://52.79.241.205:80/Cocos")
    # ws.send("load|{}|all".format(username))
    # json_data = ws.recv()
    # json_data = eval(json_data)
    # print("session: {}".format(request.user))
    # print("cookies: {}".format(username))
    # if json_data['items'][-1]['buy_algo'] == None:
    #     json_data1 = ''
    # else:
    #     json_data1 = eval(json_data['items'][-1]['buy_algo'])
    # if json_data['items'][-1]['sell_algo'] == None:
    #     json_data2 = ''
    # else:
    #     json_data2 = eval(json_data['items'][-1]['sell_algo'])
    print(json_data1)
    print(json_data2)

    market = json_data1['algo']['market']
    hourday_tp = json_data1['algo']['hourday']
    srt_date = json_data1['algo']['srt_date']
    end_date = json_data1['algo']['end_date']
    srt_time = json_data1['algo']['srt_time']
    end_time = json_data1['algo']['end_time']
    bns_tp = json_data1['algo']['buysell']

    Prc_history = pd.read_csv('upbit_krwbtc_1day.csv')
    Prc_history = Prc_history[-150:]
    Prc_history.reset_index(drop=True, inplace=True)

    # 시세데이터 get
    #     df = get_price_data('upbit','1d')
    #     print(df)
    # df = Set_Indicator(df,json_data)

    # result= Fet_Algo(Prc_history,json_data,bns_tp,json_data)
    result = ParsingJson.Parsing_Main(json_data1, json_data2, market, srt_date, end_date, srt_time, end_time, hourday_tp)
    if hourday_tp == 'day':  # 일봉일 경우
        bitcoin_dt = ParsingJson.Get_DtPrc(market, srt_date, end_date)
    else:  # 시간봉일 경우
        bitcoin_dt = ParsingJson.Get_HrPrc(market, srt_date, end_date, srt_time, end_time)
        bitcoin_dt['timestamp'] = bitcoin_dt[['timestamp', 'time']].apply(lambda x: 'T'.join(x), axis=1)

    trade_list = []
    final_balance = init_krw_bal
    final_increase = 0
    final_profit = 0
    krw_bal = 0;
    btc_bal = 0;
    avg_prc = 0;
    if not result:
        print("해당 조건에 충족하는 주문일이 없습니다.")
    else:
        date_list = np.array(result).T[0]
        type_list = np.array(result).T[1]
        trade_list, final_balance, final_increase, final_profit, krw_bal, btc_bal, avg_prc = backtestapi.execute_backtest(
            bitcoin_dt=bitcoin_dt, init_krw_bal=init_krw_bal, order_quantity=order_quantity, date_list=date_list, type_list=type_list, hourday=hourday_tp)
        final_increase = "%.2f" % final_increase
        final_profit = "%.2f" % final_profit
######################################################################

    if hourday_tp == 'day':
        upbit_min = pd.read_csv('upbit_krwbtc_1day.csv')
    else:
        upbit_min = pd.read_csv('upbit_krwbtc_1hr.csv')
    upbit_min.reset_index(drop=True, inplace=True)
    upbit_min = backtestapi.macd(upbit_min)
    upbit_min = backtestapi.rsi(upbit_min)
    upbit_min = backtestapi.obv(upbit_min)

    timestamps = upbit_min['timestamp']
    opens = upbit_min['open']
    closes = upbit_min['close']
    highs = upbit_min['high']
    lows = upbit_min['low']

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
        temp.append(timestamps[i])
        temp.append(lows[i])
        temp.append(opens[i])
        temp.append(closes[i])
        temp.append(highs[i])
        if hourday_tp == 'day':
            temp.append(timestamps[i][:10])
        else:
            temp.append(timestamps[i])
        # temp.append(tooltips[i])
        data.append(temp)
    # print( upbit_min['close'][-30:].tolist())


    bal_diff = int(final_balance-init_krw_bal)
    bal_diff = str(bal_diff)
    if len(bal_diff) > 6:
        if len(bal_diff) == 7 and bal_diff[0] == '-':
            bal_diff = bal_diff[0:-3] + ',' + bal_diff[-3:]
        else:
            bal_diff = bal_diff[0:-6]+','+bal_diff[-6:-3]+','+bal_diff[-3:]
    else:
        bal_diff = bal_diff[0:-3] + ',' + bal_diff[-3:]

    krw_bal = int(krw_bal)
    krw_bal = str(krw_bal)
    if len(krw_bal) > 6:
        krw_bal = krw_bal[0:-6]+','+krw_bal[-6:-3] + ',' + krw_bal[-3:]
    elif len(krw_bal) > 3:
        krw_bal = krw_bal[0:-3] + ',' + krw_bal[-3:]

    avg_prc = int(avg_prc)
    avg_prc = str(avg_prc)
    if len(avg_prc) > 6:
        avg_prc = avg_prc[0:-6] + ',' + avg_prc[-6:-3] + ',' + avg_prc[-3:]
    elif len(avg_prc) > 3:
        avg_prc = avg_prc[0:-3] + ',' + avg_prc[-3:]

    cur_prc = int(closes[len(closes)-1])
    cur_prc = str(cur_prc)
    if len(cur_prc) > 6:
        cur_prc = cur_prc[0:-6] + ',' + cur_prc[-6:-3] + ',' + cur_prc[-3:]
    elif len(cur_prc) > 3:
        cur_prc = cur_prc[0:-3] + ',' + cur_prc[-3:]

    fin_bal = int(final_balance)
    fin_bal = str(fin_bal)
    if len(fin_bal) > 6:
        fin_bal = fin_bal[0:-6] + ',' + fin_bal[-6:-3] + ',' + fin_bal[-3:]
    elif len(fin_bal) > 3:
        fin_bal = fin_bal[0:-3] + ',' + fin_bal[-3:]

    init_bal = int(init_krw_bal)
    init_bal = str(init_bal)
    if len(init_bal) > 6:
        init_bal = init_bal[0:-6] + ',' + init_bal[-6:-3] + ',' + init_bal[-3:]
    elif len(init_bal) > 3:
        init_bal = init_bal[0:-3] + ',' + init_bal[-3:]
#########################################################






    start_date = srt_date
    end_date = end_date
    trade_num = len(trade_list)

    return render(request, 'garage/test.html', {'data': upbit_min['close'][-30:].tolist(),
                                                'labels': upbit_min['timestamp'][-30:].tolist(),
                                                'trades': trade_list,
                                                'datas': data,
                                                'init_bal': init_bal,
                                                'fin_bal': fin_bal,
                                                'bal_diff': bal_diff,
                                                'fin_prf': final_profit,
                                                'fin_inc': final_increase,
                                                'st_date': start_date,
                                                'end_date': end_date,
                                                'trade_num': trade_num,
                                                'krw_bal': krw_bal,
                                                'btc_bal': btc_bal,
                                                'avg_prc': avg_prc,
                                                'cur_prc': cur_prc})

def home(request):
    """
    index페이지 로드

    :param request:
    :return:
    """
    return render(request, 'garage/index.html', {})

def intro(request):
    """
    intro페이지 로드

    :param request:
    :return:
    """
    return render(request, 'garage/intro.html', {})

def mypage(request):
    username = request.COOKIES.get('username')
    ws = create_connection("ws://13.124.102.83:80/Cocos")
    ws.send("load|{}|all".format(username))
    json_data = ws.recv()
    json_data = eval(json_data)

    #print(json_data['items'][-1]['algo_nm'])
    for i in json_data['items']:
        print(i['algo_nm'])

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
                username=request.POST["username"], password=request.POST["password1"], email=request.POST["email"])
            # 해당 유저로 로그인 처리
            auth.login(request, user)
            ws = create_connection("ws://13.124.102.83:80/JoinMem")
            ws.send("save|{}|{}".format(user.username, user.email))
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

