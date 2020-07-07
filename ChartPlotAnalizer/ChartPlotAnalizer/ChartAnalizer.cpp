#include "ChartAnalizer.h"




ChartAnalizer::ChartAnalizer(TIME_MODE mode, tm minTime, tm maxTime, int maxLookback)
{
	this->mode = mode;
	this->startTimePoint = minTime; // - maxLookback by timemode

	this->results = new map<tm, map<string, TA_Real>*, cmpByStringLength>();
	this->plots = vector<tm>();


	//temp file read 20171109 data
	this->startTimePoint.tm_year = 2017 - 1900;
	this->startTimePoint.tm_mon = 11 - 1;
	this->startTimePoint.tm_mday = 9;
	this->startTimePoint.tm_hour = 0;
	this->startTimePoint.tm_min = 0;

	this->endTimePoint.tm_year = 2017 - 1900;
	this->endTimePoint.tm_mon = 11 - 1;
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
		lineNum++;

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

TA_RetCode ChartAnalizer::CA_RSI(tm timePoint, int period, TA_Real* outRSI)
{
	int DO_NOT_BOTHER = 0;
	int outIndex = 0;
	int index = GetIndexByTime(timePoint);
	//TA_Real* tempOut = new TA_Real[period];
	//TA_RetCode retCode = TA_RSI(0, TA_RSI_Lookback(period)+1, &close[index], period, 
	//							&outIndex, &DO_NOT_BOTHER, tempOut);
	TA_RetCode retCode = TA_RSI(index, index, close, period,
		&outIndex, &DO_NOT_BOTHER, outRSI);
	//*outRSI = tempOut[0];

	//delete tempOut;

	return retCode;
}

TA_RetCode ChartAnalizer::CA_ATR(tm timePoint, int period, TA_Real* outATR)
{
	int DO_NOT_BOTHER = 0;
	int index = GetIndexByTime(timePoint);
	TA_RetCode retCode = TA_ATR(0, TA_ATR_Lookback(period), &high[index], &low[index], 
		&close[index], period, &DO_NOT_BOTHER, &DO_NOT_BOTHER, outATR);

	return retCode;
}

void ChartAnalizer::SetPlots(vector<tm> plots)
{
	this->plots = plots;
}

void ChartAnalizer::PrintResults()
{
	char time[80];
	char key[100];
	for (auto iter = results->begin() ; iter != results->end() ; iter++)
	{
		strftime(time, 80, "%H:%M.", &iter->first);

		cout <<":::-------" <<time << "-------::::" << endl;


		for (auto inter = iter->second->begin(); inter != iter->second->end(); inter++)
		{
			
			cout << inter->first << " : " << inter->second << endl;
			//cin >> key;
		}
	}
}



TA_RetCode ChartAnalizer::EvaluateTA()
{
	ClearResults();

	vector<thread> threads;

	CA_RSITest(4, 40, 0, plots.size());
	//RSI test Thread

	
	/*
	int slice = 10;
	for (int k = 0; k < slice; k++)
	{
		int from = (plots.size() / slice) * k;
		int to = (plots.size() / slice) * (k+1);

		threads.push_back(thread([this, from, to]() {
			this->CA_RSITest(4, 20, from, to);
			}));

		threads.push_back(thread([this, from, to]() {
			this->CA_RSITest(21, 40, from, to);
			}));
	}*/
	
	/*
	threads.push_back(thread([this]() {
		this->CA_RSITest(4, 20, 0, plots.size()/2);
			}));

	threads.push_back(thread([this]() {
		this->CA_RSITest(21, 40, 0, plots.size()/2);
		}));
	threads.push_back(thread([this]() {
		this->CA_RSITest(4, 20, plots.size()/2, plots.size());
		}));

	threads.push_back(thread([this]() {
		this->CA_RSITest(21, 40, plots.size()/2, plots.size());
		}));
	*/
	for (auto& th : threads)
	{
		th.join();
	}

	return TA_RetCode();
}


//@@Warning
//this index calculation is for 24hr full time trade use
int ChartAnalizer::GetIndexByTime(tm time)
{
	int div = 60; // temp 1 min setting
	time.tm_year -= 1900;
	time.tm_mon -= 1;
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
		map<string, TA_Real>* tempMap = new map<string, TA_Real>();
		tempMap->insert(pair<string, TA_Real>(ta, value));
		this->results->insert(pair<tm, map<string, TA_Real>*>(plot, tempMap));

		//insert string key for further use
		keys.insert(ta);
		
	}
	else // key already exist
	{
		auto found = this->results->at(plot);
		found->insert(pair<string, TA_Real>(ta, value));
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

void ChartAnalizer::AnalyzeResult()
{
	for (auto iter = results->begin(); iter != results->end(); iter++)
	{
		vector<TA_Real> values;
		for (auto inter = keys.begin(); inter != keys.end(); inter++)
		{
			string key = *inter;
			if (key != "")
			{
				auto mapInside =iter->second->find(key);
				if (mapInside != iter->second->end())
				{
					values.push_back(mapInside->second);
				}
			}
		}
		sort(values.begin(), values.end());

	}
}

void ChartAnalizer::ClearResults()
{
	lock.lock();

	for (auto iter = results->begin(); iter != results->end(); iter++)
	{
		for (auto inter = iter->second->begin(); inter != iter->second->end(); inter++)
		{
			delete iter->second;
		}
	}

	keys.clear();
	this->results->clear();

	lock.unlock();
}

void ChartAnalizer::TestRandomPlots()
{
	srand((unsigned int)time(NULL));
	int randy = rand() % 50;
	plots.clear();
	
	/*
	tm temp = { 0 };
	int hourmin = rand() % (1440 - 50) + 50;
	temp.tm_year = 2017;
	temp.tm_mon = 11;
	temp.tm_mday = 9;


	temp.tm_hour = 21;
	temp.tm_min = 13;
	plots.push_back(temp);*/
	
	
	for (int k = 0; k < 50 + randy; k++)
	{
		//temp file read 20171109 data
		tm temp = {0};
		int hourmin = rand() % (1440- 50) + 50;
		temp.tm_year = 2017;
		temp.tm_mon = 11;
		temp.tm_mday = 9;


		temp.tm_hour = hourmin / 60;
		temp.tm_min = hourmin % 60;



		
		plots.push_back(temp);
	}
}

void ChartAnalizer::CA_RSITest(int periodFrom, int periodTo, int plotFrom, int plotTo)
{

	for (int i = plotFrom; i < plotTo; i++)
	{
		tm now = this->plots[i];
		int period = 0;
		for (period = periodFrom; period <= periodTo; period++)
		{
			TA_Real output;
			auto result = this->CA_RSI(now, period, &output);
			if (result == TA_RetCode::TA_SUCCESS)
			{
				char buffer[40] = {0};
				//_itoa_s(period, buffer,40, 10);
				sprintf_s(buffer, 40, "%02d", period);
				
				string key = "RSI" + string(buffer);
				InsertResult(now, key, output);

			}
		}
	}
}
