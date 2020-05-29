import Binance
import pandas as pd

prev = pd.read_csv('/home/garage/workspace/price_update_crontab/binance_btcusdt_1min.csv',
                   index_col=False)
last_timestamp = prev.iloc[-1][0]

binance = Binance.BinanceAPI()

df = binance.get_klines(interval='1M', term='1d')

new_df = pd.DataFrame()

index = 0 
for i in range(len(df)):
    if str(df.iloc[i]['timestamp']) == last_timestamp:
        index = i
        break

next_df = prev[:-1:].append(df[index:])
next_df.to_csv('/home/garage/workspace/price_update_crontab/binance_btcusdt_1min.csv',
              index = False)