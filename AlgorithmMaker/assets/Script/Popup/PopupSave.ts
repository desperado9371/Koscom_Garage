// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

import AlgorithmManager from "../AlgorithmManager";
import TutorialManager from "../TutorialManager";

const {ccclass, property} = cc._decorator;

@ccclass
export default class PopupSave extends cc.Component {

    @property(cc.EditBox)
    algoName: cc.EditBox = null;

    @property(cc.EditBox)
    memo: cc.EditBox = null;


    // LIFE-CYCLE CALLBACKS:

    // onLoad () {}

    close(){
        this.node.destroy();
    }

    onSaveButton(){
        var am = AlgorithmManager.getInstance();
        if(this.memo.string == "" || this.memo.string == null){
            this.memo.string = " ";
        }
        
        am.SaveAlgorithm(this.algoName.string, this.memo.string);
        am.showSaveTooltip();

        TutorialManager.getInstance().nextTutorialByIndex(12);
        this.close();
    }

    start () {
        var tuto = TutorialManager.getInstance();
        if(tuto != null){
            if(tuto.isTutorial == true){
                this.algoName.string = "RSI 튜토리얼";
            }
        }
    }

    // update (dt) {}
}
