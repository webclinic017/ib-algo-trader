import scipy
import numpy as np
import math

def pdf(x):
    # upper bound minus lower bound of pdf
    u = .5*math.erf(x/math.sqrt(2))
    l = .5*math.erf((-1*math.inf)/math.sqrt(2))
    r = u-l
    return r

'''
risk = TBA (risk free rate, should be implied and similar to the us treasury rate)
stprice = stock price at t=0
strike = strike price at t=T where t<T
time = yearly (months/12 or days/365 or trading_days/252)
vol = TBA (will create vol function in the future)

time    1 week = .020833
        2 week = .041667
        3 week = .062500
        1 month = .08333
'''

def call_option(stprice,strike,time,vol,risk):
    mprice = (strike) * math.exp((-1) * (risk * time))

    d1 = ((np.log(stprice / strike)) + (risk + (vol ** 2) / 2) * time) / (vol * math.sqrt(time))
    d2 = d1 - (vol * math.sqrt(time))

    y = (stprice) * (pdf(d1)) - (mprice * (pdf(d2)))
    print(y)

call_option(275.3,275,.29589,.1231,.0291)
call_option(275.3,290,.29589,(.1231+(275-290)*.001+(275-290)*.0004),.0291)
call_option(275.3,290,.29589,.1041,.0291)

call_option(275.3,260,.29589,.146,.0291)
call_option(275.3,260,.29589,(.1231+(275-260)*.001+(275-260)*.0004),.0291)
call_option(275.3,271,.29589,(.1231+(275-271)*.001),.0291)

call_option(275.3,100,.29589,.1231,.0291)