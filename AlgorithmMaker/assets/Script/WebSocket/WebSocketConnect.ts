// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import AlgorithmManager from "../AlgorithmManager";

const {ccclass, property} = cc._decorator;


@ccclass
export default class WebSocketConnect extends cc.Component {
    ws : WebSocket;
    isOpen : boolean = false;
    static sock : WebSocketConnect;
    static getSock(){
      return WebSocketConnect.sock;
    }
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {
      this.ws = new WebSocket("ws://13.124.102.83:80/Cocos");
      this.ws.onopen = this.onOpen;
      this.ws.onmessage = this.onRecieve;
      this.ws.onclose = this.onClose;
      
      WebSocketConnect.sock = this;
      
    }

    onOpen(event){
      
      this.isOpen = true;
      //this.send("Indicators");
    }

    onClose(event){
      this.isOpen = false;
    }


    recieveMode = '';
    sender = null;
    onRecieve(event){
      console.log(event.data);
      
      if(WebSocketConnect.sock.recieveMode == 'load'){
        var am = AlgorithmManager.getInstance();
        am.parseAlgorithm(event.data);
      }
      
    }

    tempStr : string = '';
    resend(event){

    }


    send(str : string, sender = null, recieveMode = ''){
      this.recieveMode = recieveMode;
      this.sender = sender;
      if(this.isOpen = true){
        try {
          this.ws.send(str);
        } catch (error) {
          this.tempStr = str;
          this.ws = new WebSocket("ws:/13.124.102.83:80/Cocos");
          this.ws.onopen = this.resend;
        }
        

      }
      else{
        console.error("WebSocket Not Connected");
      }
    }


    // update (dt) {}
}


