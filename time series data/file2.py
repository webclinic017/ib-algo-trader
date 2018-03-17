import pandas_datareader as pdr
import pandas as pd
import datetime
import quandl
import matplotlib.pyplot as plt
import numpy as np

'''
# broken, need fixing

def get(ticker, startdate, enddate):
  def data(ticker):
    return (pdr.get_data_yahoo(ticker, start=startdate, end=enddate))
  datas = map(data, ticker)
  return(pd.concat(datas, keys=ticker, names=['Ticker', 'Date']))

tickers = ['AAPL', 'MSFT', 'IBM', 'GOOG']
all_data = get(tickers, datetime.datetime(2006, 10, 1), datetime.datetime(2012, 1, 1))
'''

sum1aapl = pdr.get_data_yahoo('AAPL',
                             start=datetime.datetime(2006,10,1),
                             end=datetime.datetime(2018,1,1))

'''
#daapl.insert(loc=0, column='ticker', value=np.nan)
print(daapl)
dmsft = pdr.get_data_google('MSFT',
                             start=datetime.datetime(2006,10,1),
                             end=datetime.datetime(2018,1,1))
dibm = pdr.get_data_google('IBM',
                             start=datetime.datetime(2006,10,1),
                             end=datetime.datetime(2018,1,1))
dgoog = pdr.get_data_google('GOOG',
                             start=datetime.datetime(2006,10,1),
                             end=datetime.datetime(2018,1,1))
'''

'''
#all_data = (daapl dmsft  dibm + dgoog)
#all_data.to_csv('4tech_ohlc.csv')    #get data and saves into csv




# Isolate the `Adj Close` values and transform the DataFrame
daily_close_px = all_data[['Close']].reset_index().pivot('Date', 'Ticker', 'Close')

# Calculate the daily percentage change for `daily_close_px`
daily_pct_change = daily_close_px.pct_change()

# Plot the distributions
daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))

# Show the resulting plot
plt.show()
'''