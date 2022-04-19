#!/usr/bin/env python
# coding: utf-8
Hypothesis: People that register more hours monthly are the ones that also register time one or more entries with no description or notes People that register more hours than the mean (find out) monthly are the ones that also register one or more entries with no description or notes

H0: people who have registred one or more "Time entry without any notes" in the brokenruledescription column register more hours than the mean. create user_type column: user0 = no entries with no notes, user1 = more than 1 entries without notes
# In[671]:


import pandas as pd
import numpy as np


# In[672]:


#read database
df = pd.read_csv(r"C:\Users\marin\Downloads\rls-trainee-data-engineer_sample-data.csv")


# In[673]:


#create new df with important columns 
dftask1 = df[['brokenruledescription', 'user_id', 'hours', 'spent_date']].copy()


# In[674]:


#clean database
#nan values
dftask1 = dftask1.dropna(how="any", axis=0) 
#values equal to 0
dftask1 = dftask1[(dftask1 != 0).all(1)]


# In[675]:


#separate spent_date column by- (create year and month column)
dftask1[['year','month','day']] = dftask1['spent_date'].str.split('-', n=3, expand=True)

#delete day, year, spentdate
dftask1 = dftask1.drop(['spent_date','day'], axis = 1)

#sort by month
dftask1.sort_values(['month'])


# In[676]:


#calculate sigma 
sigma = dftask1['hours'].std() 


# In[677]:


#calculate number of different user_id (n)
n = dftask1['user_id'].nunique()


# In[678]:


#confidence interval
alpha = 95


# In[679]:


#average of hours entered by one user per month
dftask1gg = dftask1.groupby(['month']).agg({'hours':'mean'})
dftask1gg


# In[680]:


total_users_mean = dftask1gg.mean()
total_users_mean


# In[681]:


#filter the users with at least one brokenruledescription = time entry without any notes
dftask1 = dftask1.groupby(['month','user_id','brokenruledescription']).agg({'hours':'mean'})
dftask1


# In[682]:


#reset index and then for for for
dftask1 = dftask1.reset_index()


# In[683]:


#classify users
dftask1['user_type'] = [1 if d == 'Time entry without any notes.' else -1 for d in dftask1['brokenruledescription']] 


# In[684]:


#reclassify users
dftask1 = dftask1.sort_values(["month", "user_id","user_type"], ascending=[True, False,False])
count = 1
user_temp = ''

for i in dftask1.index: 
    if(dftask1["user_id"][i] == user_temp):
        tipoUser = dftask1["user_type"][i]
        dftask1["user_type"][i] = tipoUserTemp

    user_temp = dftask1["user_id"][i]
    tipoUserTemp = dftask1["user_type"][i]
    


# In[685]:


dftask1g = dftask1.groupby(['month']).agg({'hours':'mean'})
dftask1g


# In[686]:


users1_mean = dftask1g.mean()
users1_mean

mu = dftask1gg["hours"].mean()
muxobs = dftask1g["hours"].mean()
xobsN = 1000
#list for sample mean distribution
Xm = []#fill Xm, append of the mean values of the random dist. generated
for i in range (1,N):
    x = np.random.normal(mu,sigma,n) #generates a random dist. with mu=avarage, sigma=std, n=77(size) 
    Xm.append(np.mean(x)) #calculates the mean of the dist. and append it to Xm
    # xc = np.percentile(Xm, alpha) #calcular o valor crítico para a amostra gerada no intervalo de confiança
xcprint('Xc=',xc,'  Xobs = ', xobs) #mostrar o valor crítico e a média da amostra observada

if(xobs < xc):
    print("Accept H0")
else:
    print("Reject H0")
# # Easier, cleaner way and probably the right one 

# In[687]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import math


# In[688]:


dftask1all = dftask1.groupby(['month','user_id']).agg({'hours':'sum'})
dftask1all


# In[689]:


#create users1 df
dfusers1 = dftask1[dftask1['user_type'] == 1]
dfusers1


# In[690]:


dfusers1 = dfusers1.groupby(['month','user_id']).agg({'hours':'sum'})
dfusers1


