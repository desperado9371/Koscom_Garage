// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;


@ccclass
export default class WebSocketConnect extends cc.Component {
    ws : WebSocket;
    static sock : WebSocketConnect;
    static getSock(){
      return WebSocketConnect.sock;
    }
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {
      this.ws = new WebSocket("ws://54.180.86.151:80/test");
      this.ws.onopen = this.onOpen;
      this.ws.onmessage = this.onRecieve;
      WebSocketConnect.sock = this;
    }

    onOpen(event){

    }

    onRecieve(event){
      console.log(event.data);
      
    }

    send(str : string){
      this.ws.send(str);
    }


    // update (dt) {}
}

