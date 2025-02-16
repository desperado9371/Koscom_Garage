import json
Algo_group = dict()
# 중분류
Block1 = dict()
Block2 = dict()

#소분류
obv=dict()
MACD = dict()
CCI = dict()
NUM = dict()
Group1 = dict()
Group2 = dict()
Group3 = dict()
SIG = dict()
Algo = dict()

Algo["market"]="upbit"
Algo["srt_date"]="20200102"
Algo["end_date"]="20200110"
Algo["buysell"]="Buy"
Algo["block1"]=Block1
Algo["block2"]=Block2

####################################
Block1["min"]="2"
Block1["max"]="2"
Block1["total_count"]="2"
Block1["group1"] = [MACD,SIG,CCI]
Block1["group2"] = [MACD,SIG,NUM]


MACD["name"] = "macd"
MACD["val"] = {"input_close":"50000","input_n_fast":"60","input_n_slow":"30","input_n_sign":"5"}

SIG["name"] = "sig"
SIG["val"] = ">"

CCI["name"] = "obv"
CCI["val"] = {"volume":"10"}


#############################

####################################
Block2["min"]="1"
Block2["max"]="1"
Block2["total_count"]="1"
Block2["group1"] = [obv,SIG,NUM]


SIG["name"] = "sig"
SIG["val"] = ">"
#############################
obv["name"] = "obv"
obv["val"] = {"volum":"10"}
#############################
NUM["name"] = "num"
NUM["val"] = "20000"

#############################

# json 파일로 저장
Algo_group["algo"] = Algo

with open('C:\\Define_Algo.json', 'w', encoding='utf-8') as make_file:
    json.dump(Algo_group, make_file, indent="\t")

# 저장한 파일 출력하기
with open('C:\\Define_Algo.json', 'r') as f:
     json_data = json.load(f)

print(json.dumps(Algo_group, indent="\t"))