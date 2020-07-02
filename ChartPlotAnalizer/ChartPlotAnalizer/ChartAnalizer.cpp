#include "ChartAnalizer.h"



ChartAnalizer::ChartAnalizer(TIME_MODE mode, tm minTime, tm maxTime, int maxLookback)
{
	this->mode = mode;
	this->startTimePoint = minTime; // - maxLookback by timemode

	this->results = new map<tm, map<string, TA_Real>>();


	//temp file read 20171109 data
	this->startTimePoint.tm_year = 2017;
	this->startTimePoint.tm_mon = 11;
	this->startTimePoint.tm_mday = 9;
	this->startTimePoint.tm_hour = 0;
	this->startTimePoint.tm_min = 0;

	this->endTimePoint.tm_year = 2017;
	this->endTimePoint.tm_mon = 11;
	this->endTimePoint.tm_mday = 19;
	this->endTimePoint.tm_hour = 0;
	this->endTimePoint.tm_min = 0;
	ifstream inFile;
	inFile.open("tempData_20171109.csv", ifstream::in);

	this->open = new TA_Real[1440];
	this->close = new TA_Real[1440];
	this->high = new TA_Real[1440];
	this->low = new TA_Real[1440];
	this->volume = new TA_Real[1440];

	int i = 0;
	char buf[200];

	//remove first line
	inFile.getline(buf, 200);
	string delimiter = ",";
	int lineNum = 0;
	while (!inFile.eof()) {
		inFile.getline(buf, 200);
		string str(buf);
		size_t pos = 0;
		string token;
		
		int tokenNum = 0;
		while ((pos = str.find(delimiter)) != std::string::npos) {
			token = str.substr(0, pos);
			
			switch (tokenNum)
			{
			case 0: // time
				
				break;

			case 1: // open
				this->open[lineNum] = atoi(token.c_str());
				break;

			case 2: // close
				this->close[lineNum] = atoi(token.c_str());
				break;

			case 3: // high
				this->high[lineNum] = atoi(token.c_str());
				break;

			case 4: // low
				this->low[lineNum] = atoi(token.c_str());
				break;

			case 5: // volume
				this->volume[lineNum] = atof(token.c_str());
				break;
			}

			tokenNum++;
			str.erase(0, pos + delimiter.length());

		}

	}

	inFile.close();
	//temp data load done
}

ChartAnalizer::~ChartAnalizer()
{
	delete (this->open);
	delete (this->close);
	delete (this->high);
	delete (this->low);
	delete (this->volume);

	delete results;
}

TA_RetCode ChartAnalizer::RSI(tm timePoint, int period, TA_Real* outRSI)
{
	int DO_NOT_BOTHER = 0;
	int index = GetIndexByTime(timePoint);
	TA_RetCode retCode = TA_RSI(0, TA_RSI_Lookback(period), &close[index], period, 
								&DO_NOT_BOTHER, &DO_NOT_BOTHER, outRSI);

	return retCode;
}

TA_RetCode ChartAnalizer::ATR(tm timePoint, int period, TA_Real* outATR)
{
	int DO_NOT_BOTHER = 0;
	int index = GetIndexByTime(timePoint);
	TA_RetCode retCode = TA_ATR(0, TA_ATR_Lookback(period), &high[index], &low[index], 
		&close[index], period, &DO_NOT_BOTHER, &DO_NOT_BOTHER, outATR);

	return retCode;
}



int ChartAnalizer::GetIndexByTime(tm time)
{
	int div = 60; // temp 60 seconds setting
	time_t calc = mktime(&time) - mktime(&this->startTimePoint);

	int ret = calc / div; // div to get index
	return ret;
}

int ChartAnalizer::InsertResult(tm plot, string ta, TA_Real value)
{
	lock.lock();

	//key does not exist
	if (this->results->find(plot) == results->end())
	{
		this->results->insert(pair<tm, map<string, TA_Real>>(plot, map<string, TA_Real>()));
	}
	else // key already exist
	{
		auto found = this->results->at(plot);
		found.insert(pair<string, TA_Real>(ta, value));
	}

	lock.unlock();
	return 0;
}

int ChartAnalizer::InsertResult(map<string, TA_Real>* plotInfo, string ta, TA_Real value)
{
	lock.lock();

	
	plotInfo->insert(pair<string, TA_Real>(ta, value));


	lock.unlock();
	return 0;
}
