// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class PopupSaveTooltip extends cc.Component {



    
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}
    @property(Number)
    stayingTime : Number = 5;

    @property(Number)
    fadingTime : Number = 3;

    start () {
        cc.tween(this.node)
        .delay(this.stayingTime.valueOf())
        .to(this.fadingTime.valueOf(), {opacity: 0})
        .call(() => {
            this.node.destroy();
        }).start();
    }

    onNoButton(){
        this.node.destroy();
    }

    onYesButton(){
        location.href = "/mypage";
    }

    update (dt) {


    }
}
