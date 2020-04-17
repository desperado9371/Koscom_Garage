// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import HandItem from "./HandItem";
import Card from "./Card";
import HandManager from "./HandManager";

const {ccclass, property} = cc._decorator;

@ccclass
export default class Deck extends HandItem {

    package: [HandItem];
    handManager : HandManager = null;


    onClick(): Function {
        
        var hm = HandManager.getInstance();
        hm.displayNextHand(this.package);
        
        return;
    }

    init(nextItems: [HandItem]){
        this.package = nextItems;
    }

    start () {
        
    }

    displayCards(){

    }

    // update (dt) {}
}
