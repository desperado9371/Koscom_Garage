import MouseManager from "./MouseManager";
import DockingSlot from "./DockingSlot"
import PropertyBox from "./PropertyBox";
import BlockGroup from "./BlockGroup";

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

    propertyBox : PropertyBox = null;

    @property
    initOnLoad = false;

    hideRelation(){
        if(this.relationSymbol.active == true){
            
            this.relationSymbol.active = false;
        }
    }
    showRelation(){
        if(this.relationSymbol.active == false){

            this.relationSymbol.active= true;
        }
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

            val.input_period = "14";
        }
        else if(cardName == 'obv'){
            val.input_volume = "10";

        }
        if(cardName == 'num'){
            
            json.val = this.body.getComponentInChildren(cc.Label).string;
            
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

    init(width:number, color:number, titleText:string, bodyText:string, isStuck:boolean = false){
        
        if(this.title == null){
            this.title = this.node.getChildByName("title");
        }
        
        if(cc.director.getCollisionManager().enabled == false){
            cc.director.getCollisionManager().enabled = true;
        }

        //this.node.width = width;
        this.color = color;
        //this.title.getComponent(cc.Label).string = titleText;
        //this.body.getComponent(cc.Label).string = bodyText;


        //색상 설정
        if(this.title != null){
            switch(this.color){
                case BlockColor.Brown:
                    this.title.color = new cc.Color(140,71,3,235);
                break;
                case BlockColor.Blue:
                    this.title.color = new cc.Color(26,95,186,235);
                break;
                case BlockColor.Red:
                    this.title.color = new cc.Color(175,26,26,235);
                break;
                case BlockColor.Gray:
                    this.title.color = new cc.Color(71,71,71,235);
                break;
                case BlockColor.LightGold:
                    this.title.color = new cc.Color(140,140,71,235);
                break;
                case BlockColor.DarkPurple:
                    this.title.color = new cc.Color(71,71,95,235);
                break;
            }
            
        }


        //마우스 이벤트 코드 설정
        //property box로 연동위해 준비
        if(this.mouseManager == null || this.propertyBox == null){
            var parent = this.node;
            while(true){
                if(parent.parent.name === "Canvas"){
                    parent = parent.parent;
                    break;
                }
                parent = parent.parent;
            }
            this.mouseManager = parent.getComponentInChildren(MouseManager);
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
    unstickThreshold = 40;
    start () {

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
                    else{
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

    mouseUpEventHandler(event){
        if(this.isDown == true){
            console.debug("mouse up called");
            this.isDown = false;
            this.propertyBox.onBlockClick(this);
        }
    }

    mouseDownEventHandler(event){
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
                this.connedtedMode = 'firstSlot';
                var comp = other.node.parent.parent.getComponent(BlockGroup);
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
                    this.connedtedMode = 'slot';
                    
                    this.connectedSlot = other;
                    other.getComponent(DockingSlot).block.getComponent(Block).nextBlock = this;
                    this.stuckPos.x = this.mouseManager.getMousePos().x;
                    this.stuckPos.y = this.mouseManager.getMousePos().y;
                }
            }
        }
    }
    onCollisionStay(other:cc.Collider, self:cc.Collider){

    }
    onCollisionExit(other:cc.Collider, self:cc.Collider){

    }

}
