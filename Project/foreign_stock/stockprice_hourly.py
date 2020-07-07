import yfinance as yf
import pandas as pd
from datetime import datetime

fb = yf.Ticker("FB")
amzn = yf.Ticker("AMZN")
aapl = yf.Ticker("AAPL")
goog = yf.Ticker("GOOG")
tsla = yf.Ticker("TSLA")

prev_facebook = pd.read_csv('/home/garage/workspace/foreign_stock/facebook_1hour.csv')
prev_apple = pd.read_csv('/home/garage/workspace/foreign_stock/apple_1hour.csv')
prev_amazon = pd.read_csv('/home/garage/workspace/foreign_stock/amazon_1hour.csv')
prev_google = pd.read_csv('/home/garage/workspace/foreign_stock/google_1hour.csv')
prev_tesla = pd.read_csv('/home/garage/workspace/foreign_stock/tesla_1hour.csv')

for i in range(len(prev_facebook)):
    prev_facebook['Datetime'][i] = pd.Timestamp(prev_facebook['Datetime'][i],tz='America/New_York')
for i in range(len(prev_apple)):
    prev_apple['Datetime'][i] = pd.Timestamp(prev_apple['Datetime'][i],tz='America/New_York')
for i in range(len(prev_amazon)):
    prev_amazon['Datetime'][i] = pd.Timestamp(prev_amazon['Datetime'][i],tz='America/New_York')
for i in range(len(prev_google)):
    prev_google['Datetime'][i] = pd.Timestamp(prev_google['Datetime'][i],tz='America/New_York')
for i in range(len(prev_tesla)):
    prev_tesla['Datetime'][i] = pd.Timestamp(prev_tesla['Datetime'][i],tz='America/New_York')

prev_facebook = prev_facebook.set_index('Datetime')
prev_apple = prev_apple.set_index('Datetime')
prev_amazon = prev_amazon.set_index('Datetime')
prev_google = prev_google.set_index('Datetime')
prev_tesla = prev_tesla.set_index('Datetime')
    
fb_hist = fb.history(period='1y', interval='60m' ).drop(columns=['Dividends', 'Stock Splits'])
amzn_hist = amzn.history(period='1y', interval='60m').drop(columns=['Dividends', 'Stock Splits'])
aapl_hist = aapl.history(period='1y', interval='60m').drop(columns=['Dividends', 'Stock Splits'])
goog_hist = goog.history(period='1y', interval='60m').drop(columns=['Dividends', 'Stock Splits'])
tsla_hist = tsla.history(period='1y', interval='60m').drop(columns=['Dividends', 'Stock Splits'])

fb_index = 0
for i in range(len(fb_hist.index)):
    if prev_facebook.index[-1] == fb_hist.index[i]:
        fb_index = i
        break
fb_hist = prev_facebook.append(fb_hist[fb_index-1::])

amzn_index = 0
for i in range(len(amzn_hist.index)):
    if prev_amazon.index[-1] == amzn_hist.index[i]:
        amzn_index = i
        break
amzn_hist = prev_amazon.append(amzn_hist[amzn_index-1::])

goog_index = 0
for i in range(len(goog_hist.index)):
    if prev_google.index[-1] == goog_hist.index[i]:
        goog_index = i
        break
goog_hist = prev_google.append(goog_hist[goog_index-1::])

tsla_index = 0
for i in range(len(tsla_hist.index)):
    if prev_tesla.index[-1] == tsla_hist.index[i]:
        tsla_index = i
        break
tsla_hist = prev_tesla.append(tsla_hist[tsla_index-1::])

aapl_index = 0
for i in range(len(aapl_hist.index)):
    if prev_apple.index[-1] == aapl_hist.index[i]:
        aapl_index = i
        break
aapl_hist = prev_apple.append(aapl_hist[aapl_index-1::])

fb_hist.to_csv('/home/garage/workspace/foreign_stock/facebook_1hour.csv')
amzn_hist.to_csv('/home/garage/workspace/foreign_stock/amazon_1hour.csv')
aapl_hist.to_csv('/home/garage/workspace/foreign_stock/apple_1hour.csv')
goog_hist.to_csv('/home/garage/workspace/foreign_stock/google_1hour.csv')
tsla_hist.to_csv('/home/garage/workspace/foreign_stock/tesla_1hour.csv')