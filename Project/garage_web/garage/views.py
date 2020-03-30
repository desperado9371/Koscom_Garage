from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from binance.client import Client
from datetime import datetime
import numpy as np
import pandas as pd
import sys
import ta

# Create your views here.
from sphinx.builders.html import return_codes_re


def post_list(request):
    return render(request, 'garage/index.html', {})


def algo(request):
    return render(request, 'garage/algo.html', {})


@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            print("login as "+username)
            return redirect('/')
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
    auth.logout(request)
    return redirect('/')



def backtest(request):
    # client = Client('ng0Zhq6ea42X3QxMV2RAubZxs508gguTISRwM13lQFFPrDDTxRiqmq3pBvIcvJMy',
    #                 'vHZDWuQvPf4mcaDvzxwRbtIWDbWuCyFyyG59bCZeTW6A6sd98qbHfCsFDVDdN3wn')
    # klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 month ago UTC")
    #
    #
    #
    # unix_timestamps = []
    # for kline in klines:
    #     unix_timestamps.append(kline[0])
    #
    # timestamps = []
    #
    # closed_prices = []
    # open_prices = []
    # high_prices = []
    # low_prices = []
    # volume = []
    # print(sys.path)
    # df = pd.DataFrame(list(zip(open_prices, closed_prices, high_prices, low_prices, volume)), index=timestamps,
    #                   columns=['open', 'close', 'high', 'low', 'volume'])
    #
    # for kline in klines:
    #     closed_prices.append(float(kline[4]))
    #     open_prices.append(float(kline[1]))
    #     high_prices.append(float(kline[2]))
    #     low_prices.append(float(kline[3]))
    #     volume.append(float(kline[5]))
    #
    # for unix_timestamp in unix_timestamps:
    #     timestamps.append(datetime.fromtimestamp(unix_timestamp / 1000).strftime("%m/%d/%Y"))
    #
    # for kline in klines:
    #     unix_timestamps.append(kline[0])
    #
    # candledata = []
    # for i in range(len(timestamps)):
    #     candledata.append([timestamps[i],low_prices[i],open_prices[i],closed_prices[i],high_prices[i]])
    #
    # print(candledata)

    upbit_min = pd.read_csv('upbit_krwbtc_1min.csv')

   # print( upbit_min['close'][-30:].tolist())

    return render(request, 'garage/bt_index.html', {'data': upbit_min['close'][-60:].tolist(),
                                                   'labels': upbit_min['timestamp'][-60:].tolist()})
