from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from datetime import datetime
import numpy as np
import pandas as pd
import sys
import ta

# Create your views here.
#from sphinx.builders.html import return_codes_re


def post_list(request):
    return render(request, 'garage/index.html', {})


# def login_test(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = auth.authenticate(request, username=username, password=password)
#         if user is not None:
#             auth.login(request, user)
#             response = redirect('/')
#             response.set_cookie('username', username)
#             print("login as " + username)
#             return response
#         else:
#             print("login fail")
#             return render(request, 'garage/logintest.html', {'error': 'username or password is incorrect!'})
#     return render(request, 'garage/logintest.html', {})
#
#
# def signup_test(request):
#     if request.method == "POST":
#         if request.POST["password1"] == request.POST["password2"]:
#             user = User.objects.create_user(
#                 username=request.POST["username"], password=request.POST["password1"])
#             auth.login(request, user)
#             return redirect('/')
#         return render(request, 'garage/signuptest.html', {})
#     return render(request, 'garage/signuptest.html', {})



def algo(request):
    if request.COOKIES.get('username') is not None:
        print("cookie found!")
        print(request.COOKIES.get('username'))
    return render(request, 'garage/algo.html', {})


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            response = redirect('/')
            response.set_cookie('username', username)
            print("login as "+username)
            return response
        else:
            print("login fail")
            return render(request, 'garage/login.html', { 'error':'username or password is incorrect!'})
    return render(request, 'garage/login.html', {})


@csrf_exempt
def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(
                username=request.POST["username"], password=request.POST["password1"])
            auth.login(request, user)
            return redirect('/')
        return render(request, 'garage/signup.html', {})
    return render(request, 'garage/signup.html', {})


def logout(request):
    response = redirect('/')
    response.delete_cookie('username')
    auth.logout(request)
    return response


def algomaker(request):
    return render(request, 'garage/cocos_algo.html', {})


def backtest(request):

    upbit_min = pd.read_csv('upbit_krwbtc_1day.csv')

    # print( upbit_min['close'][-30:].tolist())

    return render(request, 'garage/backtest.html', {'data': upbit_min['close'][-30:].tolist(),
                                                   'labels': upbit_min['timestamp'][-30:].tolist()})


def send_order(market='upbit', order_type='buy', quantity=1, target_date="2018-10-11", krw_balance=0.0,
               btc_balance=0.0):
    bitcoin_dt = pd.read_csv('upbit_krwbtc_1day.csv')

    target_date = datetime.strptime(target_date, "%Y-%m-%d")

    price = -1

    for index, bitcoin in bitcoin_dt.iterrows():
        temp = datetime.strptime(bitcoin['timestamp'][:10], "%Y-%m-%d")
        if temp == target_date:
            price = float(bitcoin['close'])
            break;

    if order_type == 'buy':
        if (price * quantity) <= krw_balance:
            krw_balance = krw_balance - (price * quantity)
            btc_balance = btc_balance + quantity
            print("주문 성공 : 구매 -  btckrw:{} 수량:{} 원화잔고:{} 비트코인잔고:{}".
                  format(float(bitcoin['close']), quantity, krw_balance, btc_balance))
        else:
            print("주문실패 : 잔고부족")

    elif order_type == 'sell':
        if quantity <= btc_balance:
            krw_balance = krw_balance + (price * quantity)
            btc_balance = btc_balance - quantity
            print("주문 성공 : 판매 -  btckrw:{} 수량:{} 원화잔고:{} 비트코인잔고:{}".
                  format(float(bitcoin['close']), quantity, krw_balance, btc_balance))
        else:
            print("주문실패 : 잔고부족")

    return krw_balance, btc_balance
