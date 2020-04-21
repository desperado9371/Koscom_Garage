// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import HandItem from "./HandItem";
import Card from "./Card";
import Deck from "./Deck";

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
        this.init();
    }              
    hands : HandItem[][] = [];
    handIndex = 0;
    
    init(){
        var h : HandItem[] = [];
        var d = new Deck();
        d.testInit();
        h.push(d);
        h.push(d);
        h.push(d);

        this.hands.push(h);

        this.displayHand();
    }


    setNextHand(hand : HandItem[]){
        
        this.hands[this.handIndex+1] = hand;
    }

    displayPreviousHand(){
        this.handIndex--;
        this.displayHand();
    }

    displayNextHand(){
        this.handIndex++;
        this.displayHand();
    }
    displayHand(){
        var hand = this.hands[this.handIndex];
        this.handParent.destroyAllChildren();
        for(var k = 0; k < hand.length; k++){
            var item = hand[k];
            var obj:cc.Node = null;
            
            if(item.getType() === 'Card'){
                obj = cc.instantiate(this.cardPrefab);
                var card = obj.getComponent(Card);
                card.testInit();
            }
            else if(item.getType() === 'Deck'){
                obj = cc.instantiate(this.deckPrefab);
                var deck = obj.getComponent(Deck);
                deck.testInit();
            }
            else{
                console.log("type error"); 
            }
            obj.setParent(this.handParent);
        }

    }
    



    // update (dt) {}
}
