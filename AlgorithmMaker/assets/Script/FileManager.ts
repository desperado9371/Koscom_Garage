// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class FileManager extends cc.Component {

    static instance : FileManager = null;
    static getInstance() : FileManager{

        return FileManager.instance;
    }
    @property(cc.TextAsset)
    cardDataFile : cc.TextAsset = null;
    // LIFE-CYCLE CALLBACKS:
    
    @property(cc.SpriteFrame)
    cardMomentum : cc.SpriteFrame = null;

    @property(cc.SpriteFrame)
    cardPrice : cc.SpriteFrame = null;

    @property(cc.SpriteFrame)
    cardTrend : cc.SpriteFrame = null;
    
    @property(cc.SpriteFrame)
    cardVolume : cc.SpriteFrame = null;

    cardData : {} = {};
    getCardData(cardName : string){
        return this.cardData[cardName];
    }
    onLoad () {
        if(FileManager.instance === null){
            FileManager.instance = this;
        }
        var lines = this.cardDataFile.text.split('\r\n');
        var col_names = [];
        for(var k = 0; k < lines.length; k++){
            var line = lines[k].split('\"').join('');
            if(line == '' || line == null){
                continue;
            }
            if(k == 0){ // first line is column name
                col_names = line.split('\t');
            }
            else{

                for(var j = 0; j < col_names.length; j++){
                    var col = line.split('\t');
                    if(j == 0){
                        this.cardData[col[1].toLowerCase()] = {};
                    }
                    this.cardData[col[1].toLowerCase()][col_names[j]] = col[j].split('|').join('\r\n');;
                }
            }
        }

        console.log(this.cardData);
    }
    start () {
        
    }

    // update (dt) {}
}
