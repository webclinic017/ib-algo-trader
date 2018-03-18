import pandas_datareader as pdr
import pandas as pd
import datetime
import quandl
import matplotlib.pyplot as plt
import numpy as np
import pandas.plotting as pdp
import statsmodels.api as sm
from pandas.core import datetools
import pandas.tseries

all_data = pd.read_csv('all_data.csv')
# Add a column `diff` to `aapl`
#aapl['diff'] = aapl.Open - aapl.Close

# Delete the new `diff` column
#del aapl['diff']

# Plot the closing prices for `aapl`
#aapl['Close'].plot(grid=True)

# Show the plot
#plt.show()
all_data['all_returns'] = np.log(all_data['AdjClose'] / all_data['AdjClose'].shift(1))

#all_data.to_csv('tempfile1.csv')

aapl_returns = all_data[all_data.Ticker == 'AAPL']
aaplm = aapl_returns.loc[:,['Date', 'all_returns']]
aaplm.rename(columns={'all_returns': 'AAPL_return'}, inplace=True)

msft_returns = all_data[all_data.Ticker == 'MSFT']
msftm = msft_returns.loc[:,['Date', 'all_returns']]
msftm.rename(columns={'all_returns': 'MSFT_return'}, inplace=True)


#aaplm.to_csv('temp1.csv')
#msftm.to_csv('temp2.csv')
return_data = pd.merge(aaplm,msftm, how='outer', on='Date')[1:]
#return_data.to_csv('AAPLvsMSFT_data.csv')

# Add a constant
x = sm.add_constant(return_data['AAPL_return'])

# Construct the model
model = sm.OLS(return_data['MSFT_return'],x).fit()

# Plot returns of AAPL and MSFT
plt.plot(return_data['AAPL_return'], return_data['MSFT_return'], 'r.')

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

# Show the plot
plt.show()