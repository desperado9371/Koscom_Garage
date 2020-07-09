#!/usr/bin/env python
# coding: utf-8

# In[2]:

import mysql.connector as sql
import glob
import pandas as pd



# In[3]:


df = pd.read_csv("/home/garage/workspace/price_update_crontab/upbit_krwbtc_1hr.csv")
df = df.tail(2)
print(df)


# In[4]:


db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()

tmp = str(df.iloc[0]['timestamp']).replace("-","")
tmp = tmp.split('T')
base_dt = tmp[0]

coin_type = 'krwbtc'
base_time = tmp[1]
open_price = df.iloc[0]['open']
close_price = df.iloc[0]['close']
high_price = df.iloc[0]['high']
low_price = df.iloc[0]['low']
volumn = df.iloc[0]['volume']

query = "INSERT INTO history_hr_prc_upbit VALUES('{}','{}','{}',{},{},{},{},{})".format(base_dt,base_time,coin_type,open_price,close_price,high_price,low_price,volumn)
db_cursor.execute(query)
print(query)
    
db_connection.commit()
db_connection.close()

# In[ ]:




