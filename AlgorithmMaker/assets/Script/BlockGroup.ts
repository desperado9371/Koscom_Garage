import LinkedList from "./Collections/LinkedList"
import Block from "./Block";

// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class BlockGroup extends cc.Component {

    
    list : LinkedList<Block> = new LinkedList();
    // LIFE-CYCLE CALLBACKS:
    /**
     *
     */

    onLoad () {

    }

    start () {

    }

    addBlockHead(block : Block){
        if(!this.list.contains(block)){
            this.list.add(block);
        }
    }
    removeBlockHead(block : Block){
        if(this.list.contains(block)){
            this.list.remove(block);
        }
    }

    lateUpdate(){
        var l = this.list;
        if(this.list.size() <= 0){
            return;
        }

        var block = this.list.firstNode;
        while(block != null){
            
            var pos = block.element.node.position;
            var tmpBlock = block.element;
            while(tmpBlock != null){
                tmpBlock.node.setPosition(pos);
                pos.x += 138;
                tmpBlock = tmpBlock.nextBlock;
            }

            block = block.next;
        }
    }

    onCollisionEnter(other:cc.Collider, self:cc.Collider){
        if(other.node.group === 'block')
        {
            var blk = other.node.getComponent(Block);
            if(blk.connectedSlot == null){
                this.addBlockHead(blk);
            }
        }
    }
    onCollisionStay(other:cc.Collider, self:cc.Collider){

    }
    onCollisionExit(other:cc.Collider, self:cc.Collider){
        if(other.node.group === 'block')
        {
            var blk = other.node.getComponent(Block);
            if(blk.connectedSlot == null){
                this.removeBlockHead(blk);
            }
        }
    }

    // update (dt) {}
}
