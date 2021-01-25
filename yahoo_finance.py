import yfinance as yf

def price(ticker, period='1d',columns=['Close']):
    '''
    Returns a DataFrame of prices for ticker from Yahoo Finance API 
    '''
    obj = yf.Ticker(ticker)
    return obj.history(period=period)[columns]

def prices(tickers, period='1h',columns=['Close']):
    '''
    Returns a DataFrame of prices for a list of tickers from Yahoo Finance API 
    '''
    prices = pd.DataFrame()
    for ticker in tickers:
        ticker_prices = price(ticker, period, columns)
        if ticker_prices.dropna().empty == False:
            prices = pd.concat([prices, ticker_prices], axis=1)
        else:
            print(f"{ticker} has no data!")
    return prices
