import EventHandler from "./EventHandler"

// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class MouseManager extends cc.Component {

    mouseEvent : cc.Event.EventMouse;
    mousePos : cc.Vec2 = new cc.Vec2();
    downObject : EventHandler = null;
    // LIFE-CYCLE CALLBACKS:

    physicsManager : cc.PhysicsManager = null;
    init(){
        cc.director.getCollisionManager().enabled = true;
        this.physicsManager = cc.director.getPhysicsManager();
        this.physicsManager.enabled = true;
        this.node.on(cc.Node.EventType.MOUSE_MOVE, this.mouseMoveEventHandler, this);

    }
    start () {
       this.init();
        
    }

    mouseMoveEventHandler(event){
        this.mousePos = event.getLocation();
    }

    mouseDownEventHandler(event : cc.Event.EventTouch){
        var touchLoc = event.getLocation();
        var collider = this.physicsManager.testPoint(touchLoc);
        console.log(collider + ": " + touchLoc);
        
        if(collider != null){
            var handler = collider.node.getComponent(EventHandler);
            handler.touchDownHandler(event);
            this.downObject = handler;
        }
    }

    mouseUpEventHandler(event : cc.Event.EventTouch){
        var touchLoc = event.getLocation();
        var collider = this.physicsManager.testPoint(touchLoc);
        if(collider != null){
            var handler = collider.node.getComponent(EventHandler);
            handler.touchDownHandler(event);
            if(this.downObject != null){
                this.downObject.touchUpHandler(event);
            }
        }
    }

    getMousePos() : cc.Vec2{
        return this.mousePos;
    }

    getMouseDelta() : cc.Vec2{
        return this.mouseEvent.getDelta();
    }


    onDisable(){
        cc.director.getCollisionManager().enabled = false;
    }
}

