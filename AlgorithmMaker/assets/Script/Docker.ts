// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class Docker extends cc.Component {

    @property(cc.Node)
    block : cc.Node = null;

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


        if(this.block === null){
            this.block = this.node.parent;
        }
    }
    start () {
        this.init();
    }

    onCollisionEnter(other: cc.Collider, self: cc.Collider){
        
        /*if(other.node.group === "slot" && ){

        }*/
    }

    onCollisionStay(other: cc.Collider, self: cc.Collider){

    }
    onCollisionExit(other: cc.Collider, self: cc.Collider){

    }

    // update (dt) {}
}
