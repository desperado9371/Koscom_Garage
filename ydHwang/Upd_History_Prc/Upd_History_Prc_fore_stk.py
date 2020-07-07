#!/usr/bin/env python
# coding: utf-8

# In[23]:


import glob
import pandas as pd
import mysql.connector as sql

df = pd.read_csv("/home/garage/amazon_1day.csv")
df = df.tail(1)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[13]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Date']).replace("-","")
    #tmp = tmp.split('T')
    base_dt = tmp
    
    coin_type = 'amazon'
    #base_time = tmp[1]
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_dt_prc_fore_stk VALUES('{}','{}',{},{},{},{},{})".format(base_dt,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[24]:


df = pd.read_csv("/home/garage/facebook_1day.csv")
df = df.tail(1)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[15]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Date']).replace("-","")
    #tmp = tmp.split('T')
    base_dt = tmp
    
    coin_type = 'facebook'
    #base_time = tmp[1]
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_dt_prc_fore_stk VALUES('{}','{}',{},{},{},{},{})".format(base_dt,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[25]:


df = pd.read_csv("/home/garage/apple_1day.csv")
df = df.tail(1)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[18]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Date']).replace("-","")
    #tmp = tmp.split('T')
    base_dt = tmp
    
    coin_type = 'apple'
    #base_time = tmp[1]
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_dt_prc_fore_stk VALUES('{}','{}',{},{},{},{},{})".format(base_dt,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[26]:


df = pd.read_csv("/home/garage/google_1day.csv")
df = df.tail(1)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[20]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Date']).replace("-","")
    #tmp = tmp.split('T')
    base_dt = tmp
    
    coin_type = 'google'
    #base_time = tmp[1]
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_dt_prc_fore_stk VALUES('{}','{}',{},{},{},{},{})".format(base_dt,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[27]:


df = pd.read_csv("/home/garage/tesla_1day.csv")
df = df.tail(1)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[22]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Date']).replace("-","")
    #tmp = tmp.split('T')
    base_dt = tmp
    
    coin_type = 'tesla'
    #base_time = tmp[1]
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_dt_prc_fore_stk VALUES('{}','{}',{},{},{},{},{})".format(base_dt,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[ ]:




