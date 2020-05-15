// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import Block from "./Block";
import LineList from "./LineList";
import { LinkedList } from "./Collections";
import BlockGroup from "./BlockGroup";


const {ccclass, property} = cc._decorator;

@ccclass
export default class AlgorithmLine extends cc.Component {



    @property(cc.Node)
    group: cc.Node = null;

    @property(cc.Node)
    plusButton: cc.Node = null;

    @property(cc.Node)
    minusButton: cc.Node = null;

    @property(cc.Node)
    emptyGroup: cc.Node = null;



    static ySpacing = 240;
    static xSpacing = 50;
    static xThreshold = 500;
    static baseHeight = 240;

    groupList : LinkedList<BlockGroup> = null;
    toJson(){
        var json : any = {};

        if(this.groupList.size() == 0){
            return null;
        }

        json.min = (this.groupList.size()-1).toString();
        json.max = (this.groupList.size()-1).toString();
        json.total_count = (this.groupList.size()-1).toString();
        for(var k = 1; k <= this.groupList.size(); k++){
            var j = this.groupList.elementAtIndex(k-1).toJson();
            if(j != null){
                
                json["group"+k] = j;
            }
        }


        return json;

    }
    addEmptyGroup(){
        var newNode = cc.instantiate(this.emptyGroup);
        var comp = newNode.getComponent(BlockGroup);
        comp.parentLine = this;
        newNode.setParent(this.node);
        
        var lastGroup = this.groupList.last();
        
        //first to add
        var xPos = 0;
        var yPos = 0;
        
        //first group position
        /*if(lastGroup == null){
            xPos = 20;
            yPos = -34;
        }
        else{
            
            xPos = lastGroup.node.position.x + lastGroup.filledGroup.width + AlgorithmLine.xSpacing;
            yPos = lastGroup.node.position.y;
            
            if(xPos > AlgorithmLine.xThreshold){
                yPos -= AlgorithmLine.ySpacing;
                xPos = 20;
            }
        }*/
        
        this.groupList.add(comp);
        newNode.setPosition(xPos, yPos);
        newNode.active = true;
        this.repositionGroups();
        this.resizeLine();
        
    }
    resizeLine(){
        var firstGroup = this.groupList.first();
        var lastGroup = this.groupList.last();

        var yDiff = (firstGroup.node.position.y - lastGroup.node.position.y) /  AlgorithmLine.ySpacing;
        this.node.height = AlgorithmLine.baseHeight + AlgorithmLine.ySpacing * yDiff;


    }

    repositionGroups(){
        
        var prevGroup : BlockGroup = null;
        var xPos = 0;
        var yPos = 0;
        for(var k = 0; k < this.groupList.size(); k++){
            var elem = this.groupList.elementAtIndex(k);
            if(prevGroup == null){
                xPos = 20;
                yPos = -34;
            }
            else{
                
                xPos = prevGroup.node.position.x + prevGroup.filledGroup.width + AlgorithmLine.xSpacing;
                yPos = prevGroup.node.position.y;
                
                if(xPos > AlgorithmLine.xThreshold){
                    
                    yPos -= AlgorithmLine.ySpacing;
                    xPos = 20;
                }
            }
            elem.node.setPosition(xPos, yPos);
            prevGroup = elem;
            
        }
    }
    removeGroup(group : BlockGroup){
        this.groupList.remove(group);
        group.node.destroy();
    }
    repositionStartBlock(){

    }
    onPlusButtonClick(){
        this.group.active = true;
        this.plusButton.active = false;
        this.addEmptyGroup();
    }
   
    


    init(lineParent:cc.Node, blockParent:cc.Node){
        this.group.active = false;
        this.plusButton.active = true;
        //this.startBlock.node.active = false;
        //this.startBlock.init(150, 1, '시작블록', '', true);

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
        

        //this.startBlock.node.setParent(blockParent);
        
    }
    // LIFE-CYCLE CALLBACKS:

    onLoad () {
        if(this.groupList == null){
            this.groupList = new LinkedList<BlockGroup>();
        }
    }

    start () {
        
    }

    
    update (dt) {
        var cnt = 0;
        this.repositionGroups();
        for(var k = 0; k < this.groupList.size(); k++){
            var elem = this.groupList.elementAtIndex(k);
            if(elem.targetBlock == null){
                cnt++;
            }
            if(cnt > 1){
                this.removeGroup(elem);
                return;
            }
        }
    }
}
