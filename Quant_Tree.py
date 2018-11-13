import pandas as pd
import tushare as ts
import datetime
import matplotlib
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ochl
import matplotlib.ticker as ticker

begin_time = '2017-07-01'
end_time = '2017-10-01'
code = "000001"
df = ts.get_hist_data(code, start=begin_time, end=end_time)
df = df.sort_index(0)
df_idx = df.index.values

#    df.plot()

fig, ax = plt.subplots(figsize=(20, 10)) # 设置图片大小。

# https://matplotlib.org/api/finance_api.html#module-matplotlib.finance
# matplotlib.finance.candlestick2_ochl(ax, opens, closes, highs, lows, width=4, colorup='r', colordown='g', alpha=0.75)
candlestick2_ochl(ax = ax, 
                 opens=df["open"].values, closes=df["close"].values,
                 highs=df["high"].values, lows=df["low"].values, 
                 width=0.75, colorup='r', colordown='g', alpha=0.75)

ax.xaxis.set_major_locator(ticker.MaxNLocator(20))
# 设置自动格式化时间。
def mydate_formatter(x,pos):
    try:
        return df_idx[int(x)]
    except IndexError:
        return ''
ax.xaxis.set_major_formatter(ticker.FuncFormatter(mydate_formatter))

plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
ax.grid(True)
plt.title(code)
plt.show()