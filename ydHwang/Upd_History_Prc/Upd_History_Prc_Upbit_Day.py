#!/usr/bin/env python
# coding: utf-8

# In[3]:


import mysql.connector as sql
import glob
import pandas as pd



# In[4]:


df = pd.read_csv("/home/garage/workspace/price_update_crontab/upbit_krwbtc_1day.csv")


# In[5]:


df = df.tail(1)
print(df)


# In[6]:


db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[7]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['timestamp']).replace("-","")
    tmp = tmp.split('T')
    base_dt = tmp[0]
    
    coin_type = 'krwbtc'
    base_time = tmp[1]
    open_price = df.iloc[i]['open']
    close_price = df.iloc[i]['close']
    high_price = df.iloc[i]['high']
    low_price = df.iloc[i]['low']
    volumn = df.iloc[i]['volume']

    query = "INSERT INTO history_dt_prc_upbit VALUES('{}','{}',{},{},{},{},{})".format(base_dt,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()
db_connection.close()

# In[ ]:




