// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class TutorialManager extends cc.Component {

    static instance : TutorialManager = null;
    static getInstance() : TutorialManager{

        return TutorialManager.instance;

    }

    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    ws : WebSocket;
    mode = "";
    start () {
        TutorialManager.instance = this;
        this.ws = new WebSocket("ws:/13.124.102.83:80/ControlMem");
        this.ws.onopen = this.onOpen;
        this.ws.onmessage = this.onRecieve;
        this.ws.onclose = this.onClose;
    }

    onOpen(event){

    }
    onClose(event){

    }
    onRecieve(event){
        console.log("Tutorial data recieved : " + event.data);
        if(this.mode == "check"){
            if(event.data == "0"){
                this.tutorialStart();
            }
        }
    }

    tutorialStart(){
        console.log("tutorial started");
    }

    tutorialCheck(){
        this.mode = "check";
        var userID = this.getCookie('username');
        this.ws.send("load|dbtest123");
        //this.ws.send("load|" + userID);
    }

    tutorialDone(){
        var userID = this.getCookie('username');
        this.ws.send("update|dbtest123");
        //this.ws.send("update|" + userID);
    }
    getCookie(name: string): string {
        const nameLenPlus = (name.length + 1);
        return document.cookie
            .split(';')
            .map(c => c.trim())
            .filter(cookie => {
                return cookie.substring(0, nameLenPlus) === `${name}=`;
            })
            .map(cookie => {
                return decodeURIComponent(cookie.substring(nameLenPlus));
            })[0] || null;
    }

    setTutorialItem(){

    }

    

    // update (dt) {}
}
