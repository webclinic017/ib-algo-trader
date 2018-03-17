import pandas_datareader as pdr
import pandas as pd
import datetime
import quandl
import matplotlib.pyplot as plt
import numpy as np


daapl = pdr.get_data_yahoo('AAPL',
                             start=datetime.datetime(2006,10,1),
                             end=datetime.datetime(2018,1,1))