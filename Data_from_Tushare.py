import importlib
from urllib.request import urlopen
import re
import sys
from bs4 import BeautifulSoup
import ssl
import tushare as ts

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
        # 6 with 上海A股， 3 with 创业板， 0 with 深圳A股 总共3633只A股
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

original_code = urlTolist()
# download_data(['M','W','D'],original_code)

