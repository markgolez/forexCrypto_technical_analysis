import time
import datetime
start1 = time.perf_counter()
start2 = time.process_time()
start3 = datetime.datetime.now()

import file_update as fu
import analysis as an
import currency_index as ci
import cbot as cb
import rsi
import crypto as btc
import aisklearn as sk
##import polynom as po

import threading
import pandas as pd
from pandas import ExcelWriter
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

import tkinter as tk
from tkinter import ttk
#from PIL import Image


def cur_index(dfs):
    ci.main(dfs,no_of_rows,'forex')


def btc_update():
     btcPrice = btc.main(no_of_rows)


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
            new_path = path + x +' rsi '+ new_start3 + '.png'
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
    


def main():

    thread1 = threading.Thread(target=btc_update)
    thread1.start()
    dfs = fu.main()
    thread2 = threading.Thread(target=cur_index, args=(dfs,))
    thread2.start()
    for pair in pairs:
        sheet = pair.rsplit('.', 1)[0]
        path = 'excel/indicators/'+pair
        df = dfs[sheet]
        df = cb.main(df)
       
        df = df.dropna()
        prediction = sk.sk_learn(df, sheet)
        predictions[sheet] = prediction[:250]
        df.insert(4, "AI Predictions", prediction)
        df.to_csv(path, index=False,date_format='%m-%d-%Y')
        print('Done saving indicator for ',sheet)
        rsi.price_rsiSummary(df,sheet,no_of_rows,'forex')
     
    predictions.insert(0,'Date',df['Date'])
    
##    predictions = pd.read_csv('excel/forex_predictions.csv')
    thread3 = threading.Thread(target=trade, args=(predictions,))
    thread3.start()

    pred_path = 'excel/forex_predictions.csv'
    predictions.to_csv(pred_path, index=False,date_format='%m-%d-%Y')
    
    thread1.join()
    thread2.join()
    thread3.join()



##    filename = 'rsi/'+str(today)+'/major_index.png'
##    image = Image.open(filename)
##    image.show()
    




print('A: Update Forex and Btc Prices')
print('B: Graph Major Currency Index')
print('C: Do A and B')
print('D: Run everything \n')

valid = False
while not valid:
##    clear = os.system('CLS')
    letter = 'D' #input('Please enter the letter of your choice: ')    
    if letter == 'A':
        dfs = fu.main()
        btc.file_update()
        valid = True
    elif letter == 'B':
        ci.main2()
        valid = True
    elif letter == 'C':
        dfs = fu.main()
        ci.main2()
        valid = True
    elif letter == 'D':
        no_of_rows = 250  #int(input('Please enter number of days to graph: '))
        predictions = pd.DataFrame()
        today = start3.date()
        rsi_dir = 'rsi/'+str(today)+'/forex/'
        NORM_FONT = ("Helvetica", 10)
        new_start3 = str(start3)
        new_start3 = new_start3.replace(":", "'")
        pairs = os.listdir('excel/prices/')
        sheets = [x.rsplit('.', 1)[0] for x in pairs]
        print('Pairs to update:\n',sheets)
        print('Total sheets to update: ', len(sheets))
        main()
        valid = True
    else:
        print('Wrong Input')
        continue





stop1 = time.perf_counter()
stop2 = time.process_time()
print('Perf Counter: ', stop1 - start1)
print('Process Time: ', stop2 - start2)
elapsed = datetime.datetime.now()-start3
print('Time Started ', start3)
print('Time Finished ',datetime.datetime.now())
print('Time Elapsed ', elapsed)
