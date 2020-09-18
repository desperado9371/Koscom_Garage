#!/usr/bin/env python
# coding: utf-8

# In[90]:


import mysql.connector as sql
import glob
import pandas as pd
from datetime import datetime


# In[91]:


df = pd.read_csv("/home/garage/workspace/price_update_crontab/upbit_krwbch_1min.csv")


# In[92]:


df = df.tail(11)
print(df)


# In[93]:


db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[94]:



query = 'SELECT max(base_time) FROM history_prc_upbit WHERE base_dt = %s and coin_type = %s'
db_cursor.execute(query,(datetime.today().strftime("%Y%m%d"),'bch',))
print(datetime.today().strftime("%Y%m%d"))
max_time = db_cursor.fetchone()[0]
print(max_time)


# In[95]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['timestamp']).replace("-","")
    tmp = tmp.split('T')
    if max_time >= tmp[1] :
        continue
    base_dt = tmp[0]
    coin_type = 'bch'
    base_time = tmp[1]
    print(base_time)
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




