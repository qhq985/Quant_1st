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

original_code = urlTolist()
print('[CODE:',original_code[0],']\n',getHistoryData(original_code[0],'W'))