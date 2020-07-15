#!/usr/bin/env python
# coding: utf-8

# In[208]:


#!/usr/bin/env python
# coding: utf-8

# In[170]:


import mysql.connector as sql
import glob
import pandas as pd
from datetime import datetime,timedelta
import json

#일자를 원하는 만큼 앞당김
def Move_dt(date,movement=0):
    if int(movement) >0:
        print("movement는 0이하만 가능합니다")
        return 'movement는 0이하만 가능합니다'
    date=str(date)
    date_frame = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    date_frame = date_frame + timedelta(days=int(movement))
    date = str(date_frame)[0:4]+ str(date_frame)[5:7]+ str(date_frame)[8:10]
    return date

def Move_hr(date,hour,movement=0):
    if int(movement) >0:
        print("movement는 0이하만 가능합니다")
        return 'movement는 0이하만 가능합니다'
    date=str(date)
    date_frame = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]),int(str(hour)[0:2]))
    date_frame = date_frame + timedelta(hours=int(movement))
    date = str(date_frame)[0:4]+ str(date_frame)[5:7]+ str(date_frame)[8:10]+str(date_frame)[11:13]
    print(date)
    return date

def Move_stk_hr(date,hour,movement=0):
    if movement >0:
        print("movement는 0이하만 가능합니다")
        return 'movement는 0이하만 가능합니다'
    if int(hour) > 15 or int(hour) <9:
        print("해외주식시장 시간은 9~15만 가능합니다")
        return '해외주식시장 시간은 9~15만 가능합니다'  
    hour = int(hour)
    Move_day=abs(movement)//7
    Move_hour=abs(movement)%7
    print('move_day:'+str(Move_day)+' move_hour: '+str(Move_hour))
    date=str(date)
    date_frame = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    date_frame = date_frame + timedelta(days=(-Move_day))
    print(date_frame)
    print(hour - Move_hour)
    if int(hour - Move_hour) < 9:
        date_frame = date_frame + timedelta(days=(-1))
        hour=16-(9-(hour - Move_hour))
    else:
        hour = hour - Move_hour
    
    if int(hour) < 10:
        hour_string = '0'+str(hour)
    else:
        hour_string = str(hour)
    date = str(date_frame)[0:4]+ str(date_frame)[5:7]+ str(date_frame)[8:10]+hour_string
    print(date)
    return date

def FetDtPrc(market,srt_date,end_date,movement=0):
    print("market: "+market + "srt_date: "+srt_date + " end_date: "+end_date+ " movement: "+str(movement))
    s_json_data=0
    # 시작일 - 전일자
    srt_date = Move_dt(srt_date,movement)
    # 끝일 - 전일자
    end_date = Move_dt(end_date,movement)
    print("market: "+market + "srt_date: "+srt_date + " end_date: "+end_date+ " movement: "+str(movement))
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

def FetHrPrc(market='upbit',srt_date='0',end_date='99999999', srt_time = '00', end_time='24',movement=0):
    s_json_data=0
    print("market: "+market + "srt_date: "+srt_date+srt_time+ " end_date: "+end_date+end_time+" movement: "+str(movement))
    srt_date=Move_hr(srt_date,srt_time,movement)
    srt_time=srt_date[8:10]
    srt_date=srt_date[0:8]
    print("srt_date: "+srt_date)
    print("srt_time: "+srt_time)
    
    end_date=Move_hr(end_date,end_time,movement)
    end_time=end_date[8:10]
    print("end_time: "+end_time)
    end_date=end_date[0:8]
    end_time = end_time + ':00:00'
    print("end_date: "+end_date)
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





def FetDtForeStkPrc(stk_nm ,srt_date,end_date,movement=0):
    print("stk_nm: "+stk_nm + "srt_date: "+srt_date + " end_date: "+end_date+ " movement: "+str(movement))
    s_json_data=0
    if int(movement) >0:
        print("movement는 0이하만 가능합니다")
        return 'movement는 0이하만 가능합니다'
    movement = abs(int(movement))
    
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 
    
    # 지원하지 않는 주식종목은 skip
    if stk_nm !='apple' and stk_nm !='tesla' and stk_nm !='facebook' and stk_nm !='google' and stk_nm !='amazon' :
        print('지원하지 않는 종목입니다')
        return 0
    try:
        if movement == 0:
            query = 'SELECT base_dt,open_price,close_price,high_price,low_price,volumn FROM history_dt_prc_fore_stk WHERE base_dt >= %s and base_dt <= %s and stk_type= %s'
            db_cursor.execute(query,(srt_date,end_date,stk_nm,))
            data = db_cursor.fetchall() 
        else :
            query = 'SELECT count(*) FROM history_dt_prc_fore_stk WHERE base_dt >= %s and base_dt <= %s and stk_type= %s'
            db_cursor.execute(query,(srt_date,end_date,stk_nm,))
            count = db_cursor.fetchone()[0]
            query = 'SELECT ALL_TABLE.base_dt,ALL_TABLE.open_price,ALL_TABLE.close_price,ALL_TABLE.high_price,ALL_TABLE.low_price,ALL_TABLE.volumn                    FROM (SELECT * FROM history_dt_prc_fore_stk                    WHERE STK_TYPE=%s AND BASE_DT <= %s                     ORDER BY BASE_DT DESC LIMIT %s) ALL_TABLE                    ORDER BY BASE_DT LIMIT %s'
            db_cursor.execute(query,(stk_nm,end_date,int(count)+movement,count,))
            data = db_cursor.fetchall() 
        
    finally:
        db_connection.close()
    
    #df = pd.DataFrame(data,columns=['timestamp','open','close','high','low','volumn'])
    s_json_data = json.dumps(data)
    print(s_json_data)
    return str(s_json_data)

