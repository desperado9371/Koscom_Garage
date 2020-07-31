// ChartPlotAnalizer.cpp : 이 파일에는 'main' 함수가 포함됩니다. 거기서 프로그램 실행이 시작되고 종료됩니다.
//

#include <iostream>
#include "ChartAnalizer.h"
#include "ta-lib/ta_func.h"
#include <time.h>

using namespace std;

TA_Real* open, * close;
int GetIndexByTime(tm time)
{
    tm start = { 0 };
    start.tm_year = 2017 - 1900;
    start.tm_mon = 11 - 1;
    start.tm_mday = 9;
    start.tm_hour = 0;
    start.tm_min = 0;

    int div = 60; // temp 1 min setting
    time.tm_year -= 1900;
    time.tm_mon -= 1;
    time_t calc = mktime(&time) - mktime(&start);

    int ret = calc / div; // div to get index
    return ret;
}

#define Y_AXIS 20
#define X_AXIS 40
void DisplayChart(tm time)
{
    system("cls");
    int index = GetIndexByTime(time);

    double minVal = DBL_MAX;
    double maxVal = DBL_MIN;

    //find min max
    for (int k = index - X_AXIS; k <= index; k++)
    {
        double openValue = open[k];
        double closeValue = close[k];
        if (minVal > openValue)
        {
            minVal = openValue;
        }
        if (minVal > closeValue)
        {
            minVal = closeValue;
        }
        if (maxVal < openValue)
        {
            maxVal = openValue;
        }
        if (maxVal < closeValue)
        {
            maxVal = closeValue;
        }
    }

    int chart[X_AXIS][Y_AXIS] = { {0} };
    for (int k = index - X_AXIS; k < index; k++)
    {
        double openValue = open[k];
        double closeValue = close[k];
        double from = openValue >= closeValue ? closeValue : openValue;
        double to = openValue < closeValue ? closeValue : openValue;
        int fromIndex = (from - minVal) / (maxVal - minVal) * (Y_AXIS-1);
        int toIndex = (to - minVal) / (maxVal - minVal) * (Y_AXIS-1) ;
        int xOffset = index - X_AXIS;
        for (int j = fromIndex; j <= toIndex; j++)
        {
            chart[k - xOffset][j] = (openValue >= closeValue) ? (int)1 : (int)-1;
        }
    }

    for (int y = 0; y < Y_AXIS; y++)
    {
        for (int x = 0; x < X_AXIS; x++)
        {
            if (chart[x][y] == 1)
            {
                cout << "▒";
            }
            else if (chart[x][y] == -1)
            {
                cout << "■";
            }
            else
            {
                cout << "　";

            }
        }
        cout << endl;
    }
}


int main(int argc, char* argv[])
{
    unsigned int st = time(NULL);

    ChartAnalizer ca(TIME_MODE::MINUTE, tm(), tm());
    //ca.TestRandomPlots();


    tm start = { 0 };
    start.tm_year = 2017;
    start.tm_mon = 11;
    start.tm_mday = 9;
    start.tm_hour = 0;
    start.tm_min = 120;
    

    open = ca.open;
    close = ca.close;
    vector<tm> plots;
    while (true)
    {
        DisplayChart(start);
        char input = getchar();
        if (input == 'b')
        {
            plots.push_back(start);
        }
        else if (input == 'x')
        {
            break;
        }
        else if (input == '\n')
        {

        }
        else
        {
            fflush(stdin);
            start.tm_min++;
        }
    }
    ca.SetPlots(plots);
    ca.EvaluateTA();
    //ca.PrintResults();
    ca.AnalizeResult("RSI04");
    cout << "Time Taken " << time(NULL) - st << endl;
    return 0;

}

