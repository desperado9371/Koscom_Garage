// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import HandItem from "./HandItem";

const {ccclass, property} = cc._decorator;

@ccclass
export default class HandManager extends cc.Component {

    @property(cc.Node)
    handParent: cc.Node = null;

    @property(cc.Prefab)
    cardPrefab: cc.Prefab = null;

    @property(cc.Prefab)
    deckPrefab: cc.Prefab = null;

    static instance : HandManager = null;
    static getInstance() : HandManager{
        if(this.instance === null){
            var node = cc.instantiate(new cc.Node());
            var hm = node.addComponent(HandManager);
            HandManager.instance = hm;
        }
        return HandManager.instance;
    }

    // LIFE-CYCLE CALLBACKS:

    onLoad () {
        if(HandManager.instance === null){
            HandManager.instance = this;
        }
    }

    start () {
        if(HandManager.instance === null){
            HandManager.instance = this;
        }
    }                                                                             

    hands : [[HandItem]];
    handIndex = 0;

    displayNextHand(hand : [HandItem]){
        this.handIndex++;
        this.hands[this.handIndex] = hand;

    }

    displayPreviousHand(){
        this.handIndex--;
    }

    displayHand(){
        var hand = this.hands[this.handIndex];
        this.handParent.destroyAllChildren();

    }
    



    // update (dt) {}
}