def FetHrForeStkPrc(market='fore',stk_nm='apple',srt_date='0',end_date='99999999', srt_time = '00', end_time='24',movement=0):
    s_json_data=0
    #시간입력이 범위 벗어난경우
    if int(srt_time) < 9:
        srt_time = '00'
    elif int(srt_time) >15:
        srt_time = '15'
    if int(end_time) < 9:
        end_time = '00'
    elif int(end_time) >15:
        end_time = '15'
        
    movement = abs(int(movement))#Limit 에 사용해야되서 절대값(양수)로 변경    
    end_time = end_time + ':00:00'
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 
    
    try:
        # 이동값이 없는경우
        if movement == 0:
            if market == 'fore' and srt_date != end_date:
                query = 'SELECT base_dt,base_time,open_price,close_price,high_price,low_price,volumn                 FROM history_hr_prc_fore_stk                 WHERE base_dt = %s and base_time >= %s and stk_type = %s                union SELECT base_dt,base_time,open_price,close_price,high_price,low_price,volumn                 FROM history_hr_prc_fore_stk WHERE base_dt > %s and base_dt < %s and stk_type = %s                union SELECT base_dt,base_time,open_price,close_price,high_price,low_price,volumn                 FROM history_hr_prc_fore_stk WHERE base_dt = %s and base_time <= %s and stk_type = %s'
                db_cursor.execute(query,(srt_date,srt_time,stk_nm,srt_date,end_date,stk_nm,end_date,end_time,stk_nm))          
            elif market == 'fore' and srt_date == end_date:
                query = 'SELECT base_dt,base_time,open_price,close_price,high_price,low_price,volumn                 FROM history_hr_prc_fore_stk WHERE base_dt = %s and base_time >= %s and base_time <= %s and stk_type = %s'
                db_cursor.execute(query,(srt_date,srt_time,end_time,stk_nm))
            else :
                print('Market 값이 잘못됏습니다.')  
            data = db_cursor.fetchall() 
            db_connection.commit()
        else:#이동값이 있는경우
            if market == 'fore' and srt_date != end_date:#날짜가 다른경우
                query = 'SELECT count(*) from(SELECT * FROM history_hr_prc_fore_stk                 WHERE base_dt = %s and base_time >= %s and stk_type = %s                union SELECT * FROM history_hr_prc_fore_stk WHERE base_dt > %s and base_dt < %s and stk_type = %s                union SELECT * FROM history_hr_prc_fore_stk WHERE base_dt = %s and base_time <= %s and stk_type = %s) A'
                db_cursor.execute(query,(srt_date,srt_time,stk_nm,srt_date,end_date,stk_nm,end_date,end_time,stk_nm)) 
                count = db_cursor.fetchone()[0]
                print(count)
                query = 'SELECT Tmp.base_dt,base_time,open_price,close_price,high_price,low_price,volumn from (SELECT * FROM history_hr_prc_fore_stk WHERE base_dt <= %s and base_time <= %s and stk_type = %s                         ORDER BY BASE_DT DESC, BASE_TIME DESC LIMIT %s) Tmp                         order by BASE_DT, BASE_TIME LIMIT %s'
                db_cursor.execute(query,(end_date,end_time,stk_nm,int(count)+movement,count,)) 
                data = db_cursor.fetchall() 
            elif market == 'fore' and srt_date == end_date:#날짜가 같은경우
                data = []
                count = int(end_time[0:2])- int(srt_time)
                print(count)
                if count > 0 :
                    query = 'SELECT Tmp.base_dt,base_time,open_price,close_price,high_price,low_price,volumn from (SELECT * FROM history_hr_prc_fore_stk WHERE base_dt <= %s and base_time <= %s and stk_type = %s                             ORDER BY BASE_DT DESC, BASE_TIME DESC LIMIT %s) Tmp                             order by BASE_DT, BASE_TIME LIMIT %s'
                    db_cursor.execute(query,(end_date,end_time,stk_nm,int(count)+movement,count,)) 
                    data = db_cursor.fetchall() 
                
    finally:
        db_connection.close()
    
    s_json_data = json.dumps(data)
    print(s_json_data)
    return str(s_json_data)

if __name__ == "__main__":
    print("start")
    #FetDtPrc('upbit','20200702','20200703')
    #FetDtForeStkPrc('apple','20200304','20200306',-2)
    #Move_stk_hr(20200714,15,-8)
    FetHrForeStkPrc('fore','tesla','20200401','20200403','10','15',-4)
    #FetHrPrc('upbit','20200701','20200706','02','22',0)
# if __name__ == "__main__":
#     print("start")
#     FetDtPrc('upbit','20180101','20180301')


# In[ ]:





# In[ ]:




