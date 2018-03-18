import pandas_datareader as pdr
import pandas as pd
import datetime
import quandl
import matplotlib.pyplot as plt
import numpy as np
import pandas.plotting as pdp
import statsmodels.api as sm
from pandas.core import datetools

# if use quandl (AdjClose)

def get(tickers, startdate, enddate):
  def data(ticker):
    return (pdr.get_data_quandl(ticker, start=startdate, end=enddate))
  datas = map(data, tickers)
  return(pd.concat(datas, keys=tickers, names=['Ticker', 'Date']))

tickers = ['AAPL', 'MSFT', 'IBM', 'GOOG']

all_data = get(tickers, datetime.datetime(2006, 10, 1), datetime.datetime(2018, 1, 1))
all_data.to_csv('all_data_quandl_original.csv')
#all_data = pd.read_csv('all_data.csv') # Cannot parse the same data from web data

daily_close_px = all_data[['AdjClose']].reset_index().pivot('Date', 'Ticker', 'AdjClose')
daily_close_px.to_csv('all_data_quandl_1_dailyclose.csv')

daily_pct_change = daily_close_px.pct_change()
daily_pct_change.to_csv('all_data_quandl_2_dailypctchange.csv')

daily_pct_change.hist(bins=50, sharex=True, figsize=(12,8))

plt.savefig('all_data_quandl_3_hist.png')   # need to have the data before plt.show() or data will be cleared
plt.show()

#pd.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1,figsize=(12,12))   # this function is broken, use pd.plotting as pdp
pdp.scatter_matrix(daily_pct_change, diagonal='kde', alpha=0.1,figsize=(12,12))

plt.savefig('all_data_quandl_4_scattermatrix.png')
plt.show()


'''
Moving Windows, when u compute the stats on window of data by a particular period of time, then slide the window 
across the data by a specific interval. Continually calculated as long as the window falls first within the dates
of the time series.
'''
#data = quandl.get('AAPL', authtoken='-VQTkx89BPNGVyjKvD1p')
# from earlier reference (file1)
aapl = pdr.get_data_quandl('AAPL',
                           start=datetime.datetime(2006, 10, 1),
                           end=datetime.datetime(2018, 1, 1))



#must use own data, can request 20 pulls per 10 min from quandl (uses AdjClose)
#csv (uses Close)
#aapl = pd.read_csv('aapl_ohlc.csv')

adj_close_px_aapl = aapl['AdjClose']

# Calculate the moving average:
# rolling_mean(window[, min_periods, ...]) 'Moving mean'.
# rolling_std(arg, window[, min_periods, ...]) 	'Moving standard deviation'.
# rolling_max(arg, window[, min_periods, ...]) 	'Moving max of 1d array of dtype=float64 along axis=0 ignoring NaNs'.
# rolling_var(arg, window[, min_periods, ...]) 	'Numerically stable implementation using Welford’s method'.
# rolling_median(arg, window[, min_periods, ...]) 	'O(N log(window)) implementation using skip list'.
# for reference 'http://pandas.pydata.org/pandas-docs/version/0.17.0/api.html#standard-moving-window-functions'
moving_avg_aapl = adj_close_px_aapl.rolling(window=40).mean()
moving_avg_aapl.to_csv('aapl_movingavg_rolling40.csv')

# Inspect the result
print(moving_avg_aapl[-10:])     # displaying only last 10 values

# Short moving window rolling mean
aapl['42'] = adj_close_px_aapl.rolling(window=40).mean()

# Long moving window rolling mean
aapl['252'] = adj_close_px_aapl.rolling(window=252).mean()

# Plot the adjusted closing price, the short and long windows of rolling means
aapl[['AdjClose', '42', '252']].plot()

plt.savefig('aapl_rollingmeans.png')
plt.show()

#Volatitlity Calculation
# pd.rolling_std(data, window=x) * math.sqrt(window)    # moving historical s.d. of log returns

# Define the minumum of periods to consider
min_periods = 75

# Calculate the volatility, for all_data
vol = daily_pct_change.rolling(min_periods).std() * np.sqrt(min_periods)
vol.to_csv('all_data_quandl_5_vol.csv')

# Plot the volatility
vol.plot(figsize=(10, 8))

plt.savefig('all_data_quandl_6_vol.png')
plt.show()

# Ordinary Least-Squares Regression (OLS)

# Isolate the adjusted closing price
all_adj_close = all_data[['AdjClose']]

# Calculate the returns
all_returns = np.log(all_adj_close / all_adj_close.shift(1))
all_returns.to_csv('all_data_quandl_7_returnspct.csv')

# Isolate the AAPL returns
aapl_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'AAPL']
aapl_returns.index = aapl_returns.index.droplevel('Ticker')

# Isolate the MSFT returns
msft_returns = all_returns.iloc[all_returns.index.get_level_values('Ticker') == 'MSFT']
msft_returns.index = msft_returns.index.droplevel('Ticker')

# Build up a new DataFrame with AAPL and MSFT returns
return_data = pd.concat([aapl_returns, msft_returns], axis=1)[1:]
return_data.columns = ['AAPL', 'MSFT']
return_data.to_csv('AAPLvsMSFT_datapct.csv')

# Add a constant
X = sm.add_constant(return_data['AAPL'])

# Construct the model
model = sm.OLS(return_data['MSFT'],X).fit()

# Print the summary
print(model.summary())

# Plot returns of AAPL and MSFT
plt.plot(return_data['AAPL'], return_data['MSFT'], 'r.')

# Add an axis to the plot
ax = plt.axis()

# Initialize `x`
x = np.linspace(ax[0], ax[1] + 0.01)

# Plot the regression line
plt.plot(x, model.params[0] + model.params[1] * x, 'b', lw=2)

# Customize the plot
plt.grid(True)
plt.axis('tight')
plt.xlabel('Apple Returns')
plt.ylabel('Microsoft returns')

plt.savefig('AAPLvsMSFT_scatterpct.png')
plt.show()

# Plot the rolling correlation
return_data['MSFT'].rolling(window=252).corr(return_data['AAPL']).plot()

plt.savefig('AAPLvsMSFT_corr.png')
plt.show()