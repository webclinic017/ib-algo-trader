import pandas_datareader as pdr
import pandas as pd
import datetime
import quandl
import matplotlib.pyplot as plt
import numpy as np
import pandas.plotting as pdp


def get(tickers, startdate, enddate):
  def data(ticker):
    return (pdr.get_data_morningstar(ticker, start=startdate, end=enddate))
  datas = map(data, tickers)
  return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

tickers = ['AAPL', 'MSFT', 'IBM', 'GOOG']

all_data = get(tickers, datetime.datetime(2006, 10, 1), datetime.datetime(2018, 1, 1))

#all_data = pd.read_csv('all_data.csv') # Cannot parse the same data from web data

daily_close_px = all_data[['Close']].reset_index().pivot('Date', 'Ticker', 'Close')

daily_pct_change = daily_close_px.pct_change()

daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))

#plt.savefig('all_data_hist.png')   # need to have the data before plt.show() or data will be cleared
plt.show()

#pd.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1,figsize=(12,12))   # this function is broken, use pd.plotting as pdp
pdp.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1,figsize=(12,12))

plt.savefig('all_data_scattermatrix.png')
plt.show()


'''
Moving Windows, when u compute the stats on window of data by a particular period of time, then slide the window 
across the data by a specific interval. Continually calculated as long as the window falls first within the dates
of the time series.
'''
#data = quandl.get('AAPL', authtoken='-VQTkx89BPNGVyjKvD1p')
# from earlier reference (file1)
aapl = pdr.get_data_morningstar('AAPL',
                           start=datetime.datetime(2006, 10, 1),
                           end=datetime.datetime(2018, 1, 1))



#must use own data, can request 20 pulls per 10 min from quandl (uses AdjClose)
#csv (uses Close)
#aapl = pd.read_csv('aapl_ohlc.csv')

adj_close_px = aapl['Close']

# Calculate the moving average:
# rolling_mean(window[, min_periods, ...]) 'Moving mean'.
# rolling_std(arg, window[, min_periods, ...]) 	'Moving standard deviation'.
# rolling_max(arg, window[, min_periods, ...]) 	'Moving max of 1d array of dtype=float64 along axis=0 ignoring NaNs'.
# rolling_var(arg, window[, min_periods, ...]) 	'Numerically stable implementation using Welford’s method'.
# rolling_median(arg, window[, min_periods, ...]) 	'O(N log(window)) implementation using skip list'.
# for reference 'http://pandas.pydata.org/pandas-docs/version/0.17.0/api.html#standard-moving-window-functions'
moving_avg = adj_close_px.rolling(window=40).mean()

# Inspect the result
print(moving_avg[-10:])     # displaying only last 10 values

# Short moving window rolling mean
aapl['42'] = adj_close_px.rolling(window=40).mean()

# Long moving window rolling mean
aapl['252'] = adj_close_px.rolling(window=252).mean()

# Plot the adjusted closing price, the short and long windows of rolling means
aapl[['Close', '42', '252']].plot()

plt.savefig('all_data_rollingmeans.png')
plt.show()

#Volatitlity Calculation
# pd.rolling_std(data, window=x) * math.sqrt(window)    # moving historical s.d. of log returns

# Define the minumum of periods to consider
min_periods = 75

# Calculate the volatility
vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)

# Plot the volatility
vol.plot(figsize=(10, 8))

# Show the plot
plt.show()