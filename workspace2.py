import datetime
from PIL import Image

import win32console
import win32gui


def main():
    win=win32console.GetConsoleWindow()       # For closing command window
    win32gui.ShowWindow(win,0)


    today = datetime.datetime.now()
    today = today.date()
    filename = 'rsi/2020-06-25/major_index.png'
    image = Image.open(filename)
    image.show()



##
##
##def main():
##    amount = float(input('Enter Amount to transfer in Peso'))
##    bahtrate = float(input('Baht to peso rate'))
##    pesorate = float(input('Peso to Baht rate'))
##    if amount < 15000:
##        bahtfee = 150
##    elif amount < 20000:
##        bahtfee = 200
##    elif amount < 30000:
##        bahtfee = 250
##    elif amount <= 50000:
##        bahtfee = 350
##
##    if amount < 15000:
##        pesofee =150
##    elif amount < 20000:
##        pesofee = 200
##    elif amount < 30000:
##        pesofee = 250
##    elif amount <= 50000:
##        pesofee = 350
##    capital = amount/bahtrate + bahtfee
##    roi = (amount-pesofee)*pesorate
##    profit = roi - capital
##    
##    return (capital, roi, profit)
##
##    
