// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import AlgorithmLine from "./AlgorithmLine";

const {ccclass, property} = cc._decorator;

@ccclass
export default class LineList extends cc.Component {

    @property(cc.Prefab)
    line:cc.Prefab =  null;

    @property(cc.Node)
    blockParent:cc.Node = null;

    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    number = 1;
    start () {
        this.addLine();

    }
    
    addLine(){
        var newLine = cc.instantiate(this.line);
        
        newLine.setParent(this.node);
        var lineComp = newLine.getComponent(AlgorithmLine);
        lineComp.init(this.node, this.blockParent);
        lineComp.setConditionNumber(this.number);
        this.number++;
        newLine.active= true;
        newLine.position = new cc.Vec3(0,0,0);

        return lineComp;
    }

    removeLine(){
        
    }

    // update (dt) {}
}
