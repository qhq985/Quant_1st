import importlib
from urllib.request import urlopen
import re
import sys
from bs4 import BeautifulSoup
import ssl
import tushare as ts
import pandas as pd
import numpy
import csv

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
    #print(code)
    for item in code:
        if item[0] == '6' or item[0] == '3' or item[0] == '0':
            allCodeList.append(item)
    return allCodeList

def writeToCSV(result, fileName):
    with open(fileName+'.csv','w') as csvfile:
        writer = csv.writer(csvfile,dialect='excel')
        for row in result:
            writer.writerow(row)




def getHistoryData(code,time):
    '''Get the history of code and return the Day, Week, or Month line'''
    if time=='D':
        return ts.get_hist_data(code, start = '2013-01-01')
    elif time=='W':
        return ts.get_hist_data(code, start = '2013-01-01', ktype='W')
    elif time=='M':
        return ts.get_hist_data(code, start = '2013-01-01', ktype='M')

original_codes = urlTolist()
period = ['M','W', 'D']
for p in period:
    for code in original_codes:
        df = getHistoryData(code,p)
        if p == 'M':
            df.to_csv('./month/'+ code + '.csv')
        if p == 'W':
            df.to_csv('./week/'+ code + '.csv')
        if p == 'D':
            df.to_csv('./day/'+ code + '.csv')
        print(code,p," is Done!")
#print(len(original_code))
#print('[CODE:',original_code[0],']\n',getHistoryData(original_code[0],'M'))
#df = getHistoryData(original_code[0],'M')
#df.to_csv(original_code[0] + '.csv')
#print(his_data[0])
#writeToCSV(his_data,original_code[0])
#a = numpy.asarray(his_data)
#numpy.savetxt("out.csv",a,delimiter=",")