#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_sockets import Sockets
import datetime
import time
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import json
import InsAlgoJson
import FetAlgoJson
import FetDtPrc


app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def index():
    return 'hello'

@sockets.route('/Cocos')
def Cocos(ws):
    while not ws.closed:
        msg = ws.receive()
        print(f'i received:{msg}')
        
        Key = str(msg).split('|')
        print("key: "+Key[0])
        
        #Indicators 수신시 지표정보 Json 전송
        if Key[0] == 'Indicators':
            with open("/home/ubuntu/ydHwang/Indicators.json", 'r') as f:
                json_data = json.load(f)
            ws.send(json.dumps(json_data, indent="\t"))
            now = 'Server send'+msg+"  "+datetime.datetime.now().isoformat()
            ws.send(now)
        #save 받을시 알고리즘 저장    
        elif Key[0] == 'save':
            print("Start save!!!!")
            print("User: "+Key[1])
            print("Algo_nm: "+Key[2])
            print("Algo: "+Key[3])
            InsAlgoJson.InsAlgoToDB(Key[1],Key[2],Key[3])
            now = 'Server saved '+msg+"  "+datetime.datetime.now().isoformat()
            ws.send(now)
            
        elif Key[0] == 'load':
            Result = '0'
            print("Start load!!!!")
            print("User: "+Key[1])
            print("Algo: "+Key[2])
            Result = FetAlgoJson.FetAlgoFromDB(Key[1],Key[2])
            print("[FET]result:"+Result)
            ws.send(Result)
        #Echo
        if msg:
            time.sleep(1)

@sockets.route('/BackServer')
def BackServer(ws):
    while not ws.closed:
        msg = ws.receive()
        print(f'i received:{msg}')
        Key = str(msg).split('|')
        print("key: "+Key[0])
        
        #Indicators 수신시 지표정보 Json 전송
        if Key[0] == 'load':
            print("Start load!!!!")
            print("market: "+Key[1])
            print("srt_date: "+Key[2])
            print("end_date: "+Key[3])
            Result = FetDtPrc.FetDtPrc(Key[1],Key[2],Key[3])
            print("[FET]result:"+Result)
            ws.send(Result)
        else :
            ws.send("잘못된 패킷입니다")
        #Echo
        if msg:
            time.sleep(1)
        
if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0',80),application=app,handler_class=WebSocketHandler)
    print('server started')
    server.serve_forever()


# In[3]:





# In[ ]:





# In[ ]:





# In[ ]:



