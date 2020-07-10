// ChartPlotAnalizer.cpp : 이 파일에는 'main' 함수가 포함됩니다. 거기서 프로그램 실행이 시작되고 종료됩니다.
//

#include <iostream>
#include "ChartAnalizer.h"
#include "ta-lib/ta_func.h"

using namespace std;



int main(int argc, char* argv[])
{
    unsigned int st = time(NULL);

    ChartAnalizer ca(TIME_MODE::MINUTE, tm(), tm());
    ca.TestRandomPlots();
    ca.EvaluateTA();
    ca.PrintResults();
    cout << "Time Taken "  << time(NULL) - st << endl;

    return 0;

}

