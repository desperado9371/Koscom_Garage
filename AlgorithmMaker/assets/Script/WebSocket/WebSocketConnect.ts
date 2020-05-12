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
    isOpen : boolean = false;
    static sock : WebSocketConnect;
    static getSock(){
      return WebSocketConnect.sock;
    }
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {
      this.ws = new WebSocket("ws://15.164.231.112:80/Cocos");
      this.ws.onopen = this.onOpen;
      this.ws.onmessage = this.onRecieve;
      this.ws.onclose = this.onClose;
      WebSocketConnect.sock = this;
      
    }

    onOpen(event){
      
      this.isOpen = true;
      this.send("Indicators");
    }

    onClose(event){
      this.isOpen = false;
    }

    onRecieve(event){
      console.log(event.data);
      
    }


    send(str : string){
      if(this.isOpen = true){
        this.ws.send(str);

      }
      else{
        console.error("WebSocket Not Connected");
      }
    }


    // update (dt) {}
}


