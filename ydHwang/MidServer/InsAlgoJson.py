#!/usr/bin/env python
# coding: utf-8

# In[20]:


#!/usr/bin/env python
# coding: utf-8

import glob
import pandas as pd
import mysql.connector as sql
from datetime import datetime


def InsAlgoToDB(user_id,algo_name,buy_algo ='',sell_algo='', memo = ' '):
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor()
    
    
#     #query = "INSERT INTO algo() VALUES({},'{}','{}','{}')".format()
    try:
        query = 'SELECT ifnull(max(algo_seq),0) FROM algo WHERE id = %s'
        db_cursor.execute(query,(user_id,))
        seq = db_cursor.fetchone()[0]
        seq = int(seq)+1
        print("User: "+user_id)
        print("Algo_nm: "+algo_name)
        print("buy_algo: "+buy_algo)
        print("sell_algo: "+sell_algo)  
        if buy_algo == '' and sell_algo == '':
            query = "INSERT INTO algo (algo_seq, id, algo_nm, date_created, memo) VALUES (%s, %s, %s, %s, %s)"
            val = (str(seq), user_id, algo_name, datetime.today().strftime("%Y%m%d"),memo)  
        elif buy_algo == '' and sell_algo !='':
            query = "INSERT INTO algo (algo_seq, id, algo_nm, sell_algo, date_created, memo) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (str(seq), user_id, algo_name, sell_algo, datetime.today().strftime("%Y%m%d"),memo)        
        elif buy_algo != '' and sell_algo =='' :
            query = "INSERT INTO algo (algo_seq, id, algo_nm, buy_algo, date_created, memo) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (str(seq), user_id, algo_name, buy_algo, datetime.today().strftime("%Y%m%d"),memo)        
        elif buy_algo != '' and sell_algo !='' :
            query = "INSERT INTO algo (algo_seq, id, algo_nm, buy_algo, sell_algo, date_created, memo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (str(seq), user_id, algo_name, buy_algo, sell_algo, datetime.today().strftime("%Y%m%d"),memo)
            print('var : '+ str(val))
        else : 
            print("알고리즘 데이터가 입력되지 않았습니다")
        print(query)
        db_cursor.execute(query, val)
        db_connection.commit()
        
    finally:
        db_connection.close()
    #db_connection.commit()
    #db_cursor.close()
    
if __name__ == "__main__":
    InsAlgoToDB('S1','테스트','','')
    #InsAlgoToDB('User_ID','테스트','')


    


# In[ ]:




