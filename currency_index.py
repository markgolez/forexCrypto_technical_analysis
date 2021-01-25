import time
import datetime
##start1 = time.perf_counter()
##start2 = time.process_time()
##start3 = datetime.datetime.now()

import cbot as cb
import datetime
import pandas as pd
from pandas import ExcelWriter
from pandas.plotting import register_matplotlib_converters
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import xlrd
import os
import threading
from PIL import Image


today = datetime.datetime.now().date()
path = 'rsi/strongBid/'
try:
    # Create target Directory
    os.mkdir(path)
    
    #print("Directory " , path ,  " Created ") 
except FileExistsError:
    pass
    #print("Directory " , path ,  " already exists")



USD = {'EUR':0.576,'JPY':0.136,'GBP':0.119,'CHF':0.036,'CAD':0.091,'NZD':0.001,'AUD':0.2,'SEK':0.042}
EUR = {'USD':0.576,'JPY':0.2,'GBP':0.2,'CHF':0.2,'CAD':0.04,'NZD':0.3,'AUD':0.2,'SEK':0.1}
JPY = {'USD':0.3,'EUR':0.2,'GBP':0.2,'CHF':0.2,'CAD':0.04,'NZD':0.3,'AUD':0.2,'SEK':0.1}
GBP = {'USD':0.3,'EUR':0.2,'JPY':0.2,'CHF':0.2,'CAD':0.04,'NZD':0.3,'AUD':0.2,'SEK':0.1}
AUD = {'USD':0.3,'EUR':0.2,'JPY':0.2,'GBP':0.2,'CHF':0.04,'CAD':0.3,'NZD':0.2,'SEK':0.1}
CHF = {'USD':0.3,'EUR':0.2,'JPY':0.2,'GBP':0.2,'CAD':0.04,'NZD':0.3,'AUD':0.2,'SEK':0.1}
CAD = {'USD':0.3,'EUR':0.2,'JPY':0.2,'GBP':0.2,'CHF':0.04,'NZD':0.3,'AUD':0.2,'SEK':0.1}
NZD = {'USD':0.3,'EUR':0.2,'JPY':0.2,'GBP':0.2,'CHF':0.04,'CAD':0.3,'AUD':0.2,'SEK':0.1}
SEK = {'USD':0.3,'EUR':0.2,'JPY':0.2,'GBP':0.2,'CHF':0.04,'CAD':0.3,'NZD':0.2,'AUD':0.1}

currency = ['USD','EUR','JPY','GBP','CHF','CAD', 'NZD', 'AUD','SEK']
colors = {'USD':'red', 'EUR': '#00ff00', 'JPY': 'magenta', 'GBP': 'cyan', 'AUD': 'blue', 'CHF':'yellow', 'CAD':'black','NZD':'orange', 'SEK':'grey'}#"purple","violet","brown","gray","alpha", "aqua","magenta", "cyan"}
currency_index = pd.DataFrame()


def setter(curr):
    if curr == 'USD':
        cur = USD
    elif curr == 'EUR':
        cur = EUR
    elif curr == 'JPY':
        cur = JPY
    elif curr == 'GBP':
        cur = GBP
    elif curr == 'CHF':
        cur = CHF
    elif curr == 'CAD':
        cur = CAD
    elif curr == 'NZD':
        cur = NZD
    elif curr == 'AUD':
        cur = AUD
    elif curr == 'SEK':
        cur = SEK

    return cur
    



def indexer(df_under, df_over, no_of_rows, curr):
    
    cur = setter(curr)
    weighted_df_under = pd.DataFrame()
    if df_under.empty == False:
        for column in df_under.columns:
            weighted_df_under['weighted'+column] = cur[column]*df_under[column]
        
        weighted_df_under['total'] = weighted_df_under.sum(axis=1)
        total = weighted_df_under['total']
    else:
        total = 0
            
    weighted_df_over = pd.DataFrame()
    if df_over.empty == False:
        for column in df_over.columns:
            weighted_df_over['weighted'+column] = 1/(cur[column]*df_over[column])
        
        weighted_df_over['total'] = weighted_df_over.sum(axis=1)
        total2 = weighted_df_over['total']
    else:
        total2 = 0   

    index_df = pd.DataFrame()
    index_df['total'] = 1/(1+total+total2)
    index_df['total'] = index_df['total'].values[::-1]
    index_df[curr+'index'] = cb.computeRSI(index_df['total'], 14, 1)
    index_df[curr+'index'] = index_df[curr+'index'].values[::-1]

    return index_df[curr+'index']



