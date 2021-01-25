import asyncio
from alpha_vantage.async_support.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
from time import sleep
import math
import aisklearn as sk
import cbot as cb
import rsi
import os
import currency_index as ci

api_key = '714CQBJCXSZH03IX'
pairs = os.listdir('excel/prices/')
pairs = [pair.rsplit('.', 1)[0] for pair in pairs]
##pairs = ['EURJPY', 'EURNZD', 'EURSEK', 'EURUSD', 'GBPAUD']

dfs = {}
n = 5
chunks = [pairs[i:i + n] for i in range(0, len(pairs), n)]


##async def get_data(pair):
##    ts = TimeSeries(key=api_key,output_format='pandas')
##    data, _ = await ts.get_intraday(symbol=pair,interval='5min', outputsize='full')
##    path = 'excel/intraday_prices/'+pair+'.csv'
##    data = pd.DataFrame(data)
##    data = data.reset_index()
##    data = data.drop(data.columns[[2, 3, 4, 5]],axis=1)
##    data.rename(columns={'date':'Date','1. open': 'Price'}, inplace=True)
##    data.to_csv(path, index=False)
####    print(data)
##    df= cb.main(data)
##    df = df.dropna()
##    prediction = sk.sk_learn(df, pair)
##    df.insert(4, "AI Predictions", prediction)
##    pred_path = 'excel/intraday_indicators/'+pair+' indicators.csv'
##    df.to_csv(pred_path, index=False)
##    print('Done saving indicators for ', pair)
##    rsi.price_rsiSummary(df,pair,250,'intraday')    
##
##
##    new_df = data.drop(data.columns[[2, 3, 4]],axis=1)
####    print(new_df)
##
##
##    await ts.close()
####    await asyncio.sleep(0.1)
##    return data
##
##async def main(chunks):
##    for each in chunks:
##        success = False
##        while success == False:
##            
##            try:
##                tasks = [get_data(pair) for pair in pairs]
##                group1 = asyncio.gather(*tasks)
##
##    ##            result = request_data(each)
##                success = True
##                print('success')
##
##            except:
##                print('trying again in 60secs')
##                sleep(61)
##
##
##            
####    loop = asyncio.get_event_loop()
##    tasks = [get_data(pair) for pair in pairs]
##    group1 = asyncio.gather(*tasks)
####    results = loop.run_until_complete(group1)
####    loop.close()
##
##    print('okay')
##
##
##asyncio.run(main(chunks))
##
####request_data(chunks[0])
##
##            
##
####    sleep(65)
##
####    dfs[sheet] = request_data(pairs[i:i+5])
##        
##
##
##
##
##
##
##
##
##
##
##
##
####ci.main(results,no_of_rows,'intraday')
##



async def get_data(pair):
    ts = TimeSeries(key=api_key,output_format='pandas')
    data, _ = await ts.get_intraday(symbol=pair,interval='5min', outputsize='full')
    path = 'excel/intraday_prices/'+pair+'.csv'
    data = pd.DataFrame(data)
    data = data.reset_index()
    data = data.drop(data.columns[[2, 3, 4, 5]],axis=1)
    data.rename(columns={'date':'Date','1. open': 'Price'}, inplace=True)
    data.to_csv(path, index=False)
    print(data)
    df= cb.main(data)
    df = df.dropna()
    prediction = sk.sk_learn(df, pair)
    df.insert(4, "AI Predictions", prediction)
    pred_path = 'excel/intraday_indicators/'+pair+' indicators.csv'
    df.to_csv(pred_path, index=False)
    print('Done saving indicators for ', pair)
    rsi.price_rsiSummary(df,pair,250,'intraday')    


    new_df = data.drop(data.columns[[2, 3, 4]],axis=1)
##    print(new_df)


    await ts.close()
    return data

loop = asyncio.get_event_loop()
tasks = [get_data(pair) for pair in pairs]
group1 = asyncio.gather(*tasks)
results = loop.run_until_complete(group1)
loop.close()


print(results)
####ci.main(results,no_of_rows,'intraday')
##

