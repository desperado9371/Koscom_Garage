// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html
import {  } from "../Collections/";
import ChartData from "./ChartData";
import TALib from "./TALib";
const {ccclass, property} = cc._decorator;


@ccclass
export default class LineChart extends cc.Component {

    
    @property(cc.Graphics)
    drawing: cc.Graphics = null;

    @property(ChartData)
    chartData : ChartData = null;


    start () {
        if(this.drawing == null){
            this.drawing = this.node.getComponent(cc.Graphics);    

        }

        this.scheduleUpdate();
        this.testTALib();
    }

    testTALib(){
 
        var result = TALib.MACD([1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1], 3, 7, 5);

        console.log(result);
    }

    scheduleUpdate(){
        var chart = this;
        if(this.chartData.data != null && this.chartData.data.length > 0){
            this.testChart();
        }
        else{
            this.scheduleOnce(function() {
                chart.scheduleUpdate();
            }, 0.1);
        }
    }

    testChart(){

        this.drawChart(this.chartData.data, 0, this.chartData.data.length);
        //this.adjustChart(50);
    }
    drawChart(candles, offset, range){
        this.drawing.clear();
        this.drawing.lineWidth = 6;
        //#FF5E99
        this.drawing.strokeColor = new cc.Color(255, 94, 153, 255);

        var start = candles.length - offset - range;
        var maximumValue = Number.MIN_SAFE_INTEGER;
        var minimumValue = Number.MAX_SAFE_INTEGER;


        for(var k = start ; k < candles.length - offset; k++){
            var item = candles[k];
            maximumValue = Math.max(maximumValue, item[5]);
            minimumValue = Math.min(minimumValue, item[4]);
        }

        var middle = maximumValue - ((maximumValue - minimumValue) / 2)
        var yScale = this.drawing.node.height / (maximumValue - minimumValue);

        var x = 0;

        for(var k = 0; k < candles.length; k++){
            var item = candles[k];
            var plot = (item[3] - middle ) * yScale;
            if(k==0){
                this.drawing.moveTo(x, plot);
            }
            else{
                this.drawing.lineTo(x, plot);
            }
            x += 20;
        }

        this.drawing.stroke();
    }


    adjustChart(offset){
        var maximumValue = Number.MIN_SAFE_INTEGER;
        var minimumValue = Number.MAX_SAFE_INTEGER;
    
        for(var k = 0; k < offset; k++){
            var item = this.chartData.data[this.chartData.data.length-(1 + k)];
            
            maximumValue = Math.max(item[4], maximumValue);
            minimumValue = Math.min(item[5], minimumValue);
        }
        
        //candleRoot.pivot.y = (maximumValue + minimumValue) / 2;
        this.drawing.node.scaleY = this.drawing.node.y / (maximumValue - minimumValue);
    }

    // update (dt) {}
}
