// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class ChartData extends cc.Component {

    data = null;

    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {
        this.getPriceData();
    }
    getPriceData(fromDate = "20200806", fromHour = "10", toDate ="20200906", toHour = "15"){
        var sock = new WebSocket("ws://15.164.166.28:80/BackServer_Hr");
        //var sock = new WebSocket("ws://15.164.166.28:80/BackServer_Day");
        var chart = this;
        sock.onmessage = function(event){
            var data = event.data;
            console.log(data);
            chart.data = eval(data);
            sock.close();
        };
        sock.onopen = function (event){
            sock.send("load|upbit|"+ fromDate+"|"+ toDate+"|"+ fromHour+"|"+ toHour+"|0|krwbtc");
            //sock.send("load|upbit|20200401|20200403|0|krwbtc");
        };
    }

}
