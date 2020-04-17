// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import HandItem from "./HandItem";
import HandMAnager from "./HandManager";

const {ccclass, property} = cc._decorator;

@ccclass
export default class Card extends HandItem {
    

    description : string = null;
    onClick(): Function {
        console.log(this.description);
        
        return;
    }

    init(){
        
    }


    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {

    }

    

    // update (dt) {}
}
