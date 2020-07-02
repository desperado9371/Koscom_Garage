// ChartPlotAnalizer.cpp : 이 파일에는 'main' 함수가 포함됩니다. 거기서 프로그램 실행이 시작되고 종료됩니다.
//

#include <iostream>
#include "ChartAnalizer.h"
#include "ta-lib/ta_func.h"

using namespace std;



int main(int argc, char* argv[])
{
    /*
    TA_Real prices[100] = {1,2,3,4,5,6,7,8,9,10,9,8,7,6,5,4,3,2};
    TA_Real outMACD[100];
    TA_Real outMACDSignal[100];
    TA_Real outMACDHist[100];
    TA_Integer outBeg;
    TA_Integer outNbElement;


    TA_RetCode ret = TA_MACD(0, TA_MACD_Lookback(12,26,9), prices, 12, 26, 9, &outBeg, &outNbElement, outMACD, outMACDSignal, outMACDHist);

    for (int i = 0; i < outNbElement; i++)
    {
        char date[5] = "";
        snprintf(date, 5, "%00004d", i+outBeg);
        cout << "Day " << date << " : " << endl;
        cout << "outMACD = " << outMACD[i] << endl << "outMACDSignal = " << outMACDSignal[i] << endl << "outMACDHist = " << outMACDHist[i] << endl;
    }

    TA_Real outRSI[100];
    
    TA_RetCode rsiRet = TA_RSI(0, TA_RSI_Lookback(14), &prices[5], 14, &outBeg, &outNbElement, outRSI);

    for (int i = 0; i < outNbElement; i++)
    {
        char date[5] = "";
        snprintf(date, 5, "%00004d", i + outBeg);
        cout << "Day " << date << " : " << endl;
        cout << "outRSI = " << outRSI[i] << endl;
    }*/

    ChartAnalizer ca(TIME_MODE::MINUTE, tm(), tm());
    
}

