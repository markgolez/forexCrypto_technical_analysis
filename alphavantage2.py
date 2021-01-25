##import os
##from datetime import datetime
##import pandas_datareader.data as web
##api_key = '714CQBJCXSZH03IX'
##f = web.DataReader("EURUSD","av-daily-adjusted",start=datetime(2020,12,15),
##                   end=datetime(2020,12,28),api_key=api_key)
##
##print(f)
##
##



import asyncio
from alpha_vantage.async_support.timeseries import TimeSeries
##from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import pandas as pd
api_key = '714CQBJCXSZH03IX'

##ts = TimeSeries(key=api_key, output_format='pandas')
##data, meta_data = ts.get_intraday(symbol='EURUSD',interval='1min', outputsize='full')
##
##
##data['4. close'].plot()
##print(data)
##plt.title('Intraday Times Series for the MSFT stock (1 min)')
##plt.show()



symbols = ['EURUSD','GBPUSD']

path = 'excel/new.av.csv'
async def get_data(symbol):
    ts = TimeSeries(key=api_key,output_format='pandas')
    data, _ = await ts.get_intraday(symbol=symbol,interval='15min', outputsize='full')
    await ts.close()
    return data

loop = asyncio.get_event_loop()
tasks = [get_data(symbol) for symbol in symbols]
group1 = asyncio.gather(*tasks)
results = loop.run_until_complete(group1)
loop.close()
print(results)
results = pd.DataFrame(results)
results = results.T
results.to_csv(path,date_format='%m-%d-%Y')
print(results)
