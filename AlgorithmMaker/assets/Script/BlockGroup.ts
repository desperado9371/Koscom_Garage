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

    @property(cc.Label)
    lblNumber: cc.Label = null;

    @property(Block)
    targetBlock : Block;

    @property(cc.Node)
    blankGroup : cc.Node = null;
    
    @property(cc.Node)
    filledGroup : cc.Node = null;

    


    list : LinkedList<Block> = new LinkedList();
    // LIFE-CYCLE CALLBACKS:
    /**
     *
     */

    onLoad () {

    }

    start () {

    }

    init(){
        
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

    WrapBlocks(startingBlock : Block){
        this.targetBlock = startingBlock;
        var count = 0;
        this.node.setPosition(startingBlock.node.x - 30, startingBlock.node.y + 15);
        var temp = startingBlock;
        var sizeX = 30;
        while(temp!= null){
            count++;
            sizeX += 160; // oneBlock size
            temp = temp.nextBlock;
        }
        //sizeX += 30; // maybe extra margin
               
        this.node.width = sizeX;
        

    }

    update (dt) {
        if(this.targetBlock != null){
            this.WrapBlocks(this.targetBlock);
        }
    }
}
