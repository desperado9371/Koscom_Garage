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

    disableGroup(){

        this.filledGroup.active = false;

        var comp = this.blankGroup.getComponent(cc.Sprite);
        comp.enabled = true;
        
        this.targetBlock = null;
    }

    activateGroup(target : Block){
        this.targetBlock = target;
        var comp = this.blankGroup.getComponent(cc.Sprite);
        comp.enabled = false;
    }

    WrapBlocks(startingBlock : Block){
        if(this.filledGroup.active === false){
            
            this.filledGroup.active = true;
        }
        this.targetBlock = startingBlock;
        var count = 0;
        var gPos = startingBlock.node.convertToWorldSpaceAR(startingBlock.node.position);
        var lPos = this.filledGroup.parent.convertToNodeSpaceAR(gPos);
        this.filledGroup.setPosition(lPos.x - 80, lPos.y + 55);
        var temp = startingBlock;
        var sizeX = 30;
        while(temp!= null){
            count++;
            sizeX += 160; // oneBlock size
            temp = temp.nextBlock;
        }
        //sizeX += 30; // maybe extra margin
               
        this.filledGroup.width = sizeX;
        

    }

    update (dt) {
        if(this.targetBlock != null){
            this.WrapBlocks(this.targetBlock);
        }
    }
}
