
let candleRoot = null;
var yBase = 0;
let keyEvents = {};
function main(){
    const app = new PIXI.Application({
        width: 800, height: 600, backgroundColor: 0xF5F7FB, resolution: window.devicePixelRatio || 1,
    });
    document.body.appendChild(app.view);
    
    const container = new PIXI.Container();
    candleContainer = new PIXI.Container();
    candleRoot = candleContainer;

    var rootContainer = app.stage.addChild(container);
    rootContainer.addChild(candleRoot);
    // Create a new texture
    

    // Move container to the center
    container.x = app.screen.width / 2;
    container.y = app.screen.height / 2;
    
    // Center bunny sprite in local container coordinates
    container.pivot.x = container.width / 2;
    container.pivot.y = container.height / 2;
    

    var r_open = getRandomArbitrary(-100, 100);
    var r_close = getRandomArbitrary(-100, 100);
    var r_high = getRandomArbitrary(-100, 100);
    var r_low = getRandomArbitrary(-100, 100);
    r_high = Math.max(r_open, r_close, r_high, r_low);
    r_low = Math.min(r_open, r_close, r_high, r_low);

    //addCandle(100+50,-100+50, 200+50, -200+50); 
    //addCandle(50+50,-50+50, 200+50, -200+50); 
    //addCandle(-55.30112080766614 ,-29.696022253883882 , -24.12087899429784 , -47.31065075174343); 
    for(var k = 0; k < 80; k++){
        
        addCandle(r_open, r_close, r_high, r_low);
        r_open = r_close;
        r_high = getRandomArbitrary(-100, 100);
        r_low = getRandomArbitrary(-100, 100);
        r_close = getRandomArbitrary(-100, 100);
        
        r_high = Math.max(r_open, r_close, r_high, r_low);
        r_low = Math.min(r_open, r_close, r_high, r_low);

    }

    chartKeyboardControl(candleRoot);

    var xPos = 0;
    var yPos = 0;
    //yBase++;
    for(var k = 0; k < candleRoot.children.length; k++){
        yPos = yBase;
        candleRoot.children[k].x = xPos;
        candleRoot.children[k].y = yPos;
        xPos += 15;
        
    }

    // Listen for animate update
    app.ticker.add((delta) => {
        
        if(keyEvents.ArrowUp == true){
            candleRoot.scale.x += 0.05*delta;
        }
        if(keyEvents.ArrowDown == true){
            candleRoot.scale.x -= 0.05*delta;
        }
        if(keyEvents.ArrowLeft == true){
            candleRoot.x -= 5*delta;
        }
        if(keyEvents.ArrowRight == true){
            candleRoot.x += 5*delta;
        }

        
        //container.rotation -= 0.01 * delta;
    });
    
}

var decendingColor = 0x4363E8;
var accendingColor = 0xDD2626;
function addCandle(open, close, high, low){
    console.log(open, close, high, low);
    const rectangle = PIXI.Sprite.from(PIXI.Texture.WHITE);
    const rectangle2 = PIXI.Sprite.from(PIXI.Texture.WHITE);
    rectangle.anchor.x = 0.5;
    rectangle.anchor.y = 0.5;
    rectangle2.anchor.x = 0.5;
    rectangle2.anchor.y = 0.5;


    var color = accendingColor;
    if(open < close){
        color = decendingColor;
    }
    rectangle.tint = color;
    rectangle2.tint = color;

    let candle = new PIXI.Container();
    var body = candle.addChild(rectangle);
    var tail = candle.addChild(rectangle2);

    body.width = 10;
    body.x = 0;
    body.height = Math.abs(open-close);
    if(body.height < 2){
        body.height = 2;
    }
    tail.width = 2;
    //tail.x = body.width / 2 - (tail.width / 2);
    tail.x  = 0;
    
    tail.height = high - low;


    body.y = open - ((open - close) / 2);
    tail.y = high - ((high - low) / 2);
    //body.y = -open;
    //tail.y = -high;
    candleRoot.addChild(candle);
    
}
//destroy all candlestick chart
function clearCandles(){
    candleRoot.destroy(true);
}

function getRandomArbitrary(min, max) {
    return Math.random() * (max - min) + min;
}

function keyboard(value) {
    let key = {};
    key.value = value;
    key.isDown = false;
    key.isUp = true;
    key.press = undefined;
    key.release = undefined;
    //The `downHandler`
    key.downHandler = event => {
      if (event.key === key.value) {
        if (key.isUp && key.press) key.press();
        key.isDown = true;
        key.isUp = false;
        event.preventDefault();
      }
    };
  
    //The `upHandler`
    key.upHandler = event => {
      if (event.key === key.value) {
        if (key.isDown && key.release) key.release();
        key.isDown = false;
        key.isUp = true;
        event.preventDefault();
      }
    };
  
    //Attach event listeners
    const downListener = key.downHandler.bind(key);
    const upListener = key.upHandler.bind(key);
    
    window.addEventListener(
      "keydown", downListener, false
    );
    window.addEventListener(
      "keyup", upListener, false
    );
    
    // Detach event listeners
    key.unsubscribe = () => {
      window.removeEventListener("keydown", downListener);
      window.removeEventListener("keyup", upListener);
    };
    
    return key;
  }

  function chartKeyboardControl(candleContainer){
    let left = keyboard("ArrowLeft"),
        up = keyboard("ArrowUp"),
        right = keyboard("ArrowRight"),
        down = keyboard("ArrowDown");

    left.press = () => {
        keyEvents.ArrowLeft = true;
    };

    left.release = () => {
        keyEvents.ArrowLeft = false;
    };



    right.press = () => {
        keyEvents.ArrowRight = true;
    };

    right.release = () => {
        keyEvents.ArrowRight = false;
    };

    
    up.press = () => {
        keyEvents.ArrowUp = true;
    };

    up.release = () => {
        keyEvents.ArrowUp = false;
    };

    
    down.press = () => {
        keyEvents.ArrowDown = true;
    };

    down.release = () => {
        keyEvents.ArrowDown = false;
    };
}