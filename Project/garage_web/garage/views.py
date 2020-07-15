from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import datetime
import numpy as np
from backtestAPI import BacktestAPI
from websocket import create_connection
import ParsingJson
import timeit
import mysql.connector
import FetPrc
import json
import pandas as pd

@login_required
def test(request):
    backtestapi = BacktestAPI()

    ################################################################
    # 백테스트 수행 관련

    # my알고리즘 페이지에서 입력한 백테스트 조건 설정에서 GET 방식으로 보내준 조건 읽어서 사용

    # 백테스트 초기자본 셋팅
    money = request.GET.get('money')
    money = money.replace(',', '')
    init_krw_bal = int(money)

    # 백테스트 1회 거래량 셋팅
    order_quantity = float(request.GET.get('coin'))

    # 사용자의 이름과 요청한 알고리즘 이름 셋팅
    username = request.user.username
    algo_name = request.GET.get('algoname')

    # 세션에셔 읽어온 사용자 이름과 http get 에서 읽어온 알고리즘 이름을 바탕으로 미들웨어에 알고리즘 정보 요청
    ws = create_connection("ws://13.124.102.83/Cocos")
    ws.send("load|{}|{}".format(username, algo_name))

    # 미들웨어로 부터 받은 데이터 파싱
    json_data = ws.recv()
    json_data = eval(json_data)

    print("알고리즘정보---")
    print(json_data)

    # 매수 알고리즘이 없을경우 empty string으로 대체
    if json_data['items'][-1]['buy_algo'] is None:
        buy_algo = ''
    else:
        buy_algo = eval(json_data['items'][-1]['buy_algo'])

    # if no sell algorithm use empty string
    if json_data['items'][-1]['sell_algo'] is None:
        sell_algo = ''
    else:
        sell_algo = eval(json_data['items'][-1]['sell_algo'])

    # 백테스트 결과 페이지에 보여줄 알고리즘 실제 이름
    algo_realname = json_data['items'][-1]['algo_nm']

    # 알고리즘 설명
    algo_memo = json_data['items'][-1]['memo']

    # 서버 이상시 알고리즘을 파일로 부터 읽을수 있도록 만든 테스트 코드
    # with open('Define_Algo.json', 'r') as f:
    #     json_data1 = json.load(f)
    # with open('Define_Algo2.json', 'r') as f:
    #     json_data2 = json.load(f)

    json_data1 = buy_algo
    json_data2 = sell_algo

    # 파싱 보내기전 필요한 정보들 로드
    # 현재 알고리즘에 저장된 시작일, 종료일, 시간/일 봉 등의 정보보다 웹에서 설정한게 우선순위를 갖고있음
    try:
        market = json_data1['algo']['market']
    except:
        market = ''
    # hourday_tp = json_data1['algo']['hourday_tp']
    # srt_date = json_data1['algo']['srt_date']
    # end_date = json_data1['algo']['end_date']
    hourday_tp = request.GET.get('hourday')
    srt_date = request.GET.get('start').replace('-', '')
    end_date = request.GET.get('end').replace('-', '')
    try:
        srt_time = json_data1['algo']['srt_time']
        end_time = json_data1['algo']['end_time']
        bns_tp = json_data1['algo']['buysell']
    except:
        srt_time = ''
        end_time = ''
        bns_tp = ''

    target = request.GET.get('target')

    if target == 'upbit':
        market = 'upbit'
        stk_nm = ''
    else:
        market = 'fore'
        stk_nm = target


    # 파싱요청
    timer_start = timeit.default_timer()  # 시작시간 체크
    try:
        temp_result = ParsingJson.Parsing_Main(json_data1, json_data2, market, stk_nm, srt_date, end_date, srt_time, end_time,
                                           hourday_tp)
    except:
        print("something went wrong")
        temp_result = list()
    timer_end = timeit.default_timer()
    print("알고리즘 파싱 {}초 소요".format(timer_end - timer_start))

    # 매수/매도 동시에 뜨면 무시하는 로직
    result = []
    ind = 0
    while ind < len(temp_result):
        if ind < len(temp_result) - 1:
            if temp_result[ind][0] != temp_result[ind + 1][0]:
                result.append(temp_result[ind])
                ind = ind + 1
            else:
                ind = ind + 2
        else:
            result.append(temp_result[ind])
            ind = ind + 1

    # 그래프 표시를 위해 시간 데이터 요청
    if market == 'fore':
        if hourday_tp == 'day':
            bitcoin_dt = ParsingJson.Get_DtForeStkPrc(market, stk_nm, srt_date, end_date)
        else:
            bitcoin_dt = ParsingJson.Get_HrForeStkPrc(market, stk_nm, srt_date, end_date)
            bitcoin_dt['timestamp'] = bitcoin_dt[['timestamp', 'time']].apply(lambda x: 'T'.join(x), axis=1)
    else:

        if hourday_tp == 'day':  # 일봉일 경우
            bitcoin_dt = ParsingJson.Get_DtPrc(market, srt_date, end_date)
        else:  # 시간봉일 경우
            bitcoin_dt = ParsingJson.Get_HrPrc(market, srt_date, end_date, srt_time, end_time)
            bitcoin_dt['timestamp'] = bitcoin_dt[['timestamp', 'time']].apply(lambda x: 'T'.join(x), axis=1)

    if bitcoin_dt.empty:
        if market == 'fore':
            if hourday_tp == 'day':
                json_result = FetPrc.FetDtForeStkPrc(market, stk_nm, srt_date, end_date)
                json_data = json.loads(json_result)
                dataframe_result = pd.DataFrame(list(json_data),
                                                columns=['timestamp', 'open', 'close', 'high', 'low', 'volume'])
                bitcoin_dt = dataframe_result
            else:
                bitcoin_dt = FetPrc.FetHrForeStkPrc(market, stk_nm, srt_date, end_date)
                bitcoin_dt['timestamp'] = bitcoin_dt[['timestamp', 'time']].apply(lambda x: 'T'.join(x), axis=1)
        else:

            if hourday_tp == 'day':  # 일봉일 경우
                bitcoin_dt = FetPrc.FetDtPrc(market, srt_date, end_date)
            else:  # 시간봉일 경우
                bitcoin_dt = FetPrc.FetHrPrc(market, srt_date, end_date, srt_time, end_time)
                bitcoin_dt['timestamp'] = bitcoin_dt[['timestamp', 'time']].apply(lambda x: 'T'.join(x), axis=1)

    # 해외 주식일 경우 환율조회해서 적용
    if market == 'fore':
        mydb = mysql.connector.connect(
            host="root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com",
            user="root",
            password="koscom!234",
            database="garage_test"
        )

        mycursor = mydb.cursor()

        mycursor.execute("SELECT base_dt, exchange_rate from exchange_rate")

        myresult = mycursor.fetchall()

        exchange_rate = myresult[-1][1]
        if not bitcoin_dt.empty:
            bitcoin_dt['close'] *= exchange_rate
            bitcoin_dt['open'] *= exchange_rate
            bitcoin_dt['low'] *= exchange_rate
            bitcoin_dt['high'] *= exchange_rate

    # 거래 내역을 관리하기위한 변수
    trade_list = []
    final_balance = init_krw_bal
    final_increase = 0
    final_profit = 0
    krw_bal = 0
    btc_bal = 0
    avg_prc = 0

    # 백테스트 실행
    timer_start = timeit.default_timer()  # 시작시간 체크

    if not result:
        print("해당 조건에 충족하는 주문일이 없습니다.")
    else:
        date_list = np.array(result).T[0]
        type_list = np.array(result).T[1]
        trade_list, final_balance, final_increase, final_profit, krw_bal, btc_bal, avg_prc = backtestapi.execute_backtest(
            bitcoin_dt=bitcoin_dt, init_krw_bal=init_krw_bal, order_quantity=order_quantity, date_list=date_list,
            type_list=type_list, hourday=hourday_tp)
        final_increase = "%.2f" % final_increase
        final_profit = "%.2f" % final_profit

    timer_end = timeit.default_timer()  # 종료시간 체크
    print("백테스트 {}초 소요".format(timer_end - timer_start))
    ######################################################################
    # 차트 관련

    # 위에서 가져온 비트코인 시세를 그대로 사용
    upbit_min = bitcoin_dt

    # 일봉인지 시간봉인지에 맞추어 날짜 포맷 셋팅
    if hourday_tp == 'day':
        for i in range(len(upbit_min)):
            temp = datetime.strptime(upbit_min['timestamp'][i], "%Y%m%d")
            temp = temp.strftime("%Y-%m-%dT09:00:00")
            upbit_min['timestamp'][i] = temp
    else:
        for i in range(len(upbit_min)):
            temp = datetime.strptime(upbit_min['timestamp'][i], "%Y%m%dT%H:%M:%S")
            temp = temp.strftime("%Y-%m-%dT%H:%M:%S")
            upbit_min['timestamp'][i] = temp

    # 데이터 셋팅
    timestamps = upbit_min['timestamp']
    opens = upbit_min['open']
    closes = upbit_min['close']
    highs = upbit_min['high']
    lows = upbit_min['low']

    # html에 넘겨줄 리스트 선언
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

    # 리스트에 데이터 삽입
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

    # 그래프에 표시할 값 계산 후 천단위 콤마 삽입
    total_prof = final_balance - init_krw_bal  # 계좌 수익금(원)
    eval_prof = (int(closes[len(closes) - 1]) - avg_prc) * btc_bal  # 평가 수익금(원)
    real_prof = total_prof - eval_prof  # 실현 수익금(원)
    eval_prof = int(eval_prof)
    real_prof = int(real_prof)
    eval_prof = f"{eval_prof:,}"
    real_prof = f"{real_prof:,}"

    # 비트코인 잔고 환산(원)
    btc_exch = int(btc_bal * (int(closes[len(closes) - 1])))
    btc_exch = f"{btc_exch:,}"

    # 계좌 수익금(원)
    bal_diff = int(final_balance - init_krw_bal)
    bal_diff = f"{bal_diff:,}"

    # 원화 잔고(원)
    krw_bal = int(krw_bal)
    krw_bal = f"{krw_bal:,}"

    # 비트코인 평단(원)
    avg_prc = int(avg_prc)
    avg_prc = f"{avg_prc:,}"

    # 비트코인 현재가
    cur_prc = int(closes[len(closes) - 1])
    cur_prc = f"{cur_prc:,}"

    # 최종 잔고
    fin_bal = int(final_balance)
    fin_bal = f"{fin_bal:,}"

    # 초기 금액
    init_bal = int(init_krw_bal)
    init_bal = f"{init_bal:,}"
    #########################################################

    # 매수/매도 동시에 뜨면 무시하는 로직
    trade_temp = []
    ind = 0
    while ind < len(trade_list):
        if ind < len(trade_list) - 1:
            if trade_list[ind][0] != trade_list[ind + 1][0]:
                trade_temp.append(trade_list[ind])
                ind = ind + 1
            else:
                ind = ind + 2
        else:
            trade_temp.append(trade_list[ind])
            ind = ind + 1

    # 거래 횟수
    trade_num = len(trade_temp)

    # 매수/매도 횟수
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
                                                'init_bal': init_bal,  # 초기자본
                                                'fin_bal': fin_bal,  # 최종잔고
                                                'bal_diff': bal_diff,  # 계좌수익금
                                                'fin_prf': final_profit,  # 수익률
                                                'fin_inc': final_increase,  # 수익률
                                                'st_date': request.GET.get('start'),  # 시작날짜
                                                'end_date': request.GET.get('end'),  # 종료날짜
                                                'trade_num': trade_num,  # 거래횟수
                                                'krw_bal': krw_bal,  # 원화 잔고
                                                'btc_bal': btc_bal,  # 빗코 잔고
                                                'avg_prc': avg_prc,  # 빗코 평단가
                                                'cur_prc': cur_prc,  # 빗코 현재가
                                                'algoname': request.GET.get('algoname'),  # 알고리즘 실제이름
                                                'algoreal': algo_realname,  # 알고리즘 시퀀스넘버
                                                'signal': trade_list,  # 거래내역
                                                'buy_num': buy_num,  # 매수횟수
                                                'sell_num': sell_num,  # 매도 횟수
                                                'eval_prof': eval_prof,  # 평가 손익
                                                'real_prof': real_prof,  # 실현 손익
                                                'btc_exch': btc_exch,  # 빗코 환전
                                                'algo_memo': algo_memo  # 메모
                                                })


