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

@login_required
def test(request):
    backtestapi = BacktestAPI()

################################################################
    # 백테스트 수행 관련

    # my알고리즘 페이지에서 입력한 백테스트 조건 설정에서 GET방식으로 보내준 조건 읽어서 사용
    money = request.GET.get('money')
    money = money.replace(',','')
    init_krw_bal =int(money)
    order_quantity = float(request.GET.get('coin'))
    final_balance = 0
    final_profit = 0
    result = []
    username = request.user.username
    algo_name = request.GET.get('algoname')

    # 세션에셔 읽어온 사용자 이름과 http get 에서 읽어온 알고리즘 이름을 바탕으로 미들웨어에 알고리즘 정보 요청
    ws = create_connection("ws://13.124.102.83/Cocos")
    ws.send("load|{}|{}".format(username, algo_name))

    # 미들웨어로 부터 받은 데이터 파싱
    json_data = ws.recv()
    json_data = eval(json_data)

    # 매수 알고리즘이 없을경우 empty string으로 대체
    if json_data['items'][-1]['buy_algo'] == None:
        buy_algo = ''
    else:
        buy_algo = eval(json_data['items'][-1]['buy_algo'])

    # if no sell algorithm use empty string
    if json_data['items'][-1]['sell_algo'] == None:
        sell_algo = ''
    else:
        sell_algo = eval(json_data['items'][-1]['sell_algo'])

    # 백테스트 결과 페이지에 보여줄 알고리즘 실제 이름
    algo_realname = json_data['items'][-1]['algo_nm']

    # 서버 이상시 알고리즘을 파일로 부터 읽을수 있도록 만든 테스트 코드
    # with open('Define_Algo.json', 'r') as f:
    #     json_data1 = json.load(f)
    # with open('Define_Algo2.json', 'r') as f:
    #     json_data2 = json.load(f)

    json_data1 = buy_algo
    json_data2 = sell_algo

    # 파싱 보내기전 필요한 정보들 로드
    # 현재 알고리즘에 저장된 시작일, 종료일, 시간/일 봉 등의 정보보다 웹에서 설정한게 우선순위를 갖고있음
    market = json_data1['algo']['market']
    hourday_tp = json_data1['algo']['hourday_tp']
    hourday_tp = request.GET.get('hourday')
    srt_date = json_data1['algo']['srt_date']
    end_date = json_data1['algo']['end_date']
    srt_date = request.GET.get('start').replace('-', '')
    end_date = request.GET.get('end').replace('-', '')
    srt_time = json_data1['algo']['srt_time']
    end_time = json_data1['algo']['end_time']
    bns_tp = json_data1['algo']['buysell']

    # 파싱요청
    result = ParsingJson.Parsing_Main(json_data1, json_data2, market, srt_date, end_date, srt_time, end_time, hourday_tp)

    # 그래프 표시를 위해 시가 데이터 요청
    if hourday_tp == 'day':  # 일봉일 경우
        bitcoin_dt = ParsingJson.Get_DtPrc(market, srt_date, end_date)
    else:  # 시간봉일 경우
        bitcoin_dt = ParsingJson.Get_HrPrc(market, srt_date, end_date, srt_time, end_time)
        bitcoin_dt['timestamp'] = bitcoin_dt[['timestamp', 'time']].apply(lambda x: 'T'.join(x), axis=1)

    # 거래 내역을 관리하기위한 변수
    trade_list = []
    final_balance = init_krw_bal
    final_increase = 0
    final_profit = 0
    krw_bal = 0
    btc_bal = 0
    avg_prc = 0

    # ttt = pd.DataFrame(result)
    # ttt.to_csv(algo_name+"tradelist.csv")

    # 백테스트 실행
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
# 차트 관련
    upbit_min = bitcoin_dt

    if hourday_tp == 'day':
        for i in range(len(upbit_min)):
            temp = datetime.strptime(upbit_min['timestamp'][i],"%Y%m%d")
            temp = temp.strftime("%Y-%m-%dT09:00:00")
            upbit_min['timestamp'][i] = temp
    else:
        for i in range(len(upbit_min)):
            temp = datetime.strptime(upbit_min['timestamp'][i],"%Y%m%dT%H:%M:%S")
            temp = temp.strftime("%Y-%m-%dT%H:%M:%S")
            upbit_min['timestamp'][i] = temp

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

    total_prof = final_balance-init_krw_bal
    eval_prof = (int(closes[len(closes)-1]) - avg_prc) * btc_bal
    real_prof = total_prof - eval_prof

    eval_prof = int(eval_prof)
    real_prof = int(real_prof)

    btc_exch = int(btc_bal * (int(closes[len(closes)-1])))
    btc_exch = f"{btc_exch:,}"

    eval_prof = f"{eval_prof:,}"
    real_prof = f"{real_prof:,}"

    bal_diff = int(final_balance-init_krw_bal)
    bal_diff = f"{bal_diff:,}"

    krw_bal = int(krw_bal)
    krw_bal = f"{krw_bal:,}"

    avg_prc = int(avg_prc)
    avg_prc = f"{avg_prc:,}"

    cur_prc = int(closes[len(closes)-1])
    cur_prc = f"{cur_prc:,}"

    fin_bal = int(final_balance)
    fin_bal = f"{fin_bal:,}"

    init_bal = int(init_krw_bal)
    init_bal = f"{init_bal:,}"
