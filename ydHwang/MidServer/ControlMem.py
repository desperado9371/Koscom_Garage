#!/usr/bin/env python
# coding: utf-8

# In[14]:


import glob
import pandas as pd
import mysql.connector as sql
from datetime import datetime
import json

def InsMem(user_id,email):
    print("id: "+user_id)
    print("email: "+email)
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor() 

    if user_id != '':
        print('실행')
        query = "INSERT INTO algo_member (id, email, tutorial_yn, date_created) VALUES (%s, %s, %s, %s)"
        val = (user_id, email, '0', datetime.today().strftime("%Y%m%d")) 
        db_cursor.execute(query, val)          
        db_connection.commit()
        result = 'Success'
    else:
        result = 'Fail'
    return result

def SelMemTutorial(user_id):
    print("id: "+user_id)
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
    return result[0]

def UpdTutorial(user_id):
    print("id: "+user_id)
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
#     print(UpdTutorial('Join4'))

# if __name__ == "__main__":
#     print("start")
#     InsMem('Test_id','test@test.com')


# In[ ]:




