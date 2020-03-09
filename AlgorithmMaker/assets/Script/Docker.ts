import Block from "./Block";

// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class Docker extends cc.Component {

    @property(Block)
    block : Block = null;

    isConnected = false;
    connectedTo = null;
    groupDepth = 0;
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}
    init(){
        // Physics 켜주는 코드
        if(cc.director.getCollisionManager().enabled === false){
            cc.director.getCollisionManager().enabled = true;
        }

    }
    start () {
        this.init();
    }


    //부모로 Collision Foward
    onCollisionEnter(other:cc.Collider, self:cc.Collider){
        this.block.onCollisionEnter(other, self);
    }
    onCollisionStay(other:cc.Collider, self:cc.Collider){
        this.block.onCollisionStay(other, self);

    }
    onCollisionExit(other:cc.Collider, self:cc.Collider){
        this.block.onCollisionExit(other, self);

    }

    // update (dt) {}
}
