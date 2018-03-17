import pandas_datareader as pdr
import pandas as pd
import datetime
import quandl
import matplotlib.pyplot as plt

'''
#sum1aapl = pdr.get_data_google('AAPL',
                             start=datetime.datetime(2006,10,1),
                             end=datetime.datetime(2018,1,1))

#sum2aapl = quandl.get('WIKI/AAPL', start_date="2006-10-01", end_date='2018-01-01')

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


