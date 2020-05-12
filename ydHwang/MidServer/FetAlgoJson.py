#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

import glob
import pandas as pd
import mysql.connector as sql
from datetime import datetime
import json


def FetAlgoFromDB(user_id,request_seq):
    print("Fet_User: "+user_id)
    print("Fet_Algo_seq: "+request_seq)
    db_connection = sql.connect(host='root.cqyptexqvznx.ap-northeast-2.rds.amazonaws.com',port=int(3306), database='garage_test', user='root', password='koscom!234')
    db_cursor = db_connection.cursor()
    
    
    #query = "INSERT INTO algo() VALUES({},'{}','{}','{}')".format()
    try:
        if request_seq == 'all':
            query = 'SELECT * FROM algo WHERE id = %s '
            db_cursor.execute(query,(user_id,))
            myresult = db_cursor.fetchall()
            items = [dict(zip( [key[0] for key in db_cursor.description], row)) for row in myresult]
            tmp = json.dumps({'items': items})
            data = json.loads(tmp)
            #print(tmp)
        else :
            query = 'SELECT * FROM algo WHERE id = %s AND algo_seq = %s'
            db_cursor.execute(query,(user_id,request_seq,))
            myresult = db_cursor.fetchall()
            items = [dict(zip( [key[0] for key in db_cursor.description], row)) for row in myresult]
            tmp = json.dumps({'items': items})
            data = json.loads(tmp)
           # print(tmp)                 
        db_connection.commit()
    finally:
        db_connection.close()

#     print(data)
    return str(data)

# if __name__ == "__main__":
#    print("start")
#    FetAlgoFromDB('User_ID','all')



    


# In[ ]:





# In[ ]:




