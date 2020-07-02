#pragma once

#include <ctime>
#include "ta-lib/ta_func.h"
#include "ChartAnalizerCommon.h"
#include "ta-lib/ta_defs.h"
#include <iostream>
#include <fstream>
#include <thread>
#include <mutex>
#include <map>
#include <utility>


using namespace std;

class ChartAnalizer
{
public :
	/*
	* initialize Class
	* @minTime : loadFrom
	* @maxTime : loadTo
	* @maxLookback : least number of data needed for minTime to be first output. 
	*				 Default -1 if Lookback is already considered
	*/
	ChartAnalizer(TIME_MODE mode, tm minTime, tm maxTime, int maxLookback = -1);
	~ChartAnalizer();
	TA_RetCode RSI(tm timePoint, int period, TA_Real *outRSI);
	TA_RetCode ATR(tm timePoint, int period, TA_Real *outATR);
private:
	int GetIndexByTime(tm time);
	int InsertResult(tm plot, string ta, TA_Real value);
	int InsertResult(map<string, TA_Real>* plotInfo, string ta, TA_Real value);

	mutex lock;

	map<tm, map<string, TA_Real>>* results;

	tm startTimePoint;
	tm endTimePoint;
	TA_Real* open;
	TA_Real* close;
	TA_Real* high;
	TA_Real* low;
	TA_Real* volume;
	TIME_MODE mode;

};