def home(request):
    """
    index페이지 로드

    :param request:
    :return:
    """

    # 유저 세션이 존재하지만 쿠키가 없을 경우 쿠키 새로 생성
    if request.user.is_authenticated:
        if request.COOKIES.get('username') is None:
            response = redirect('/')
            response.set_cookie('username', request.user.username)
            return response
        print(request.user.username)

    # 알고리즘 로드를 위한 쿠키가 아직 남아있을 경우 삭제
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

    # 알고리즘 로드를 위한 쿠키가 아직 남아있을경우 삭제
    if request.COOKIES.get('algo_seq') is not None:
        response = redirect('/mypage')
        print('cookie delete')
        response.delete_cookie('algo_seq')
        return response

    # 사용자 이름 세션에서 로드
    username = request.user.username

    # 미들웨어와 웹소켓 방식으로 연결
    ws = create_connection("ws://13.124.102.83:80/Cocos")

    # 해당사용자의 모든 알고리즘 조회 요청
    ws.send("load|{}|all".format(username))

    # 데이터 수신 및 파싱
    json_data = ws.recv()
    json_data = eval(json_data)

    # 알고리즘 정보를 위한 변수
    algo_names = []
    algo_dates = []
    algo_info = []
    algo_num = 0
    temp_name = ''
    # print(json_data['items'][-1]['algo_nm'])
    for i in json_data['items']:
        algo_names.append(i['algo_nm'])
        algo_dates.append(i['date_created'])
        temp = []
        temp.append(i['algo_nm'])
        temp.append(i['date_created'])
        temp.append(i['algo_seq'])
        try:
            temp.append(eval(i['buy_algo'])['algo']['hourday_tp'])
        except:
            temp.append("")
        try:
            temp.append(eval(i['buy_algo'])['algo']['srt_date'])
        except:
            temp.append("")
        try:
            temp.append(eval(i['buy_algo'])['algo']['end_date'])
        except:
            temp.append("")
        if i['memo'] == None:
            temp.append('-')
        else:
            temp.append(i['memo'])
        algo_info.append(temp)
    # print(algo_names)
    # print(algo_dates)
    # print(len(json_data['items']))
    realmoney = 0

    today = datetime.now().strftime("%Y-%m-%d")
    print(today)
    return render(request, 'garage/mypage.html', {'algo_names': algo_names,
                                                  'algo_dates': algo_dates,
                                                  'algo_info': algo_info,  # 알고리즘 정보
                                                  'algo_num': algo_num,
                                                  'name0': temp_name,
                                                  'realmoney': realmoney,
                                                  'today': today,
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
        # print(request.POST)
        remember = False
        if 'remember-me' not in request.POST:
            remember = False
        else:
            remember = True
        print(remember)
        # auth에 id 와 pw 전달하여 로그인 시도
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)

        # 로그인 성공시
        if user is not None:
            # 로그인 세션 생성
            auth.login(request, user)
            response = redirect('/')
            if remember:
                response.set_cookie('remember', 'true', max_age=86400 * 30)
                response.set_cookie('username', username, max_age=86400 * 30)
            else:
                response.set_cookie('username', username)
                response.delete_cookie('remember')
            # print("login as "+username)
            return response
        # 로그인 실패
        else:
            print("login fail")
            return render(request, 'garage/login.html', {'error': '아이디 혹은 비밀번호가 잘못 입력되었습니다.'})

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

        try:
            if request.POST["password1"] == request.POST["password2"]:
                # DB에 신규유저 추가
                user = User.objects.create_user(
                    username=request.POST["username"], password=request.POST["password1"], email=request.POST["email"])
                # 해당 유저로 로그인 처리
                auth.login(request, user)
                ws = create_connection("ws://13.124.102.83:80/JoinMem")
                ws.send("save|{}|{}".format(user.username, user.email))
                response = redirect('/algomaker')
                response.set_cookie('username', request.POST["username"])
                # print("login as "+username)
                return response
        except:
            return render(request, 'garage/signup.html', {'error': '이미 가입된 아이디 입니다. '})
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
    if 'remember' not in request.COOKIES:
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
                                                   'target':request.GET.get('target'),
                                                   })


def ready(request):
    return render(request, 'garage/ready.html', )