#########################################################

    start_date = srt_date
    end_date = end_date

    trade_temp = []

    ind = 0

    while ind < len(trade_list):
        if ind < len(trade_list) - 1:
            if trade_list[ind][0] != trade_list[ind+1][0]:
                trade_temp.append(trade_list[ind])
                ind = ind + 1
            else:
                ind = ind + 2
        else:
            trade_temp.append(trade_list[ind])
            ind = ind + 1

    trade_num = len(trade_temp)

    buy_num = 0
    sell_num = 0

    for i in trade_temp:
        if i[1] == 'buy':
            buy_num = buy_num + 1
        else:
            sell_num = sell_num + 1




    return render(request, 'garage/test.html', {'data': upbit_min['close'][-30:].tolist(),
                                                'labels': upbit_min['timestamp'][-30:].tolist(),
                                                'trades': trade_temp,
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
                                                'cur_prc': cur_prc,
                                                'algoname': request.GET.get('algoname'),
                                                'algoreal': algo_realname,
                                                'signal': trade_list,
                                                'buy_num': buy_num,
                                                'sell_num': sell_num,
                                                'eval_prof': eval_prof,
                                                'real_prof': real_prof,
                                                'btc_exch': btc_exch,
                                                })


def home(request):
    """
    index페이지 로드

    :param request:
    :return:
    """
    if request.user.is_authenticated:
        if request.COOKIES.get('username') is None:
            response = redirect('/')
            response.set_cookie('username', request.user.username)
            return response
        print(request.user.username)

    if request.COOKIES.get('algo_seq') is not None:
        response = redirect('/')
        print('cookie delete')
        response.delete_cookie('algo_seq')
        return response

    return render(request, 'garage/index.html', {})


def intro(request):
    """
    intro페이지 로드

    :param request:
    :return:
    """
    return render(request, 'garage/intro.html', {})


@login_required
def mypage(request):
    # username = request.COOKIES.get('username')

    if request.COOKIES.get('algo_seq') is not None:
        response = redirect('/mypage')
        print('cookie delete')
        response.delete_cookie('algo_seq')
        return response


    username = request.user.username
    ws = create_connection("ws://13.124.102.83:80/Cocos")
    ws.send("load|{}|all".format(username))
    json_data = ws.recv()
    json_data = eval(json_data)

    algo_names = []
    algo_dates = []
    algo_info = []
    algo_num = 0
    temp_name =''
    #print(json_data['items'][-1]['algo_nm'])
    for i in json_data['items']:
        algo_names.append(i['algo_nm'])
        algo_dates.append(i['date_created'])
        temp = []
        temp.append(i['algo_nm'])
        temp.append(i['date_created'])
        temp.append(i['algo_seq'])
        temp.append(eval(i['buy_algo'])['algo']['hourday_tp'])
        temp.append(eval(i['buy_algo'])['algo']['srt_date'])
        temp.append(eval(i['buy_algo'])['algo']['end_date'])
        algo_info.append(temp)
    # print(algo_names)
    # print(algo_dates)
    # print(len(json_data['items']))
    temp_name = algo_names[0]
    realmoney = 0
    return render(request, 'garage/mypage.html',{'algo_names': algo_names,
                                                 'algo_dates': algo_dates,
                                                 'algo_info': algo_info,
                                                 'algo_num': algo_num,
                                                 'name0': temp_name,
                                                 'realmoney': realmoney,
                                                 })


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
    response.delete_cookie('algo_seq')
    auth.logout(request)
    return response


@login_required
def algomaker(request):
    """
    알고리즘 제작(cocos) 페이지 로드
    :param request:
    return:
    """

    if request.COOKIES.get('username') == None:
        response = redirect('/algomaker')
        response.set_cookie('username', request.user.username)
        return response

    response = redirect('/algomaker')

    if request.META['HTTP_REFERER'][-7:] != 'mypage/' and request.COOKIES.get('algo_seq') is not None:
        print('cookie delete')
        response.delete_cookie('algo_seq')
        return response

    return render(request, 'garage/cocos_algo.html', )


@login_required
def loading(request):
    check = 1
    return render(request, 'garage/loading.html', {'check': check,
                                                   'algoname': request.GET.get('algoname'),
                                                   'start': request.GET.get('start'),
                                                   'end': request.GET.get('end'),
                                                   'money': request.GET.get('money'),
                                                   'coin': request.GET.get('coin'),
                                                   'hourday': request.GET.get('hourday'),
                                                  })


def ready(request):
    return render(request,'garage/ready.html',)
