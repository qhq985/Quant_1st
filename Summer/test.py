import matplotlib.pyplot as plt
from WindPy import *
from datetime import *
import pandas as pd
import numpy as np
w.start()

data=w.wsd('600519.SH','open,high,low,close,volume','2018-01-01','2018-06-28')
data1=pd.DataFrame(data.Data,index=['open','high','low','close','volume'],columns=data.Times).T


fig, ax = plt.subplots(figsize=(20,6))
ax = data1['volume'].plot(kind='Bar', color=['r' if x[4] > x[1] else 'g' for x in data1.itertuples()])
ax.set_xticklabels([x.strftime('%Y-%m-%d') for x in data.Times])
plt.show()
