import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("ggplot")  

df = pd.read_excel('./IF00jicha.xlsx')


# df2 = pd.DataFrame()
df1 = np.array(df[['IF00.CFE','SH300','Basis','Basis Ratio']])

df2 = pd.DataFrame(df1,columns = ['IF00.CFE','SH300','Basis','Basis Ratio'],index = df.iloc[:,0])


fig = plt.figure(figsize=(12, 8))
ax1 = fig.add_subplot(3,1,1)
ax1.plot(df2[['IF00.CFE']],color='blue', linewidth=1.0, label='IF000.CFE')
ax1.plot(df2[['SH300']],color='red', linewidth=1.0, linestyle='--',label='SH300')
plt.title('IF00.CFE&SH300').set_fontsize(fontsize = 15)
plt.tight_layout(5)
plt.legend(loc='upper left')
ax2 = fig.add_subplot(3,1,2)
ax2.plot(df2[['Basis']],linewidth=1.0)
plt.title('Basis').set_fontsize(fontsize = 15)
plt.tight_layout(5)
ax3 = fig.add_subplot(3,1,3)
ax3.plot(df2[['Basis Ratio']],linewidth=1.0)
plt.title('Basis Ratio').set_fontsize(fontsize = 15)

print(df2)

plt.show()

