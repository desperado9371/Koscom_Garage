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
#include <vector>
#include <functional>
#include <time.h>
#include <set>
#include <algorithm>


using namespace std;
struct cmpByStringLength {
	bool operator()(const tm& a, const tm& b) const {
		tm tempa = a;
		tempa.tm_year -= 1900;
		tempa.tm_mon -= 1;
		tm tempb = b;
		tempb.tm_year -= 1900;
		tempb.tm_mon -= 1;
		return mktime(&tempa) < mktime(&tempb);
		//return a.length() < b.length();
	}
};

struct AnalysisOutput {
	TA_Real valueFrom;
	TA_Real valueTo;
};
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
	TA_RetCode CA_RSI(tm timePoint, int period, TA_Real *outRSI);
	TA_RetCode CA_ATR(tm timePoint, int period, TA_Real *outATR);
	void SetPlots(vector<tm> plots);
	void PrintResults();

	//uses Thread
	TA_RetCode EvaluateTA();
	void TestRandomPlots();
	void CA_RSITest(int periodFrom, int periodTo, int plotFrom, int plotTo);
private:
	int GetIndexByTime(tm time);
	int InsertResult(tm plot, string ta, TA_Real value);
	int InsertResult(map<string, TA_Real>* plotInfo, string ta, TA_Real value);
	void AnalyzeResult();
	AnalysisOutput AnalyzeValueVector(vector<TA_Real>& source);
	void ClearResults();

	mutex lock;

	vector<tm> plots;
	map<tm, map<string, TA_Real>*, cmpByStringLength>* results;
	set<string> keys;

	tm startTimePoint;
	tm endTimePoint;
	TA_Real* open;
	TA_Real* close;
	TA_Real* high;
	TA_Real* low;
	TA_Real* volume;
	TIME_MODE mode;



};

