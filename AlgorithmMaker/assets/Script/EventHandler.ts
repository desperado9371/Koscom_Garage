// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default abstract class EventHandler extends cc.Component{
    abstract touchDownHandler(event : cc.Event.EventTouch)  : void;
    abstract touchCancel(event : cc.Event.EventTouch)  : void;
    abstract touchUpHandler(event : cc.Event.EventTouch)  : void;
}
