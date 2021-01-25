import time
from datetime import datetime
start1 = time.perf_counter()
start2 = time.process_time()
start3 = datetime.now()


from dateutil import tz
import asyncio
from alpha_vantage.async_support.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
from time import sleep
import math
import aisklearn as sk
import analysis as an
import cbot as cb
import rsi
import os
import currency_index as ci
import shutil

api_key = '714CQBJCXSZH03IX'
pairs = os.listdir('excel/prices/')
pairs = [pair.rsplit('.', 1)[0] for pair in pairs]
dfs = {}
n = 5
chunks = [pairs[i:i + n] for i in range(0, len(pairs), n)]
print(chunks)
to_zone = tz.tzlocal()
predictions = pd.DataFrame()
today = datetime.now().date()
rsi_dir = 'rsi/'+str(today)+'/intraday/'


def mkdir(path):
    try:
        #Create target Directory
        os.mkdir(path)
        print("Directory " , path ,  " Created ")
    except FileExistsError:
        print("Directory " , path ,  " already exists")




def transfered(bid, path):
    
    
    mkdir(path)
    for each in bid:
##        filenames = [x+' rsi.png' for x in each]
        for x in each:
            old_path = rsi_dir + x +' rsi.png'
            print(old_path)
            new_path = path + x +' rsi '+ str(datetime.now()) + 'intraday.png'
            print(new_path)
            try:
                shutil.copyfile(old_path,new_path)
            except:
                print(x, "doesn't exist")

    return



def transfer(strong_buy, strong_sell, buy, sell):
    
    if len(strong_buy)!=0 or len(strong_sell)!=0:        
        path = 'rsi/strongBid/'
        bid = [strong_buy, strong_sell]
        transfered(bid, path)
        
    
    if len(buy)!=0 or len(sell)!=0:        
        path = 'rsi/bid/'
        bid = [buy, sell]
        transfered(bid, path)    

    return




def popupmsg(msg):
    
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Close", command = popup.destroy)
    B1.pack()
    popup.mainloop()



def trade(predictions):

    
    buy, sell = an.trade(predictions)
    print('Buy',buy)
    print('Sell',sell)
    strong_buy,strong_sell = an.strength(buy,sell)
    print(strong_buy)
    print(strong_sell)  
    transfer(strong_buy, strong_sell, buy, sell)
    bids = {'Strong buy': strong_buy, 'Strong sell': strong_sell, 'Buy':buy, 'Sell':sell}
    bids_key =  list(bids.keys())
    msg = ''
    for each in bids_key:
        if len(bids[each]) != 0:
            s = ', '.join(bids[each])
            msg = msg + each + ': '+s+'\n'
##    popupmsg(msg)

    return




async def get_data(pair,timeframe):

    
    ts = TimeSeries(key=api_key,output_format='pandas')
    data, _ = await ts.get_intraday(symbol=pair,interval=timeframe, outputsize='full')
    path = 'excel/intraday_prices/'+timeframe+'/'+pair+'.csv'
    data = pd.DataFrame(data)
    data = data.reset_index()
    data = data.drop(data.columns[[2, 3, 4, 5]],axis=1)
    data.rename(columns={'date':'Date','1. open': 'Price'}, inplace=True)
    data['Date'] = data['Date'].dt.tz_localize('utc').dt.tz_convert(to_zone).astype(str).str[:-6]
    data['Date']= pd.to_datetime(data['Date'])
    data.to_csv(path, index=False)
##    print(data)
    df = cb.main(data)
    df = df.dropna()
    prediction = sk.sk_learn(df, pair)
    predictions[pair] = prediction[:250]
    df.insert(4, "AI Predictions", prediction)
    path = 'excel/intraday_indicators/'+timeframe+'/'+pair+' indicators.csv'
    df.to_csv(path, index=False)
    print('Done saving indicators for ', pair)
    rsi.price_rsiSummary(df,pair,1000,'intraday')    


    await ts.close()
    return (data,pair)



def request_data(timeframe):
    i = 0
    

    
    for each in chunks:
        if i != 0:
            sleep(61)
        else:
            i = 1
        
        loop = asyncio.get_event_loop()
        tasks = [get_data(pair,timeframe) for pair in each]
        group1 = asyncio.gather(*tasks)
        results = loop.run_until_complete(group1)     
        





