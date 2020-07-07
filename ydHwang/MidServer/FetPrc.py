#!/usr/bin/env python
# coding: utf-8

# In[13]:


import glob
import pandas as pd
import mysql.connector as sql
from datetime import datetime
import json

def FetDtPrc(market,srt_date,end_date):
    print("market: "+market)
    print("srt_date: "+srt_date)
    print("end_date: "+end_date)
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 
    
    try:
        if market == 'upbit':
            query = 'SELECT base_dt,open_price,close_price,high_price,low_price,volumn FROM history_dt_prc_upbit WHERE base_dt >= %s and base_dt <= %s '
            #query = 'SELECT JSON_ARRAYAGG(JSON_OBJECT("base_dt",base_dt,"open_price",open_price,"close_price",close_price,"high_price",high_price,"low_price",low_price,"volumn",volumn)) FROM history_dt_prc_upbit WHERE base_dt >= %s and base_dt <= %s '
            db_cursor.execute(query,(srt_date,end_date,))
            data = db_cursor.fetchall()  
        else :
            query = 'SELECT base_dt,open_price,close_price,high_price,low_price,volumn FROM history_dt_prc_binance WHERE base_dt >= %s and base_dt <= %s '
            db_cursor.execute(query,(srt_date,end_date,))
            data = db_cursor.fetchall()               
        db_connection.commit()
    finally:
        db_connection.close()
    
    #df = pd.DataFrame(data,columns=['timestamp','open','close','high','low','volumn'])
    print("조회완료")
    s_json_data = json.dumps(data)
    return str(s_json_data)

def FetHrPrc(market='upbit',srt_date='0',end_date='99999999', srt_time = '00', end_time='24'):
    print("market: "+market)
    print("srt_date: "+srt_date)
    print("end_date: "+end_date)
    print("srt_time: "+srt_time)
    end_time = end_time + ':00:00'
    print("end_time: "+end_time)
    
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 
    
    try:
        if market == 'upbit' and srt_date != end_date:
            query = 'SELECT base_dt,base_time,open_price,close_price,high_price,low_price,volumn FROM history_hr_prc_upbit WHERE base_dt = %s and base_time >= %s                union SELECT base_dt,base_time,open_price,close_price,high_price,low_price,volumn FROM history_hr_prc_upbit WHERE base_dt > %s and base_dt < %s                union SELECT base_dt,base_time,open_price,close_price,high_price,low_price,volumn FROM history_hr_prc_upbit WHERE base_dt = %s and base_time <= %s'
            db_cursor.execute(query,(srt_date,srt_time,srt_date,end_date,end_date,end_time))
            data = db_cursor.fetchall()  
        elif market == 'upbit' and srt_date == end_date:
            query = 'SELECT base_dt,base_time,open_price,close_price,high_price,low_price,volumn FROM history_hr_prc_upbit WHERE base_dt = %s and base_time >= %s and base_time <= %s'
            db_cursor.execute(query,(srt_date,srt_time,end_time))
            data = db_cursor.fetchall() 
        else :
            print('바이낸스는 아직 시간봉처리 안함 2020.05.28')
            #바이낸스는 아직 시간봉처리 안함 2020.05.28
            #query = 'SELECT base_dt,open_price,close_price,high_price,low_price,volumn FROM history_dt_prc_binance WHERE base_dt >= %s and base_dt <= %s and base_time >= %s and base_time <=%s'
            #db_cursor.execute(query,(srt_date,end_date,srt_time,end_time,))
            #data = db_cursor.fetchall()               
        db_connection.commit()
    finally:
        db_connection.close()
    
    #df = pd.DataFrame(data,columns=['timestamp','open','close','high','low','volumn'])
    s_json_data = json.dumps(data)
    print("조회완료")
    return str(s_json_data)

def FetDtForeStkPrc(stk_nm ,srt_date,end_date):
    print("stk_nm: "+stk_nm)
    print("srt_date: "+srt_date)
    print("end_date: "+end_date)
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 
    
    # 지원하지 않는 주식종목은 skip
    if stk_nm !='apple' and stk_nm !='tesla' and stk_nm !='facebook' and stk_nm !='google' and stk_nm !='amazon' :
        print('지원하지 않는 종목입니다')
        return 0
    try:
        query = 'SELECT base_dt,open_price,close_price,high_price,low_price,volumn FROM history_dt_prc_fore_stk WHERE base_dt >= %s and base_dt <= %s and stk_type= %s'
        db_cursor.execute(query,(srt_date,end_date,stk_nm,))
        data = db_cursor.fetchall()  
        db_connection.commit()
    finally:
        db_connection.close()
    
    #df = pd.DataFrame(data,columns=['timestamp','open','close','high','low','volumn'])
    s_json_data = json.dumps(data)
    print(s_json_data)
    return str(s_json_data)

if __name__ == "__main__":
    print("start")
    FetDtForeStkPrc('apple','20200101','20200301')

# if __name__ == "__main__":
#     print("start")
#     FetDtPrc('upbit','20180101','20180301')


# In[ ]:




