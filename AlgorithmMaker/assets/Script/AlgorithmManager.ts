import WebSocketConnect from "./WebSocket/WebSocketConnect";
import AlgorithmLine from "./AlgorithmLine";

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



    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {
        //화면대응
        cc.view.resizeWithBrowserSize(true);
        cc.view.setDesignResolutionSize(1280, 720, cc.ResolutionPolicy.SHOW_ALL);
        
    }

    SaveAlgorithm(){
        var json : any = {} ;
        var jsonIn : any = {}
        jsonIn.market = "upbit";
        jsonIn.srt_date = "20200102";
        jsonIn.end_date = "20200110";
        jsonIn.buysell = "buy";
        
        var algoLines = this.lineParent.getComponentsInChildren(AlgorithmLine);
        for(var k = 0; k < algoLines.length; k++){
            var j = algoLines[k].toJson();
            if(j != null){
                jsonIn["block" + (k+1)] = j;
            }
        }
        json.algo =jsonIn;
        
        console.log(JSON.stringify(json));
        
        WebSocketConnect.getSock().send('save|test_user|test_algo_name|'+JSON.stringify(json)+'|');

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
