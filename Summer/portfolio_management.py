# # 组合管理APP
# 系统说明：
# 1.持仓包含了股票、基金、期货三种形式。
# 2.期货采用收盘价估值
# 3.期货合约，如果当时指定合约不存在，则采用当时的主力合约，直到指定合约可交易；如果没有指定合约，则默认为主力合约及其切换
# 4.股票可能改变代码或拆股，如枫叶教育1317.HK (持有期间如果有分红则默认为分红再投资。因为wind的价格是复权的)
# 5.股票最多30个，期货10个，股指3个

# ############################################################################################################################################
# ############################################################################################################################################

from WindPy import *
from datetime import *
import pandas as pd
import numpy as np
import talib as ta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

w.start()

# 一、参数说明
# 基础参数：
# 起始日期，截止日期 （etc. 2017-12-29）'yyyy-mm-dd'
# 资金（默认：30000000）
# 股票起始总仓位 （默认：70%）
# 股指对冲比例 （默认：50%）
# 股票权重方式： 等权（默认） 设定仓位 设定股数
# 股票参数：
# 股票代码 （etc. 000001.sz）
# 注：可无限加更多的股票代码，代码形式为List
# 例：['000001.sz', '000002.sz', '000004.sz', '000005.sz']
# 股指参数：
# 股指代码 （etc. IF1809.CFE）
# 注：对冲默认为 IF1809.CFE(沪深300期货1809合约).
# 如果有2个期货股指，如IF+IC，则设定自定义股指比例为 4:1；如IF+IH，则 1:1；如IH+IC，也按照 4:1.
# 按照这个比例来分配50%的对冲仓位，代码形式为List  
# 例：['IF1809.CFE', 'IC,CFE']
# 对冲日期 （etc. 2017-12-29）'yyyy-mm-dd'
# 注：默认为一开始就对冲
# 期货参数：
# 期货代码 （etc. RB1810.SHF）
# 注：可默认加无限多期货，期货不用投入本金，只用保证金，按照设定手数或仓位来计算，代码形式为List
# 例：['RB1810.SHF', 'NI1809.SHF', 'SR809.CZC', 'M1809.DCE']
# 投资日期 （etc. 2017-12-29）'yyyy-mm-dd'

# ##########################################################################################################################################

# 二、股票参数更改
today = date.today()
today = datetime.strftime(today, '%Y-%m-%d')
# 资金，默认3000w
capital = 30000000
# 起始日期，截止日期(默认今天)  'yyyy-mm-dd'
start_date, end_date = '2017-12-29', today
# 股票代码
stock_list = ['600519.sh']
# 股票起始总仓位 （默认：70%）
start_position = 0.7
# 股票权重方式： 1.等权（默认） 2.设定仓位百分比  3.设定股数  下面填 1 or 2 or 3
stock_weight_method = 1 



# 若等权则下面都不用填（股份保留到整数）
stock_weight = []
stock_shares = []
stock_percent = []
stock_start_price = w.wsd(stock_list,'close',start_date,start_date,"Currency=CNY;PriceAdj=F").Data[0]
stock_end_price = w.wsd(stock_list,'close',end_date,end_date,"Currency=CNY;PriceAdj=F").Data[0]
stock_name = w.wsd(stock_list,'sec_name',end_date,end_date).Data[0]
if stock_weight_method == 1:
    for i in range(len(stock_list)):
        stock_percent.append(1/len(stock_list))
        stock_shares.append(int(capital*start_position/len(stock_list)/stock_start_price[i]/10)*10) 
        stock_weight.append(stock_shares[i]*stock_start_price[i])
elif stock_weight_method == 2:
    
    # 若选设定仓位，则填下面list的内容，注意总资金不能大于设定 
    stock_percent = [0.1,0.1,0.1,0.1,0.1,0.1,0.1,0.1]
    
    for i in range(len(stock_list)):
        stock_weight.append(stock_percent[i]*capital*start_position)
        stock_shares.append(int(stock_weight[i]/stock_start_price[i]/10)*10)
elif stock_weigt_method == 3:
    
    # 若选设定股数 ，则填下面list的内容，注意总资金不能大于设定 
    stock_shares = [1,1,1,1,1,1,1,1]
    
    for i in range(len(stock_list)):
        stock_weight.append(stock_shares[i]*stock_start_price[i])
        stock_percent.append(stock_weight[i]/(capital*start_position))

assert sum(stock_weight) <= capital*start_position, '总仓位数大于最大投入资金'        
assert sum(stock_percent) <= 1, '总仓位比例大于1'        

stock_data_initial = pd.DataFrame(np.array([stock_list,stock_name,stock_start_price,stock_end_price,stock_shares,stock_weight,stock_percent]),
                                  index = ['股票代码','股票名称','起始价','现价','股份','市值','仓位占比']).T

print('\n股票总览')
print('起始：{}  今日：{}  总资金：{}  总投资占比: {}\n'.format(start_date,end_date,capital, start_position))

    
stock_data_initial.index=range(1,len(stock_data_initial)+1)
print(stock_data_initial)

# ##################################################################################################################

# 三、股指参数更改
# 2个期货股指，如IF+IC，则设定自定义股指比例为 4:1；如IF+IH，则 1:1；如IH+IC，也按照 4:1.
# 1. IF  2. IF+IC(4:1)  3. IF+IH(1:1)  4.IH+IC(4:1)
index_method = 1
# 对冲起始日期，默认和股票一样 'yyyy-mm-dd'
start_hedge_date = '2017-12-29'
# 股指对冲比例 （默认：50%）
hedge_ratio = 0.5


# 以下不用填
if index_method == 1:
    index_1806 = w.wsd('IF1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Data[0]
    index_time = w.wsd('IF1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Times
    index_1809 = w.wsd('IF1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Data[0]
    index_time += w.wsd('IF1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Times
    index_time = [datetime.strftime(i,'%Y-%m-%d') for i in index_time ]
    index_df = pd.DataFrame(np.array([index_time,index_1806+index_1809]),index = ['日期','自定义股指价格 IF']).T
elif index_method ==2:
    index_1806 = w.wsd('IF1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Data[0]
    index_time = w.wsd('IF1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Times
    index_1809 = w.wsd('IF1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Data[0]
    index_time += w.wsd('IF1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Times
    index_time = [datetime.strftime(i,'%Y-%m-%d') for i in index_time ]
    index1 = index_1806+index_1809
    index2_1806 = w.wsd('IC1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Data[0]
    index2_1809 = w.wsd('IC1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Data[0]
    index2 = index2_1806+index2_1809
    index_self = []
    for i in range(len(index_time)):
        index_self.append(index1[i]*0.8+index2[i]*0.2)
        
    index_df = pd.DataFrame(np.array([index_time,index_self]),index = ['日期','自定义股指价格 IF+IC(4:1)']).T
elif index_method ==3:
    index_1806 = w.wsd('IF1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Data[0]
    index_time = w.wsd('IF1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Times
    index_1809 = w.wsd('IF1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Data[0]
    index_time += w.wsd('IF1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Times
    index_time = [datetime.strftime(i,'%Y-%m-%d') for i in index_time ]
    index1 = index_1806+index_1809
    index2_1806 = w.wsd('IH1806.CFE','close',start_date,'2018-01-19',"TradingCalendar=SSE").Data[0]
    index2_1809 = w.wsd('IH1809.CFE','close','2018-01-20',end_date,"TradingCalendar=SSE").Data[0]
    index2 = index2_1806+index2_1809
    index_self = []
    for i in range(len(index_time)):
        index_self.append(index1[i]*0.5+index2[i]*0.5)
        
    index_df = pd.DataFrame(np.array([index_time,index_self]),index = ['日期','自定义股指价格 IF+IH(1:1)']).T
elif index_method ==4:
    index_1806 = w.wsd('IH1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Data[0]
    index_time = w.wsd('IH1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Times
    index_1809 = w.wsd('IH1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Data[0]
    index_time += w.wsd('IH1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Times
    index_time = [datetime.strftime(i,'%Y-%m-%d') for i in index_time ]
    index1 = index_1806+index_1809
    index2_1806 = w.wsd('IC1806.CFE','close',start_date,'2018-01-19',"Currency=CNY;PriceAdj=F").Data[0]
    index2_1809 = w.wsd('IC1809.CFE','close','2018-01-20',end_date,"Currency=CNY;PriceAdj=F").Data[0]
    index2 = index2_1806+index2_1809
    index_self = []
    for i in range(len(index_time)):
        index_self.append(index1[i]*0.8+index2[i]*0.2)
        
    index_df= pd.DataFrame(np.array([index_time,index_self]),index = ['日期','自定义股指价格 IH+IC(4:1)']).T
print('\n自定义股指总览')   
index_df.iloc[:,1] = index_df.iloc[:,1].astype(float) 
hedge_price = index_df[index_df['日期'] == start_hedge_date].iloc[0,1]
hedge_position = hedge_ratio*start_position*capital
hedge_shares = int(hedge_position/hedge_price)

index_df['股指期货市值'] = index_df.iloc[:,1]*hedge_shares
index_df['股指期货市值'] = index_df['股指期货市值'].where(index_df['日期'] >= start_hedge_date, 0)
hedge_start_position = index_df[index_df['日期'] == start_hedge_date].iloc[0,2]
print('\n对冲日期：{}  股指份数：{}  初始股指仓位：{}'.format(start_hedge_date,hedge_shares,hedge_start_position))


print(index_df)

# ##########################################################################################################################

# 四、期货参数更改


# 4.1 获取期货日行情（主力以持仓量计算）
# 输入日期，提供当日期货商品名称和代码以供投资参考
# 默认为投资起始日 etc 2017-12-29

# 输入需要查看期货行情的日期，默认为 2017-12-29
future_date = '2017-12-29'
error_code,future_data_df = w.wset("sectorconstituent", "date="+future_date+";sectorId=1000010084000000",usedf=True)
future_data_df = future_data_df.drop(['2','6'],axis=0)
pd.set_option('max_rows', 50)
print(future_data_df)

# ###################################################################
# 4.2 设置期货的list，确定主力合约
# 期货代码 （etc. RB1810.SHF）为List形势，可设定仓位，也可设定手数

# 期货代码 exc. 螺纹 RB.SHF 镍 NI1.SHF 白糖 SR.CZC 豆粕 M.DCE
future_list = ['RB.SHF','NI.SHF','SR.CZC','M.DCE']


# 以下都不用填写
# 获取主力合约列表 
error_code,future_code = w.wsd(future_list, "trade_hiscode", future_date, end_date,usedf=True)
future_code = future_code.drop_duplicates()
future_code.index = future_code.index.strftime('%Y-%m-%d')
# Extract the moth contact code of the first day
future_code_month = list(future_code.iloc[0,:]) 
print(future_code)

# ###################################################################
# 4.3 生成各商品期货数据（由不同主力合约拼接而成）
def future_history(code,date1,date2):
    '''Return the price histroy of a future from Wind'''
    future_hist = w.wsd(code, "close", date1, date2).Data[0]
    return future_hist

print('各期货主力仓位起始和截止日期：')
future_a = []
for i in range(len(future_list)):
    future_b = []
    print(future_list[i])
    future_index_date = future_code.iloc[:,i].drop_duplicates()
    for j in range(len(future_index_date)):
        date_1 = future_index_date.index[j]
        if j+1 >= len(future_index_date):
            date_2 = end_date
        else:   
            date_2 = (datetime.strptime(future_index_date.index[j+1],'%Y-%m-%d') + timedelta(days = -1)).strftime('%Y-%m-%d')
        print(date_1,date_2)
        future_b += future_history(future_index_date[j],date_1,date_2)
    future_a.append(future_b)
print('\n期货价格总览')
future_times = w.tdays(future_date, end_date,  "TradingCalendar=SHFE").Data[0]
future_times = [datetime.strftime(i,'%Y-%m-%d') for i in future_times ]
future_price = pd.DataFrame(future_a, index= future_list,columns =future_times).T
pd.set_option('max_rows', 20)
print(future_price)

# ###################################################################
# 4.4 设置投资方式和投资日期
# 仓位投资占总资金比例，默认0.7
start_position_future = 0.7
# 设定期货投资日期, 默认和股票一样 'yyyy-mm-dd'
start_future_date = '2017-12-29'
# 选择投资方式 1: 等权 2.设定各仓位比例 3.设定手数 （默认为 1.等权)
future_method = 1

# # 投资方式1: 设定总仓位 （默认：70%）默认资金为3000w——等权, 不用填写
future_start_price = list(future_price[future_price.index == start_future_date].iloc[0,:])
future_percent = []
future_shares = []
future_weight = []
future_name = w.wsd(future_list,'sec_name',end_date,end_date).Data[0]  
future_contractmultiplier = w.wsd(future_code_month,'contractmultiplier',end_date,end_date).Data[0] 


if future_method == 1:
    for i in range(len(future_list)):
        future_percent.append(1/len(future_list))
        future_shares.append(int(capital*start_position_future/len(future_list)/future_start_price[i]/future_contractmultiplier[i]))
        future_weight.append(future_shares[i]*future_contractmultiplier[i]*future_start_price[i])                             
elif future_method == 2:
    # 若选设定仓位，则填下面list的内容，注意总资金不能大于设定
    future_percent = [0.25,0.25,0.25,0.25]
    for i in range(len(future_list)):
        future_weight.append(future_percent[i]*capital*start_position_future)
        future_shares.append(int(future_weight[i]/future_start_price[i]/future_contractmultiplier[i]))
elif future_method ==3:
    # 若选设定手数 ，则填下面list的内容，注意总资金不能大于设定 
    future_shares = [1,1,1,1]
    for i in range(len(future_list)):
        future_weight.append(future_shares[i]*future_start_price[i]*future_contractmultiplier[i])
        future_percent.append(future_weight[i]/(capital*start_position_future))
                             
assert sum(future_weight) <= capital*start_position_future, '总仓位数大于最大投入资金'                                
assert sum(future_percent) <= 1, '总仓位比例大于1' 

 
future_data_initial = pd.DataFrame(np.array([future_list,future_name,future_start_price,future_shares,future_contractmultiplier,future_weight,future_percent]),
                                  index = ['商品期货代码','商品名称','起始价','手数','合约乘数','市值','仓位占比']).T                           

future_start_position_total = sum(future_weight)
print('\n商品期货总览')
print('起始：{}  今日：{}  总资金：{}  总投资占比: {}  初始期货总仓位: {}\n'.format(start_future_date,end_date,capital, start_position_future,future_start_position_total))
print(future_data_initial)


# ###################################################################
# 4.5 商品期货市值总览

future_position_df = future_price.iloc[:,:]*future_shares
future_position_df['商品期货市值'] = future_position_df.apply(lambda x: x.sum(), axis=1)
future_position_df.reset_index(level=0, inplace=True)
future_position_df.rename(columns = {'index':'日期'}, inplace = True)
future_df = future_position_df[['日期','商品期货市值']]
future_position_df.iloc[:,1:] = future_position_df.where(future_position_df['日期'] >= start_future_date, 0)
print('\n商品期货市值总览')

print(future_position_df)


# #################################################################################################################################################
# 五、价格总览
stock_data = w.wsd(stock_list,'close',start_date,end_date,"Currency=CNY;PriceAdj=F")
stock_df = pd.DataFrame(stock_data.Data,index = stock_name).T

portfolio_df = pd.concat([index_df.iloc[:,:-1],stock_df],join="outer",axis=1)
print('\n价格总览')

portfolio_df


# #################################################################################################################################################
# 六、市值总览

position_df = portfolio_df.iloc[:,2:]*stock_shares
print('\n市值总览')
position_df['股票总市值'] = position_df.apply(lambda x: x.sum(), axis=1)
position_df = pd.concat([index_df.iloc[:,0],position_df.iloc[:,-1],index_df.iloc[:,2],future_position_df.iloc[:,-1]],join="outer",axis=1)
position_df['股票总收益'] = position_df['股票总市值']-position_df[position_df['日期'] ==start_date].iloc[0,1]
position_df['股指对冲收益'] = hedge_start_position-position_df['股指期货市值']
position_df['股指对冲收益'] = position_df['股指对冲收益'].where(index_df['日期'] >= start_hedge_date, 0)
position_df['商品期货收益'] = position_df['商品期货市值']-future_start_position_total
position_df['商品期货收益'] = position_df['商品期货收益'].where(index_df['日期'] >= start_future_date, 0)
position_df['组合总收益'] = position_df['股指对冲收益']+position_df['股票总收益']+position_df['商品期货收益']
position_df['股票走势'] = position_df['股票总市值']/position_df[position_df['日期'] ==start_date].iloc[0,1]-1
position_df['股指走势'] = index_df.iloc[:,1]/index_df[index_df['日期'] ==start_date].iloc[0,1]-1
position_df['期货走势'] = position_df['商品期货收益']/capital
position_df['组合投资回报率'] = position_df['组合总收益']/capital


pd.set_option('max_columns', 20)
position_df

# #################################################################################################################################################
# 七、图像

# 7.1 总收益走势
from WindCharts import *
line_position_df = position_df.drop(['股指期货市值','股票总市值','商品期货市值','股票走势','股指走势','期货走势','组合投资回报率'],axis=1)
line_return_df = position_df.drop(['股指期货市值','股票总市值','商品期货市值','股指对冲收益','股票总收益','商品期货收益','组合总收益'],axis=1)
line_position_df.set_index(["日期"], inplace=True)
line_return_df.set_index(["日期"], inplace=True)
chart = WLine(title='总收益走势',subtitle='起始日期:'+start_date+'    对冲日期:'+start_hedge_date+'    期货日期:'+start_future_date,data=line_position_df, category=list(line_position_df.columns))
chart.plot()

# ###############################################################

# 7.2 回报率走势
chart = WLine(title='回报率走势',subtitle='起始日期:'+start_date+'    对冲日期:'+start_hedge_date+'    期货日期:'+start_future_date ,data=line_return_df, category=list(line_return_df.columns))
chart.plot()
