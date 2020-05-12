// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import HandItem from "./HandItem";
import HandMAnager from "./HandManager";
import BlockList from "./BlockList";
import Block from "./Block";

const {ccclass, property} = cc._decorator;

@ccclass
export default class Card extends HandItem {

    @property(cc.Label)
    lblCardName : cc.Label = null;

    blockList : BlockList = null;
    
    getType(): string {
        return 'Card';
    }

    createdBlock : Block = null;
    draggedUp = false;
    
    getRandomArbitrary(min, max) {
        return Math.random() * (max - min) + min;
    }
    description : string = null;
    onClick(): Function {
        console.log(this.description);
        
        return;
    }

    init(name){
        this.lblCardName = name;
    }
    testInit(){
        this.description = 'z';
    }


    // LIFE-CYCLE CALLBACKS:
    createThreshold = 0;
    onLoad () {
         //Getting Car Node
  
    let mouseDown = false;
    //Record mouse click status when user clicks
    this.node.on(cc.Node.EventType.MOUSE_DOWN, (event)=>{
        mouseDown = true;
    });

    this.node.on(cc.Node.EventType.MOUSE_LEAVE, (event)=>{
        this.createdBlock = null;
        mouseDown = false;
    });

    
    //Drag and drop only when the user presses the mouse
    this.node.on(cc.Node.EventType.MOUSE_MOVE, (event)=>{
        if(!mouseDown) return;
        //Get the information of the last point of the mouse distance
        let delta = event.getDelta();
        //Adding qualifications
        this.createThreshold += delta.y;
        //console.log(this.createThreshold);
        
        if(this.createThreshold > 50 && this.createdBlock == null){
            this.createdBlock = this.createdBlock = BlockList.getInstance().addBlockWithEvent(event);

            //this.createThreshold = 0;
            //mouseDown = false;
            this.draggedUp = true;
            console.log("block created");
        }
        else if(this.draggedUp && this.createThreshold < 50 && this.createdBlock != null){
            this.createdBlock.node.destroy();
            this.createdBlock = null;
            this.draggedUp = false;
            console.log("block destroied");
        }
        else if(this.createThreshold < 50){
            this.draggedUp = false;
        }


    });
    //Restore state when mouse is raised
    this.node.on(cc.Node.EventType.MOUSE_UP, (event)=>{
        if(this.createdBlock != null){
            this.createdBlock.mouseUpEventHandler(event);
        }
        mouseDown = false;
        this.createThreshold = 0;
        this.draggedUp = false;
        this.createdBlock = null;
    });
    }

    start () {

    }

    

    // update (dt) {}
}