def rsIndex(cur, subdf, no_of_rows):
    df_under = pd.DataFrame()
    df_over = pd.DataFrame()
    sheets =  list(subdf.keys())
    for sheet in sheets:
        x = sheet[:3]
        y = sheet[-3:]
        if x == cur:
            df = subdf[sheet]
            df_over[y] = df['Price'][0:no_of_rows]
        elif y == cur:
            df = subdf[sheet]
            df_under[x] = df['Price'][0:no_of_rows]
        else:
            continue
        
    currency_index[cur] = indexer(df_under,df_over,no_of_rows,cur)
    
    return


def cur_index(dfs, no_of_rows,market):
    
    threads = []
    pairs = list(dfs.keys())
    df = dfs[pairs[0]]
    currency_index['Date'] = df['Date'][0:no_of_rows]
    
    for cur in currency:
        
        cur_pairs = [i for i in pairs if cur in i]
        subdf ={x: dfs[x] for x in cur_pairs}
        rsIndex(cur, subdf, no_of_rows)

    path = 'excel/'+market+'_currency_index.csv'
    currency_index.to_csv(path, index=False)   

    return currency_index


def show(filename):

    image = Image.open(filename)
    image.show()




def graph_indexes(currency_index, no_of_rows,market):

    length = 12.5 + (no_of_rows//20)
    width = 8.5 + (no_of_rows//50)
    fig = plt.figure(figsize=(length,8.5))
    title = 'Major Currency Index Last '+ str(no_of_rows) + ' Days (' + str(today) + ')' 
    fig.suptitle(title,fontsize= 16)
    ax = fig.add_subplot(111)
    columns = list(currency_index.columns)
    columns = columns[1:]
    dates = currency_index['Date'][0:no_of_rows]

    min_ticks = no_of_rows//12
    locator = mdates.AutoDateLocator(minticks=min_ticks, maxticks=min_ticks+10)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    
    for idx, cur in enumerate(columns):
        ax.plot(currency_index['Date'][0:no_of_rows], currency_index[cur][0:no_of_rows], color=colors[cur], label = cur+' index')
        
##    plt.xticks(np.arange(0, len(dates), 12))
    plt.xticks(rotation=50,fontsize=9)
    plt.xlabel('Date', fontsize = 12)
    plt.ylabel('Index', fontsize= 12)
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.subplots_adjust(left = 0.05, bottom=0.1, right=0.9, top=0.93)
    if market == 'crypto':
        filename = path + '/'+str(today)+' major_crypto_index.png'
    elif market == 'forex':
        filename = path + '/'+str(today)+' major_forex_index.png'
    elif market == 'intraday':
        filename = path + '/'+str(today)+' intraday_major_index.png'
    plt.savefig(filename, dpi=100)
    print('Done Ploting Major  Indexes Graph') 
##    plt.show()
    plt.close()

    show(filename)

    return









def main(dfs, no_of_rows,market):
    currency_index = cur_index(dfs, no_of_rows,market)
    graph_indexes(currency_index, no_of_rows,market)


    return



def main2():
    dfs = {}
    pairs = os.listdir('excel/prices/')
    no_of_rows = int(input('Please enter number of days to graph: '))

    for pair in pairs:
        sheet = pair.rsplit('.', 1)[0]
        path = 'excel/prices/'+pair
        df = pd.read_excel(path, sheet_name=sheet)
        dfs[sheet] = df
##    print(dfs)
    currency_index = cur_index(dfs,no_of_rows)
    graph_indexes(currency_index,no_of_rows)
   

    return










##main2()    
##
##
##
##
##stop1 = time.perf_counter()
##stop2 = time.process_time()
####print('Perf Counter: ', stop1 - start1)
####print('Process Time: ', stop2 - start2)
##elapsed = datetime.datetime.now()-start3
####print('Time Started ', start3)
####print('Time Finished ',datetime.datetime.now())
##print('Time Elapsed ', elapsed)
