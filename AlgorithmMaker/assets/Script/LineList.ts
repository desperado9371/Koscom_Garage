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

    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {
        this.addLine();
    }
    
    addLine(){
        var newLine = cc.instantiate(this.line);
        newLine.setParent(this.node);
        newLine.getComponent(AlgorithmLine).init(this.node);
        newLine.active= true;
        newLine.position = new cc.Vec3(0,0,0);
    }

    removeLine(index:number){
        this.node.removeChild(this.node.children[index]);
    }

    // update (dt) {}
}
