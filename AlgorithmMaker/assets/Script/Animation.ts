// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class Animation extends cc.Component {

    @property(cc.Vec3)
    posFrom: cc.Vec3;

    @property(cc.Vec3)
    posTo: cc.Vec3;

    @property(cc.Vec3)
    scaleFrom: cc.Vec3;

    @property(cc.Vec3)
    scaleTo: cc.Vec3;

    @property(Number)
    duration: Number = 5;

    @property(Function)
    callback :Function = null;

    isCallbackCalled = false;
    currentTime = 0;
    forward = 1;
    startAnim(){
        this.currentTime = 0;
        this.isCallbackCalled = false;
        this.forward = 1;
    }

    startAnimBackward(){
        this.currentTime = this.duration.valueOf();
        this.isCallbackCalled = false;
        this.forward = -1;
    }

    whenAnimDone(){
        if(this.forward > 0){
            this.startAnimBackward();
        }
        else{
            this.startAnim();
        }
    }

    start(){
        this.callback = this.whenAnimDone;
        this.startAnim();
    }

    update (dt) {
        this.currentTime += dt * this.forward;
        if(this.currentTime > this.duration && this.forward > 0){
            if(this.isCallbackCalled === false){
                this.callback();
                this.isCallbackCalled = true;
            }
            this.currentTime = this.duration.valueOf();
        }
        else if( this.currentTime < 0 && this.forward < 0){
            if(this.isCallbackCalled === false){
                this.callback();
                this.isCallbackCalled = true;
            }
            this.currentTime = 0;
        }
        var posRes : cc.Vec3 = new cc.Vec3();
        cc.Vec3.lerp(posRes, this.posFrom, this.posTo, this.currentTime/this.duration.valueOf());
        var scaleRes : cc.Vec3 = new cc.Vec3();
        cc.Vec3.lerp(scaleRes, this.scaleFrom, this.scaleTo, this.currentTime/this.duration.valueOf());

        console.log(posRes + " ... " +scaleRes);
        
        this.node.setPosition(posRes);
        this.node.scaleX = scaleRes.x;
        this.node.scaleY = scaleRes.y;

    }
}
