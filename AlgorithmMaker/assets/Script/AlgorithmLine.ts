// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class AlgorithmLine extends cc.Component {



    @property(cc.Node)
    group: cc.Node = null;

    @property(cc.Node)
    plusButton: cc.Node = null;

    @property(cc.Node)
    minusButton: cc.Node = null;


    onPlusButtonClick(){
        this.group.active = true;
        this.plusButton.active = false;
        this.minusButton.active = true;
    }
    onMinusButtonClick(){
        this.group.active = false;
        this.plusButton.active = true;
        this.minusButton.active = false;
    }
    init(){
        this.group.active = false;
        this.plusButton.active = true;
        this.minusButton.active = false;
    }
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {
        this.init();
    }

    // update (dt) {}
}
