// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import { LinkedList } from "./Collections";
import TutorialHand from "./TutorialHand";

const {ccclass, property} = cc._decorator;

@ccclass
export default class TutorialManager extends cc.Component {

    static instance : TutorialManager = null;
    static getInstance() : TutorialManager{

        return TutorialManager.instance;

    }
    @property(cc.Node)
    tutorialParent: cc.Node = null;
    @property(cc.Node)
    highlightParent: cc.Node = null;

    @property(cc.Node)
    rootCanvas : cc.Node = null;

    @property(TutorialHand)
    tutorialHand : TutorialHand = null;

    @property(cc.Node)
    squareMask : cc.Node = null;
    @property(cc.Node)
    ellipseMask : cc.Node = null;
    // LIFE-CYCLE CALLBACKS:

    isTutorial = false;
    // onLoad () {}

    @property(cc.Node)
    testFrom : cc.Node = null;
    @property(cc.Node)
    testTo : cc.Node = null;



    ws : WebSocket;
    mode = "";
    start () {

        //this.clickTutorial(this.testFrom);
        TutorialManager.instance = this;
        this.ws = new WebSocket("ws:/13.124.102.83:80/ControlMem");
        this.ws.onopen = this.onOpen;
        this.ws.onmessage = this.onRecieve;
        this.ws.onclose = this.onClose;
        
        //this.tutorialStart();
        
    }

    onOpen(event){
        TutorialManager.getInstance().tutorialCheck();
    }
    onClose(event){

    }
    onRecieve(event){
        console.log("Tutorial data recieved : " + event.data);
        this.index = 0;

        if(event.data == "0"){
            TutorialManager.getInstance().tutorialStart();
        }
        
        else{
            //TutorialManager.getInstance().tutorialDone();
        }
    }

    tutorialStart(){
        this.isTutorial = true;

        this.tutorialList = new LinkedList<string>();
        this.tutorialList.add('AlgorithmMain/buyView/scrollview/view/content/buyLineParent/[0]');//1
        this.tutorialList.add('HandScroll/scrollview/view/content/[1]');//2
        this.tutorialList.add('HandScroll/scrollview/view/content/[1]|AlgorithmMain/buyView/scrollview/view/content/buyLineParent/[0]/BlockGroup/BlankGroup');//3
        this.tutorialList.add('RedoButton');//4
        this.tutorialList.add('HandScroll/scrollview/view/content/[5]|AlgorithmMain/buyView/scrollview/view/content/buyLineParent/[0]/BlockGroup/FilledGroup')//5
        this.tutorialList.add('AlgorithmMain/btnSell');//6
        this.tutorialList.add('AlgorithmMain/sellView/scrollview/view/content/sellLineParent/[0]');//7
        this.tutorialList.add('HandScroll/scrollview/view/content/[5]|AlgorithmMain/sellView/scrollview/view/content/sellLineParent/[0]/BlockGroup/BlankGroup');//8
        this.tutorialList.add('HandScroll/scrollview/view/content/[1]');//9
        this.tutorialList.add('HandScroll/scrollview/view/content/[1]|AlgorithmMain/sellView/scrollview/view/content/sellLineParent/[0]/BlockGroup/FilledGroup');//10
        this.tutorialList.add('AlgorithmMain/btnSave');//11
        this.tutorialList.add('PopopParent/[0]/body/btnSave');//12


        this.tutorialParent.active = true;
        this.highlightParent.active = true;
        this.tutorialHand.node.active = true;
        console.log("tutorial started");
        this.nextTutorial();
    }

    tutorialCheck(){
        this.mode = "check";
        var userID = this.getCookie('username');
        //this.ws.send("load|dbtest123");
        this.ws.send("load|" + userID);
    }

    tutorialDone(){
        var userID = this.getCookie('username');
        if(this.isTutorial){
            this.ws.send("update|" + userID);
        }
        this.isTutorial = false;
        this.tutorialParent.active = false;
        this.highlightParent.active = false;
        this.tutorialHand.node.active = false;
        //this.ws.send("update|dbtest123");
    }
    getCookie(name: string): string {
        const nameLenPlus = (name.length + 1);
        return document.cookie
            .split(';')
            .map(c => c.trim())
            .filter(cookie => {
                return cookie.substring(0, nameLenPlus) === `${name}=`;
            })
            .map(cookie => {
                return decodeURIComponent(cookie.substring(nameLenPlus));
            })[0] || null;
    }

    tutorialList : LinkedList<string> = null;
    index = 0;
    current : LinkedList<cc.Node> = null;
    hideHighlight(){
        this.squareMask.active = false;
        this.ellipseMask.active  = false;
    }
    nextTutorial(){
        
        this.clickObject = null;
        if(this.isTutorial == false){
            return;
        }
        if(this.index >= this.tutorialList.size()){
            this.tutorialDone();
            return;
        }

        var tutoStr = this.tutorialList.elementAtIndex(this.index);
        if(tutoStr.includes('|')){

  
            var split = tutoStr.split('|');
            var from = this.findObject(split[0], 0);
            var to = this.findObject(split[1], 0); 
            this.dragTutorialTest(from,to);
        
            //this.dragTutorialTest(from, to);
        }
        else{
            var click = this.findObject(tutoStr, 0);
            this.clickTutorial(click);
        }
        this.index++;
    }

    clickObject :cc.Node = null;

