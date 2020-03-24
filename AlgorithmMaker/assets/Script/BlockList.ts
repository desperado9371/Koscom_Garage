// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import Block from "./Block";

const {ccclass, property} = cc._decorator;

@ccclass
export default class BlockList extends cc.Component {

    @property(cc.Prefab)
    block:cc.Prefab = null;

    addBlock(){
        var blk = cc.instantiate(this.block);
        var comp = blk.getComponent(Block);
        blk.setParent(this.node);
        blk.setPosition(0,0,0);
        comp.initWithRand();
    }

    start () {

    }

    // update (dt) {}
}
