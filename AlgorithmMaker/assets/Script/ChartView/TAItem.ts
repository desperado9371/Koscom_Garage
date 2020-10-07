// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class TAItem extends cc.Component {

    @property(cc.Label)
    title: cc.Label = null;
    @property(cc.Label)
    percent: cc.Label = null;

    @property(cc.Label)
    tradeCount: cc.Label = null;

    @property(cc.Sprite)
    percentageBg :cc.Sprite = null;

    @property(cc.SpriteFrame)
    lossFrame : cc.SpriteFrame = null;

    @property(cc.SpriteFrame)
    profitFrame : cc.SpriteFrame = null;

    setTitle(text){
        this.title.string = text;
    }
    setPercent(number){
        if(number < 0){
            this.percentageBg.spriteFrame = this.lossFrame;
        }
        else{
            this.percentageBg.spriteFrame = this.profitFrame;


        }
        this.percent.string = number + "%";
    }

    setTradeCount(number){
        this.tradeCount.string = number + "회";
    }

    // update (dt) {}
}
