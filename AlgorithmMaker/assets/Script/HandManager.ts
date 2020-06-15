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

        var vol = new Deck();
        vol.setCategory("거래량");
        vol.pushCard("OBV");
        vol.pushCard("ADI");
        vol.pushCard("CMF");
        vol.pushCard("MFI");
        vol.pushCard("FI");


        var trend = new Deck();
        trend.setCategory("추세");
        trend.pushCard("MACD");
        trend.pushCard("RSI");
        trend.pushCard("MACD|시그널");
        trend.pushCard("ADX");
        trend.pushCard("CCI");
        trend.pushCard("TRIX");

        var momentum = new Deck();
        momentum.setCategory("모멘텀");
        momentum.pushCard("스토캐스틱");
        momentum.pushCard("TSI");
        momentum.pushCard("ROC");
        momentum.pushCard("AO");

        var volatility  = new Deck();
        volatility.setCategory("변동성");
        volatility.pushCard("볼린저밴드|중심선");
        volatility.pushCard("볼린저밴드|상한선");
        volatility.pushCard("볼린저밴드|하한선");
        volatility.pushCard("볼린저밴드|밴드폭");
        volatility.pushCard("ATR");

        
        h.push(vol);
        h.push(trend);
        h.push(momentum);
        h.push(volatility);
        var numCard = new Card();
        numCard.dataInit('숫자카드');
        h.push(numCard);

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
                var cast = item as Deck;
                deck.setCategory(cast.category);
                deck.init(originalDeck.package);
            }
            else{
                console.log("type error"); 
            }
            obj.setParent(this.handParent);
            obj.setPosition(0,0,0);
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
