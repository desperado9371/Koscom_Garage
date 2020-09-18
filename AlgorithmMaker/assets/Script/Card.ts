// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import HandItem from "./HandItem";
import HandMAnager from "./HandManager";
import BlockList from "./BlockList";
import Block from "./Block";
import AlgorithmManager from "./AlgorithmManager";
import PropertyBox from "./PropertyBox";
import FileManager from "./FileManager";

const {ccclass, property} = cc._decorator;

@ccclass
export default class Card extends HandItem {

    @property(cc.Sprite)
    imgCardImage : cc.Sprite = null;
    @property(cc.Label)
    lblCardName : cc.Label = null;

    @property(String)
    initCardName : String = "";

    @property(Boolean)
    selfInit : Boolean = false;

    inited = false;
    blockList : BlockList = null;
    cardName = "";
    
    getType(): string {
        return 'Card';
    }

    createdBlock : Block = null;
    draggedUp = false;
    
    getRandomArbitrary(min, max) {
        return Math.random() * (max - min) + min;
    }
    description : string = null;
    onClick(): Function {
        console.log(this.description);
        
        return;
    }
    dataInit(name){
        this.cardName = name;
    }
    init(name){

        this.cardName = name;
        
        if(name.includes("|")){
            this.cardName = name.replace("|", "\r\n");
        }
        if(this.lblCardName!= null){
            this.lblCardName.string = this.cardName;

        }



        var cardName = name.toLowerCase();
        if(cardName == 'macd'){
            this.lblCardName.string = 'MACD';

        }
        else if (cardName == 'open' || cardName == 'close' || cardName == 'high' || cardName == 'low'){

        }
        else if(cardName == 'days_ago')
        {
            this.lblCardName.string = 'n일전 종가';
        }
        else if(cardName.includes('macd') ){
            name = 'MACD|시그널';
            this.cardName = 'MACD|시그널';
            this.lblCardName.string = 'MACD\r\n시그널';
        }
        else if(cardName == 'adi') {

        }
        else if(cardName == 'stoch'){
            name = '스토캐스틱';
            this.cardName = '스토캐스틱';
            this.lblCardName.string = '스토캐스틱';
        }
        else if(cardName == 'tsi' || cardName == 'ao'){
            
        }
        else if(cardName == 'rsi' ){

            
        }
        else if(cardName == 'obv'){
            

        }
        if(cardName == 'num' || cardName == '숫자카드'){
            this.lblCardName.string = '숫자카드';

        }
        else if(cardName.includes("bollinger")) {
            if(cardName.includes("hband")){
                name = '볼린저밴드\r\n상한선';
                this.cardName = '볼린저밴드\r\n상한선';
                this.lblCardName.string  = '볼린저밴드\r\n상한선';
            }
            else if(cardName.includes("lband")){
                name = '볼린저밴드\r\n하한선';
                this.cardName = '볼린저밴드\r\n하한선';
                this.lblCardName.string  = '볼린저밴드\r\n하한선';
            }
            else if(cardName.includes("mband")){
                name = '볼린저밴드\r\n중심선';
                this.cardName = '볼린저밴드\r\n중심선';
                this.lblCardName.string  = '볼린저밴드\r\n중심선';
            }
            else if(cardName.includes("wband")){
                name = '볼린저밴드\r\n밴드폭';
                this.cardName = '볼린저밴드\r\n밴드폭';
                this.lblCardName.string  = '볼린저밴드\r\n밴드폭';
            }
        }
        else if(cardName == 'cci' || cardName == 'cmf'){
            
        }
        else if(cardName == 'atr' || cardName == 'adx' || cardName == 'mfi'  ){
            
        }
        else if( cardName == 'fi'){
            
        }
        else if(cardName == 'trix'){
            
        }
        else if(cardName == 'roc'){
            
        }


        var cardData = FileManager.getInstance().getCardData(name.toLowerCase());
        if(cardData == null){
            this.imgCardImage.node.active = false;
            return;
        }
        this.imgCardImage.node.active = true;
        var category : string = cardData.category;
        if(category.includes('거래량')){
            this.imgCardImage.spriteFrame = FileManager.getInstance().cardVolume;
        }
        else if(category.includes('추세')){
            this.imgCardImage.spriteFrame = FileManager.getInstance().cardTrend;
            
        }
        else if(category.includes('모멘텀')){
            this.imgCardImage.spriteFrame = FileManager.getInstance().cardMomentum;
            
        }
        else if(category.includes('변동성')){
            this.imgCardImage.spriteFrame = FileManager.getInstance().cardPrice;
            
        }

        this.onLoad();

    }
    testInit(){
        this.description = 'z';
    }

    getCardName(){
        return this.cardName;
    }


    // LIFE-CYCLE CALLBACKS:
    createThreshold = 0;
    onLoad () {
         //Getting Car Node
  
        let mouseDown = false;
        //Record mouse click status when user clicks
        this.node.on(cc.Node.EventType.MOUSE_DOWN, (event)=>{
            PropertyBox.getInstance().onCardClick(this);
            mouseDown = true;
        });

        this.node.on(cc.Node.EventType.MOUSE_LEAVE, (event)=>{
            this.createdBlock = null;
            mouseDown = false;
        });

        
        //Drag and drop only when the user presses the mouse
        this.node.on(cc.Node.EventType.MOUSE_MOVE, (event)=>{
            if(!mouseDown) return;
            //Get the information of the last point of the mouse distance
            let delta = event.getDelta();
            //Adding qualifications
            this.createThreshold += delta.y;
            //console.log(this.createThreshold);
            
            if(this.createThreshold > 25 && this.createdBlock == null){
                this.createdBlock = this.createdBlock = AlgorithmManager.getInstance().addBlockWithEvent(event, this);

                //this.createThreshold = 0;
                //mouseDown = false;
                this.draggedUp = true;
                console.log("block created");
            }
            else if(this.draggedUp && this.createThreshold < 25 && this.createdBlock != null){
                this.createdBlock.node.destroy();
                this.createdBlock = null;
                this.draggedUp = false;
                console.log("block destroied");
            }
            else if(this.createThreshold < 25){
                this.draggedUp = false;
            }


        });
        //Restore state when mouse is raised
        this.node.on(cc.Node.EventType.MOUSE_UP, (event)=>{
            if(this.createdBlock != null){
                this.createdBlock.mouseUpEventHandler(event);
            }
            mouseDown = false;
            this.createThreshold = 0;
            this.draggedUp = false;
            this.createdBlock = null;
        });
    }

    start () {

    }

    

    // update (dt) {}
}
