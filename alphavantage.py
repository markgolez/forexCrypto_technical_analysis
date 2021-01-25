import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.foreignexchange import ForeignExchange
import matplotlib.pyplot as plt
##API key: 714CQBJCXSZH03IX
api_key = '714CQBJCXSZH03IX'
ts = TimeSeries(key=api_key, output_format='pandas')
fx = ForeignExchange(key=api_key, output_format='pandas')

def get_price(ticker,columns=['05. price','07. latest trading day']):
    '''
    Returns a DataFrame of prices for ticker on Alpha Vantage API 
    '''
    data, meta_data= ts.get_quote_endpoint(ticker)
    data.reset_index(inplace=True)
    data = data[columns]
    data.columns = ['price', 'date']
    data.set_index('date', inplace=True)
    return data

def get_prices(tickers,columns=['05. price','07. latest trading day']):
    '''
    Returns a DataFrame of prices for a list of tickers on Alpha Vantage API  
    '''
    prices = pd.DataFrame()
    for ticker in tickers:
        ticker_prices = get_price(ticker, columns)
        ticker_prices.columns = [ticker]
        if ticker_prices.dropna().empty == False:
            prices = pd.concat([prices, ticker_prices], axis=1)
        else:
            print(f"{ticker} has no data!")
    return prices

def get_rate(from_curr, to_curr='GBP', columns=['5. Exchange Rate', '6. Last Refreshed']):
    '''
    Returns the spot rate from Alpha Vantage API
    '''
    rate, metadata = fx.get_currency_exchange_rate(from_currency=from_curr, to_currency=to_curr)
    rate.reset_index(inplace=True)
    rate = rate[columns]
    rate.columns = ['rate', 'date']
    rate.set_index('date', inplace=True)
    rate.index = pd.to_datetime(rate.index).strftime('%Y-%m-%d')
    return rate


def get_rates(from_currencies, to_curr='GBP', columns=['5. Exchange Rate', '6. Last Refreshed']):
    '''
    Returns a DataFrame of rates for a list of currencies on Alpha Vantage API  
    '''
    rates = pd.DataFrame()
    for curr in from_currencies:
        rate = get_rate(from_curr=curr, to_curr=to_curr, columns=columns)
        rate.columns = [curr]
        if rate.dropna().empty == False:
            rates = pd.concat([rates, rate], axis=1)
        else:
            print(f"{curr} has no data!")
    return rates






from alpha_vantage.foreignexchange import ForeignExchange
from pprint import pprint
cc = ForeignExchange(key=api_key)
# There is no metadata in this call
data, _ = cc.get_currency_exchange_rate(from_currency='EUR',to_currency='USD')
pprint(data)


##
##
##import asyncio
##from alpha_vantage.async_support.timeseries import TimeSeries
##
##symbols = ['AAPL', 'GOOG', 'TSLA', 'MSFT']
##
##
##async def get_data(symbol):
##    ts = TimeSeries(key='YOUR_KEY_HERE')
##    data, _ = await ts.get_quote_endpoint(symbol)
##    await ts.close()
##    return data
##
##loop = asyncio.get_event_loop()
##tasks = [get_data(symbol) for symbol in symbols]
##group1 = asyncio.gather(*tasks)
##results = loop.run_until_complete(group1)
##loop.close()
##print(results)
##
##
##
##
##
##
##
##import asyncio
##from alpha_vantage.async_support.timeseries import TimeSeries
##
##symbols = [('EUR','USD'), ('USD','JPY'), ('GBP','USD')]
##
##
##async def get_data(symbol):
##    cc = ForeignExchange(key=api_key)
##    data, _ = await cc.get_currency_exchange_rate(from_currency=symbol[0],to_currency=symbol[1])
##    await cc.close()
##    return data
##
##loop = asyncio.get_event_loop()
##tasks = [get_data(symbol) for symbol in symbols]
##group1 = asyncio.gather(*tasks)
##results = loop.run_until_complete(group1)
##loop.close()
##print(results)
##
##
