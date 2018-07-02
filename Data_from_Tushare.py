import importlib
from urllib.request import urlopen
import re
import sys
from bs4 import BeautifulSoup
import ssl
import tushare as ts
import pandas as pd
import numpy as numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches 
import datetime 



ssl._create_default_https_context = ssl._create_unverified_context


def urlTolist():
    '''Get the code of All Shanghai Stocks'''
    allCodeList = []
    url = "http://quote.eastmoney.com/stocklist.html"
    html = urlopen(url).read().decode('gbk')
    soup = BeautifulSoup(html, features = "lxml")
    s = r'<li><a target="_blank" href="http://quote.eastmoney.com/\S\S(.*?).html">'
    pat = re.compile(s)
    code = pat.findall(html)
    for item in code:
        # 6 with 上海A股， 3 with 创业板， 0 with 深圳A股 总共3639只A股
        if item[0] == '6' or item[0] == '3' or item[0] == '0':
            allCodeList.append(item)
    return allCodeList

def getHistoryData(code,time):
    '''Get the history of code and return the Day, Week, or Month line'''
    if time=='D':
        return ts.get_hist_data(code)
    elif time=='W':
        return ts.get_hist_data(code,ktype='W')
    elif time=='M':
        return ts.get_hist_data(code,ktype='M')


def download_data(period,totalcodes):
    '''Download all history data of code to local'''
    print('The total number of type A stock is',len(original_code),'\n')
    for p in period:
        for code in totalcodes:
            df = getHistoryData(code,p)
            if p == 'M':
                df.to_csv('./month/'+ code + '.csv')
            if p == 'W':
                df.to_csv('./week/'+ code + '.csv')
            if p == 'D':
                df.to_csv('./day/'+ code + '.csv')
            print(code,p," is Done!")

def input_indicator():
    '''Input the indicator from Wind'''
    df = pd.read_excel('./Indicator.xlsx')

    return df


def candle_plot(quotes, sec):   # quotes:Matket_data-Dateframe type    sec：title   
    '''Draw a candle picture of a code, two pic, one is price, one is volumn'''
    _color_balck__= '#0F0F0F'
    __color_green__= '#00FFFF'
    __color_yellow__ = '#EE9A00'
    __color_purple__ = '#9900CC'
    __linewidth__ = 2

    # Create Canvas
    fig = plt.figure(figsize=(16,8))
    fig.set_tight_layout(True)

    ax1 = fig.add_subplot(2,1,1)  # K Line
    ax1.set_title(sec,fontsize = 15)
    ax2 = fig.add_subplot(2,1,2)   # Volumn
    ax1.set_axisbelow(True)
    ax2.set_axisbelow(True)

    ax1.grid(True, axis = 'y')
    ax2.grid(True, axis = 'y')
    ax1.set_xlim(-1,len(quotes)+1)
    ax2.set_xlim(-1,len(quotes)+1)

    for i in range(len(quotes)):
        close_price = quotes.ix[i, 'close_x']
        open_price = quotes.ix[i, 'open_x']
        high_price = quotes.ix[i, 'high_x']
        low_price = quotes.ix[i, 'low_x']
        vol = quotes.ix[i, 'volume']
        trade_date = quotes.index[i]

        if close_price > open_price:  # Draw Positive Line
            ax1.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, fill=False, color='r'))
            ax1.plot([i+0.075, i+0.075], [low_price, open_price], 'r')
            ax1.plot([i+0.075, i+0.075], [close_price, high_price], 'r')
            ax2.add_patch(patches.Rectangle((i-0.2, 0), 0.4, vol, fill=False, color='r'))
        else: # Draw Negative Line
            ax1.add_patch(patches.Rectangle((i-0.2, open_price), 0.4, close_price-open_price, color='g'))
            ax1.plot([i, i], [low_price, high_price], color='g')
            ax2.add_patch(patches.Rectangle((i-0.2, 0), 0.4, vol, color='g'))

    # Set title
    ax1.set_title("Price(RMB)", fontsize=15, loc='left', color='r')
    ax2.set_title("Volume(*100)",  fontsize=15,  color='r')

    #Set Ticks
    ax1.set_xticks(range(0,len(quotes), 15))  # The position
    ax2.set_xticks(range(0,len(quotes), 15)) 
    ax1.set_xticklabels([(quotes.index[i]).strftime('%Y-%m-%d') for i in ax1.get_xticks()])  # The content of ticks
    ax2.set_xticklabels([(quotes.index[i]).strftime('%Y-%m-%d') for i in ax2.get_xticks()])
    # Moving AVG Line

    ax1.plot(list(quotes['ma5']), color='b', linewidth=__linewidth__ , label='MA5-')
    ax1.plot(list(quotes['ma10']), color=__color_yellow__, linewidth=__linewidth__ , label='MA10-')
    ax1.plot(list(quotes['ma20']), color=__color_purple__, linewidth=__linewidth__ , label='MA20-')
    # Legend / Notation

    ax1.legend(loc='lower right')
    # Volumn AVG Line
    ax2.plot(list(quotes['v_ma5']) ,color='b', linewidth=__linewidth__ , label='VOLUME5-')
    ax2.plot(list(quotes['v_ma10']), color=__color_yellow__, linewidth=__linewidth__ ,label='VOLUME10-')
    # Legend / Notation

    ax2.legend(loc='upper right')
    return fig



# original_code = urlTolist()
# download_data(['M','W','D'],original_code)

# print(input_indicator())

data = ts.get_h_data("600519",start='2018-01-01') # 前复权
data = data.drop(['volume'],axis=1)
sqjt = ts.get_hist_data('600519',start = '2008-01-01')
data = pd.merge(data,sqjt, how ='left',left_index=True, right_index=True)
data.sort_index(inplace=True)
candle_plot(data, "Market Data-600518")

plt.show()
