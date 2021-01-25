from time import sleep
import datetime
import pandas as pd
from pandas import ExcelWriter
import numpy as np
from forex_python.bitcoin import BtcConverter
import xlrd

import aisklearn as sk
import cbot as cb
import rsi

import cryptocompare


b = BtcConverter()
## return current price
def current_price():
    '''input: currency pair
       output: current price of the input currency pair
    '''
    date_now = datetime.datetime(2010, 7, 24, 19, 39, 36, 815417)
    rate = b.get_previous_price('USD', date_now)#get_rate(pair[:3], pair[-3:], date_now)

    return rate



## return updated date and price
def update_price(newdf,crypto):
    '''input: list of dates to update price and currency pair
       output: price and dates
    '''

    success = False
    while success == False:
        try:
            data = cryptocompare.get_historical_price(crypto, 'USD', newdf['Date'])
            print(newdf)
            print(data)
            
            rate = data[crypto]['USD']            
##            rate = b.get_previous_price('USD', newdf['Date'])
            success = True
##            print(rate)
        except:
            sleep(0)
    sleep(0)

    return rate



def save(writer, df, sheetName):
    df.to_excel(writer, sheet_name = sheetName, index=False)




def file_update(crypto):
    ''' update date_price.xlsx historical prices 
    '''
    print('Updating prices for ', crypto)
    file_name = crypto+'_date_price.xlsx'
    path = 'excel/crypto_prices/'+crypto+'_date_price.xlsx'
    date_price = pd.ExcelWriter(path, engine='xlsxwriter',datetime_format='mmm d yyyy', date_format='mmmm dd yyyy')
    df = pd.read_excel(path)
    start_date = df["Date"][0].date()
    start_date = start_date + datetime.timedelta(days = 1)
    date_now = datetime.datetime.now().date()#datetime.datetime(2020, 4, 26, 22, 39, 36, 815417)
    date1 = datetime.date(int(start_date.strftime("%Y")),int(start_date.strftime("%m")),int(start_date.strftime("%d")))
    date2 = datetime.date(int(date_now.strftime("%Y")),int(date_now.strftime("%m")),int(date_now.strftime("%d")))
    no_of_days = (date2 - date1).days

    if no_of_days > 0:
        newdf = pd.DataFrame()
        newdf['Date'] = pd.date_range(start_date, periods=no_of_days, freq='D')
        newdf['Date'] = newdf['Date'].values[::-1]
        
        newdf['Price'] = newdf.apply(update_price, axis = 1,args=(crypto,))

        df = pd.concat([newdf, df])
        df.reset_index(inplace=True)
        df = df.drop(['index'],axis=1)
##        print(df)
        save(date_price, df, crypto)
        date_price.save()
##        btc_date_price.close()
    
        
    print(no_of_days, 'days', crypto, 'price updated')

    return df


def main(no_of_rows):
    no_of_rows = 1000
    crypto_list = ['BTC','XRP','ETH','TRX','BNB','BSV','EOS','WBTC','ADA','BCH']
    for crypto in crypto_list:
        df = file_update(crypto)
        print('Done updating prices for ',crypto)
        df= cb.main(df)
        df = df.dropna()
        prediction = sk.sk_learn(df, crypto)
        df.insert(4, "AI Predictions", prediction)
        pred_path = 'excel/crypto_indicators/'+crypto+' indicators.csv'
        df.to_csv(pred_path, index=False,date_format='%m-%d-%Y')
        print('Done saving indicators for ', crypto)
        rsi.price_rsiSummary(df,crypto,no_of_rows,'crypto')    

    return

##main(1000)








##import cryptocompare
##import datetime
##
####coin_list = cryptocompare.get_coin_list(format=False)
##
##
##price = cryptocompare.get_historical_price('XRP', 'USD', datetime.datetime(2018,5,15))
##print(price)
##
##







##import requests
##
##TICKER_API_URL = 'https://api.coinmarketcap.com/v1/ticker/'
##
##def get_latest_crypto_price(crypto):
##  
##  response = requests.get(TICKER_API_URL+crypto)
##  response_json = response.json()
##  
##  return float(response_json[0]['price_usd'])
##
##
##
##def main():
##  
##  last_price = -1
##  
##  while True:
##    
##    crypto = 'bitcoin'
##    price = get_latest_crypto_price(crypto)
##  
##    if price != last_price:
##      print('Bitcoin price: ',price)
##      last_price = price
##
##
##main()
