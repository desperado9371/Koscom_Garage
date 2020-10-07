// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import { profileEnd } from "console";
import ChartData from "./ChartData";
import TAItem from "./TAItem";
import TALib from "./TALib";

const {ccclass, property} = cc._decorator;

@ccclass
export default class TAView extends cc.Component {

    @property(cc.Node)
    itemRoot : cc.Node = null;

    @property(cc.Node)
    TAItem : cc.Node = null;

    @property(ChartData)
    chartData : ChartData = null;

    data = [];
    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    start () {


        this.scheduleUpdate();

    }

    scheduleUpdate(){
        var chart = this;
        if(this.chartData.data != null && this.chartData.data.length > 0){
            chart.calcAll();
        }
        else{
            this.scheduleOnce(function() {
                chart.scheduleUpdate();
            }, 0.1);
        }
    }
    calcAll(){
        this.clearItems();
        var candles = this.chartData.data;
        for(var k = 0 ; k < candles.length; k++){
            var item = candles[k];
            this.data[k] = item[3]
        }
        this.calcMACD(20, 14, 7);
        this.calcRSI(5, 30, 70);
        this.calcRSI(14, 30, 70);
        this.calcRSI(15, 30, 70);
        this.calcRSI(16, 30, 70);
        this.calcRSI(17, 30, 70);
    }
    clearItems(){
        var root = this.itemRoot;
        this.TAItem.active = false;
        this.TAItem.setParent(this.node.parent);
        root.destroyAllChildren();
        this.TAItem.setParent(this.node);

    }
    createItem() : TAItem{
        var obj = cc.instantiate(this.TAItem);
        obj.active = true;
        obj.setParent(this.itemRoot);
        var item = obj.getComponent(TAItem);
        return item;
    }
    calcBollBand(){
        var item = this.createItem();
        var percent = 100;
        item.setTitle("MACD Signal");

        //calc RSI profit percentage

        var output = TALib.BOLL(this.data, )
        //var percentage = 100;
        var isHolding = false;
        var boughtPrice = 0;
        var prevSignal = 0;
        for(var k = 0; k < output[2].length; k++)
        {
            var currentPrice = this.data[k];

                // buy
                if(output[2][k] > 0 && prevSignal < 0){
                    if(isHolding === false ){
                        isHolding = true;
                        boughtPrice = currentPrice;
                        prevSignal = output[2][k];
                    }
                }
                // sell
                else if(output[2][k] < 0 && prevSignal > 0){

                    if(isHolding === true){
                        isHolding = false;
                        percent += percent * ((currentPrice - boughtPrice)/boughtPrice);
                        prevSignal = output[2][k];
                        tradeCount++;
                    }
                }
                else if(output[2][k] != 0 && output[2][k] !== NaN){ // initialize first 
                    prevSignal = output[2][k];
                }
                
            
        }

        item.setPercent((percent-100).toFixed(2));
    }
    calcMACD(long, short, sig){
        var item = this.createItem();
        var percent = 100;
        item.setTitle("MACD Signal");

        //calc RSI profit percentage

        var output = TALib.MACD(this.data, short, long, sig);
        //var percentage = 100;
        var isHolding = false;
        var boughtPrice = 0;
        var prevSignal = 0;
        var tradeCount = 0;
        for(var k = 0; k < output[2].length; k++)
        {
            var currentPrice = this.data[k];

                // buy
                if(output[2][k] > 0 && prevSignal < 0){
                    if(isHolding === false ){
                        isHolding = true;
                        boughtPrice = currentPrice;
                        prevSignal = output[2][k];
                    }
                }
                // sell
                else if(output[2][k] < 0 && prevSignal > 0){

                    if(isHolding === true){
                        isHolding = false;
                        percent += percent * ((currentPrice - boughtPrice)/boughtPrice);
                        prevSignal = output[2][k];
                        tradeCount++;
                    }
                }
                else if(output[2][k] != 0 && output[2][k] !== NaN){ // initialize first 
                    prevSignal = output[2][k];
                }
                
            
        }

        item.setPercent((percent-100).toFixed(2));
        item.setTradeCount(tradeCount);
    }
    calcRSI(period, buyUnder, sellOver){
        var item = this.createItem();
        var percent = 100;
        item.setTitle("RSI " + period);

        //calc RSI profit percentage

        var output = TALib.RSI(this.data, period);
        //var percentage = 100;
        var isHolding = false;
        var boughtPrice = 0;
        var tradeCount = 0;
        for(var k = 0; k < output.length; k++)
        {
            var currentPrice = this.data[k];
            if(output[k] !== null){
                if(output[k] <= buyUnder){ // buy
                    if(isHolding === false){
                        isHolding = true;
                        boughtPrice = currentPrice;
                    }
                    else{

                    }
                }
                else if(output[k] >= sellOver){// sell
                    if(isHolding === true){
                        isHolding = false;
                        percent += percent * ((currentPrice - boughtPrice)/boughtPrice);
                        tradeCount++;
                    }
                }
            }
        }

        item.setPercent((percent-100).toFixed(2));
        item.setTradeCount(tradeCount);
        
    }

    // update (dt) {}
}
