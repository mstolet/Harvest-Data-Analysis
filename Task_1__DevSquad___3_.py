#!/usr/bin/env python
# coding: utf-8

# # Test whether: People that register more hours monthly are the ones that also register time one or more entries with no description or notes.
H0: people who have registred one or more "Time entry without any notes" in the brokenruledescription column register more hours than the mean. create user_type column: user0 = no entries with no notes, user1 = more than 1 entries without notes
# ## Read database and clean it up

# In[133]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import math


# In[134]:


import pandas as pd
import numpy as np


# In[135]:


#read database
df = pd.read_csv(r"C:\Users\marin\Downloads\rls-trainee-data-engineer_sample-data.csv")


# In[136]:


#create new df with important columns 
dftask1 = df[['brokenruledescription', 'user_id', 'hours', 'spent_date']].copy()


# In[137]:


#clean database
#nan values
dftask1 = dftask1.dropna(how="any", axis=0) 
#values equal to 0
dftask1 = dftask1[(dftask1 != 0).all(1)]


# In[138]:


#separate spent_date column by- (create year and month column)
dftask1[['year','month','day']] = dftask1['spent_date'].str.split('-', n=3, expand=True)

#delete day, year, spentdate
dftask1 = dftask1.drop(['spent_date','day'], axis = 1).sort_values(['month'])


# ## Classify users that entered one or more "Entry without any notes"

# In[139]:


#filter the users with at least one brokenruledescription = time entry without any notes
dftask1 = dftask1.groupby(['month','user_id','brokenruledescription']).agg({'hours':'mean'}).reset_index()


# In[140]:


#classify entry type.Type 1 is for those who entered one or more "time entry without any notes", else, type -1.
dftask1['user_type'] = [1 if d == 'Time entry without any notes.' else -1 for d in dftask1['brokenruledescription']] 


# In[141]:


#classify users by entrys classification
dftask1 = dftask1.sort_values(["month", "user_id","user_type"], ascending=[True, False,False])

user_temp = ''

for i in dftask1.index: 
    if(dftask1["user_id"][i] == user_temp):
        tipoUser = dftask1["user_type"][i]
        dftask1["user_type"][i] = tipoUserTemp

    user_temp = dftask1["user_id"][i]
    tipoUserTemp = dftask1["user_type"][i]
    


# ## Create a DF for users type 1 (who have entries without any notes) hours

# In[142]:


#create users1 df
dfusers1 = dftask1[dftask1['user_type'] == 1]


# In[143]:


#Save dataframe to use in task number 3
dfusers1.to_csv('users1_before_groupby', index=False)


# In[144]:


dfusers1 = dfusers1.groupby(['month','user_id']).agg({'hours':'sum'}).reset_index()


# ## Create a DF for all the users (1 and -1) hours

# In[145]:


dftask1all = dftask1.groupby(['month','user_id']).agg({'hours':'sum'})


# ## Run t test

# In[146]:


#Run the T-test for the mean of ONE group of scores. See at: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
stats.ttest_1samp(a = dfusers1['hours'], popmean = dftask1all['hours'].mean())


# ## Run correlation test

# In[147]:


dftask1 = dftask1.groupby(['month','user_id','user_type']).agg({'hours':'sum'}).reset_index()


# In[148]:


#simply get the correlation number
dftask1['user_type'].corr(dftask1['hours'])


# In[149]:


#gives a more visual result (more interesting to check corr between multiple variables)
import seaborn as sns
import matplotlib.pyplot as plt

#heat map
sns.heatmap(dftask1.corr(), annot=True, cmap="Wistia")
plt.show()

#plot
sns.pairplot(df1) 
plt.show()