# In[691]:


meanpop = dftask1all.mean()
meansamp = dfusers1.mean()


# In[692]:


meanpop


# In[700]:


stats.ttest_1samp(a = dfusers1['hours'], popmean = dftask1all['hours'].mean())


# In[694]:


#calculate number of different users
df = dftask1all.reset_index()
i = df['user_id'].nunique()
i


# In[695]:


#calculate number of different users1
df1 = dfusers1.reset_index()
n = df1['user_id'].nunique()
n


# In[696]:


#range 
sigma = dfusers1.std()/math.sqrt(n) #52 is the sample size


# In[697]:


df = pd.DataFrame(stats.t.interval(0.95, df = 51, loc = dfusers1.mean(), scale = sigma), columns = ['range']) 
#df = df.transpose()
df


# In[703]:


if df.at[0,'range'] <= popmean and df.at[1,'range'] >= popmean[0,'range']:
    print('accept null hypothesys')
else:
    print('reject null hypothesys')


# # Correlation test

# In[709]:


dftask1 = dftask1.groupby(['month','user_id','user_type']).agg({'hours':'sum'})
#reset index
dftask1 = dftask1.reset_index()
dftask1


# In[710]:


dftask1['user_type'].corr(dftask1['hours'])


# In[711]:


import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(dftask1.corr(), annot=True, cmap="Wistia") #annot é pra mostrar os números, cmap é pra escolher as cores e o wistia é um que ele gosta de usar
plt.show()


sns.pairplot(df1) #cria os gráficos em azul
plt.show()


# # Kinda wrong

# In[ ]:


total_users_hours = dftask1gg['hours'].copy()
users1_hours = dftask1g['hours'].copy()


# In[ ]:


total_users_hours


# In[ ]:


popmean = total_users_hours.mean()
popsamp = users1_hours.mean()

print(popmean)
print(popsamp)


# In[ ]:


stats.ttest_1samp(a = users1_hours, popmean = total_users_hours.mean())

p-value is equal to 0.04 wich means that the probabiility of seeing a result as extreme as the one observed due to chance is around 4% if the null hypothesys was true. That is, we are gonna see a result as extreme as observed 4% of the times. 

if p-value is lower than the significance value (1-alpha) = reject null hypothesys
# In[ ]:


df = pd.DataFrame (users1_hours, columns = ['hours'])
n = df['hours'].count()
n


# In[ ]:


sigma = users1_hours.std()/math.sqrt(n) #12 is the sample size

df = pd.DataFrame(stats.t.interval(0.95, df = 11, loc = users1_hours.mean(), scale = sigma), columns = ['range']) 
df


# In[ ]:


popmean


# In[ ]:


if df.at[1,'range'] <= popmean >= df.at[1,'range']:
    print('Yes. The more entries a user has without any notes, more likely he is to enter more hours than the rest')
else:
    print('No.')


# # Correlation test

# In[ ]:


df1 = dftask1[['user_id', 'user_type', 'hours']].copy()

df1 = df1.groupby(['user_id', 'user_type']).agg({'hours':'sum'})

#reset index
df1 = df1.reset_index()

df1


# In[ ]:


df1['user_type'].corr(df1['hours'])


# In[ ]:


import seaborn as sns
import matplotlib.pyplot as plt

sns.heatmap(df1.corr(), annot=True, cmap="Wistia") #annot é pra mostrar os números, cmap é pra escolher as cores e o wistia é um que ele gosta de usar
plt.show()


sns.pairplot(df1) #cria os gráficos em azul
plt.show()


# # Testing stats library

# In[ ]:


#correlation between user_type and hours
from scipy.stats import pearsonr

corr, _ = pearsonr(df1['user_type'], df1['hours'])
print('Pearsons correlation: %.3f' % corr)


# In[ ]:


import statsmodels.api as sn
import numpy as pn
import pandas as pd


# In[ ]:


n = 77
pnull = 3.32
phat = xobs
sn.stats.proportions_ztest(phat*n, n, pnull)


# In[ ]:




