// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import Block from "./Block";
import BlockGroup from "./BlockGroup";
import FileManager from "./FileManager";
import Card from "./Card";

const {ccclass, property} = cc._decorator;

@ccclass
export default class PropertyBox extends cc.Component {
    @property(Card)
    insideCard : Card = null;
    @property(cc.Label)
    lblCategory : cc.Label = null;
    
    @property(cc.Label)
    lblSummary : cc.Label = null;

    
    @property(cc.Label)
    lblCalc : cc.Label = null;

    
    @property(cc.Label)
    lblDetail : cc.Label = null;

    
    @property(cc.Label)
    lblExplanation : cc.Label = null;

    
    @property(cc.Label)
    lblHowToUse : cc.Label = null;

    block : Block = null;
    group : BlockGroup = null;
    // LIFE-CYCLE CALLBACKS:
    cardData : {} = null;

    static instance : PropertyBox = null;
    static getInstance() : PropertyBox{

        return PropertyBox.instance;
    }
    onLoad () {
        PropertyBox.instance = this;
    }
    onBlockClick(block : Block){
        this.lblCategory.node.parent.active = true;
        var cardName = block.getCardName().toLowerCase();
        if(cardName == '숫자카드'){
            return;
        }
        if(this.cardData == null){
            this.cardData =  FileManager.getInstance().cardData;
        }



        this.insideCard.init(cardName);
        this.lblCategory.string = this.cardData[cardName].category;
        this.lblSummary.string = this.cardData[cardName].summary;
        this.lblCalc.string = this.cardData[cardName].calc;
        this.lblDetail.string = this.cardData[cardName].detail;
        this.lblExplanation.string = this.cardData[cardName].explanation;
        this.lblHowToUse.string = this.cardData[cardName].how_to_use;

    }
    onCardClick(card : Card){
        this.lblCategory.node.parent.active = true;
        var cardName = card.getCardName().toLowerCase();
        if(cardName == '숫자카드'){
            return;
        }
        if(this.cardData == null){
            this.cardData =  FileManager.getInstance().cardData;
        }

        if(cardName.includes("\r\n")){
            cardName = cardName.replace("\r\n", "|");
        }

        this.insideCard.init(cardName);
        this.lblCategory.string = this.cardData[cardName].category;
        this.lblSummary.string = this.cardData[cardName].summary;
        this.lblCalc.string = this.cardData[cardName].calc;
        this.lblDetail.string = this.cardData[cardName].detail;
        this.lblExplanation.string = this.cardData[cardName].explanation;
        this.lblHowToUse.string = this.cardData[cardName].how_to_use;

    }
    onSaveButton(){

    }
    start () {
        this.lblCategory.node.parent.active = false;
    }

    // update (dt) {}
}
