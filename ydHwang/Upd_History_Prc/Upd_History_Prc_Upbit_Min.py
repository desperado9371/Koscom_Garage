#!/usr/bin/env python
# coding: utf-8

# In[71]:


import mysql.connector as sql
import glob
import pandas as pd
from datetime import datetime


# In[72]:


df = pd.read_csv("/home/garage/workspace/price_update_crontab/upbit_krwbtc_1min.csv")


# In[73]:


df = df.tail(11)
print(df)


# In[74]:


db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[75]:



query = 'SELECT max(base_time) FROM history_prc_upbit WHERE base_dt = %s and coin_type = %s'
db_cursor.execute(query,(datetime.today().strftime("%Y%m%d"),'krwbtc',))
print(datetime.today().strftime("%Y%m%d"))
max_time = db_cursor.fetchone()[0]
print(max_time)


# In[76]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['timestamp']).replace("-","")
    tmp = tmp.split('T')
    base_dt = tmp[0] 
    coin_type = 'krwbtc'
    base_time = tmp[1]
    if max_time >= tmp[1] :
        continue  
    open_price = df.iloc[i]['open']
    close_price = df.iloc[i]['close']
    high_price = df.iloc[i]['high']
    low_price = df.iloc[i]['low']
    volumn = df.iloc[i]['volume']

    query = "INSERT INTO history_prc_upbit VALUES('{}','{}','{}',{},{},{},{},{})".format(base_dt,base_time,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    db_connection.commit()

db_connection.close()


# In[ ]:




