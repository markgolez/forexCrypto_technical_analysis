import time
import datetime
##start1 = time.perf_counter()
##start2 = time.process_time()
##start3 = datetime.datetime.now()

from time import sleep
import datetime
import pandas as pd
from pandas import ExcelWriter
import numpy as np
from forex_python.converter import get_rate, CurrencyRates
import xlrd
import os



## return current price
def current_price(pair):
    '''input: currency pair
       output: current price of the input currency pair
    '''
    date_now = datetime.datetime.now().date()
    rate = get_rate(pair[:3], pair[-3:], date_now)

    return rate



## return dates to update
def update_date(last_date):
    ''' input: last date
        outpu: list of last date to current date
    '''
    start_date = last_date
    date_now = datetime.datetime.now().date()
    dates_to_update = []
    x = 0
    while last_date != date_now:
        last_date = start_date + datetime.timedelta(days = x)
        day = int(last_date.strftime("%w"))
        if day == 0:
            x += 1
        elif day == 6:
            x += 1
        else:
            dates_to_update.append(last_date)
            x += 1    
    dates_to_update.reverse()

    return dates_to_update




## return updated date and price
def update_price(dates_to_update, pair):
    '''input: list of dates to update price and currency pair
       output: price and dates
    '''
    prices = []
    
    for date in dates_to_update:
        rate = get_rate(pair[:3], pair[-3:], date) 
        success = False
        while success == False:
            try:
                rate = get_rate(pair[:3], pair[-3:], date)
                success = True

            except:
                sleep(1)
        sleep(1)
        prices.append(rate)
    new_df = pd.DataFrame(
             {"Price" : prices},
              index = dates_to_update)

    return new_df



def save(writer, df, pair):
    df.to_excel(writer, sheet_name = pair, index=False)




def file_update(pair, sheet):
    ''' update date_price.xlsx historical prices 
    '''
    
    path = 'excel/prices/'+pair
    date_price = pd.ExcelWriter(path, engine='xlsxwriter',datetime_format='mmm d yyyy', date_format='mmmm dd yyyy')
    df = pd.read_excel(path, sheet_name=sheet)
##    df = df.iloc[2:,:]
    last_date = df["Date"][0].date()
    date_now = datetime.datetime.now().date()
    
    dates_to_update = update_date(last_date)
    if len(dates_to_update) != 0:
        new_df = update_price(dates_to_update,sheet)
        df = df.set_index("Date")
        df = pd.concat([new_df, df.iloc[1:,:]])
        df.reset_index(inplace=True)
        df.rename(columns={'index':'Date'}, inplace=True)
        save(date_price, df, sheet)
        date_price.save()
##        date_price.close()
    print('Done updating prices for ', sheet)
        
    return df



def main():
    dfs = {}
    pairs = os.listdir('excel/prices/')    
    for pair in pairs:
        sheet = pair.rsplit('.', 1)[0]
        df = file_update(pair,sheet)
        dfs[sheet] = df

    msg = 'All pairs are updated and saved!'
    print(msg)
    
    return dfs


##main()


##stop1 = time.perf_counter()
##stop2 = time.process_time()
####print('Perf Counter: ', stop1 - start1)
####print('Process Time: ', stop2 - start2)
##elapsed = datetime.datetime.now()-start3
####print('Time Started ', start3)
####print('Time Finished ',datetime.datetime.now())
##print('Time Elapsed ', elapsed)
