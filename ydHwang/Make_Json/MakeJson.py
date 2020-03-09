import json
ta_group = dict()

# 중분류
Volumn = dict()
Volatility = dict()
Trend = dict()
Momentum = dict()
Others = dict()



############################# Volumn
# Accumulation Distribution Index
ADI = dict()
ADI["name"] = "ADI"
ADI["Arg"] = ['high','low','close','volume']
Volumn["ADI"] = ADI

# On Balance Volume
OBV = dict()
OBV["name"] = "OBV"
OBV["Arg"] = ['close','volume']
Volumn["OBV"] = OBV

# Chaikin Money Flow (CMF)
CMF = dict()
CMF["name"] = "CMF"
CMF["Arg"] = ['high','low','close','volume']
Volumn["CMF"] = CMF

# Force Index (FI)
FI = dict()
FI["name"] = "FI"
FI["Arg"] = ['high','low','volume']
Volumn["FI"] = FI

# Ease of Movement (EoM, EMV)
EoM = dict()
EoM["name"] = "EoM"
EoM["Arg"] = ['high','low','volume']
Volumn["EoM"] = EoM

# Volume-price Trend (VPT)
VPT = dict()
VPT["name"] = "VPT"
VPT["Arg"] = ['close','volume']
Volumn["VPT"] = VPT

# Negative Volume Index (NVI)
NVI = dict()
NVI["name"] = "NVI"
NVI["Arg"] = ['close','volume']
Volumn["NVI"] = NVI

############################# Volatility
# Average True Range (ATR)
ATR = dict()
ATR["name"] = "ATR"
ATR["Arg"] = ['close','high','low','volume']
Volatility["ATR"] = ATR

# Bollinger Bands (BB)
BB = dict()
BB["name"] = "BB"
BB["Arg"] = ['close']
Volatility["BB"] = BB

# Keltner Channel (KC)
KC = dict()
KC["name"] = "KC"
KC["Arg"] = ['close','high','low']
Volatility["KC"] = KC

# Donchian Channel (DC)
DC = dict()
DC["name"] = "DC"
DC["Arg"] = ['close']
Volatility["DC"] = DC

#############################Trend
# Moving Average Convergence Divergence (MACD)
MACD = dict()
MACD["name"] = "MACD"
MACD["Arg"] = ['close']
Trend["MACD"] = MACD

# Average Directional Movement Index (ADX)
ADX = dict()
ADX["name"] = "ADX"
ADX["Arg"] = ['high','low','close']
Trend["ADX"] = ADX

# Vortex Indicator (VI)
VI = dict()
VI["name"] = "VI"
VI["Arg"] = ['high','low','close']
Trend["VI"] = VI

# Trix (TRIX)
TRIX = dict()
TRIX["name"] = "TRIX"
TRIX["Arg"] = ['high','low','close']
Trend["TRIX"] = TRIX

# Mass Index (MI)
MI = dict()
MI["name"] = "MI"
MI["Arg"] = ['high','low']
Trend["MI"] = MI

# Commodity Channel Index (CCI)
CCI = dict()
CCI["name"] = "CCI"
CCI["Arg"] = ['high','low','close']
Trend["CCI"] = CCI

# Detrended Price Oscillator (DPO)
DPO = dict()
DPO["name"] = "DPO"
DPO["Arg"] = ['close']
Trend["DPO"] = DPO

# KST Oscillator (KST)
KST = dict()
KST["name"] = "KST"
KST["Arg"] = ['close']
Trend["KST"] = KST

# Ichimoku Kinkō Hyō (Ichimoku)
Ichimoku = dict()
Ichimoku["name"] = "Ichimoku"
Ichimoku["Arg"] = ['high','low','close']
Trend["Ichimoku"] = Ichimoku

# Parabolic Stop And Reverse (Parabolic SAR)
Parabolic_SAR = dict()
Parabolic_SAR["name"] = "Parabolic_SAR"
Parabolic_SAR["Arg"] = ['high','low','close']
Trend["Parabolic_SAR"] = Parabolic_SAR

#############################Momentum
# Money Flow Index (MFI)
MFI = dict()
MFI["name"] = "MFI"
MFI["Arg"] = ['high','low','close','Volumn']
Momentum["MFI"] = MFI

# Relative Strength Index (RSI)
RSI = dict()
RSI["name"] = "RSI"
RSI["Arg"] = ['close']
Momentum["RSI"] = RSI

# True strength index (TSI)
TSI = dict()
TSI["name"] = "TSI"
TSI["Arg"] = ['close']
Momentum["TSI"] = TSI

# Ultimate Oscillator (UO)
UO = dict()
UO["name"] = "UO"
UO["Arg"] = ['high','low','close']
Momentum["UO"] = UO

# Stochastic Oscillator (SR)
SR = dict()
SR["name"] = "SR"
SR["Arg"] = ['high','low','close']
Momentum["SR"] = SR

# Williams %R (WR)
WR = dict()
WR["name"] = "WR"
WR["Arg"] = ['high','low','close']
Momentum["WR"] = WR

# Awesome Oscillator (AO)
AO = dict()
AO["name"] = "AO"
AO["Arg"] = ['high','low']
Momentum["AO"] = AO

# Kaufman's Adaptive Moving Average (KAMA)
KAMA = dict()
KAMA["name"] = "KAMA"
KAMA["Arg"] = ['close']
Momentum["KAMA"] = KAMA

# Rate of Change (ROC)
ROC = dict()
ROC["name"] = "ROC"
ROC["Arg"] = ['close']
Momentum["ROC"] = ROC

#############################Others
# Daily Return (DR)
DR = dict()
DR["name"] = "DR"
DR["Arg"] = ['close']
Others["DR"] = DR

# Daily Log Return (DLR)
DLR = dict()
DLR["name"] = "DLR"
DLR["Arg"] = ['close']
Others["DLR"] = DLR

# Cumulative Return (CR)
CR = dict()
CR["name"] = "CR"
CR["Arg"] = ['close']
Others["CR"] = CR

# json 파일로 저장
ta_group["Volumn"] = Volumn
ta_group["Volatility"] = Volatility
ta_group["Trend"] = Trend
ta_group["Momentum"] = Momentum
ta_group["Others"] = Others

with open('C:\\Define_ta.json', 'w', encoding='utf-8') as make_file:
    json.dump(ta_group, make_file, indent="\t")

# 저장한 파일 출력하기
with open('C:\\Define_ta.json', 'r') as f:
     json_data = json.load(f)

print(json.dumps(ta_group, indent="\t"))