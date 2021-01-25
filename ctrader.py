import time
import datetime
start1 = time.perf_counter()
start2 = time.process_time()
start3 = datetime.datetime.now()



import asyncio

import matplotlib.pyplot as plt
import pandas as pd
from time import sleep
import math
import aisklearn as sk
import cbot as cb
import rsi
import os
import currency_index as ci
from runauto import trade


dfs = {}
predictions = pd.DataFrame()

async def analysis(pair):
    path = 'excel/ctrader/'+pair+'.csv'
    df = pd.read_csv(path,parse_dates=["date"])
    df = df.drop(df.columns[[2, 3, 4]],axis=1)
    df.rename(columns={'date':'Date','open': 'Price'}, inplace=True)
    dfs[pair] = df
    df = cb.main(df)
    df = df.dropna()
    prediction = sk.sk_learn(df, pair)
    predictions[pair] = prediction[:250]
    df.insert(4, "AI Predictions", prediction)
    pred_path = 'excel/intraday_indicators/'+pair+' indicators.csv'
    df.to_csv(pred_path, index=False)
    print('Done saving indicators for ', pair)
    rsi.price_rsiSummary(df,pair,250,'intraday')    


    await asyncio.sleep(0.1)
    return 



def main():
    symbols = os.listdir('excel/ctrader/')
    pairs = [x.rsplit('.', 1)[0] for x in symbols]
##    print(pairs)
    loop = asyncio.get_event_loop()
    tasks = [analysis(pair) for pair in pairs]
    group1 = asyncio.gather(*tasks)
    results = loop.run_until_complete(group1)
    print(dfs[pairs[0]])
    predictions.insert(0,'Date',dfs[pairs[0]])
    trade(predictions)
    
    
    no_of_rows = 300# int(input('Please enter number of days to graph: '))
    currency_index = ci.cur_index(dfs, no_of_rows,'intrday')
    ci.graph_indexes(currency_index, no_of_rows,'intraday')





    
        
main()





stop1 = time.perf_counter()
stop2 = time.process_time()
print('Perf Counter: ', stop1 - start1)
print('Process Time: ', stop2 - start2)
elapsed = datetime.datetime.now()-start3
print('Time Started ', start3)
print('Time Finished ',datetime.datetime.now())
print('Time Elapsed ', elapsed)



##    
##
##def main():
####    request_data()
##    dfs = {}
##    intraday_pairs = os.listdir('excel/intraday_prices/')
##    no_of_rows = 300# int(input('Please enter number of days to graph: '))
##
##    for pair in intraday_pairs:
##        sheet = pair.rsplit('.', 1)[0]
##        path = 'excel/intraday_prices/'+pair
##        df = pd.read_csv(path)
##        dfs[sheet] = df
####    print(dfs)
##    currency_index = ci.cur_index(dfs, no_of_rows,'intrday')
##    ci.graph_indexes(currency_index, no_of_rows,'intraday')
##   
##
##
##
##
##
##
##
##def main():
####    request_data()
##    dfs = {}
##    intraday_pairs = os.listdir('excel/ctrader/')
##    no_of_rows = 300# int(input('Please enter number of days to graph: '))
##
##    for pair in intraday_pairs:
##        sheet = pair.rsplit('.', 1)[0]
##        path = 'excel/ctrader/'+pair
##        df = pd.read_csv(path)
##        df = df.drop(df.columns[[2, 3, 4]],axis=1)
##        df.rename(columns={'date':'Date','open': 'Price'}, inplace=True)
##        dfs[sheet] = df
##        df = cb.main(data)
##        df = df.dropna()
##        prediction = sk.sk_learn(df, pair)
##        df.insert(4, "AI Predictions", prediction)
##        pred_path = 'excel/intraday_indicators/'+pair+' indicators.csv'
##        df.to_csv(pred_path, index=False)
##        print('Done saving indicators for ', pair)
##        rsi.price_rsiSummary(df,pair,250,'intraday') 
##        print(dfs)
##
##   
##
##
##    
##    currency_index = ci.cur_index(dfs, no_of_rows,'intrday')
##    ci.graph_indexes(currency_index, no_of_rows,'intraday')
##   
##
##
##
##main()

