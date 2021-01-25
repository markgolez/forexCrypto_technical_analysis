from time import sleep
import pandas as pd
from pandas import ExcelWriter
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

from scipy.signal import argrelextrema
import datetime
from forex_python.converter import get_rate, CurrencyRates
import os

import sklearn
##import polynom as po
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.datasets import load_iris

register_matplotlib_converters()


#setting parameters
points = 30 #local min and max
bollinger = 200
std = 2
periods = [1, 3, 5, 7, 15, 30, 90]


def computeRSI (data, k, periods):
    diff = data.diff(periods).dropna()        # diff in one field(one day)

    #this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff
    
    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[ diff>0 ]
    
    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[ diff < 0 ]
    
    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg   = up_chg.ewm(com=k-1 , min_periods=k).mean()
    down_chg_avg = down_chg.ewm(com=k-1 , min_periods=k).mean()
    
    rs = abs(up_chg_avg/down_chg_avg)
    rsi = 100 - 100/(1+rs)
    return rsi



def rsi_bid(df):
##    columns = df.columns
##    rsiColumns = [i for i in columns if 'rsi' in i]
    if df['rsi1'] < 20 and df['rsi3'] < 20 and df['rsi5'] < 20 and df['rsi7'] < 20 and df['rsi15']< 20 and df['rsi30']<20 and df['rsi90']<20:
        rsi_bid = 'Buy'
    elif df['rsi1']>80 and df['rsi3']>80 and df['rsi5']>80 and df['rsi7']>80 and df['rsi15']>80 and df['rsi30']>80 and df['rsi90']>80:
        rsi_bid = 'Sell'
    else:
        rsi_bid = 'Neutral'

    return rsi_bid




def bid_column(df):
    df = df.copy()
    #assign Buy and Sell to local extrema and minima
    with np.errstate(invalid='ignore'):
        df['min'] = df.iloc[argrelextrema(df.Price.values, np.less_equal, order=points)[0]]['Price']
        df['max'] = df.iloc[argrelextrema(df.Price.values, np.greater_equal, order=points)[0]]['Price']
        
    df['min'] = df['min'].fillna(0)
    df['max'] = df['max'].fillna(0)
    df["min"] = pd.cut(df["min"], 2, labels = ["Neutral", "Buy"] )
    df["max"] = pd.cut(df["max"], 2, labels = ["Neutral", "Sell"] )

    x = df['min'].loc[lambda x: x=="Buy"].index    
    for i in x:
        if i < 3:
            for j in range(4+i):
                df["min"][j]="Buy"
        elif i > len(df['min'])-3:
            last = len(df['min']) - i
            for j in range(3+last):
                df["min"][i-3+j]="Buy"
        else:
            for j in range(7):
                df["min"][i-3+j]="Buy"

    
    y = df['max'].loc[lambda x: x=="Sell"].index
    for i in y:
        if i < 3:
            for j in range(4+i):
                df["max"][j]="Sell"
        elif i > len(df['max'])-3:
            last = len(df['max']) - i
            for j in range(3 + last):
                df["max"][i-3+j]="Sell"
        else:
            for j in range(7):
                df["max"][i-3+j]="Sell"
    
    df["min"] = pd.Categorical(df["min"].replace('Neutral', np.nan), categories=["Neutral","Buy","Sell"])
    df["max"] = pd.Categorical(df["max"].replace('Neutral', np.nan), categories=["Neutral","Buy","Sell"])
    df['Bid'] = df['min'].combine_first(df['max'])
    df['Bid'] = df['Bid'].fillna('Neutral')
    df = df.drop(['min','max'],axis=1)
    
    return(df['Bid'])
    


def main(df):
      
    #df = pd.read_excel('forex.xlsx', parse_dates =["Date"], sheet_name = pair )        
    df['Bid'] = bid_column(df)
    
    df["Gain"] = 10000*df['Price'] -10000*df['Price'].shift(-1)

##    accumulated forward gain
##    for i in x:
##        df["ref"+str(i)] = df["Gain"].rolling(i).sum()
##        for j in range(i-1):
##            df["ref"+str(i)].iloc[j] = df["Gain"].iloc[:j+1].sum()
##    df["refsum"]=df.iloc[:,3:10].sum(axis=1)
##        
##    df["Bid"] = pd.cut(df["refsum"], 5, labels = ["A", "B", "C", "D", "E"] )
##    print(df[["refsum","Bid"]])
##    accumulate average gain
    df[["Date","Price","Gain"]] = df[["Date","Price","Gain"]].values[::-1]
    
    #turn off chain assignment error
    pd.set_option('mode.chained_assignment', None)            

    for i in periods:
        df["ave"+str(i)] = df["Gain"].rolling(i).mean()
        for j in range(i-1):
            df["ave"+str(i)].iloc[j] = df["Gain"].iloc[:j+1].mean()
        df["ave"+str(i)]=df["ave"+str(i)].values[::-1]

    #accumulated backward gain
    for i in periods:
        df["sum"+str(i)] = df["Gain"].rolling(i).sum()
        for j in range(i-1):
            df["sum"+str(i)].iloc[j] = df["Gain"].iloc[:j+1].sum()
        df["sum"+str(i)]=df["sum"+str(i)].values[::-1]

    df["sumsum"]=df.iloc[:,11:17].sum(axis=1)
    
    #reset chain assignment error
    pd.reset_option('mode.chained_assignment')     
    #rsi
    df = df.reset_index()
    df = df.drop(['index'],axis=1)
    for i in periods:
        df["rsi"+str(i)] = computeRSI(df["Price"], 14, i)
        df["rsi"+str(i)]= df["rsi"+str(i)].values[::-1]

    #df["rsisum"]=df.loc['rsi3','rsi90'].sum(axis=1)

    df["Sma"] = df.iloc[:,1].rolling(window=20).mean()
    df['Ema'] = df.iloc[:,1].ewm(span=40,adjust=False).mean()
    df["Upperbound"] = df.iloc[:,1].rolling(window=bollinger).mean() + df.iloc[:,1].rolling(window=bollinger).std()*std
    df["Lowerbound"] = df.iloc[:,1].rolling(window=bollinger).mean() - df.iloc[:,1].rolling(window=bollinger).std()*std
    
    df[["Date","Price","Gain","Sma","Ema","Upperbound","Lowerbound"]]=df[["Date","Price","Gain","Sma","Ema","Upperbound","Lowerbound"]].values[::-1]
    df = df.dropna()
    rsibid = df.apply(rsi_bid, axis = 1)
    df.insert(3, 'Bid1', rsibid)
    
    return(df)

