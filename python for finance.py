import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

#start = dt.datetime(2016,1,1,1)
#end = dt.datetime(2017,12,31,1)

#df = web.DataReader('TSLA', 'google', start, end)
#print(df.head(100))

#df.to_csv('tsla.csv')

'''plot below'''

df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)

print(df.head(10))
print(df[['Open','High']].head())

df['Close'].plot()
plt.show()

'''
part 3
'''

'''
style.use('ggplot')
df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
df['100 MA'] = df['Close'].rolling(window=100, min_periods=0).mean()
#df.dropna(inplace=True)

print(df.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.plot(df.index, df['Close'])
ax1.plot(df.index, df['100 MA'])
ax2.bar(df.index, df['Volume'])

plt.show()
'''

'''
part 4
'''

'''
style.use('ggplot')

df = pd.read_csv('tsla.csv', parse_dates=True, index_col=0)
#df['100 MA'] = df['Close'].rolling(window=100, min_periods=0).mean()

df_ohlc = df['Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace=True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)

#print(df_ohlc.head())

ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)

ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

plt.show()
'''

'''
part 5
'''

