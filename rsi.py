from scipy.signal import argrelextrema
from sorted_months_weekdays import Month_Sorted_Month, Weekday_Sorted_Week
import datetime
import pandas as pd
from pandas.plotting import register_matplotlib_converters

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import numpy as np
import xlrd
import os

colors = ["red", "blue", "yellow", "green", "cyan","black","orange","purple","violet","brown","gray","alpha", "aqua","magenta", "cyan"]    

points = 10

today = datetime.datetime.now().date()
path = 'rsi/'+str(today)
try:
    # Create target Directory
    os.mkdir(path)
    #print("Directory " , path ,  " Created ") 
except FileExistsError:
    pass
    #print("Directory " , path ,  " already exists")

try:
    # Create target Directory
    os.mkdir(path+'/intraday')
    os.mkdir(path+'/crypto')
    os.mkdir(path+'/forex')
    
    
    #print("Directory " , path ,  " Created ") 
except FileExistsError:
    pass
    #print("Directory " , path ,  " already exists")



pairs = os.listdir('excel/indicators/')




def bid_column(df):

    df = df.copy()
    #assign Buy and Sell to local extrema and minima
##    with np.errstate(invalid='ignore'):
    df['min'] = df.iloc[argrelextrema(df.Price.values, np.less_equal, order=points)[0]]['Price']
    df['max'] = df.iloc[argrelextrema(df.Price.values, np.greater_equal, order=points)[0]]['Price']

##    df['min'] = df.Price[(df.Price.shift(1) > df.Price) & (df.Price.shift(-1) > df.Price)]
##    df['max'] = df.Price[(df.Price.shift(1) < df.Price) & (df.Price.shift(-1) < df.Price)]

    df['min'] = df['min'].fillna(0)
    df['max'] = df['max'].fillna(0)
    df["min"] = pd.cut(df["min"], 2, labels = ["Neutral", "Buy"] )
    df["max"] = pd.cut(df["max"], 2, labels = ["Neutral", "Sell"] )
    df["min"] = pd.Categorical(df["min"].replace('Neutral', np.nan), categories=["Neutral","Buy","Sell"])
    df["max"] = pd.Categorical(df["max"].replace('Neutral', np.nan), categories=["Neutral","Buy","Sell"])
    df['Bid'] = df['min'].combine_first(df['max'])
    df['Bid'] = df['Bid'].fillna('Neutral')
    df = df.drop(['min', 'max'],axis=1)
    
    return(df)



def buy_sell(df, bid, column_name):
    new = df.copy()
    new[column_name+bid] = new.loc[(new[column_name]==bid),['Date']]
    new = new.dropna()
    
    
##    counted = count_elements(new[bid])

    return new[column_name+bid]



def count_elements(seq) -> dict:
    """Tally elements from `seq`."""
    hist = {}
    for i in seq:
        hist[i] = hist.get(i, 0) + 1
##        print(i, hist[i])
    return hist



def price_rsiSummary(df,pair,no_of_rows,market):
    
    #axs = (ax1, ax2)
    df = bid_column(df)
    df = df.head(no_of_rows)
    bid = ['Buy', 'Sell']
    bid_vert_lines = []
    bid1_vert_lines = []
    bid2_vert_lines = []
    for  each in bid:
        x = buy_sell(df, each, 'Bid')
        bid_vert_lines.append(x)
        y = buy_sell(df, each, 'Bid1')
        bid1_vert_lines.append(y)
        z = buy_sell(df, each, 'AI Predictions')
        bid2_vert_lines.append(z)
        
    length = 12.5 + (no_of_rows//20)
    width = 8.5 + (no_of_rows//50)
    fig,  axs = plt.subplots(2, sharex=True, figsize=(length,width))
    price_ax, rsi_ax = axs
    title = pair + ' Price and Rsi Summary Graph (' + str(today) + ')'     
    fig.suptitle(title,fontsize= 16)
    price_ax.plot(df['Date'], df['Price'], color='black', label = 'Price')
    price_ax.plot(df['Date'], df['Upperbound'], color='blue', label = 'Bollinger')
    price_ax.plot(df['Date'], df['Lowerbound'], color='blue', label = 'Bollinger')
    price_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    columns = df.columns
    rsiColumns = [i for i in columns if 'rsi' in i]
    for index, each in enumerate(rsiColumns):
        rsi_ax.plot(df['Date'][0:no_of_rows], df[each][0:no_of_rows], color=colors[index], label = each)
    rsi_ax.axhline(y=20)
    rsi_ax.axhline(y=80)

    #extrema bid
    vert_color = ['#00ff00', '#ff0000']
    for idx, each in enumerate(bid_vert_lines):
        for index, every in enumerate(each):
            rsi_ax.axvline(x = every, color = vert_color[idx])#, label = bid[idx] if index == 0 else "")
            price_ax.axvline(x = every, color = vert_color[idx], label = 'Ext '+bid[idx] if index == 0 else "")
    #rsi bid
    bid1_vert_color = ['blue', 'orange']
    for idx, each in enumerate(bid1_vert_lines):
        for index, every in enumerate(each):
            rsi_ax.axvline(x = every, color = bid1_vert_color[idx], linestyle='--', dashes=(30, 1))
            price_ax.axvline(x = every, color = bid1_vert_color[idx], linestyle='--', dashes=(30, 1), label = 'Rsi '+ bid[idx] if index == 0 else "")
    #AI bid
    bid2_vert_color = ['cyan', 'magenta']
    for idx, each in enumerate(bid2_vert_lines):
        for index, every in enumerate(each):
            rsi_ax.axvline(x = every, color = bid2_vert_color[idx], linestyle=':', dashes=(5, 1))
            price_ax.axvline(x = every, color = bid2_vert_color[idx], linestyle=':', dashes=(5, 1), label = 'AI '+bid[idx] if index == 0 else "")

    price_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    rsi_ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
   
    yaxis = axs.flat
    yaxis[0].set(ylabel='Price')
    yaxis[1].set(ylabel='Rsi Index')

    min_ticks = no_of_rows//20
    locator = mdates.AutoDateLocator(minticks=min_ticks, maxticks=min_ticks+100)
    formatter = mdates.ConciseDateFormatter(locator)
    rsi_ax.xaxis.set_major_locator(locator)
    rsi_ax.xaxis.set_major_formatter(formatter)

    plt.xlabel('Date', fontsize = 12)
    plt.xticks(rotation=50,fontsize=9)
    plt.subplots_adjust(left = 0.08, top=0.93, bottom=0.1, hspace=0.03, wspace=0.1)
    if market == 'crypto':
        filename = path + '/crypto/' + pair + ' rsi.png'
    elif market == 'forex':
        filename = path + '/forex/' + pair + ' rsi.png'
    elif market == 'intraday':
        filename = path + '/intraday/' + pair + ' rsi.png'
    plt.savefig(filename, dpi=100)
    print('Done saving ', pair , 'RSI') 
##    plt.show()
    plt.close()

    return 



def main():


    for pair in pairs:
        path = 'excel/indicators/'+pair
        sheet = pair.rsplit('.', 1)[0]
        df = pd.read_csv(path, parse_dates=['Date'], infer_datetime_format=True)
        price_rsiSummary(df,sheet)


    return


##main()
