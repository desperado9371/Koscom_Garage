#!/usr/bin/env python
# coding: utf-8

# In[1]:


import glob
import pandas as pd
import mysql.connector as sql


# In[2]:


df = pd.read_csv("/home/garage/workspace/price_update_crontab/binance_btcusdt_1day.csv")


# In[3]:


df = df.tail(1)
print(df)


# In[4]:


#db_connection = sql.connect(host='localhost', database='garage_test', user='garage', password='koscom!234')
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[5]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['timestamp']).replace("-","")
    tmp = tmp.split(' ')
    base_dt = tmp[0]
    
    coin_type = 'krwbtc'
    base_time = tmp[1]
    open_price = df.iloc[i]['open']
    close_price = df.iloc[i]['close']
    high_price = df.iloc[i]['high']
    low_price = df.iloc[i]['low']
    volumn = df.iloc[i]['volume']

    query = "INSERT INTO history_dt_prc_binance VALUES('{}','{}',{},{},{},{},{})".format(base_dt,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[ ]:




