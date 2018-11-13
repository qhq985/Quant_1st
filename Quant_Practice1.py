import numpy as np
import math
import scipy.stats as sp
import time
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from scipy.optimize import brentq

def call_option_pricer(spot,strike,maturity,r,vol):
    d1 = (np.log(spot/strike) + (r + vol**2/2)*maturity)/(vol*np.sqrt(maturity))
    d2 = d1 - vol*np.sqrt(maturity)

    price = spot * sp.norm.cdf(d1) - strike * np.exp(-r*maturity)*sp.norm.cdf(d2)
    return price

def call_option_pricer_monte_carlo(spot,strike, maturity, r, vol, num_of_path = 5000):
    randomSeries = scipy.random.randn(num_of_path)
    s_t = spot * np.exp((r - vol**2/2)*maturity + randomSeries * vol * np.sqrt(maturity))
    sumValue = np.maximum(s_t - strike, 0.0).sum()
    price = np.exp(-r*maturity)*sumValue/num_of_path
    return price

print(call_option_pricer(2.45,2.5,0.25,0.05,0.25))

portfolioSize = range(1,10000,500)
timeSpent =  []

spot = 2.45
strike = 2.50
maturity = 0.25
r = 0.05
vol = 0.25

# for size in portfolioSize:
#     now = time.time()
#     strikes = np.linspace(2.0,3.0,size)
#     for i in range(size):
#         res = call_option_pricer(spot,strikes[i],maturity,r,vol)
#     timeSpent.append(time.time()-now)

print('Option price by Monte Carlo : %.4f' % call_option_pricer_monte_carlo(spot, strike, maturity, r, vol))

pathScenario = range(1000, 50000, 1000)
numberOfTrials = 100

confidenceIntervalUpper = []
confidenceIntervalLower = []
means = []

for scenario in pathScenario:
    res = np.zeros(numberOfTrials)
    for i in range(numberOfTrials):
        res[i] = call_option_pricer_monte_carlo(spot, strike, maturity, r, vol, num_of_path = scenario)
    means.append(res.mean())
    confidenceIntervalUpper.append(res.mean() + 1.96*res.std())
    confidenceIntervalLower.append(res.mean() - 1.96*res.std())

plt.figure(figsize = (12,8))
tabel = np.array([means,confidenceIntervalUpper,confidenceIntervalLower]).T
plt.plot(pathScenario, tabel)
plt.title(u'Monte Carlo Simulation', fontsize = 18)
plt.legend([u'Mean', u'95%-CI upper bound', u'95%-CI lower bound'])
plt.ylabel(u'Price', fontsize = 15)
plt.xlabel(u'Simulation times', fontsize = 15)
plt.grid(True)
plt.show()

class cost_function:
    def __init__(self, target):
        self.targetValue = target

    def __call__(self,x):
        return call_option_pricer(spot,strike,maturity,r,x)-self.targetValue

target = call_option_pricer(spot,strike,maturity,r,vol)
cost_sample = cost_function(target)

# Use Brent Algrithom to calculate 
impliedVol = brentq(cost_sample, 0.01, 0.5)

print('Real vol: %.2f' % (vol*100),'%')
print('Implicit vol: %.2f' %(impliedVol*100),'%')
