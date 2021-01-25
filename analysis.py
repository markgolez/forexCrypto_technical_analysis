import pandas as pd


def trade(df):

    df.drop(['Date'],axis=1)
    buy = []
    sell = []
    for pair in df.columns:
        if df[pair][0] == 'Buy' and df[pair][1] == 'Buy':
            buy.append(pair)
        elif df[pair][0] == 'Sell' and df[pair][1] == 'Sell':
            sell.append(pair)
        else:
            continue

    return (buy, sell)



def strength(buy, sell):


    strong_buy = []
    strong_sell = []

    for first_pair in buy:
        for second_pair in buy:
            if first_pair[-3:] == second_pair[:3]:
                cur_pair = first_pair[:3] + second_pair[-3:]
                strong_buy.append(cur_pair)
            else:
                continue

##            print(first_pair, second_pair, cur_pair, 'aBuy')
    
        for second_pair in sell:
            if first_pair[-3:] == second_pair[-3:]:
                cur_pair = first_pair[:3] + second_pair[:3]
                strong_buy.append(cur_pair)
##                print(first_pair, second_pair, cur_pair, 'bBuy')
            elif first_pair[:3] == second_pair[:3]:
                cur_pair = first_pair[-3:] + second_pair[-3:]
                strong_sell.append(cur_pair)
##                print(first_pair, second_pair, cur_pair, 'csell')
            else:
                continue



    for first_pair in sell:
        for second_pair in sell:
            if first_pair[-3:] == second_pair[:3]:
                cur_pair = first_pair[:3] + second_pair[-3:]
                strong_sell.append(cur_pair)
##                print(first_pair, second_pair, cur_pair, 'dSell')
            else:
                continue
    
        for second_pair in buy:
            if first_pair[-3:] == second_pair[-3:]:
                cur_pair = first_pair[:3] + second_pair[:3]
                strong_sell.append(cur_pair)
##                print(first_pair, second_pair, cur_pair, 'eSell')
            elif first_pair[:3] == second_pair[:3]:
                cur_pair = first_pair[-3:] + second_pair[-3:]
                strong_buy.append(cur_pair)
##                print(first_pair, second_pair, cur_pair, 'fBuy')
            else:
                continue
    strong_buy, strong_sell = set(strong_buy), set(strong_sell)

    return (list(strong_buy), list(strong_sell))


##df = pd.read_excel('predictions.xlsx', sheet_name='predictions')
##buy, sell = trade(df)
##x = strength(buy, sell)
##print(x)
