import WebSocketConnect from "./WebSocket/WebSocketConnect";
import AlgorithmLine from "./AlgorithmLine";
import Block from "./Block";
import Card from "./Card";
import LineList from "./LineList";
import BlockList from "./BlockList";
import TutorialManager from "./TutorialManager";

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

    @property(cc.Node)
    popupParent : cc.Node = null;
    @property(cc.Prefab)
    popupSave : cc.Prefab = null;
    @property(cc.Prefab)
    popupSaveTooltip : cc.Prefab = null;

    @property(cc.ScrollView)
    buyScrollView :cc.ScrollView = null;
    @property(cc.ScrollView)
    sellScrollView :cc.ScrollView = null;


    setScrollActive(active){
        this.buyScrollView.enabled = active;
        this.sellScrollView.enabled = active;

    }
    isBuy = true;
    switchBuySell(isBuy){

        this.isBuy = !isBuy;

        
        
        
        this.buyScrollView.node.active = !this.isBuy;
        this.lineParent.active = !this.isBuy;
        this.blockParent.active = !this.isBuy;
        this.buyUnderline.active = !this.isBuy;
        this.sellScrollView.node.active = this.isBuy;
        this.sellBlockParent.active = this.isBuy;
        this.sellLineParent.active = this.isBuy;
        this.sellUnderline.active = this.isBuy;
        
        this.isBuy = this.lineParent.active;
    }

    showSaveTooltip(){
        cc.instantiate(this.popupSaveTooltip).setParent(this.popupParent);
    }
    showSavePopup(){
        cc.instantiate(this.popupSave).setParent(this.popupParent);
        this.scheduleOnce(function() {
            // Here `this` is referring to the component
            TutorialManager.getInstance().nextTutorialByIndex(11);
        }, 0.1);
        
    }

    switchToBuy(){
        this.switchBuySell(true);
    }

    switchToSell(){
        TutorialManager.getInstance().nextTutorialByIndex(6);
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

    deleteCookie(name: string){
        document.cookie = name + '=; expires=Thu, 01 Jan 1999 00:00:10 GMT;';
    }


    SaveAlgorithm(algorithmName :string, memo :string){

        if(algorithmName == '' || algorithmName == null){
            algorithmName = 'test_algo';
        }
        var json : any = {} ;
        var jsonIn : any = {}
        jsonIn.market = "upbit";
        jsonIn.srt_date = "20190101";
        jsonIn.end_date = "20200415";
        jsonIn.buysell = "buy";
        jsonIn.srt_time = "00";
        jsonIn.end_time = "24";
        jsonIn.hourday_tp = "hour";

        
        var algoLines = this.lineParent.getComponentsInChildren(AlgorithmLine);
        for(var k = 0; k < algoLines.length; k++){
            var j = algoLines[k].toJson();
            if(j != null){
                jsonIn["block" + (k+1)] = j;
            }
        }
        json.algo =jsonIn;

        if(algoLines.length == 1 && algoLines[0].isEmpty() == true){
            json = "";
        }
        
        var sellJson : any = {} ;
        var sellJsonIn : any = {}
        sellJsonIn.market = "upbit";
        sellJsonIn.srt_date = "20190101";
        sellJsonIn.end_date = "20200415";
        sellJsonIn.buysell = "sell";
        sellJsonIn.srt_time = "00";
        sellJsonIn.end_time = "24";
        sellJsonIn.hourday_tp = "hour";
        
        var sellAlgoLines = this.sellLineParent.getComponentsInChildren(AlgorithmLine);
        
        
        for(var k = 0; k < sellAlgoLines.length; k++){
            var j = sellAlgoLines[k].toJson();
            if(j != null){
                sellJsonIn["block" + (k+1)] = j;
            }
        }
        sellJson.algo =sellJsonIn;

        if(sellAlgoLines.length == 1 && sellAlgoLines[0].isEmpty() == true){
            sellJson = "";
        }
        
        var user_id = this.getCookie('username');
        if(user_id == null){
            user_id = 'test_user';
        }

        var buy = json == "" ? '' : JSON.stringify(json);
        var sell = sellJson == "" ? '' : JSON.stringify(sellJson);


        WebSocketConnect.getSock().send('save|'+user_id+'|'+algorithmName+'|'+buy+'|'+sell+'|'+memo);

    }
    
    requestIndicators(){
        WebSocketConnect.getSock().send('Indicators');
    }

    sending = false;
    loadAlgorithm(seq){
        //WebSocketConnect.getSock().send('load|test_user|12', this, 'load');
        this.sending = true;
        var user_id = this.getCookie('username');
        if(user_id == null){
            user_id = 'test_user';
        }
        WebSocketConnect.getSock().send('load|'+user_id+'|' + seq, this, 'load');

    }

    testLoadAlgorithm(){
        var user_id = this.getCookie('username');
        if(user_id == null){
            user_id = 'test_user';
        }
        WebSocketConnect.getSock().send('load|'+user_id+'|all', this, 'load');
    }

    parseAlgorithm(algorithm : string,  algorithmName : string = ''){

        var json = (0, eval)('(' + algorithm + ')');


        

        
        var buyAlgo;
        var sellAlgo;
        if(algorithmName == null || algorithmName == ''){
            json = json.items[json.items.length-1];
            buyAlgo = json.buy_algo;
            sellAlgo = json.sell_algo;
        }
        else{
            for(var k =0; k < json.length ; k++){
                if(json.items[k].algo_nm == algorithmName){
                    json = json.items[k];
                    buyAlgo = json.buy_algo.algo;
                    sellAlgo = json.sell_algo.algo;
                }
            }
        }

        buyAlgo = (0, eval)('(' + buyAlgo + ')');
        sellAlgo = (0, eval)('(' + sellAlgo + ')');

        var blocks;
        var min, max;
        //buy algo 
        blocks = buyAlgo.algo;


        for(var k = 0; true; k++){
            //create line
            var lines = this.lineParent.getComponentsInChildren(AlgorithmLine);
            var blkNum = k + 1;
            if(k >= lines.length){
                break;
            }
            lines[k].onPlusButtonClick();
            var block = blocks["block"+blkNum];
                    if(block == null){
                        break;
                    }

            min = block.min;
            max = block.max;
    
            if(min != max){
                lines[k].changeCondition();
            }
            //line setting done

            for(var j = 0; j < block.total_count; j++){
                //create group
                var blockList = this.blockParent.getComponent(BlockList);
                
                 

                var groupNum = j + 1;
                var group = block["group"+groupNum];
                var prevCard = null;
                var sign = null;
                for(var i = 0; i < group.length; i++){
                    //create card

                    var card = group[i];
                    var cardName = card.name;
                    var variables = card.val;
                    if(cardName == 'sig'){
                        sign = card.val;
                        continue;
                    }
                    var newBlock = blockList.addBlock();

                    
                    newBlock.init(0,0, cardName, '');
                    if(cardName == 'num'){
                        newBlock.setBodyString(variables);
                    }
                    else{
                        newBlock.setBodyString(variables[Object.keys(variables)[0]]);
                    }
                    if(i == 0){
                        
                        newBlock.dockToFirstSlot(lines[k].groupList.elementAtIndex(j));
                        lines[k].groupList.elementAtIndex(j).targetBlock = newBlock;
                        prevCard = newBlock;
                    }
                    else{
                        newBlock.dockToOtherBlock(prevCard);
                        newBlock.relationSymbol.getComponent(cc.Label).string = sign;
                        sign = null;
                        prevCard = newBlock;
                    }
                }
                /*for (var key in group) {
                    console.log(' name=' + key + ' value=' + group[key]);

                }*/
            }
        }

        //sell algo

        blocks = sellAlgo.algo;


        for(var k = 0; true; k++){
            //create line
            var lines = this.sellLineParent.getComponentsInChildren(AlgorithmLine);
            var blkNum = k + 1;
            if(k >= lines.length){
                break;
            }
            lines[k].onPlusButtonClick();
            var block = blocks["block"+blkNum];
                    if(block == null){
                        break;
                    }

            min = block.min;
            max = block.max;
    
            if(min != max){
                lines[k].changeCondition();
            }
            //line setting done

            for(var j = 0; j < block.total_count; j++){
                //create group
                var blockList = this.sellBlockParent.getComponent(BlockList);
                
                 

                var groupNum = j + 1;
                var group = block["group"+groupNum];
                var prevCard = null;
                var sign = null;
                for(var i = 0; i < group.length; i++){
                    //create card

                    var card = group[i];
                    var cardName = card.name;
                    var variables = card.val;
                    if(cardName == 'sig'){
                        sign = card.val;
                        continue;
                    }
                    var newBlock = blockList.addBlock();

                    
                    newBlock.init(0,0, cardName, '');
                    if(cardName == 'num'){
                        newBlock.setBodyString(variables);
                    }
                    else{
                        newBlock.setBodyString(variables[Object.keys(variables)[0]]);
                    }

                    if(i == 0){
                        newBlock.dockToFirstSlot(lines[k].groupList.elementAtIndex(j));
                        lines[k].groupList.elementAtIndex(j).targetBlock = newBlock;
                        prevCard = newBlock;
                    }
                    else{
                        newBlock.dockToOtherBlock(prevCard);
                        newBlock.relationSymbol.getComponent(cc.Label).string = sign;
                        sign = null;
                        prevCard = newBlock;
                    }
                }
                /*for (var key in group) {
                    console.log(' name=' + key + ' value=' + group[key]);

                }*/
            }
        }
        this.loaded = true;
        this.deleteCookie('algo_seq');
    }


    



    onRecieveIndicators(json : string){
        var indicators: JSON = JSON.parse(json);
        var jsonRoot = Object.getOwnPropertyNames(indicators);
        
    }

    loaded = false;
    tryTime = 0;
    update (dt) {
        this.tryTime += dt;
        if(this.tryTime > 2 && this.loaded == false){
            this.tryTime = 0;
            this.sending = false;
            var loadSeq = this.getCookie('algo_seq');
            if(loadSeq != null && this.sending == false){
                this.loadAlgorithm(loadSeq);
            }
        }

    }
}
