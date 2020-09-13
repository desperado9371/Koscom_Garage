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
    getPriceData(fromDate = "20200401", fromHour = "10", toDate ="20200403", toHour = "15"){
        var sock = new WebSocket("ws://13.124.102.83:80/BackServer_Hr");
        var chart = this;
        sock.onmessage = function(event){
            var data = event.data;
            console.log(data);
            chart.data = eval(data);
            sock.close();
        };
        sock.onopen = function (event){
            sock.send("load|upbit|"+ fromDate+"|"+ toDate+"|"+ fromHour+"|"+ toHour+"|0");
        };
    }

}
