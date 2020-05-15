// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import Block from "./Block";
import BlockGroup from "./BlockGroup";

const {ccclass, property} = cc._decorator;

@ccclass
export default class PropertyBox extends cc.Component {
    
    @property(cc.EditBox)
    relationBox: cc.EditBox = null;

    @property(cc.EditBox)
    title: cc.EditBox = null;

    @property(cc.EditBox)
    body: cc.EditBox = null;

    @property(cc.Node)
    workplz:cc.Node = null;


    block : Block = null;
    group : BlockGroup = null;
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}
    onBlockClick(block : Block){
        this.block = block;
        this.title.string = block.title.getComponentInChildren(cc.Label).string;
        this.body.string = block.body.getComponentInChildren(cc.Label).string;
        this.relationBox.string = block.relationSymbol.getComponent(cc.Label).string;
    }
    onSaveButton(){
        if(this.block != null){
            var comp =  this.block.title.getComponentInChildren(cc.Label);
            comp.string = this.title.string;

            var bodyComp = this.block.body.getComponentInChildren(cc.Label);
            bodyComp.string = this.body.string;
            
            this.block.relationSymbol.getComponent(cc.Label).string = this.relationBox.string;
        }
        else if (this.group != null){

        }
    }
    start () {

    }

    // update (dt) {}
}
