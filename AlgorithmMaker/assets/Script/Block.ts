import MouseManager from "./MouseManager";
import DockingSlot from "./DockingSlot"

// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html
const BlockColor = cc.Enum ({			
    Brown : 0,
    Blue: 1,
    Red: 2, 
    Gray: 3, 
    LightGold: 4, 
    DarkPurple: 5,	
});
const {ccclass, property} = cc._decorator;

@ccclass
export default class Block extends cc.Component {

    
    @property(MouseManager)
    mouseManager : MouseManager = null;

    @property({type: BlockColor})
    color = BlockColor.Brown
    @property(cc.Node)
    title: cc.Node = null;
    @property(cc.Node)
    body: cc.Node = null;

    @property(cc.Node)
    relationSymbol: cc.Node = null;

    @property
    initOnLoad = false;


    // LIFE-CYCLE CALLBACKS:

    getRandomArbitrary(min, max) {
        return Math.random() * (max - min) + min;
    }
      
    initWithRand(){
        this.init(100, this.getRandomArbitrary(0,5), 'Title' + this.getRandomArbitrary(0,500), 'Body');
    }

    init(width:number, color:number, titleText:string, bodyText:string, isStuck:boolean = false){
        
        if(this.title == null){
            this.title = this.node.getChildByName("title");
        }
        
        if(cc.director.getCollisionManager().enabled == false){
            cc.director.getCollisionManager().enabled = true;
        }

        this.node.width = width;
        this.color = color;
        //this.title.getComponent(cc.Label).string = titleText;
        //this.body.getComponent(cc.Label).string = bodyText;


        //색상 설정
        if(this.title != null){
            switch(this.color){
                case BlockColor.Brown:
                    this.title.color = new cc.Color(140,71,3,235);
                break;
                case BlockColor.Blue:
                    this.title.color = new cc.Color(26,95,186,235);
                break;
                case BlockColor.Red:
                    this.title.color = new cc.Color(175,26,26,235);
                break;
                case BlockColor.Gray:
                    this.title.color = new cc.Color(71,71,71,235);
                break;
                case BlockColor.LightGold:
                    this.title.color = new cc.Color(140,140,71,235);
                break;
                case BlockColor.DarkPurple:
                    this.title.color = new cc.Color(71,71,95,235);
                break;
            }
            
        }


        //마우스 이벤트 코드 설정
        if(this.mouseManager == null){
            var parent = this.node;
            while(true){
                if(parent.parent.name === "Canvas"){
                    parent = parent.parent;
                    break;
                }
                parent = parent.parent;
            }
            this.mouseManager = parent.getComponentInChildren(MouseManager);
        }

        if(isStuck === false){
            this.node.on(cc.Node.EventType.TOUCH_END, this.mouseUpEventHandler, this);
            this.node.on(cc.Node.EventType.TOUCH_CANCEL, this.mouseUpEventHandler, this);
            this.node.on(cc.Node.EventType.TOUCH_START, this.mouseDownEventHandler, this);
        }


    }
    onLoad () {
        if(this.initOnLoad){
            
            this.init(100, this.getRandomArbitrary(0,5), 'Title', 'Body');
        }
    }


    //드래그 이동에 관한 변수들
    isDown = false;
    startPos : cc.Vec2 = new cc.Vec2();
    dPos: cc.Vec2 = new cc.Vec2();
    nodePos : cc.Vec3 = new cc.Vec3();
    unstickThreshold = 40;
    start () {

    }


    update (dt) {
        
        //포지션 이동 설정
        if(this.isDown === true){
            var mousePos = this.mouseManager.getMousePos();
            //붙은 블록이 있는지에 따라 따라 붙음
            if(this.connectedSlot != null){
                this.dPos.x = this.stuckPos.x - mousePos.x;
                this.dPos.y = this.stuckPos.y - mousePos.y;
                if(this.dPos.len() > this.unstickThreshold){
                    this.connectedSlot.getComponent(DockingSlot).block.getComponent(Block).nextBlock = null;
                    this.connectedSlot = null;
                }
                else{
                    var otherBlock = this.connectedSlot.getComponent(DockingSlot).block;
                    this.node.setPosition(otherBlock.position.x + 138, otherBlock.position.y);
                }
            }
            else{
                this.dPos.x = this.startPos.x - mousePos.x;
                this.dPos.y = this.startPos.y - mousePos.y;
                this.node.setPosition(this.nodePos.x - this.dPos.x, 
                                     this.nodePos.y - this.dPos.y);

            }
            


        }

        //다른 블록에 끌려가는 것
        if(this.connectedSlot != null && this.isDown === false){
            var otherBlock = this.connectedSlot.getComponent(DockingSlot).block;
            this.node.setPosition(otherBlock.position.x + 138, otherBlock.position.y);
                       
        }

        
    }

    lateUpdate(){
        //다른 블록에 끌려가는 것
        if(this.connectedSlot != null && this.isDown === false){
            var otherBlock = this.connectedSlot.getComponent(DockingSlot).block;
            this.node.setPosition(otherBlock.position.x + 138, otherBlock.position.y);
                
        }
    }

    mouseUpEventHandler(event){
        if(this.isDown == true){
            console.debug("mouse up called");
            this.isDown = false;

        }
    }

    mouseDownEventHandler(event){
        if(this.isDown == false){
            this.stuckPos.x = this.mouseManager.getMousePos().x;
            this.stuckPos.y = this.mouseManager.getMousePos().y;
            this.startPos = this.mouseManager.getMousePos();
            this.nodePos = this.node.position;
            this.isDown = true;
        }


        console.debug("mouse down called");
    }

    connectedSlot : cc.Collider = null;
    nextBlock : Block = null;
    stuckPos : cc.Vec3 = new cc.Vec3();
    onCollisionEnter(other:cc.Collider, self:cc.Collider){
        if(other.node.group === 'group' && self.node.group === 'block')
        {
            
        }
        else{
            if(this.isDown === true && self.node.group === 'docker'){
                if(this.connectedSlot === null){
                    
                    this.connectedSlot = other;
                    other.getComponent(DockingSlot).block.getComponent(Block).nextBlock = this;
                    this.stuckPos.x = this.mouseManager.getMousePos().x;
                    this.stuckPos.y = this.mouseManager.getMousePos().y;
                }
            }
        }
    }
    onCollisionStay(other:cc.Collider, self:cc.Collider){

    }
    onCollisionExit(other:cc.Collider, self:cc.Collider){

    }

}
