// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import Block from "./Block";
import LineList from "./LineList";

const {ccclass, property} = cc._decorator;

@ccclass
export default class AlgorithmLine extends cc.Component {



    @property(cc.Node)
    group: cc.Node = null;

    @property(cc.Node)
    plusButton: cc.Node = null;

    @property(cc.Node)
    minusButton: cc.Node = null;

    @property(Block)
    startBlock: Block = null;



    onPlusButtonClick(){
        this.group.active = true;
        this.plusButton.active = false;
        this.startBlock.node.active = true;
        //this.minusButton.active = true;
    }
    onMinusButtonClick(){
        this.group.active = false;
        this.plusButton.active = true;
        this.startBlock.node.active = false;
        //this.minusButton.active = false;
    }


    init(lineParent:cc.Node){
        this.group.active = false;
        this.plusButton.active = true;
        this.startBlock.node.active = false;
        this.startBlock.init(50, 1, '시작블록', '');

        var onMinusClick = new cc.Component.EventHandler();
        onMinusClick.target = lineParent;
        onMinusClick.component = 'LineList';
        onMinusClick.handler = 'removeLine';
        
        
        var onPlusClick = new cc.Component.EventHandler();
        onPlusClick.target = lineParent;
        onPlusClick.component = 'LineList';
        onPlusClick.handler = 'addLine';

        this.plusButton.getComponent(cc.Button).clickEvents.push(onPlusClick);
        this.minusButton.getComponent(cc.Button).clickEvents.push(onMinusClick);
        
        //this.minusButton.active = false;
    }
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {

    }

    // update (dt) {}
}
