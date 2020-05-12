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

    static instance : BlockList = null;
    static getInstance() : BlockList{
        if(this.instance === null){
            var node = cc.instantiate(new cc.Node());
            var hm = node.addComponent(BlockList);
            BlockList.instance = hm;
        }
        return BlockList.instance;
    }
    onLoad () {
        if(BlockList.instance === null){
            BlockList.instance = this;
        }
    }
    addBlock(){
        var blk = cc.instantiate(this.block);
        var comp = blk.getComponent(Block);
        blk.setParent(this.node);
        blk.setPosition(0,0,0);

        return comp;
    }

    addBlockAt(x, y){
        var blk = cc.instantiate(this.block);
        var comp = blk.getComponent(Block);
        var loc = this.node.convertToNodeSpace(new cc.Vec2(x,y));
        blk.setParent(this.node);
        blk.setPosition(loc.x, loc.y, 0);
        
    }

    addBlockWithEvent(event): Block{
        var blk = cc.instantiate(this.block);
        var comp = blk.getComponent(Block);
        var eventLoc = event.getLocation();
        
        console.log("EventSpace " + eventLoc + blk.position);
        var loc = this.node.convertToNodeSpaceAR(new cc.Vec2(eventLoc.x, eventLoc.y));
        blk.setParent(this.node);
        console.log("NodeSpace " + loc+ blk.position);
        comp.initWithRand();
        comp.mouseRemoteDownEventHandler(event, loc.x, loc.y);
        //blk.setPosition(loc.x, loc.y, 0);
        //console.log(blk.position);
        return comp;
    }

    start () {

    }

    // update (dt) {}
}
