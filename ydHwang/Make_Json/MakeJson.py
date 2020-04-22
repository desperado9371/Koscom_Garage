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

# Chaikin Money Flow (CMF)
CMF = dict()
CMF["name"] = "CMF"
CMF["Arg"] = ['high','low','close','volume','period']
Volumn["CMF"] = CMF

# Ease of Movement (EoM, EMV)
EoM = dict()
EoM["name"] = "EoM"
EoM["Arg"] = ['high','low','volume','period']
Volumn["EoM"] = EoM

# Force Index (FI)
FI = dict()
FI["name"] = "FI"
FI["Arg"] = ['high','low','close','volume','period']
Volumn["FI"] = FI

# Money Flow Index (MFI)
MFI = dict()
MFI["name"] = "MFI"
MFI["Arg"] = ['high','low','close','Volumn','period']
Momentum["MFI"] = MFI

# Negative Volume Index (NVI)
NVI = dict()
NVI["name"] = "NVI"
NVI["Arg"] = ['close','volume']
Volumn["NVI"] = NVI

# On-balance volume (OBV)
OBV = dict()
OBV["name"] = "OBV"
OBV["Arg"] = ['close','volume']
Volumn["OBV"] = OBV

# Volume-price Trend (VPT)
VPT = dict()
VPT["name"] = "VPT"
VPT["Arg"] = ['close','volume']
Volumn["VPT"] = VPT

# Volume Weighted Average Price (VWAP)
VWAP = dict()
VWAP["name"] = "VWAP"
VWAP["Arg"] = ['high','low','close','Volumn','period']
Volumn["VWAP"] = VWAP

############################# Volatility
# Average True Range (ATR)
ATR = dict()
ATR["name"] = "ATR"
ATR["Arg"] = ['high','low','close','period']
Volatility["ATR"] = ATR

# Bollinger Bands (BB)
BB = dict()
BB["name"] = "BB"
BB["Arg"] = ['close','period','ndev']
Volatility["BB"] = BB

# Donchian Channel (DC)
DC = dict()
DC["name"] = "DC"
DC["Arg"] = ['close','period','ndev']
Volatility["DC"] = DC

# Keltner Channel (KC)
KC = dict()
KC["name"] = "KC"
KC["Arg"] = ['high','low''close','period']
Volatility["KC"] = KC



#############################Trend
# Average Directional Movement Index (ADX)
ADX = dict()
ADX["name"] = "ADX"
ADX["Arg"] = ['high','low','close','period']
Trend["ADX"] = ADX

# Aroon Indicator (AI)
AI = dict()
AI["name"] = "AI"
AI["Arg"] = ['close','period']
Trend["AI"] = AI

# Commodity Channel Index (CCI)
CCI = dict()
CCI["name"] = "CCI"
CCI["Arg"] = ['high','low','close','period','constant']
Trend["CCI"] = CCI

# Detrended Price Oscillator (DPO)
DPO = dict()
DPO["name"] = "DPO"
DPO["Arg"] = ['close','period']
Trend["DPO"] = DPO

# Exponential Moving Average (EMA)
EMA = dict()
EMA["name"] = "EMA"
EMA["Arg"] = ['close','period']
Trend["EMA"] = EMA

# Ichimoku Kinkō Hyō (Ichimoku)
Ichimoku = dict()
Ichimoku["name"] = "Ichimoku"
Ichimoku["Arg"] = ['high','low','n1_period','n2_period','n3_period']
Trend["Ichimoku"] = Ichimoku

# KST Oscillator (KST)
KST = dict()
KST["name"] = "KST"
KST["Arg"] = ['close','r1_period','r2_period','r3_period','r4_period','n1_period','n2_period','n3_period','n4_period','nsig']
Trend["KST"] = KST

# Moving Average Convergence Divergence (MACD)
MACD = dict()
MACD["name"] = "MACD"
MACD["Arg"] = ['close','n_fast','n_slow','n_sign']
Trend["MACD"] = MACD

# Mass Index (MI)
MI = dict()
MI["name"] = "MI"
MI["Arg"] = ['high','low','n_period','n2_period']
Trend["MI"] = MI

# Parabolic Stop And Reverse (Parabolic SAR)
Parabolic_SAR = dict()
Parabolic_SAR["name"] = "Parabolic_SAR"
Parabolic_SAR["Arg"] = ['high','low','close','step','max_step']
Trend["Parabolic_SAR"] = Parabolic_SAR

# Simple Moving Average (SMA )
SMA = dict()
SMA["name"] = "SMA"
SMA["Arg"] = ['close','period']
Trend["SMA"] = SMA

# Trix (TRIX)
TRIX = dict()
TRIX["name"] = "TRIX"
TRIX["Arg"] = ['close','period']
Trend["TRIX"] = TRIX

# Vortex Indicator (VI)
VI = dict()
VI["name"] = "VI"
VI["Arg"] = ['high','low','close','period']
Trend["VI"] = VI

#############################Momentum
# Awesome Oscillator (AO)
AO = dict()
AO["name"] = "AO"
AO["Arg"] = ['high','low','short_period','log_period']
Momentum["AO"] = AO

# Kaufman's Adaptive Moving Average (KAMA)
KAMA = dict()
KAMA["name"] = "KAMA"
KAMA["Arg"] = ['close','period','pow1','pow2']
Momentum["KAMA"] = KAMA

# Rate of Change (ROC)
ROC = dict()
ROC["name"] = "ROC"
ROC["Arg"] = ['close','period']
Momentum["ROC"] = ROC

# Relative Strength Index (RSI)
RSI = dict()
RSI["name"] = "RSI"
RSI["Arg"] = ['close','period']
Momentum["RSI"] = RSI

# Money Flow Index (MFI)
MFI = dict()
MFI["name"] = "MFI"
MFI["Arg"] = ['high','low','close','Volumn']
Momentum["MFI"] = MFI

# Stochastic Oscillator (SR)
SR = dict()
SR["name"] = "SR"
SR["Arg"] = ['close','high','low','period','d_n']
Momentum["SR"] = SR


# True strength index (TSI)
TSI = dict()
TSI["name"] = "TSI"
TSI["Arg"] = ['close','high_period','low_period']
Momentum["TSI"] = TSI

# Ultimate Oscillator (UO)
UO = dict()
UO["name"] = "UO"
UO["Arg"] = ['high','low','close','short_period','medium_period','long_period','ws','wm','wl']
Momentum["UO"] = UO


# Williams %R (WR)
WR = dict()
WR["name"] = "WR"
WR["Arg"] = ['high','low','close','lbp']
Momentum["WR"] = WR



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