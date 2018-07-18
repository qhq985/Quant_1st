import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

plt.style.use("ggplot")  

df = pd.read_excel('oil_future.xlsx')

def timestamp_toString(stamp):
    return time.strftime("%c", time.strptime(stamp))

# Input data and adjust

df1 = pd.DataFrame(df[['Time1','SC']])
df2 = pd.DataFrame(df[['Time2','Brent']])
df3 = pd.DataFrame(df[['Time3','WTI']])
df4 = pd.DataFrame(df[['Time4','EX']])
df1.columns = ['Time','SC']
df2.columns = ['Time','Brent']
df3.columns = ['Time','WTI']
df4.columns = ['Time','EX']
df1 = df1.dropna()
df2 = df2.dropna()
df3 = df3.dropna()
df4 = df4.dropna()
df_all = pd.merge(df1,df2, on = 'Time')
df_all = pd.merge(df_all, df3, on = 'Time')
df_all = pd.merge(df_all, df4, on = 'Time')
df_all.sort_index(inplace=True,ascending=False)
df_all.index = range(1,len(df_all)+1)

df_all.to_csv('final_oil.csv')
# Analysis
print('[Analysis]')
print(df_all.describe())

df_Brent1 = (df_all['Brent'])*df_all['EX']  
df_WTI1 = (df_all['WTI'])*df_all['EX']

df_new = pd.concat([df_all,df_Brent1,df_WTI1],axis=1)
df_new = df_new.drop(['Brent','WTI'],axis=1)
df_new.columns = ['Time','SC','EX','Brent_Adj','WTI_Adj']



df_diff1 = - df_new['Brent_Adj'] + df_new['SC']
df_diff2 = - df_new['WTI_Adj'] + df_new['SC']

df_new = pd.concat([df_new,df_diff1,df_diff2],axis=1)
df_new.columns = ['Time','SC','EX','Brent_Adj','WTI_Adj','DIFF_Brent_SC','DIFF_WTI_SC']

timeline = np.array(pd.read_excel('Time.xlsx'))
timeline = timeline.T
time1 = timeline.tolist()

# for i in range(len(df_new)):
#     timeline.append(timestamp_toString(time_stp[i]))

x =  range(1,795)
# Draw picture
fig = plt.figure(figsize=(18, 8))
ax1 = fig.add_subplot(2,1,1)
ax1.plot(x,df_new['SC'],color='blue', linewidth=1.0, label='SC1809')
ax1.plot(x,df_new['Brent_Adj'],color='red', linewidth=1.0, label='Brent')
ax1.plot(x,df_new['WTI_Adj'],color='green', linewidth=1.0, label='Wti')
plt.title('Price').set_fontsize(fontsize = 15)
xticks = list(range(min(x),max(x),50))+[79]
print(xticks)
xticklabels = ['2018/3/26','2018/3/28','2018/4/3','2018/4/10','2018/4/12','2018/4/17','2018/4/19','2018/4/24','2018/4/26','2018/5/3','2018/5/8','2018/5/10','2018/5/15','2018/5/17','2018/5/22','2018/5/25','2018/5/29']
plt.legend(loc='upper left')
# set ticks and tick labels
ax1.set_xticks(xticks)
ax1.set_xticklabels(xticklabels,rotation=15)

plt.tight_layout(5)
plt.ylabel("Price(RMB)")
plt.xlabel("time")


ax2 = fig.add_subplot(2,1,2)
ax2.plot(df_new['DIFF_Brent_SC'],color='blue', linewidth=1.0, label='DIFF_Brent_SC')
ax2.plot(df_new['DIFF_WTI_SC'],color='red', linewidth=1.0, label='DIFF_WTI_SC')

plt.title('Price_Diff').set_fontsize(fontsize = 15)
plt.tight_layout(5)
plt.legend(loc='upper left')
plt.ylabel("Price_diff(RMB)")
plt.xlabel("time")
ax2.set_xticks(xticks)
ax2.set_xticklabels(xticklabels,rotation=15)


fig1 = plt.figure(figsize=(18, 8))
ax3 = fig1.add_subplot(1,1,1)
plt.plot(df_new['DIFF_Brent_SC'],color='g', linewidth=1.0)
plt.axhline(-18.8, ls='-.',color= 'r',linewidth=2.0)
plt.axhline(-23.8, ls ='-.',color= 'm',linewidth=2.0)
plt.text(-10, -18.5, 'Y= -20',
         fontdict={'size': 13, 'color': 'black'})
plt.text(-10, -23.5, 'Y= -24',
         fontdict={'size': 13, 'color': 'black'})
plt.title('Price_Diff of BRENT and SC').set_fontsize(fontsize = 15)
plt.tight_layout(5)
plt.legend(loc='upper left')
plt.ylabel("Price_diff(RMB)")
plt.xlabel("time")
ax3.set_xticks(xticks)
ax3.set_xticklabels(xticklabels,rotation=15)
plt.show()

print('[Correlation]')
df_corr = pd.DataFrame(df_new[['SC','Brent_Adj','WTI_Adj']])
print(df_corr.corr())

df_diff = df_new[['DIFF_Brent_SC','DIFF_WTI_SC']]
print('[Analysis_adjusted]')
print(df_diff.describe())
df_new.to_csv('final_oil_new.csv')