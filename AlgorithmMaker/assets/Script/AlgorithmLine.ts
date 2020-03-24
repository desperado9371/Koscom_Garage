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
        //한개 이상인경우엔 그냥 기존 라인 삭제
        if(this.node.parent.childrenCount > 1){
            var block = this.startBlock;
            while(true){
                var nextBlock = this.startBlock.nextBlock;
                block.node.destroy();
                if(nextBlock === null){
                    break;
                }
                block = nextBlock;
            }

            this.node.destroy();
        }
        //남은 그룹이 한개인경우엔 내용을 지우지 않고 줄인다.
        else{

            //첫라인을 지울경우 start block 제외하고 지워줌
            var block = this.startBlock.nextBlock;
            while(block != null){
                var nextBlock = this.startBlock.nextBlock;
                block.node.destroy();
                if(nextBlock === null){
                    break;
                }
                block = nextBlock;
            }
            this.node.destroy();


            this.group.active = false;
            this.plusButton.active = true;
            this.startBlock.node.active = false;

        }
        //this.minusButton.active = false;
    }

    


    init(lineParent:cc.Node, blockParent:cc.Node){
        this.group.active = false;
        this.plusButton.active = true;
        this.startBlock.node.active = false;
        this.startBlock.init(50, 1, '시작블록', '', true);

        /*var onMinusClick = new cc.Component.EventHandler();
        onMinusClick.target = lineParent;
        onMinusClick.component = 'LineList';
        onMinusClick.handler = 'removeLine';*/
        
        
        var onPlusClick = new cc.Component.EventHandler();
        onPlusClick.target = lineParent;
        onPlusClick.component = 'LineList';
        onPlusClick.handler = 'addLine';

        this.plusButton.getComponent(cc.Button).clickEvents.push(onPlusClick);
        //this.minusButton.getComponent(cc.Button).clickEvents.push(onMinusClick);
        

        this.startBlock.node.setParent(blockParent);
        
    }
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {

    }

    // update (dt) {}
}
