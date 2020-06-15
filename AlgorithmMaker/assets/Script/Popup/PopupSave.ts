// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import AlgorithmManager from "../AlgorithmManager";

const {ccclass, property} = cc._decorator;

@ccclass
export default class PopupSave extends cc.Component {

    @property(cc.EditBox)
    algoName: cc.EditBox = null;


    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    close(){
        this.node.destroy();
    }

    onSaveButton(){
        var am = AlgorithmManager.getInstance();
        
        am.SaveAlgorithm(this.algoName.string);
        am.showSaveTooltip();

        this.close();
    }

    start () {

    }

    // update (dt) {}
}
