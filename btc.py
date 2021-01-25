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



btc_date_price = pd.ExcelWriter('excel/btc_date_price.xlsx', engine='xlsxwriter',datetime_format='mmm d yyyy', date_format='mmmm dd yyyy')

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
def update_price(newdf):
    '''input: list of dates to update price and currency pair
       output: price and dates
    '''
    success = False
    while success == False:
        try:
            rate = b.get_previous_price('USD', newdf['Date'])
            success = True
##            print(rate)
        except:
            sleep(5)
    sleep(3)

    return rate



def save(writer, df, sheetName):
    df.to_excel(writer, sheet_name = sheetName, index=False)




def file_update():
    ''' update date_price.xlsx historical prices 
    '''
    print('Updating prices for BTC...')
    df = pd.read_excel('excel/btc_date_price.xlsx')
    start_date = df["Date"][0].date()
    start_date = start_date + datetime.timedelta(days = 1)
    date_now = datetime.datetime.now().date()#datetime.datetime(2020, 4, 26, 22, 39, 36, 815417)
    date1 = datetime.date(int(start_date.strftime("%Y")),int(start_date.strftime("%m")),int(start_date.strftime("%d")))
    date2 = datetime.date(int(date_now.strftime("%Y")),int(date_now.strftime("%m")),int(date_now.strftime("%d")))
    no_of_days = (date2 - date1).days
    print(no_of_days, ' days to update')
    if no_of_days > 0:
        newdf = pd.DataFrame()
        newdf['Date'] = pd.date_range(start_date, periods=no_of_days, freq='D')
        newdf['Date'] = newdf['Date'].values[::-1]
        
        newdf['Price'] = newdf.apply(update_price, axis = 1)

        df = pd.concat([newdf, df])

        save(btc_date_price, df, 'BTC')
        btc_date_price.save()
##        btc_date_price.close()
    
        
    print(no_of_days, ' days BTC price updated')

    return df


def main(no_of_rows):
    no_of_rows = 1500
    df = file_update()
    print('Done updating prices for BTC')
    df= cb.main(df)

    df = df.dropna()
    prediction = sk.sk_learn(df, 'BTC')
    df.insert(4, "AI Predictions", prediction)
    pred_path = 'excel/btc indicators.csv'
    df.to_csv(pred_path, index=False,date_format='%m-%d-%Y')
    print('Done saving BTC indicators')
    rsi.price_rsiSummary(df,'BTC',no_of_rows)    

    return

##main(1000)





##def main():
##    
##    
##    df = file_update()
##    
##    print('Done updating prices for BTC')
##    df = cb.main(df)
##    save(btc_indicators_writer, df, 'BTC')
##    print(df)
##    btc_indicators_writer.save()
####    prediction_writer.close()
##    btc_indicators_writer.close()
##
##    df = pd.read_excel('xls/btc_indicator.xlsx')
##    rsi.price_rsiSummary(df,'BTC')
##
##    return
##
##
####main()
