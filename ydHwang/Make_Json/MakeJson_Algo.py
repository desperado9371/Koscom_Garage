import json
Algo_group = dict()
# 중분류
Block = dict()

#소분류
MACD = dict()
CCI = dict()

Algo = dict()
Algo["min"]="2"
Algo["max"]="2"
Algo["BuySell"]="Buy"
Algo["Block"]=Block


Block["MACD"] = MACD
Block["CCI"] = CCI


MACD["name"] = "MACD"
MACD["input_close"] = "50000"
MACD["input_n_fast"] = "60"
MACD["input_n_slow"] = "30"
MACD["input_n_sign"] = "5"
MACD["Triger_sign"] = ">"
MACD["Triger_val"] = "5"


CCI["name"] = "CCI"
CCI["input_high"] = "50000"
CCI["input_low"] = "60"
CCI["input_close"] = "30"
CCI["input_period"] = "5"
CCI["input_constant"] = "5"
MACD["Triger_sign"] = "<"
MACD["Triger_val"] = "2"
############################# Volumn


# json 파일로 저장
Algo_group["Algo"] = Algo

with open('C:\\Define_Algo.json', 'w', encoding='utf-8') as make_file:
    json.dump(Algo_group, make_file, indent="\t")

# 저장한 파일 출력하기
with open('C:\\Define_Algo.json', 'r') as f:
     json_data = json.load(f)

print(json.dumps(Algo_group, indent="\t"))