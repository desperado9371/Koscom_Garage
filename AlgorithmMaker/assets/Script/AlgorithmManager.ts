import WebSocketConnect from "./WebSocket/WebSocketConnect";
import AlgorithmLine from "./AlgorithmLine";
import Block from "./Block";
import Card from "./Card";

// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class AlgorithmManager extends cc.Component {

    @property(cc.Node)
    lineParent: cc.Node = null;

    @property(cc.Node)
    sellLineParent: cc.Node = null;

    @property(cc.Node)
    blockParent : cc.Node = null;

    @property(cc.Node)
    sellBlockParent : cc.Node = null;

    @property(cc.Node)
    buyUnderline : cc.Node = null;
    @property(cc.Node)
    sellUnderline : cc.Node = null;

    @property(cc.Prefab)
    block : cc.Prefab = null;

    isBuy = true;
    switchBuySell(isBuy){
        this.isBuy = !isBuy;
 
        this.lineParent.active = !this.isBuy;
        this.blockParent.active = !this.isBuy;
        this.buyUnderline.active = !this.isBuy;
        this.sellBlockParent.active = this.isBuy;
        this.sellLineParent.active = this.isBuy;
        this.sellUnderline.active = this.isBuy;
        
        this.isBuy = this.lineParent.active;
    }

    switchToBuy(){
        this.switchBuySell(true);
    }

    switchToSell(){
        this.switchBuySell(false);
    }


    static instance : AlgorithmManager = null;
    static getInstance() : AlgorithmManager{
        return AlgorithmManager.instance;
    }
    onLoad () {
        if(AlgorithmManager.instance === null){
            AlgorithmManager.instance = this;
        }
    }

    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {
        //화면대응
        cc.view.resizeWithBrowserSize(true);
        //cc.view.setDesignResolutionSize(1280, 720, cc.ResolutionPolicy.SHOW_ALL);
        

        this.isBuy = false;
        this.switchToBuy();
    }

    addBlockWithEvent(event, cardInfo :Card): Block{
        var blk = cc.instantiate(this.block);
        var comp = blk.getComponent(Block);
        var eventLoc = event.getLocation();
        
        console.log("EventSpace " + eventLoc + blk.position);
        var loc = this.node.convertToNodeSpaceAR(new cc.Vec2(eventLoc.x, eventLoc.y));
        
        var parent = this.isBuy ? this.blockParent : this.sellBlockParent;
        
        blk.setParent(parent);
        console.log("NodeSpace " + loc+ blk.position);
        comp.init(0, 1, cardInfo.lblCardName.string, "0", false);
        comp.mouseRemoteDownEventHandler(event, loc.x, loc.y);
        //blk.setPosition(loc.x, loc.y, 0);
        //console.log(blk.position);
        return comp;
    }

    SaveAlgorithm(){
        var json : any = {} ;
        var jsonIn : any = {}
        jsonIn.market = "upbit";
        jsonIn.srt_date = "20190101";
        jsonIn.end_date = "20200415";
        jsonIn.buysell = "buy";
        
        var algoLines = this.lineParent.getComponentsInChildren(AlgorithmLine);
        for(var k = 0; k < algoLines.length; k++){
            var j = algoLines[k].toJson();
            if(j != null){
                jsonIn["block" + (k+1)] = j;
            }
        }
        json.algo =jsonIn;
        
        var sellJson : any = {} ;
        var sellJsonIn : any = {}
        sellJsonIn.market = "upbit";
        sellJsonIn.srt_date = "20190101";
        sellJsonIn.end_date = "20200415";
        sellJsonIn.buysell = "sell";
        
        var sellAlgoLines = this.sellLineParent.getComponentsInChildren(AlgorithmLine);
        for(var k = 0; k < sellAlgoLines.length; k++){
            var j = sellAlgoLines[k].toJson();
            if(j != null){
                sellJsonIn["block" + (k+1)] = j;
            }
        }
        sellJson.algo =sellJsonIn;
        
        WebSocketConnect.getSock().send('save|test_user|test_algo_name|'+JSON.stringify(json)+'|'+JSON.stringify(sellJson));

    }
    requestIndicators(){
        WebSocketConnect.getSock().send('Indicators');
    }

    loadAlgorithm(){
        WebSocketConnect.getSock().send('load|test_user|all');

    }

    onRecieveIndicators(json : string){
        var indicators: JSON = JSON.parse(json);
        var jsonRoot = Object.getOwnPropertyNames(indicators);
        
    }

    // update (dt) {}
}
