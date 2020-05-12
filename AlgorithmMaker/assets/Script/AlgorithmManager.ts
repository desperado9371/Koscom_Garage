import WebSocketConnect from "./WebSocket/WebSocketConnect";

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
        var testJson : JSON ;
        testJson = JSON.parse('{\"algo\": {\"min\": \"1\",\"max\": \"1\",\"numCondition\": \"1\",\"conditions\": [{\"blocks\": [{\"name\": \"MACD\",\"candleDuration\": \"1\",\"shortMA\": \"5\",\"longMA\": \"12\",\"calcSymbol\": \"\"},{\"name\": \"CCI\",\"candleDuration\": \"1\",\"value\": \"3\",\"calcSymbol\": \">\"},{\"name\": \"number\",\"value\": \"10\",\"calcSymbol\": \"*\"}]}]}}');
        console.log(JSON.stringify(testJson));
        
        //WebSocketConnect.getSock().send('save|test_user|test_algo_name|'+JSON.stringify(testJson));
        this.requestIndicators();
        

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
