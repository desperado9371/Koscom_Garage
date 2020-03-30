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
        
        #Indicators 수신시 지표정보 Json 전송
        if msg == 'Indicators':
            with open("/home/ubuntu/ydHwang/Indicators.txt", 'r') as f:
                json_data = json.load(f)
            print(json.dumps(json_data, indent="\t") )
            ws.send(json.dumps(json_data, indent="\t"))
            
        #Echo    
        if msg:
            now = 'Server receieved '+msg+datetime.datetime.now().isoformat()
            ws.send(now)
            print(f'i sent:{now}')
            time.sleep(1)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0',80),application=app,handler_class=WebSocketHandler)
    print('server started')
    server.serve_forever()


# In[4]:





# In[ ]:




