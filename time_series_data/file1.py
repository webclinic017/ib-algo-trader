import pandas_datareader as pdr
import pandas as pd
import datetime
import quandl
quandl.ApiConfig.api_key = '-VQTkx89BPNGVyjKvD1p'
import matplotlib.pyplot as plt
import numpy as np

'''
#sum1aapl = pdr.get_data_google('AAPL',
                             start=datetime.datetime(2006,10,1),
                             end=datetime.datetime(2018,1,1))


#sum2aapl = quandl.get('WIKI/AAPL', start_date="2006-10-01", end_date='2018-01-01')     #WIKI = US STOCKS

#print(sum1aapl)

#sum1aapl.to_csv('aapl_ohlc.csv')    #get data and saves into csv
'''

sum1aapl = pd.read_csv('aapl_ohlc.csv', header=0, index_col='Date', parse_dates=True)

print(sum1aapl.index)   # inspect index
print(sum1aapl.columns) # inspect columns
close10 = sum1aapl['Close'][-10:]

print(sum1aapl.loc[pd.Timestamp('2006-11-01'):pd.Timestamp('2006-12-31')].head())      # .head inspects first 5 rows
print(sum1aapl.loc['2007'].head())      # first 5 of 2007
print(sum1aapl.iloc[22:43])             # from index 22 to 43
print(sum1aapl.iloc[[22,43], [0, 3]])   # only index 22, 43 and columns 0,3

sample = sum1aapl.sample(20)            # randomly selects 20 values
print(sample)

monthly_aapl = sum1aapl.resample('M').mean()    # to monthly level
print(monthly_aapl)

sum1aapl['diff'] = sum1aapl.Open - sum1aapl.Close
#del sum1aapl['diff']


print(sum1aapl['diff'])

plt.plot(sum1aapl.index, sum1aapl['diff'])
plt.show()

#sum1aapl.to_csv('aapl_ohlc_modded.csv')        # with 'diff' column included

sum1aapl['Close'].plot(grid=True)
plt.show()

daily_close = sum1aapl['Close']                 # Closing price
daily_pct_change = daily_close.pct_change()     # change closing to percent mode
daily_pct_change.fillna(0,inplace=True)
print("--------raw daily %--------")
print(daily_pct_change)

daily_log_returns = np.log(daily_close.pct_change()+1)
print("--------ln returns--------")
print(daily_log_returns)

ax1=daily_pct_change
ax2=daily_log_returns

#oscillation of returns, red = raw, green = log

plt.plot(ax1, 'r')
plt.plot(ax2, 'g')
plt.show()

bm_aapl = sum1aapl.resample('BM').apply(lambda x: x[-1])    # resample aapl to business months, take last observation as value
bm_aapl.pct_change()

q_aapl = sum1aapl.resample('4M').mean()     # Resample `aapl` to quarters, take the mean as value per quarter
q_aapl.pct_change()

'''
pct_change() obscures the daily % calculation. Use pd.shift() instead, then divide daily_close 
by daily_close.shift(1) -1. 

The first index will be N/A due to this 
'''

daily_pct_change = daily_close / daily_close.shift(1) - 1       # real adjusted daily % change
print(daily_pct_change)

#plotting the distribution of daily % change
daily_pct_change.hist(bins=50)          # histogram frequncy dist.
plt.show()
print(daily_pct_change.describe())      # pulls summary of statistics


cum_daily_return = (1 + daily_pct_change).cumprod()     # cumulative daily returns
print(cum_daily_return)

#plotting cum returns
cum_daily_return.plot(figsize=(12,8))
plt.show()

#change from cum daily returns to cum monthly returns
cum_monthly_return = cum_daily_return.resample("M").mean()
print(cum_monthly_return)