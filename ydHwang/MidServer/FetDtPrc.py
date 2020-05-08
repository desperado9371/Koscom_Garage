#!/usr/bin/env python
# coding: utf-8

# In[40]:


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
    s_json_data = json.dumps(data)
    print(s_json_data)
    return str(s_json_data)

if __name__ == "__main__":
    print("start")
    FetDtPrc('upbit','20180101','20180301')


# In[ ]:




