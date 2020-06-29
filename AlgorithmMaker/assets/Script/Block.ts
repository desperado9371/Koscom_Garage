import MouseManager from "./MouseManager";
import DockingSlot from "./DockingSlot"
import PropertyBox from "./PropertyBox";
import BlockGroup from "./BlockGroup";
import TutorialManager from "./TutorialManager";
import AlgorithmManager from "./AlgorithmManager";

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
export default class Block extends cc.Component {

    static offset = 157;
    @property(MouseManager)
    mouseManager : MouseManager = null;

    @property({type: BlockColor})
    color = BlockColor.Brown
    @property(cc.Node)
    title: cc.Node = null;
    @property(cc.Node)
    body: cc.Node = null;

    @property(cc.Node)
    relationSymbol: cc.Node = null;

    @property(cc.Node)
    relationCircle: cc.Node = null;

    @property(cc.Node)
    alterRelationParent:cc.Node = null;

    propertyBox : PropertyBox = null;

    @property
    initOnLoad = false;

    getBodyString(){
        return this.body.getComponentInChildren(cc.EditBox).string;
    }
    setBodyString(str){
        this.body.getComponentInChildren(cc.EditBox).string = str;
    }
    toJson(){
        var json :any = {};
        var val : any = {};
        var cardName = this.title.getComponentInChildren(cc.Label).string.toLowerCase();

        json.name = cardName;
        if(cardName == 'macd'){
            val.close = "50000";
            val.n_fast = "5";
            val.n_slow = "3";
            val.n_sign = "5";
        }
        else if(cardName == 'rsi'){

            val.period = this.getBodyString();
        }
        else if(cardName == 'obv'){
            val = {};

        }
        else if(cardName.includes('macd') ){
            json.name = 'macd_signal';
            val.n_fast= "6",
            val.n_slow= "2",
            val.n_sign= "5"
        }
        else if(cardName.includes('스토캐스틱') || cardName == 'stoch'){
            json.name = 'stoch';
            val.period = this.getBodyString();
        }
        else if(cardName == 'adi'){
            val = {};
        }
        else if (cardName == 'open' || cardName == 'close' || cardName == 'high' || cardName == 'low'){
            val = {};
        }
        else if(cardName == 'ao'){
            val.long = "34";
            val.short = "5";
        }
        else if(cardName == 'tsi'){
            val.high = "25";
            val.low = "13";
        }
        else if(cardName.includes("볼린저밴드")){
            if(cardName.includes("상한선")){
                json.name = 'bollinger_hband';
            }
            else if(cardName.includes("하한선")){
                json.name = 'bollinger_lband';
            }
            else if(cardName.includes("중심선")){
                json.name = 'bollinger_mband';
            }
            else if(cardName.includes("밴드폭")){
                json.name = 'bollinger_wband';
            }
            val.period = this.getBodyString();
        }

        else{
            val.period = this.getBodyString();
        }
        
        
        
        



        
        if(cardName == '숫자카드'){
            json.name = 'num';
            json.val = this.getBodyString();
        }
        else{
            json.val = val;
        }

        

        return json;

    }

    sigToJson(){
        var json :any = {};
        var symbol = this.relationSymbol.getComponent(cc.Label).string;

        json.name = "sig";
        json.val = symbol;

        return json;
    }

    // LIFE-CYCLE CALLBACKS:

    getRandomArbitrary(min, max) {
        return Math.random() * (max - min) + min;
    }
      
    initWithRand(){
        this.init(150, this.getRandomArbitrary(0,5), 'Title' + this.getRandomArbitrary(0,500), 'Body');
    }

    getCardName(){
        return this.title.getComponentInChildren(cc.Label).string;
    }


    init(width:number, color:number, cardName:string, bodyText:string, isStuck:boolean = false){
        if(this.mouseManager == null){
            this.mouseManager = MouseManager.getInstance();
        }
        if(this.title == null){
            this.title = this.node.getChildByName("title");
        }
        
        if(cc.director.getCollisionManager().enabled == false){
            cc.director.getCollisionManager().enabled = true;
        }

        cardName = cardName.toLowerCase();
        this.title.getComponentInChildren(cc.Label).string = cardName;
        
        if(cardName == 'macd'){
            this.title.getComponentInChildren(cc.Label).string = 'MACD';
            this.body.active = false;
        }
        else if (cardName == 'open' || cardName == 'close' || cardName == 'high' || cardName == 'low' || cardName == 'volume'){
            this.body.active = false;
        }
        else if(cardName.includes('macd') ){
            this.title.getComponentInChildren(cc.Label).string = 'MACD\r\n시그널';
            this.body.active = false;
        }
        else if(cardName == 'adi') {
            this.body.active = false;
        }
        else if(cardName == 'stoch' || cardName.includes('스토캐스틱')){
            this.body.active = false;
        }
        else if(cardName == 'tsi' || cardName == 'ao'){
            this.body.active = false;
        }
        else if(cardName == 'rsi' ){
            var tm = TutorialManager.getInstance();
            if(tm.isTutorial){

                if(tm.index == 10){

                    this.relationSymbol.getComponent(cc.Label).string = "<";
                }
            }
            this.setBodyString('14');
        }
        else if(cardName == 'obv'){
            this.body.active = false;

        }
        if(cardName == 'num' || cardName == '숫자카드'){
            this.title.getComponentInChildren(cc.Label).string = '숫자카드';
            this.setBodyString('50');
            var tutoIndex = TutorialManager.getInstance().index;
            if(tutoIndex == 5){
                this.setBodyString(20);
                this.relationSymbol.getComponent(cc.Label).string = "<";
            }
            else if(tutoIndex == 8){
                this.setBodyString(80);
            }
        }
        else if(cardName.includes("bollinger") || cardName.includes("볼린저")) {
            if(cardName.includes("hband") || cardName.includes('상한선')){
                this.title.getComponentInChildren(cc.Label).string = '볼린저밴드\r\n상한선';
            }
            else if(cardName.includes("lband")|| cardName.includes('하한선')){
                this.title.getComponentInChildren(cc.Label).string = '볼린저밴드\r\n하한선';
            }
            else if(cardName.includes("mband")|| cardName.includes('중심선')){
                this.title.getComponentInChildren(cc.Label).string = '볼린저밴드\r\n중심선';
            }
            else if(cardName.includes("wband")|| cardName.includes('밴드폭')){
                this.title.getComponentInChildren(cc.Label).string = '볼린저밴드\r\n밴드폭';
            }
            this.setBodyString('20');
        }
        else if(cardName == 'cci' || cardName == 'cmf'){
            this.setBodyString('20');
        }
        else if(cardName == 'atr' || cardName == 'adx' || cardName == 'mfi'  ){
            this.setBodyString('14');
        }
        else if( cardName == 'fi'){
            this.setBodyString('13');
        }
        else if(cardName == 'trix'){
            this.setBodyString('15');
        }
        else if(cardName == 'roc'){
            this.setBodyString('12');
        }

        


        //this.node.width = width;
        this.color = color;
        
        //this.body.getComponent(cc.Label).string = bodyText;
        


        //마우스 이벤트 코드 설정
        //property box로 연동위해 준비
        if(this.propertyBox == null){
            var parent = this.node;
            while(true){
                if(parent.parent.name === "Canvas"){
                    parent = parent.parent;
                    break;
                }
                parent = parent.parent;
            }
            this.propertyBox = parent.getComponentInChildren(PropertyBox);
        }


        if(isStuck === false){
            this.node.on(cc.Node.EventType.TOUCH_END, this.mouseUpEventHandler, this);
            this.node.on(cc.Node.EventType.TOUCH_CANCEL, this.mouseUpEventHandler, this);
            this.node.on(cc.Node.EventType.TOUCH_START, this.mouseDownEventHandler, this);
        }


    }
    onLoad () {
        if(this.initOnLoad){
            
            this.init(100, this.getRandomArbitrary(0,5), 'Title', 'Body');
        }
    }


    //드래그 이동에 관한 변수들
    isDown = false;
    startPos : cc.Vec2 = new cc.Vec2();
    dPos: cc.Vec2 = new cc.Vec2();
    nodePos : cc.Vec3 = new cc.Vec3();
    unstickThreshold = 100;
    start () {

    }
    
    setRelationActive(active){
        if(this.relationSymbol.active == !active){

            this.relationSymbol.active = active;
            this.relationCircle.active = active;
        }
    }
    update (dt) {
 
        //포지션 이동 설정
        if(this.isDown === true){
            var mousePos = this.mouseManager.getMousePos();
            //붙은 블록이 있는지에 따라 따라 붙음
            if(this.connectedSlot != null){
                this.dPos.x = this.stuckPos.x - mousePos.x;
                this.dPos.y = this.stuckPos.y - mousePos.y;
                if(this.dPos.len() > this.unstickThreshold){
                    if(this.connedtedMode == 'slot'){
                        this.connectedSlot.getComponent(DockingSlot).block.getComponent(Block).nextBlock = null;
                        this.connectedSlot = null;

                    }
                    else if(this.connedtedMode == 'firstSlot'){
                        var comp = this.connectedSlot.node.parent.parent.getComponent(BlockGroup);
                        this.connectedSlot = null;
                        comp.disableGroup();

                        
                    }
                    this.connedtedMode = '';
                }
                else{
                    this.updatePos();
                }


            }
            else{

                this.dPos.x = this.startPos.x - mousePos.x;
                this.dPos.y = this.startPos.y - mousePos.y;
                this.node.setPosition(this.nodePos.x - this.dPos.x, 
                                     this.nodePos.y - this.dPos.y);
                /*console.log(new cc.Vec2(this.nodePos.x - this.dPos.x, 
                    this.nodePos.y - this.dPos.y).toString());*/
                

            }
            


        }

        //다른 블록에 끌려가는 것
        if(this.isDown === false){

            this.updatePos();
        }


        if(this.connedtedMode == 'slot'){
            this.setRelationActive(true);
        }
        else if(this.connedtedMode == 'firstSlot'){
            this.setRelationActive(false);
        }
        else{//nothing attached
            this.setRelationActive(false);
        }

        
    }
    onRelationChangeButton(){
        this.alterRelationParent.active = true;
    }
    onRelationChangeClick(sender){
        var send = sender.currentTarget as cc.Node;
        var comp = send.getComponentInChildren(cc.Label);
        this.relationSymbol.getComponent(cc.Label).string = comp.string;
        this.alterRelationParent.active = false;
    }

    updatePos(){
        if(this.connectedSlot != null  && this.connedtedMode == 'slot'){
            var otherBlock = this.connectedSlot.getComponent(DockingSlot).block;
            this.node.setPosition(otherBlock.position.x + Block.offset, otherBlock.position.y);
                       
        }
        else if(this.connectedSlot != null  && this.connedtedMode == 'firstSlot'){
            var comp = this.connectedSlot.node.parent.parent.getComponent(BlockGroup);
            if(comp.targetBlock == null ){
                return;
            }
            var otherSlot = this.connectedSlot.node.parent;
            var gPos = otherSlot.convertToWorldSpaceAR(otherSlot.position);      
            var lPos = this.node.parent.convertToNodeSpaceAR(gPos);
            this.node.setPosition(lPos.x, lPos.y);
        }
    }

    lateUpdate(){
        this.updatePos();
    }

    setScrollActive(active){
        AlgorithmManager.getInstance().setScrollActive(active);
    }

    mouseUpEventHandler(event){
        this.setScrollActive(true);
        if(this.isDown == true){
            console.debug("mouse up called");
            this.isDown = false;
            this.propertyBox.onBlockClick(this);
        }
        if(this.connedtedMode == 'firstSlot'){
            TutorialManager.getInstance().nextTutorialByIndex(3);
            TutorialManager.getInstance().nextTutorialByIndex(8);

        }
        else if(this.connedtedMode == 'slot'){
            TutorialManager.getInstance().nextTutorialByIndex(10);
            TutorialManager.getInstance().nextTutorialByIndex(5);

        }
    }


    mouseDownEventHandler(event){
        if(this.mouseManager == null){
            this.mouseManager = MouseManager.getInstance();
        }
        this.setScrollActive(false);
        if(this.isDown == false){
            this.stuckPos.x = this.mouseManager.getMousePos().x;
            this.stuckPos.y = this.mouseManager.getMousePos().y;
            this.startPos = this.mouseManager.getMousePos();
            this.nodePos = this.node.position;
            this.isDown = true;
        }



        console.debug("mouse down called");
    }

    mouseRemoteDownEventHandler(event, x, y){
        if(this.mouseManager == null){
            this.mouseManager = MouseManager.getInstance();
        }
        this.mouseManager.movingBlock = this;
        //this.setScrollActive(false);
        if(this.isDown == false){
            this.stuckPos.x = this.mouseManager.getMousePos().x;
            this.stuckPos.y = this.mouseManager.getMousePos().y;
            this.startPos = this.mouseManager.getMousePos();
            this.isDown = true;
            
            var eventLoc = event.getLocation();
            
            
            var loc = this.node.convertToNodeSpaceAR(new cc.Vec2(this.stuckPos.x, this.stuckPos.y));
            this.nodePos = new cc.Vec3(loc.x, loc.y, 0);
            this.node.setPosition(this.nodePos);

        }


        console.debug("mouse down called");
    }

    mouseRemoteUpEventHandler(event){
        if(this.isDown == true){
            console.debug("mouse up called");
            this.isDown = false;
            this.propertyBox.onBlockClick(this);
        }
        //this.setScrollActive(true);
        if(this.connedtedMode == 'firstSlot'){
            TutorialManager.getInstance().nextTutorialByIndex(3);
            TutorialManager.getInstance().nextTutorialByIndex(8);

        }
        else if(this.connedtedMode == 'slot'){
            TutorialManager.getInstance().nextTutorialByIndex(10);
            TutorialManager.getInstance().nextTutorialByIndex(5);

        }
    }

    connedtedMode = '';
    connectedSlot : cc.Collider = null;
    nextBlock : Block = null;
    stuckPos : cc.Vec3 = new cc.Vec3();
    onCollisionEnter(other:cc.Collider, self:cc.Collider){
        if(other.node.group === 'group' && self.node.group === 'block')
        {
            
        }
        else if(other.node.group === 'firstSlot' && self.node.group === 'block'){
            
            if(this.connectedSlot === null){
                var comp = other.node.parent.parent.getComponent(BlockGroup);
                if(comp.targetBlock != null){
                    return;
                }
                this.connedtedMode = 'firstSlot';
                comp.activateGroup(this);
                this.connectedSlot = other;
                this.stuckPos.x = this.mouseManager.getMousePos().x;
                this.stuckPos.y = this.mouseManager.getMousePos().y;
                comp.parentLine.addEmptyGroup();
                
            }
            
            
            
        }
        else{
            if(this.isDown === true && self.node.group === 'docker' && other.node.group === 'slot'){
                if(this.connectedSlot === null){
                    var nextBlock = other.getComponent(DockingSlot).block.getComponent(Block).nextBlock;
                    if(nextBlock != null){
                        return;
                    }
                    this.connedtedMode = 'slot';
                    
                    this.connectedSlot = other;

                    other.getComponent(DockingSlot).block.getComponent(Block).nextBlock = this;
                    this.stuckPos.x = this.mouseManager.getMousePos().x;
                    this.stuckPos.y = this.mouseManager.getMousePos().y;
                }
            }
        }
    }

    dockToFirstSlot(other : BlockGroup){
        var comp = other;
        if(comp.targetBlock != null){
            return;
        }
        this.connedtedMode = 'firstSlot';
        comp.activateGroup(this);
        //this.connectedSlot = other.node.getChildByName('hitbox').getComponent(cc.Collider);
        this.connectedSlot = other.node.getChildByName('BlankGroup').getChildByName('hitbox').getComponent(cc.Collider);

        this.stuckPos.x = this.mouseManager.getMousePos().x;
        this.stuckPos.y = this.mouseManager.getMousePos().y;
        comp.parentLine.addEmptyGroup();
    }
    dockToOtherBlock(other : Block){
        var nextBlock = other.nextBlock;
        if(nextBlock != null){
            return;
        }
        this.connedtedMode = 'slot';
        
        this.connectedSlot = other.node.getChildByName('Relation').getChildByName('dockingSlot').getComponent(cc.Collider);

        other.nextBlock = this;
        this.stuckPos.x = this.mouseManager.getMousePos().x;
        this.stuckPos.y = this.mouseManager.getMousePos().y;
    }
    onCollisionStay(other:cc.Collider, self:cc.Collider){

    }
    onCollisionExit(other:cc.Collider, self:cc.Collider){

    }

}
