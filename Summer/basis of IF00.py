import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel('.IF00jicha.xlsx')


# df2 = pd.DataFrame()
df1 = np.array(df[['IF00.CFE','SH300','Basis','Basis Ratio']])

df2 = pd.DataFrame(df1,columns = ['IF00.CFE','SH300','Basis','Basis Ratio'],index = df.iloc[:,0])


fig = plt.figure()
ax1 = fig.add_subplot(2,1,1)
df2.plot()
ax2 = fig.add_subplot(2,2,3)
ax3 = fig.add_subplot(2,2,4)

print(df)

plt.show()

