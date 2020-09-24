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

    setTitle(text){
        this.title.string = text;
    }
    setPercent(number){
        if(number < 0){
            this.percent.node.color = cc.Color.BLUE;
        }
        else{
            this.percent.node.color = cc.Color.RED;

        }
        this.percent.string = number + "%";
    }

    // update (dt) {}
}
