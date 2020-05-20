// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class FollowObject extends cc.Component {

    @property(cc.Node)
    target: cc.Node = null;

    @property(cc.Vec2)
    offset: cc.Vec2 = null;


    start () {

    }

    update (dt) {
        this.node.setPosition(this.node.position.x ,this.target.position.y - this.target.height+ this.offset.y)
    }
}
