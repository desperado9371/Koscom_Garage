// Learn TypeScript:
//  - https://docs.cocos.com/creator/manual/en/scripting/typescript.html
// Learn Attribute:
//  - https://docs.cocos.com/creator/manual/en/scripting/reference/attributes.html
// Learn life-cycle callbacks:
//  - https://docs.cocos.com/creator/manual/en/scripting/life-cycle-callbacks.html

const {ccclass, property} = cc._decorator;

@ccclass
export default class TALib {

    
        static _skip(arr, period) {
            let j = 0;
            for (let k = 0; j < arr.length; j++) {
                if (!isNaN(arr[j]))
                {k++;}
                if (k == period)
                {break;}
            }
            return j;
        }
        static _sum(arr, num) {
            let sum = 0.0;
            for (let i = 0; i < num; i++) {
                if (!isNaN(arr[i])) {
                    sum += arr[i];
                }
            }
            return sum;
        }
    
        static _avg(arr, num) {
            let n = 0;
            let sum = 0.0;
            for (let i = 0; i < num; i++) {
                if (!isNaN(arr[i])) {
                    sum += arr[i];
                    n++;
                }
            }
            return sum / n;
        }
    
        static _zeros(len) {
            let n = [];
            for (let i = 0; i < len; i++) {
                n.push(0.0);
            }
            return n;
        }
    
        static _set(arr, start, end, value) {
            let e = Math.min(arr.length, end);
            for (let i = start; i < e; i++) {
                arr[i] = value;
            }
        }
    
        static _diff(a, b) {
            let d = [];
            for (let i = 0; i < b.length; i++) {
                if (isNaN(a[i]) || isNaN(b[i])) {
                    d.push(NaN);
                } else {
                    d.push(a[i] - b[i]);
                }
            }
            return d;
        }
        static _move_diff(a) {
            let d = [];
            for (let i = 1; i < a.length; i++) {
                d.push(a[i] - a[i - 1]);
            }
            return d;
        }
        static _sma(S, period) {
            let R = TALib._zeros(S.length);
            let j = TALib._skip(S, period);
            TALib._set(R, 0, j, NaN);
            if (j < S.length) {
                let sum = 0;
                for (let i = j; i < S.length; i++) {
                    if (i == j) {
                        sum = TALib._sum(S, i + 1);
                    } else {
                        sum += S[i] - S[i - period];
                    }
                    R[i] = sum / period;
                }
            }
            return R;
        }
    
        static _smma(S, period) {
            let R = TALib._zeros(S.length);
            let j = TALib._skip(S, period);
            TALib._set(R, 0, j, NaN);
            if (j < S.length) {
                R[j] = TALib._avg(S, j + 1);
                for (let i = j + 1; i < S.length; i++) {
                    R[i] = (R[i - 1] * (period - 1) + S[i]) / period;
                }
            }
            return R;
        }
        static _ema(S, period) {
            let R = TALib._zeros(S.length);
            let multiplier = 2.0 / (period + 1);
            let j = TALib._skip(S, period);
            TALib._set(R, 0, j, NaN);
            if (j < S.length) {
                R[j] = TALib._avg(S, j + 1);
                for (let i = j + 1; i < S.length; i++) {
                    R[i] = ((S[i] - R[i - 1]) * multiplier) + R[i - 1];
                }
            }
            return R;
        }
        static _cmp(arr, start, end, cmpFunc) {
            let v = arr[start];
            for (let i = start; i < end; i++) {
                v = cmpFunc(arr[i], v);
            }
            return v;
        }
        static _filt(records, n, attr, iv, cmpFunc) {
            if (records.length < 2) {
                return NaN;
            }
            let v = iv;
            let pos = n !== 0 ? records.length - Math.min(records.length - 1, n) - 1 : 0;
            for (let i = records.length - 2; i >= pos; i--) {
                if (typeof(attr) !== 'undefined') {
                    v = cmpFunc(v, records[i][attr]);
                } else {
                    v = cmpFunc(v, records[i]);
                }
            }
            return v;
        }
        static _ticks(records) {
            if (records.length === 0) {
                return [];
            }
            let ticks = [];
            if (typeof(records[0].Close) !== 'undefined') {
                for (let i = 0; i < records.length; i++) {
                    ticks.push(records[i].Close);
                }
            } else {
                ticks = records;
            }
            return ticks;
        }
        static _round(n, p) {
            if (n === null) return null;
            let m = Math.pow(10, p);
            return Math.round(n * m) / m;
        }
        static _floor(n, p) {
            if (n === null) return null;
            let m = Math.pow(10, p);
            return Math.floor(n * m) / m;
        }
        static _round_array(arr, p) {
            return arr.map(n => TALib._round(n, p));
        }
        static _floor_array(arr, p) {
            return arr.map(n => TALib._floor(n, p));
        }
    
    
    
        static Highest(records, n, attr) {
            return TALib._filt(records, n, attr, Number.MIN_VALUE, Math.max);
        }
        static Lowest(records, n, attr) {
            return TALib._filt(records, n, attr, Number.MAX_VALUE, Math.min);
        }
    
        static MA(records, period) {
            period = typeof(period) === 'undefined' ? 9 : period;
            return TALib._sma(TALib._ticks(records), period);
        }
        static SMA(records, period) {
            period = typeof(period) === 'undefined' ? 9 : period;
            return TALib._sma(TALib._ticks(records), period);
        }
    
        static EMA(records, period) {
            period = typeof(period) === 'undefined' ? 9 : period;
            return TALib._ema(TALib._ticks(records), period);
        }
    
        static MACD(records, fastEMA, slowEMA, signalEMA) {
            fastEMA = typeof(fastEMA) === 'undefined' ? 12 : fastEMA;
            slowEMA = typeof(slowEMA) === 'undefined' ? 26 : slowEMA;
            signalEMA = typeof(signalEMA) === 'undefined' ? 9 : signalEMA;
            let ticks = TALib._ticks(records);
            let slow = TALib._ema(ticks, slowEMA);
            let fast = TALib._ema(ticks, fastEMA);
            // DIF
            let dif = TALib._diff(fast, slow);
            // DEA
            let signal = TALib._ema(dif, signalEMA);
            let histogram = TALib._diff(dif, signal);
            return [TALib._round_array(dif, 3), TALib._round_array(signal, 3), TALib._round_array(histogram, 3)];
        }
    
        static BOLL(records, period, multiplier) {
            period = typeof(period) === 'undefined' ? 20 : period;
            multiplier = typeof(multiplier) === 'undefined' ? 2 : multiplier;
            let S = TALib._ticks(records);
            for (var j = period - 1; j < S.length && isNaN(S[j]); j++);
            let UP = TALib._zeros(S.length);
            let MB = TALib._zeros(S.length);
            let DN = TALib._zeros(S.length);
            TALib._set(UP, 0, j, NaN);
            TALib._set(MB, 0, j, NaN);
            TALib._set(DN, 0, j, NaN);
            let sum = 0;
            for (let i = j; i < S.length; i++) {
                if (i == j) {
                    for (var k = 0; k < period; k++) {
                        sum += S[k];
                    }
                } else {
                    sum = sum + S[i] - S[i - period];
                }
                let ma = sum / period;
                let d = 0;
                for (var k = i + 1 - period; k <= i; k++) {
                    d += (S[k] - ma) * (S[k] - ma);
                }
                let TALibev = Math.sqrt(d / period);
                let up = ma + (multiplier * TALibev);
                let dn = ma - (multiplier * TALibev);
                UP[i] = up;
                MB[i] = ma;
                DN[i] = dn;
            }
            // upper, middle, lower
            return [UP, MB, DN];
        }
    
        static KDJ(records, n, k, d) {
            n = typeof(n) === 'undefined' ? 9 : n;
            k = typeof(k) === 'undefined' ? 3 : k;
            d = typeof(d) === 'undefined' ? 3 : d;
    
            let RSV = TALib._zeros(records.length);
            TALib._set(RSV, 0, n - 1, NaN);
            let K = TALib._zeros(records.length);
            let D = TALib._zeros(records.length);
            let J = TALib._zeros(records.length);
    
            let hs = TALib._zeros(records.length);
            let ls = TALib._zeros(records.length);
            for (var i = 0; i < records.length; i++) {
                hs[i] = records[i].High;
                ls[i] = records[i].Low;
            }
    
            for (var i = 0; i < records.length; i++) {
                if (i >= (n - 1)) {
                    let c = records[i].Close;
                    let h = TALib._cmp(hs, i - (n - 1), i + 1, Math.max);
                    let l = TALib._cmp(ls, i - (n - 1), i + 1, Math.min);
                    RSV[i] = 100 * ((c - l) / (h - l));
                    K[i] = (1 * RSV[i] + (k - 1) * K[i - 1]) / k;
                    D[i] = (1 * K[i] + (d - 1) * D[i - 1]) / d;
                } else {
                    K[i] = D[i] = 50;
                    RSV[i] = 0;
                }
                J[i] = 3 * K[i] - 2 * D[i];
            }
            // remove prefix
            for (var i = 0; i < n - 1; i++) {
                K[i] = D[i] = J[i] = NaN;
            }
            return [TALib._round_array(K, 3), TALib._round_array(D, 3), TALib._round_array(J, 3)];
        }
    
