#!/usr/bin/env python
# coding: utf-8

# In[9]:


import mysql.connector as sql
import glob
import pandas as pd

df = pd.read_csv("/home/garage/workspace/foreign_stock/amazon_1hour.csv")
df = df.tail(7)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[3]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Datetime']).replace("-","")
    tmp = tmp.split(' ')
    base_dt = tmp[0]
    
    coin_type = 'amazon'
    base_time = tmp[1][0:2]+':00:00'
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_hr_prc_fore_stk VALUES('{}','{}','{}',{},{},{},{},{})".format(base_dt,base_time,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[5]:


df = pd.read_csv("/home/garage/workspace/foreign_stock/facebook_1hour.csv")
df = df.tail(7)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[6]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Datetime']).replace("-","")
    tmp = tmp.split(' ')
    base_dt = tmp[0]
    
    coin_type = 'facebook'
    base_time = tmp[1][0:2]+':00:00'
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_hr_prc_fore_stk VALUES('{}','{}','{}',{},{},{},{},{})".format(base_dt,base_time,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[7]:


df = pd.read_csv("/home/garage/workspace/foreign_stock/apple_1hour.csv")
df = df.tail(7)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[4]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Datetime']).replace("-","")
    tmp = tmp.split(' ')
    base_dt = tmp[0]
    
    coin_type = 'apple'
    base_time = tmp[1][0:2]+':00:00'
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_hr_prc_fore_stk VALUES('{}','{}','{}',{},{},{},{},{})".format(base_dt,base_time,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[2]:


df = pd.read_csv("/home/garage/workspace/foreign_stock/google_1hour.csv")
df = df.tail(7)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[3]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Datetime']).replace("-","")
    tmp = tmp.split(' ')
    base_dt = tmp[0]
    
    coin_type = 'google'
    base_time = tmp[1][0:2]+':00:00'
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_hr_prc_fore_stk VALUES('{}','{}','{}',{},{},{},{},{})".format(base_dt,base_time,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()


# In[10]:


df = pd.read_csv("/home/garage/workspace/foreign_stock/tesla_1hour.csv")
df = df.tail(7)
print(df)
db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
db_cursor = db_connection.cursor()


# In[11]:


for i in range(len(df)):
    tmp = str(df.iloc[i]['Datetime']).replace("-","")
    tmp = tmp.split(' ')
    base_dt = tmp[0]
    
    coin_type = 'tesla'
    base_time = tmp[1][0:2]+':00:00'
    open_price = df.iloc[i]['Open']
    close_price = df.iloc[i]['Close']
    high_price = df.iloc[i]['High']
    low_price = df.iloc[i]['Low']
    volumn = df.iloc[i]['Volume']

    query = "INSERT INTO history_hr_prc_fore_stk VALUES('{}','{}','{}',{},{},{},{},{})".format(base_dt,base_time,coin_type,open_price,close_price,high_price,low_price,volumn)
    db_cursor.execute(query)
    print(query)
    
db_connection.commit()
db_connection.close()

# In[ ]:




