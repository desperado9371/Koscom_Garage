import MouseManager from "./MouseManager";

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
export default class Draggable extends cc.Component {
    
    @property(MouseManager)
    mouseManager : MouseManager = null;

    @property({type: BlockColor})
    color = BlockColor.Brown
    @property(cc.Node)
    title: cc.Node = null;

    @property(cc.Collider)
    magnet: cc.Collider = null;

    @property(cc.Collider)
    slot: cc.Collider = null;

    isSlotOccupied = false;

    // LIFE-CYCLE CALLBACKS:



    init(){

        if(this.title == null){
            this.title = this.node.getChildByName("title");
        }


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
            this.mouseManager = this.node.parent.getComponentInChildren(MouseManager);
        }


        this.node.on(cc.Node.EventType.TOUCH_END, this.mouseUpEventHandler, this);
        this.node.on(cc.Node.EventType.TOUCH_CANCEL, this.mouseUpEventHandler, this);
        this.node.on(cc.Node.EventType.TOUCH_START, this.mouseDownEventHandler, this);
    }
    onLoad () {
        this.init();
    }

    isDown = false;

    startPos : cc.Vec2 = new cc.Vec2();
    dPos: cc.Vec2 = new cc.Vec2();
    nodePos : cc.Vec3 = new cc.Vec3();
    start () {




    }




    update (dt) {
        //console.log(this.dPos);
        if(this.isDown === true){
            this.dPos.x = this.startPos.x - this.mouseManager.getMousePos().x;
            this.dPos.y = this.startPos.y - this.mouseManager.getMousePos().y;
            this.node.setPosition(this.nodePos.x - this.dPos.x, 
                                 this.nodePos.y - this.dPos.y);

            
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
            this.startPos = this.mouseManager.getMousePos();
            this.nodePos = this.node.position;
            this.isDown = true;
        }


        console.debug("mouse down called");
    }
}
