import yfinance as yf
import pandas as pd

fb = yf.Ticker("FB")
amzn = yf.Ticker("AMZN")
aapl = yf.Ticker("AAPL")
goog = yf.Ticker("GOOG")
tsla = yf.Ticker("TSLA")

fb_hist = fb.history(period='max').drop(columns=['Dividends', 'Stock Splits'])
amzn_hist = amzn.history(period='max').drop(columns=['Dividends', 'Stock Splits'])
aapl_hist = aapl.history(period='max').drop(columns=['Dividends', 'Stock Splits'])
goog_hist = goog.history(period='max').drop(columns=['Dividends', 'Stock Splits'])
tsla_hist = tsla.history(period='max').drop(columns=['Dividends', 'Stock Splits'])

fb_hist.to_csv('/home/garage/workspace/foreign_stock/facebook_1day.csv')
amzn_hist.to_csv('/home/garage/workspace/foreign_stock/amazon_1day.csv')
aapl_hist.to_csv('/home/garage/workspace/foreign_stock/apple_1day.csv')
goog_hist.to_csv('/home/garage/workspace/foreign_stock/google_1day.csv')
tsla_hist.to_csv('/home/garage/workspace/foreign_stock/tesla_1day.csv')