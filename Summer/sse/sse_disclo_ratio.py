import importlib
import urllib.request
from urllib.request import urlopen
import re
import sys
from bs4 import BeautifulSoup
import json
import pandas as pd
import numpy as np
import os
import datetime
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def loads_jsonp(_jsonp):
    try:
        return json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
    except:
        raise ValueError('Invalid Input')

def scrapy_sse(url):
    Cookie = "yfx_c_g_u_id_10000042=_ck18052209502916552716365002441; yfx_mr_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_mr_f_10000042=%3A%3Amarket_type_free_search%3A%3A%3A%3Abaidu%3A%3A%3A%3A%3A%3A%3A%3Awww.baidu.com%3A%3A%3A%3Apmf_from_free_search; yfx_key_10000042=; yfx_f_l_v_t_10000042=f_t_1526953829644__r_t_1526953829644__v_t_1526955267794__r_c_0; VISITED_MENU=%5B%228765%22%2C%228766%22%2C%228761%22%2C%228705%22%2C%229836%22%5D"

    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        'Cookie': Cookie,
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9,zh-TW;q=0.8,zh;q=0.7,ja;q=0.6',
        'Host': 'query.sse.com.cn',
        'Referer': 'http://www.sse.com.cn/services/hkexsc/disclo/ratios/'
    }

    # Download the data with json version
    req = urllib.request.Request(url,None,headers)
    response = urllib.request.urlopen(req)
    the_page = response.read().decode('utf-8')
    # print(the_page)

    # Initial the variables
    currencyType = []
    buyPrice = []
    updateDate = []
    validDate = []
    sellPrice = []

    # extract the data from jason version
    dic = loads_jsonp(the_page)
    for item in dic['pageHelp']['data']:
        currencyType.append(item['currencyType'])
        buyPrice.append(item['buyPrice'])
        validDate.append(item['validDate'])
        sellPrice.append(item['sellPrice'])

    # Construct the pandas version
    df = np.array([buyPrice,sellPrice,currencyType])
    df2 = pd.DataFrame(df, index = ['BuyPrice','SellPrice','CurrencyType'],columns = validDate)

    return df2.T

now = datetime.datetime.now()
year = datetime.datetime.now().year
month = datetime.datetime.now().month
day = datetime.datetime.now().day 
begin_date = input('Begin-date(ex.20180101):')
end_date = input('End-date(ex.{}{}{}):'.format(year,month,day))


url1 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback79971&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=1&pageHelp.pageSize=25&pageHelp.pageNo=1&_=1526976338264"
url2 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback69374&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=2&pageHelp.pageSize=25&pageHelp.pageNo=2&pageHelp.endPage=21&_=1526976338265"
url3 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback45515&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=3&pageHelp.pageSize=25&pageHelp.pageNo=3&pageHelp.endPage=31&_=1526976338266"
url4 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback45442&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=4&pageHelp.pageSize=25&pageHelp.pageNo=4&pageHelp.endPage=41&_=1526976338267"
url5 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback45442&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=4&pageHelp.pageSize=25&pageHelp.pageNo=5&pageHelp.endPage=41&_=1526976338268"
url6 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback45442&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=4&pageHelp.pageSize=25&pageHelp.pageNo=6&pageHelp.endPage=41&_=1526976338269"
url7 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback45442&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=4&pageHelp.pageSize=25&pageHelp.pageNo=7&pageHelp.endPage=41&_=1526976338269"
url8 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback45442&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=4&pageHelp.pageSize=25&pageHelp.pageNo=8&pageHelp.endPage=41&_=1526976338269"
url9 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback45442&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=4&pageHelp.pageSize=25&pageHelp.pageNo=9&pageHelp.endPage=41&_=1526976338269"
url10 = "http://query.sse.com.cn/commonSoaQuery.do?&jsonCallBack=jsonpCallback45442&isPagination=true&updateDate="+begin_date+"&updateDateEnd="+end_date+"&&sqlId=FW_HGT_JSHDBL&order=validDate%7Cdesc&pageHelp.cacheSize=1&pageHelp.beginPage=4&pageHelp.pageSize=25&pageHelp.pageNo=10&pageHelp.endPage=41&_=1526976338269"


final = pd.concat([scrapy_sse(url1),scrapy_sse(url2),scrapy_sse(url3),scrapy_sse(url4),scrapy_sse(url5),scrapy_sse(url6),scrapy_sse(url7),scrapy_sse(url8),scrapy_sse(url9),scrapy_sse(url10)])
print(final)

if not os.path.exists('./sse'):
    os.makedirs('./sse')

final.to_csv('./sse/exratio.csv')