def analyse_data():

    i = 0
    for each in chunks:
        
        if i != 0:
            sleep(61)
        else:
            i = 1
            
        loop = asyncio.get_event_loop()
        tasks = [get_data(pair) for pair in each]
        group1 = asyncio.gather(*tasks)
        results = loop.run_until_complete(group1)     

    

def time_frame(timeframe):
    request_data(timeframe)
    dfs = {}
    prices_path = 'excel/intraday_prices/'+timeframe+'/'
    intraday_pairs = os.listdir(prices_path)
    no_of_rows = 300# int(input('Please enter number of days to graph: '))

    for pair in intraday_pairs:
        sheet = pair.rsplit('.', 1)[0]
        path = prices_path+pair
        df = pd.read_csv(path,parse_dates=["Date"])
        dfs[sheet] = df
##    print(dfs)
    print(predictions)
    predictions.insert(0,'Date',df['Date'])
    trade(predictions)
    pred_path = 'excel/intraday_predictions.csv'
    predictions.to_csv(pred_path, index=False,date_format='%m-%d-%Y')
    currency_index = ci.cur_index(dfs, no_of_rows,'intrday')
    ci.graph_indexes(currency_index, no_of_rows,'intraday')
   



time_frame('5min')




stop1 = time.perf_counter()
stop2 = time.process_time()
print('Perf Counter: ', stop1 - start1)
print('Process Time: ', stop2 - start2)

print('Time Started ', start3)
print('Time Finished ',datetime.now())
print('Time Elapsed ', datetime.now()-start3)



##from datetime import datetime
##from dateutil import tz
##import asyncio
##from alpha_vantage.async_support.timeseries import TimeSeries
##import matplotlib.pyplot as plt
##import pandas as pd
##from time import sleep
##import math
##import aisklearn as sk
##import analysis as an
##import cbot as cb
##import rsi
##import os
##import currency_index as ci
##
##api_key = '714CQBJCXSZH03IX'
##pairs = os.listdir('excel/prices/')
##pairs = [pair.rsplit('.', 1)[0] for pair in pairs]
##dfs = {}
##n = 5
##chunks = [pairs[i:i + n] for i in range(0, len(pairs), n)]
##print(chunks)
##to_zone = tz.tzlocal()
##predictions = pd.DataFrame()
##today = datetime.now().date()
##rsi_dir = 'rsi/'+str(today)+'/intraday/'
##dfs = {}
##intraday_pairs = os.listdir('excel/intraday_prices/')
##no_of_rows = 300# int(input('Please enter number of days to graph: '))
##intraday_pairs = [x.rsplit('.', 1)[0] for x in intraday_pairs]
##
##
##
##
##
##
##def transfered(bid, path):
##    
##    
##    mkdir(path)
##    for each in bid:
####        filenames = [x+' rsi.png' for x in each]
##        for x in each:
##            old_path = rsi_dir + x +' rsi.png'
##            print(old_path)
##            new_path = path + x +' rsi '+ str(today) + '.png'
##            print(new_path)
##            try:
##                shutil.copyfile(old_path,new_path)
##            except:
##                print(x, "doesn't exist")
##
##    return
##
##
##
##def transfer(strong_buy, strong_sell, buy, sell):
##    
##    if len(strong_buy)!=0 or len(strong_sell)!=0:        
##        path = 'rsi/strongBid/'
##        bid = [strong_buy, strong_sell]
##        transfered(bid, path)
##        
##    
##    if len(buy)!=0 or len(sell)!=0:        
##        path = 'rsi/bid/'
##        bid = [buy, sell]
##        transfered(bid, path)    
##
##    return
##
##
##
##
##def popupmsg(msg):
##    popup = tk.Tk()
##    popup.wm_title("!")
##    label = ttk.Label(popup, text=msg, font=NORM_FONT)
##    label.pack(side="top", fill="x", pady=10)
##    B1 = ttk.Button(popup, text="Close", command = popup.destroy)
##    B1.pack()
##    popup.mainloop()
##
##
##
##def trade(predictions):
##    buy, sell = an.trade(predictions)
##    print('Buy',buy)
##    print('Sell',sell)
##    strong_buy,strong_sell = an.strength(buy,sell)
##    print(strong_buy)
##    print(strong_sell)  
##    transfer(strong_buy, strong_sell, buy, sell)
##    bids = {'Strong buy': strong_buy, 'Strong sell': strong_sell, 'Buy':buy, 'Sell':sell}
##    bids_key =  list(bids.keys())
##    msg = ''
##    for each in bids_key:
##        if len(bids[each]) != 0:
##            s = ', '.join(bids[each])
##            msg = msg + each + ': '+s+'\n'
####    popupmsg(msg)
##
##    return
##
##
##async def process_data(pair):
##    path = 'excel/intraday_prices/'+pair+'.csv'
##    data = pd.read_csv(path,parse_dates=["Date"])
####    data = data.reset_index()
####    data = data.drop(data.columns[[2, 3, 4, 5]],axis=1)
####    data.rename(columns={'date':'Date','1. open': 'Price'}, inplace=True)
####    data['Date'] = data['Date'].dt.tz_localize('utc').dt.tz_convert(to_zone).astype(str).str[:-6]
##   
##    print(data)
##    dfs[pair] = data
##    df = cb.main(data)
##    df = df.dropna()
##    prediction = sk.sk_learn(df, pair)
##    predictions[pair] = prediction[:250]
##    df.insert(4, "AI Predictions", prediction)
##    indicators_path = 'excel/intraday_indicators/'+pair+' indicators.csv'
##    df.to_csv(indicators_path, index=False)
##    print('Done saving indicators for ', pair)
##    rsi.price_rsiSummary(df,pair,250,'intraday')    
##
##
##    new_df = data.drop(data.columns[[2, 3, 4]],axis=1)
####    print(new_df)
##
##
##    await sleep()
##    return (data,pair)
##
##
##
##
##async def get_data(pair):
##    ts = TimeSeries(key=api_key,output_format='pandas')
##    data, _ = await ts.get_intraday(symbol=pair,interval='15min', outputsize='full')
##    path = 'excel/intraday_prices/'+pair+'.csv'
##    data = pd.DataFrame(data)
##    data = data.reset_index()
##    data = data.drop(data.columns[[2, 3, 4, 5]],axis=1)
##    data.rename(columns={'date':'Date','1. open': 'Price'}, inplace=True)
##    data['Date'] = data['Date'].dt.tz_localize('utc').dt.tz_convert(to_zone).astype(str).str[:-6]
##    data.to_csv(path, index=False)
##    print(data)
##    df = cb.main(data)
##    df = df.dropna()
##    prediction = sk.sk_learn(df, pair)
##    predictions[pair] = prediction[:250]
##    df.insert(4, "AI Predictions", prediction)
##    path = 'excel/intraday_indicators/'+pair+' indicators.csv'
##    df.to_csv(path, index=False)
##    print('Done saving indicators for ', pair)
##    rsi.price_rsiSummary(df,pair,250,'intraday')    
##
##
##    new_df = data.drop(data.columns[[2, 3, 4]],axis=1)
####    print(new_df)
##
##
##    await ts.close()
##    return (data,pair)
##
##
##
##def request_data():
##    
##    for each in chunks:
##        sleep(61)
##        loop = asyncio.get_event_loop()
##        tasks = [get_data(pair) for pair in each]
##        group1 = asyncio.gather(*tasks)
##        results = loop.run_until_complete(group1)     
##        
##
##def analyse_data():
##
##    
##    for each in chunks:
##
##        loop = asyncio.get_event_loop()
##        tasks = [process_data(pair) for pair in each]
##        group1 = asyncio.gather(*tasks)
##        results = loop.run_until_complete(group1)     
##
##    
##
##def main():
####    request_data()
####    print(pairs)
##    loop = asyncio.get_event_loop()
##    tasks = [aprocess_data(pair) for pair in intraday_pairs]
##    group1 = asyncio.gather(*tasks)
##    results = loop.run_until_complete(group1)
##    print(dfs[pairs[0]])
##    predictions.insert(0,'Date',dfs[pairs[0]])
##    trade(predictions)
##
##
##    for pair in intraday_pairs:
##        sheet = pair.rsplit('.', 1)[0]
##        path = 'excel/intraday_prices/'+pair
##        df = pd.read_csv(path,parse_dates=["Date"])
##        
####    print(dfs)
##    print(predictions)
##    predictions.insert(0,'Date',df['Date'])
##    trade(predictions)
##    pred_path = 'excel/intraday_predictions.csv'
##    predictions.to_csv(pred_path, index=False,date_format='%m-%d-%Y')
##    currency_index = ci.cur_index(dfs, no_of_rows,'intrday')
##    ci.graph_indexes(currency_index, no_of_rows,'intraday')
##   
##
##
##
##main()

