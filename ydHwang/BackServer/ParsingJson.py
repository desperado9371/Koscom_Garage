elif indi['name'] == 'roc':
prc_lst = roc(prc_lst, n=int(indi['val']['period']))
elif indi['name'] == 'rsi':
prc_lst = rsi(prc_lst, n=int(indi['val']['period']))
elif indi['name'] == 'tsi':
prc_lst = tsi(prc_lst, r=int(indi['val']['high']), s=int(indi['val']['low']))
elif indi['name'] == 'ao':
prc_lst = ao(prc_lst, s=int(indi['val']['short']), len=int(indi['val']['long']))
elif indi['name'] == 'kama':
prc_lst = kama(prc_lst, n=int(indi['val']['ration']))
elif indi['name'] == 'stoch':
prc_lst = stoch(prc_lst, n=int(indi['val']['period']))

{
    "name": "stoch",
    "val": {
        "period": "5"
    }
}