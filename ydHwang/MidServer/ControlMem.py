#!/usr/bin/env python
# coding: utf-8

# In[18]:


import glob
import pandas as pd
import mysql.connector as sql
from datetime import datetime
import json
from InsAlgoJson import InsAlgoToDB
import logging

log = logging.getLogger()

# 로그의 출력 기준 설정
log.setLevel(logging.INFO)
# log 출력 형식
formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
log.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('./Midware_log.log')
file_handler.setFormatter(formatter)
log.addHandler(file_handler)

def InsMem(user_id,email):
    log.info("InsMem:id: "+user_id)
    log.info("InsMem:email: "+email)
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 

    if user_id != '':
        query = "INSERT INTO algo_member (id, email, tutorial_yn, date_created) VALUES (%s, %s, %s, %s)"
        val = (user_id, email, '0', datetime.today().strftime("%Y%m%d")) 
        db_cursor.execute(query, val)       
        db_connection.commit()
        result = 'Success'
    else:
        result = 'user_id empty'
    
    if result == 'Success':
        f = open("../sample_buy_algo1.json", 'r')
        sample_buy = f.read()
        f.close()
        f = open("../sample_sell_algo1.json", 'r')
        sample_sell = f.read()
        f.close()
        InsAlgoToDB(user_id,'Sample',str(sample_buy),str(sample_sell))
        #InsAlgoToDB(user_id,'Sample','1',data)
        log.info('InsMem:Sample insert Complete')
    
    log.info("InsMem결과: "+ result)
    return result

def SelMemTutorial(user_id):
    log.info("SelMemTutorial_id: "+user_id)
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 

    if user_id != '':
        print('실행')
        query = 'SELECT tutorial_yn FROM algo_member WHERE id = %s '
        db_cursor.execute(query,(user_id,))
        result = db_cursor.fetchone()               
        db_connection.commit()
    else:
        result = 'Fail(잘못된 ID)'
    log.info("SelMemTutorial: "+ result[0])
    return result[0]

def UpdTutorial(user_id):
    log.info("UpdTutorial:update_id: "+user_id)
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 

    if user_id != '':
        print('실행')
        query = 'UPDATE algo_member SET tutorial_yn = 1 WHERE ID = %s '
        db_cursor.execute(query,(user_id,))             
        db_connection.commit()
        result = 'Success'
    else:
        result = 'Fail(잘못된 ID)'
    return result

# if __name__ == "__main__":
#     print("start")
#     InsMem

# if __name__ == "__main__":
#     print("start")
#     InsMem('Sample_test_log','test@test.com')


# In[1]:





# In[ ]:




