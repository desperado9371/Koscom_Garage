// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class CAnimation extends cc.Component {

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
    callbackEvent :[Function] ;

    isPlaying = false;
    isCallbackCalled = false;
    currentTime = 0;
    forward = 0;
    startAnimWithCallback(func : [Function]){
        this.currentTime = 0.00001;
        this.isCallbackCalled = false;
        this.isPlaying = true;
        this.forward = 1;
        this.callbackEvent = func;
    }


    startAnimBackward(){
        this.currentTime = this.duration.valueOf()-0.00001;
        this.isCallbackCalled = false;
        this.forward = -1;
        this.isPlaying = true;
    }
    startAnim(){
        this.currentTime = 0.00001;
        this.isCallbackCalled = false;
        this.forward = 1;
        this.isPlaying = true;
        this.callbackEvent.push(this.startAnimBackward);
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

    }
    stopAnimation(){
        this.isPlaying = false;
        this.forward = 0;
    }

    setCallback(callbacks : [Function]){
        this.callbackEvent = callbacks;
    }

    addCallback(f : Function){
        this.callbackEvent.push(f);
    }

    update (dt) {/*
        if(this.isPlaying === false){
            return;

        }
        
        

        var posRes : cc.Vec3 = new cc.Vec3();
        cc.Vec3.lerp(posRes, this.posFrom, this.posTo, this.currentTime/this.duration.valueOf());
        var scaleRes : cc.Vec3 = new cc.Vec3();
        cc.Vec3.lerp(scaleRes, this.scaleFrom, this.scaleTo, this.currentTime/this.duration.valueOf());

        console.log(this.node.name + " = " +posRes + " ... " +scaleRes);
        
        this.node.setPosition(posRes);
        this.node.scaleX = scaleRes.x;
        this.node.scaleY = scaleRes.y;

        if(this.currentTime > this.duration && this.forward > 0){
            if(this.isCallbackCalled === false){
                

                    if(this.callbackEvent != null){
                        for(var k = 0; k < this.callbackEvent.length; k++){
                            this.callbackEvent[k]();
                        }
                        this.callbackEvent = null;
                    }

                
                this.isCallbackCalled = true;
                this.isPlaying = false;
            }
            this.currentTime = this.duration.valueOf();
        }
        else if( this.currentTime < 0 && this.forward < 0){
            if(this.isCallbackCalled === false){

                    if(this.callbackEvent != null){
                        for(var k = 0; k < this.callbackEvent.length; k++){
                            this.callbackEvent[k]();
                        }
                        this.callbackEvent = null;
                    }

                
                this.isCallbackCalled = true;
                this.isPlaying = false;
            }
            this.currentTime = 0;
        }
        this.currentTime += dt * this.forward;
    }*/
}
