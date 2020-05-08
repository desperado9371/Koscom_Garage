#!/usr/bin/env python
# coding: utf-8

# In[7]:


#!/usr/bin/env python
# coding: utf-8

import glob
import pandas as pd
import mysql.connector as sql
from datetime import datetime


def InsAlgoToDB(user_id,algo_name,trading_algo):
    print("Ins Start")
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor()
    
    
    #query = "INSERT INTO algo() VALUES({},'{}','{}','{}')".format()
    try:
        print(user_id)
        query = 'SELECT COUNT(*) FROM algo WHERE id = %s'
        db_cursor.execute(query,(user_id,))
        seq = db_cursor.fetchone()[0]
        seq = int(seq)+1
        
        print("Ins_seq: "+str(seq))
        print("Ins_User: "+user_id)
        print("Ins_Algo_nm: "+algo_name)
        print("Ins_Algo: "+trading_algo)    
        query = "INSERT INTO algo (algo_seq, id, algo_nm, trading_algo, date_created) VALUES (%s, %s, %s, %s, %s)"
        val = (str(seq),user_id,algo_name,trading_algo,datetime.today().strftime("%Y%m%d"))
        print("쿼리:"+query)
        
        db_cursor.execute(query, val)
        
        db_connection.commit()
        
    finally:
        db_connection.close()
    #db_connection.commit()
    #db_cursor.close()
    
#if __name__ == "__main__":
#    InsAlgoToDB('User_ID','','{"City": "Galle", "Description": "Best damn city in the world"}')



    


# In[ ]:





# In[5]:





# In[ ]:




