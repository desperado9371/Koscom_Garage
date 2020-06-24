// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class TutorialHand extends cc.Component {

    @property(cc.Node)
    from : cc.Node = null;

    @property(cc.Node)
    to : cc.Node = null;

    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    tween :cc.Tween = null;
    start () {

    }



    clickTween(target : cc.Node){
        if(this.tween != null){
            this.tween.stop();
        }
        var gPos = target.convertToWorldSpaceAR(cc.Vec2.ZERO);     
        var lPos = this.node.parent.convertToNodeSpaceAR(gPos);

        if(target.anchorX == 0){
            lPos.x += target.width/2;
        }
        if(target.anchorY == 1){
            lPos.y -= target.height/2;
        }
        this.node.setPosition(lPos.x, lPos.y);

        this.tween = cc.tween(this.node).to(0.5,{ scaleX: 1.1, scaleY : 1.1})
        .to(0.5,{ scaleX: 1.0, scaleY : 1.0});
        
        this.tween.repeat(99999999999999999, this.tween).start();
    }

    scrollTween(from : cc.Node, to : cc.Node){
        if(this.tween != null){
            this.tween.stop();
        }
        var gPos = from.convertToWorldSpaceAR(cc.Vec2.ZERO);      
        var fromPos = this.node.parent.convertToNodeSpaceAR(gPos);
        var gPosTo = to.convertToWorldSpace(cc.Vec2.ZERO);   
        var toPos = this.node.parent.convertToNodeSpaceAR(gPosTo);
        toPos = toPos.add(new cc.Vec2(0,to.height));
        
        console.log(toPos +" ------" + fromPos);


        this.tween = cc.tween(this.node)
        .to(0, {position: fromPos, opacity : 255})
        .to(0.5,{ scaleX: 1.1, scaleY : 1.1})
        .to(0.5,{ scaleX: 1.0, scaleY : 1.0})
        .to(2, {position : toPos})
        .to(0.5,{ scaleX: 1.3, scaleY : 1.3, opacity : 0});
        
        this.tween.repeat(99999999999, this.tween).start();
    }


    // update (dt) {}
}
