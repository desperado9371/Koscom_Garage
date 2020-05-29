#!/usr/bin/env python
# coding: utf-8

# In[3]:


import glob
import pandas as pd
import mysql.connector as sql
from datetime import datetime
import json

def Save_Mem(user_id,email):
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


# if __name__ == "__main__":
#     print("start")
#     Save_Mem('Test_id','test@test.com')


# In[ ]:




