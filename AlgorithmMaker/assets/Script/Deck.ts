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
    getType(): string {
        return 'Deck';
    }

    package: HandItem[] = null;
    handManager : HandManager = null;

    getRandomArbitrary(min, max) {
        return Math.random() * (max - min) + min;
    }
    onClick() {
        
        var hm = HandManager.getInstance();
        hm.setNextHand(this.package);
        hm.displayNextHand();
        
    }

    init(nextItems: [HandItem]){
        this.package = nextItems;
    }
    testInit(){
        this.package = new Array<HandItem>();
        this.package.push(new Deck);
        this.package.push(new Card);
        this.package.push(new Card);
        this.package.push(new Card);
    }

    start () {
        
    }

    displayCards(){

    }

    // update (dt) {}
}
