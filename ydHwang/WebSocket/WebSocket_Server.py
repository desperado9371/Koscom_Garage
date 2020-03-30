#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask
from flask_sockets import Sockets
import datetime
import time
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

app = Flask(__name__)
sockets = Sockets(app)

@app.route('/')
def index():
    return 'hello'

@sockets.route('/test')
def test(ws):
    while not ws.closed:
        msg = ws.receive()
        print('i received:{msg}')
        if msg:
            now = 'Server receieved '+msg+datetime.datetime.now().isoformat()
            ws.send(now)
            print('i sent:{now}')
            time.sleep(1)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0',80),application=app,handler_class=WebSocketHandler)
    print('server started')
    server.serve_forever()


# In[4]:





# In[ ]:




