// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import HandItem from "./HandItem";
import Card from "./Card";
import HandManager from "./HandManager";
import FileManager from "./FileManager";

const {ccclass, property} = cc._decorator;

@ccclass
export default class Deck extends HandItem {
    
    @property(cc.Sprite)
    sprite: cc.Sprite = null;

    @property(cc.Label)
    lblCategory : cc.Label = null;
    
    getType(): string {
        return 'Deck';
    }

    

    /**
     *
     */
    constructor() {
        super();
        this.package = new Array<HandItem>();
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
    category = null;
    setCategory(category){
        this.category = category;
        if(this.lblCategory != null){

            this.lblCategory.string = category;
        }
        if(this.sprite != null){
            if(category.includes('거래량')){
                this.sprite.spriteFrame = FileManager.getInstance().cardVolume;
            }
            else if(category.includes('추세')){
                this.sprite.spriteFrame = FileManager.getInstance().cardTrend;
                
            }
            else if(category.includes('모멘텀')){
                this.sprite.spriteFrame = FileManager.getInstance().cardMomentum;
                
            }
            else if(category.includes('변동성')){
                this.sprite.spriteFrame = FileManager.getInstance().cardPrice;
                
            }
        }

    }

    init(nextItems: HandItem[]){
        this.package = nextItems;
    }

    pushCard(name){
        var card = new Card();
        card.dataInit(name);
        this.package.push(card);
    }
    testInit(){
        this.package = new Array<HandItem>();
        var card = new Card();
        card.dataInit("RSI");
        this.package.push(card);
        
        card = new Card();
        card.dataInit("MACD");
        this.package.push(card);

        card = new Card();
        card.dataInit("OBV");
        this.package.push(card);

        card = new Card();
        card.dataInit("숫자카드");
        this.package.push(card);


    }

    start () {
        
    }

    displayCards(){

    }

    // update (dt) {}
}
