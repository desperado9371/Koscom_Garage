// Learn cc.Class:
//  - https://docs.cocos.com/creator/manual/en/scripting/class.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

cc.Class({
    extends: cc.Component,

    properties: {
        
        // foo: {
        //     // ATTRIBUTES:
        //     default: null,        // The default value will be used only when the component attaching
        //                           // to a node for the first time
        //     type: cc.SpriteFrame, // optional, default is typeof default
        //     serializable: true,   // optional, default is true
        // },
        // bar: {
        //     get () {
        //         return this._bar;
        //     },
        //     set (value) {
        //         this._bar = value;
        //     }
        // },
    },
    getPriceData(fromDate = "20200401", fromHour = "10", toDate ="20200403", toHour = "15"){
        var sock = new WebSocket("ws://13.124.102.83:80/BackServer_Hr");
        var chart = this;
        sock.onmessage = function(event){
            var data = event.data;
            console.log(data);
            var evalData = eval(data);
            chart.initializeWithData(evalData);
            sock.close();
        };
        sock.onopen = function (event){
            sock.send("load|upbit|"+ fromDate+"|"+ toDate+"|"+ fromHour+"|"+ toHour+"|0");
        };
    },
    initializeWithData(data){

        for(var k = 0; k < data.length; k++){
            var item = data[k];
            var datetime = item[0] + " " + item[1];
    
            addCandle(item[2], item[3], item[4], item[5], datetime);
        }
    },
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {},

    start () {

    },

    // update (dt) {},
});