    clickTutorial(target : cc.Node){
        this.squareMask.active = true;
        this.ellipseMask.active = false;
        var gPos = target.convertToWorldSpaceAR(cc.Vec2.ZERO);      
        var nodePos = this.squareMask.parent.convertToNodeSpaceAR(gPos);

        var mask = this.squareMask;
        mask.anchorX = target.anchorX;
        mask.anchorY = target.anchorY;

        mask.setPosition(nodePos);
        mask.width = target.width;
        mask.height = target.height;
        this.clickObject = target;
        this.tutorialHand.clickTween(target);
    }
    nextTutorialByIndex(index) : boolean{
        if(this.isTutorial && index == this.index){
            this.nextTutorial();
            return true;
        }
        return false;
    }
    dragTutorial(from : cc.Node, to : cc.Node){

        this.squareMask.active = false;
        this.ellipseMask.active = true;
        var gPos = from.convertToWorldSpaceAR(cc.Vec2.ZERO);      
        var fromPos = this.ellipseMask.parent.convertToNodeSpaceAR(gPos);
        var gPosTo = to.convertToWorldSpace(cc.Vec2.ZERO);   
        var toPos = this.ellipseMask.parent.convertToNodeSpaceAR(gPosTo);
        var calc = fromPos.add(toPos).divide(2);
        var widthHeight = new cc.Vec2();
        console.log(toPos +" ------" + fromPos);

        widthHeight.x = fromPos.x < toPos.x ? toPos.x - fromPos.x  : fromPos.x - toPos.x;
        widthHeight.y = fromPos.y < toPos.y ? toPos.y - fromPos.y  : fromPos.y - toPos.y;
        
        
        
        this.ellipseMask.setPosition(calc);

        
        console.log("width, height  "+widthHeight + "-----  centerPos" + calc);
        this.ellipseMask.width = widthHeight.x + 100;
        this.ellipseMask.height = widthHeight.y + 50;


        this.tutorialHand.scrollTween(from, to);
    }


    dragTutorialTest(from: cc.Node, to :cc.Node){
        this.squareMask.active = false;
        this.ellipseMask.active = true;

        if(this.index == 4 || this.index == 9){
            var fakenode = cc.instantiate(new cc.Node());
            fakenode.setParent(to);
            fakenode.anchorX = to.anchorX;
            fakenode.anchorY = to.anchorY;
            fakenode.height = to.height;
            fakenode.width = to.width;
            fakenode.setPosition(fakenode.width/2,0,0);
            to = fakenode;
        }


        var gPos = from.convertToWorldSpaceAR(cc.Vec2.ZERO);    
        var gPosTo = to.convertToWorldSpace(cc.Vec2.ZERO); 
        gPosTo.y += to.height; 
        
        //first box
        var mask = this.ellipseMask;
        var firstMask = mask;
        
        var firstPos = mask.parent.convertToNodeSpaceAR(gPos);
        firstMask.anchorX = from.anchorX;
        firstMask.anchorY = from.anchorY;
        firstMask.setPosition(firstPos.x, firstPos.y);
        firstMask.width = from.width;
        firstMask.height = from.height;
        
        //second box
        mask = mask.children[0];
        var secondMask = mask;
        secondMask.anchorX = to.anchorX;
        secondMask.anchorY = to.anchorY;

        var secondPos = secondMask.parent.convertToNodeSpaceAR(gPosTo);
        secondMask.width = to.width;
        secondMask.height = to.height;
        secondMask.setPosition(secondPos);

        //third diagonal box
        mask = mask.children[0];

        gPosTo.y -= to.height /2;
        gPosTo.x += to.width / 2;
        var first = firstMask.convertToWorldSpaceAR(cc.Vec2.ZERO);      
        var second = secondMask.convertToWorldSpace(cc.Vec2.ZERO);
        var firstNS = mask.parent.convertToNodeSpaceAR(gPos);
        var secondNS = mask.parent.convertToNodeSpaceAR(gPosTo);
        secondNS = secondNS.subtract(new cc.Vec2(0,secondMask.height));

        var vec = new cc.Vec2((gPos.x - gPosTo.x ), (gPos.y - gPosTo.y ));
        var length = Math.sqrt((vec.x * vec.x) + (vec.y * vec.y));
        var pos = new cc.Vec2((gPos.x + gPosTo.x )/ 2, (gPos.y + gPosTo.y )/ 2);
        vec.normalizeSelf();
        var angle = Math.atan2(vec.x, vec.y) * (180 / 3.141592);
        
        cc.Vec2.lerp(pos, gPos, gPosTo, 0.5);
        
        pos = mask.parent.convertToNodeSpaceAR(pos);
        mask.setPosition(pos);
        mask.rotation = (angle - 90);
        mask.width = length;
        mask.height = 100;


        this.tutorialHand.scrollTween(from, to);
    }

    highLightObjects(index){
        var list = this.tutorialList.elementAtIndex(index);
        this.current = new LinkedList<cc.Node>();

        for(var k = 0; k < list.length; k++){
            var path = list[k];
            var obj = this.findObject(path, 0)
            this.current.add(obj);
            obj.setParent(this.highlightParent);
        }
    }

    returnObjects(index){
        var list = this.tutorialList.elementAtIndex(index);

        for(var k = 0; k < list.length; k++){
            var path = list[k];
            var obj = this.findObject(path, -1)
            this.current.elementAtIndex(k).setParent(obj);
        }
    }

    findObject(str: string, offset){
        var path = str.split('/');
        var root = this.rootCanvas;
        var target : cc.Node = root;
        for(var k = 0; k < path.length - offset; k++){
            if(path[k].includes('[')){
                var number = path[k].replace('[','').replace(']','');
                target = target.children[number];
            }
            else{
                target = target.getChildByName(path[k]);
            }
        }

        return target;
    }




    
    found = false;
    update (dt) {
        
        if(this.clickObject != null && this.squareMask != null){
            var mask = this.squareMask;
            mask.width = this.clickObject.width;
            mask.height = this.clickObject.height;

            
        }
    }
}
