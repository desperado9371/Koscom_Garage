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
import FetPrc
from ControlMem import InsMem, SelMemTutorial, UpdTutorial
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


app = Flask(__name__)
sockets = Sockets(app)


@app.route('/')
def index():
    return 'hello'


@sockets.route('/Cocos')
def Cocos(ws):
    while not ws.closed:
        
        
        msg = ws.receive()
        if msg !='':
            log.info(f'i WebServer:received:{msg}')
            Key = str(msg).split('|')
            log.info("WebServer:key: " + Key[0])
        
        # Indicators 수신시 지표정보 Json 전송
        if Key[0] == 'Indicators':
            with open("/home/ubuntu/ydHwang/Indicators.json", 'r') as f:
                json_data = json.load(f)
            ws.send(json.dumps(json_data, indent="\t"))
            now = 'Server send' + msg + "  " + datetime.datetime.now().isoformat()
            ws.send(now)
        # save 받을시 알고리즘 저장
        elif Key[0] == 'save':
            log.info("WebServer:Start save!!!!")
            log.info("WebServer:User: " + Key[1])
            log.info("WebServer:Algo_nm: " + Key[2])
            log.info("WebServer:buy_algo: " + Key[3])
            log.info("WebServer:sell_algo: " + Key[4])
            log.info("WebServer:Memo: " + Key[5])
            InsAlgoJson.InsAlgoToDB(Key[1], Key[2], Key[3], Key[4],Key[5])
            now = 'Server saved ' + msg + "  " + datetime.datetime.now().isoformat()
            ws.send(now)

        elif Key[0] == 'load':
            Result = '0'
            log.info("WebServer:Start load!!!!")
            log.info("WebServer:user_id: " + Key[1])
            log.info("WebServer:request_seq: " + Key[2])
            Result = FetAlgoJson.FetAlgoFromDB(Key[1], Key[2])
            log.info("WebServer:[FET]result:" + Result)
            ws.send(Result)
        # Echo
        if msg:
            time.sleep(1)


@sockets.route('/BackServer_Day')
def BackServer_FetDay(ws):
    while not ws.closed:
        msg = ws.receive()
        log.info(f'i WebServer:BackServer_Day received:{msg}')
        Key = str(msg).split('|')
        log.info("WebServer:key:BackServer_Day  " + Key[0])

        # Indicators 수신시 지표정보 Json 전송
        if Key[0] == 'load':
            log.info("WebServer:BackServer_Day Start load!!!!")
            log.info("WebServer:BackServer_Day market: " + Key[1])
            log.info("WebServer:BackServer_Day srt_date: " + Key[2])
            log.info("WebServer:BackServer_Day end_date: " + Key[3])
            Result = FetPrc.FetDtPrc(Key[1], Key[2], Key[3])
            log.info("WebServer:BackServer_Day [FET]result:" + Result)
            ws.send(Result)
        else:
            ws.send("WebServer:BackServer_Day 잘못된 패킷입니다")
        # Echo
        if msg:
            time.sleep(1)


@sockets.route('/BackServer_Hr')
def BackServer_FetHr(ws):
    while not ws.closed:
        msg = ws.receive()
        log.info(f'i WebServer:received:{msg}')
        Key = str(msg).split('|')
        log.info("WebServer:key: " + Key[0])

        # Indicators 수신시 지표정보 Json 전송
        if Key[0] == 'load':
            log.info("WebServer:BackServer_Hr Start load!!!!")
            log.info("WebServer:BackServer_Hr market: " + Key[1])
            log.info("WebServer:BackServer_Hr srt_date: " + Key[2])
            log.info("WebServer:BackServer_Hr end_date: " + Key[3])
            log.info("WebServer:BackServer_Hr srt_time: " + Key[4])
            log.info("WebServer:BackServer_Hr end_time: " + Key[5])
            Result = FetPrc.FetHrPrc(Key[1], Key[2], Key[3], Key[4], Key[5])
            log.info("WebServer:BackServer_Hr [FET]result:" + Result)
            ws.send(Result)
        else:
            ws.send("WebServer:BackServer_Hr 잘못된 패킷입니다")
        # Echo
        if msg:
            time.sleep(1)


@sockets.route('/JoinMem')
def JoinMem(ws):
    while not ws.closed:
        msg = ws.receive()
        log.info(f'i WebServer:JoinMem received:{msg}')
        Key = str(msg).split('|')
        log.info("WebServer:JoinMem key: " + Key[0])

        # Indicators 수신시 지표정보 Json 전송
        if Key[0] == 'save':
            log.info("WebServer:JoinMem Start save!!!!")
            log.info("WebServer:JoinMem id: " + Key[1])
            log.info("WebServer:JoinMem email: " + Key[2])
            Result = InsMem(Key[1], Key[2])
            log.info("WebServer:JoinMem [Save]result:" + Result)
            ws.send(Result)
        else:
            ws.send("WebServer:잘못된 패킷입니다")
        # Echo
        if msg:
            time.sleep(1)


@sockets.route('/ControlMem')
def ControlMem(ws):
    while not ws.closed:
        msg = ws.receive()
        log.info(f'i WebServer:ControlMemreceived:{msg}')
        Key = str(msg).split('|')
        log.info("WebServer:ControlMemkey: " + Key[0])

        # Indicators 수신시 지표정보 Json 전송
        if Key[0] == 'load':
            log.info("WebServer:ControlMem load!!!!")
            log.info("WebServer:ControlMem id: " + Key[1])
            Result = SelMemTutorial(Key[1])
            log.info("WebServer:ControlMem [load]result:" + Result)
            ws.send(Result)
        elif Key[0] == 'update':
            log.info("WebServer:ControlMem Update!!!!")
            log.info("WebServer:ControlMem id: " + Key[1])
            Result = UpdTutorial(Key[1])
            log.info("WebServer:ControlMem [Update]result:" + Result)
            ws.send(Result)
        else:
            ws.send("잘못된 패킷입니다")
        # Echo
        if msg:
            time.sleep(1)


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0', 80), application=app, handler_class=WebSocketHandler)
    print('server started')
    log.info('server started')

    server.serve_forever()


# In[1]:





# In[ ]:




