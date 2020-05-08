def Chk_Meet_Condition(Prc_history,group_algo,row,meet_condtion):
#     print("Chk_Meet_Condition 시작:" + str(meet_condtion))
    meet_condtion= int(meet_condtion)
    # (case1 지표끼리 비교시)
    if group_algo[0]['name'] !='num' and group_algo[2]['name'] !='num':
        if math.isnan(Prc_history[group_algo[0]['name']][row])!= True and math.isnan(Prc_history[group_algo[2]['name']][row])!= True:
            print('case1 지표끼리 비교시')
            chk = str(Prc_history[group_algo[0]['name']][row])+str(group_algo[1]['val'])+str(Prc_history[group_algo[2]['name']][row])
            print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    elif group_algo[0]['name'] !='num' and group_algo[2]['name'] =='num':
        print('case2 지표랑 뒷부분의 상수랑 비교시')
        # (case2 지표랑 뒷부분의 상수랑 비교시)
        if math.isnan(Prc_history[group_algo[0]['name']][row])!= True and math.isnan(int(group_algo[2]['val']))!= True:
            chk = str(Prc_history[group_algo[0]['name']][row])+str(group_algo[1]['val'])+str(group_algo[2]['val'])
            print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    elif group_algo[0]['name'] =='num' and group_algo[2]['name'] !='num':
        print('case3 앞의 상수랑 뒷부분의 지표랑 비교시')
        # (case3 앞의 상수랑 뒷부분의 지표랑 비교시)
        if math.isnan(int(group_algo[0]['val']))!= True and math.isnan(Prc_history[group_algo[2]['name']][row])!= True :
            chk = str(group_algo[0]['val'])+str(group_algo[1]['val'])+str(Prc_history[group_algo[2]['name']][row])
            print(chk)
            if eval(chk) == True:
                meet_condtion = meet_condtion + 1
    return meet_condtion