        static RSI(records, period) {
            period = typeof(period) === 'undefined' ? 14 : period;
            let i;
            let n = period;
            let rsi = TALib._zeros(records.length);
            TALib._set(rsi, 0, rsi.length, NaN);
            if (records.length < n) {
                return rsi;
            }
            let ticks = TALib._ticks(records);
            let deltas = TALib._move_diff(ticks);
            let seed = deltas.slice(0, n);
            let up = 0;
            let down = 0;
            for (i = 0; i < seed.length; i++) {
                if (seed[i] >= 0) {
                    up += seed[i];
                } else {
                    down += seed[i];
                }
            }
            up /= n;
            down = -(down /= n);
            let rs = down != 0 ? up / down : 0;
            rsi[n] = 100 - 100 / (1 + rs);
            let delta = 0;
            let upval = 0;
            let downval = 0;
            for (i = n + 1; i < ticks.length; i++) {
                delta = deltas[i - 1];
                if (delta > 0) {
                    upval = delta;
                    downval = 0;
                } else {
                    upval = 0;
                    downval = -delta;
                }
                up = (up * (n - 1) + upval) / n;
                down = (down * (n - 1) + downval) / n;
                rs = up / down;
                rsi[i] = 100 - 100 / (1 + rs);
            }
            return rsi;
        }
        static OBV(records) {
            if (records.length === 0) {
                return [];
            }
            if (typeof(records[0].Close) === 'undefined') {
                throw "argument must KLine";
            }
            let R = [];
            for (let i = 0; i < records.length; i++) {
                if (i === 0) {
                    R[i] = records[i].Volume;
                } else if (records[i].Close >= records[i - 1].Close) {
                    R[i] = R[i - 1] + records[i].Volume;
                } else {
                    R[i] = R[i - 1] - records[i].Volume;
                }
            }
            return R;
        }
        static ATR(records, period) {
            if (records.length === 0) {
                return [];
            }
            if (typeof(records[0].Close) === 'undefined') {
                throw "argument must KLine";
            }
            period = typeof(period) === 'undefined' ? 14 : period;
            let R = TALib._zeros(records.length);
            let sum = 0;
            let n = 0;
            for (let i = 0; i < records.length; i++) {
                let TR = 0;
                if (i == 0) {
                    TR = records[i].High - records[i].Low;
                } else {
                    TR = Math.max(records[i].High - records[i].Low, Math.abs(records[i].High - records[i - 1].Close), Math.abs(records[i - 1].Close - records[i].Low));
                }
                sum += TR;
                if (i < period) {
                    n = sum / (i + 1);
                } else {
                    n = (((period - 1) * n) + TR) / period;
                }
                R[i] = n;
            }
            return R;
        }
        static Alligator(records, jawLength, teethLength, lipsLength) {
            jawLength = typeof(jawLength) === 'undefined' ? 13 : jawLength;
            teethLength = typeof(teethLength) === 'undefined' ? 8 : teethLength;
            lipsLength = typeof(lipsLength) === 'undefined' ? 5 : lipsLength;
            let ticks = [];
            for (let i = 0; i < records.length; i++) {
                ticks.push((records[i].High + records[i].Low) / 2);
            }
            return [
                [NaN, NaN, NaN, NaN, NaN, NaN, NaN, NaN].concat(TALib._smma(ticks, jawLength)), // jaw (blue)
                [NaN, NaN, NaN, NaN, NaN].concat(TALib._smma(ticks, teethLength)), // teeth (red)
                [NaN, NaN, NaN].concat(TALib._smma(ticks, lipsLength)), // lips (green)
            ];
        }
        static CMF(records, periods) {
            periods = periods || 20;
            let ret = [];
            let sumD = 0;
            let sumV = 0;
            let arrD = [];
            let arrV = [];
            for (let i = 0; i < records.length; i++) {
                let d = (records[i].High == records[i].Low) ? 0 : (2 * records[i].Close - records[i].Low - records[i].High) / (records[i].High - records[i].Low) * records[i].Volume;
                arrD.push(d);
                arrV.push(records[i].Volume);
                sumD += d;
                sumV += records[i].Volume;
                if (i >= periods) {
                    sumD -= arrD.shift();
                    sumV -= arrV.shift();
                }
                ret.push(sumD / sumV);
            }
            return ret;
        }
    
    

    // update (dt) {}
}
