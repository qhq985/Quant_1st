import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

plt.style.use("ggplot")  

df = pd.read_excel('DATE_OIL.xlsx')

df1 = pd.DataFrame(df[['DATE1','BRENT']])
df2 = pd.DataFrame(df[['DATE2','WTI']])
df1.columns = ['DATE','BRENT']
df2.columns = ['DATE','WTI']
df1 = df1.dropna()
df2 = df2.dropna()

df_all = pd.merge(df1,df2, on = 'DATE')

diff = df_all['BRENT'] - df_all['WTI']

fig1 = plt.figure(figsize=(18, 8))
ax3 = fig1.add_subplot(1,1,1)
plt.plot(df_all['DATE'],diff,color='g', linewidth=1.0)
plt.title('Price Diff of BRENT and WTI')
plt.tight_layout(5)
plt.ylabel("Price_diff($)")
plt.xlabel("Date")

plt.show()