// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import HandItem from "./HandItem";
import Card from "./Card";
import Deck from "./Deck";
import CAnimation from "./CAnimation";

const {ccclass, property} = cc._decorator;

@ccclass
export default class HandManager extends cc.Component {

    @property(cc.Node)
    handParent: cc.Node = null;

    @property(cc.Prefab)
    cardPrefab: cc.Prefab = null;

    @property(cc.Prefab)
    deckPrefab: cc.Prefab = null;

    @property([CAnimation])
    handAmination : [CAnimation]; 



    isHiding = true;
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

        this.hands.push(h);

        

        this.showHand();

    }


    setNextHand(hand : HandItem[]){
        
        this.hands[this.handIndex+1] = hand;
    }

    displayPreviousHand(){
        if(this.handIndex > 0){
            this.handIndex--;
            this.displayHand();

        }
    }

    displayNextHand(){
        this.handIndex++;
        this.displayHand();
    }
    displayHand(){
        this.hideHand();


    }
    
    onAnimDone(){
        HandManager.getInstance().showHand();
    }


    hideHand(){
        //this.handAmination.stop();
        this.isHiding = true;



        for(var k = 0; k < this.handAmination.length; k++){
            var anim = this.handAmination[k];
            if(k === 0 ){
                cc.tween(anim.node).to(anim.duration.valueOf(),{ position: anim.posTo, scaleX: anim.scaleTo.x})
                .call(() => {HandManager.getInstance().showHand();})
                .to(anim.duration.valueOf(),{ position: anim.posFrom, scaleX: anim.scaleFrom.x})
                .start();
            }else{
                cc.tween(anim.node).to(anim.duration.valueOf(),{ position: anim.posTo, scaleX: anim.scaleTo.x})
                .to(anim.duration.valueOf(),{ position: anim.posFrom, scaleX: anim.scaleFrom.x})
                .start();
            }

        }




        /*
        for(var k = 0; k < this.handAmination.length; k++){
            this.handAmination[k].stopAnimation();
            if(k === this.handAmination.length -1){
                
                this.handAmination[k].addCallback(this.onAnimDone);
                this.handAmination[k].startAnim();
            }
            else{
                this.handAmination[k].startAnim();
            }
        }*/
        
        
        //this.handAmination.defaultClip = this.animClip;
        //this.handAmination.currentClip = this.animClip;
        //this.handAmination.play();
        
    }

    showHand(){
        //this.handAmination.stop();
        
        var hand = this.hands[this.handIndex];
        this.handParent.destroyAllChildren();


        for(var k = 0; k < hand.length; k++){
            var item = hand[k];
            var obj:cc.Node = null;
            
            if(item.getType() === 'Card'){
                obj = cc.instantiate(this.cardPrefab);
                var card = obj.getComponent(Card);
                var original = item as Card;
                card.init(original.cardName);
            }
            else if(item.getType() === 'Deck'){
                obj = cc.instantiate(this.deckPrefab);
                var deck = obj.getComponent(Deck);
                var originalDeck = item as Deck;
                deck.init(originalDeck.package);
            }
            else{
                console.log("type error"); 
            }
            obj.setParent(this.handParent);
        }


        this.isHiding = false;
    }
    

    refreshHand(){
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



    update (dt) {
        /*for(var k = 0; k < this.handAmination.length; k++){
            this.handAmination[k].updateAnim(dt);
        }*/
    }
}
