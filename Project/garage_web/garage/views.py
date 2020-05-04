from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
import numpy as np
import pandas as pd
# Create your views here.


def test(request):

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

    return render(request, 'garage/test.html', {'data': upbit_min['close'][-30:].tolist(),
                                                   'labels': upbit_min['timestamp'][-30:].tolist(),
                                                    'datas': data[-100:]})

def home(request):
    """
    index페이지 로드

    :param request:
    :return:
    """
    return render(request, 'garage/index.html', {})


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
            return redirect('/')
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


def algomaker(request):
    """
    알고리즘 제작(cocos) 페이지 로드
    :param request:
    return:
    """
    return render(request, 'garage/cocos_algo.html', {})


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
