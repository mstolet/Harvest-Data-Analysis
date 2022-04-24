#!/usr/bin/env python
# coding: utf-8

# # Test whether: people who create manual entries have a more even distributed work time during the week, i.e., they work in a regular pace every day, registering the same average amount of hours per day.

# ## Read database and clean it up

# In[11]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import math


# In[12]:


#read database
df = pd.read_csv(r"C:\Users\marin\Downloads\rls-trainee-data-engineer_sample-data.csv")


# In[13]:


#clean database
#nan values
df = df.dropna(how="any", axis=0) 
#values equal to 0
df = df[(df != 0).all(1)]


# In[14]:


#create new df with important columns 
dftask4 = df[['user_id', 'brokenruledescription', 'hours', 'spent_date']].copy()

dftask4['month'] = pd.to_datetime(dftask4['spent_date']).dt.month
dftask4 = dftask4.drop(['spent_date'], axis = 1)
dftask4
# ## Classify users "The time entry is a manual entry running"

# In[16]:


#filter the users with at least one brokenruledescription = The time entry is a manual entry running
dftask4 = dftask4.groupby(['spent_date','user_id','brokenruledescription']).agg({'hours':'sum'}).reset_index()


# In[17]:


# Whats the name entry for people who create manual entries
dftask4.brokenruledescription.unique()


# In[18]:


#classify entry type. Type 1 is for those who entered one or more "The time entry is a manual entry stopped", else, type -1.
dftask4['user_type'] = [1 if d == 'The time entry is a manual entry stopped' else -1 for d in dftask4['brokenruledescription']] 


# In[20]:


#classify users by entrys classification
user_temp = ''

for i in dftask4.index: 
    if(dftask4["user_id"][i] == user_temp):
        tipoUser = dftask4["user_type"][i]
        dftask4["user_type"][i] = tipoUserTemp

    user_temp = dftask4["user_id"][i]
    tipoUserTemp = dftask4["user_type"][i]
    


# ## Create DF for users type 1

# In[24]:


#create users1 df
dfusers14 = dftask4[dftask4['user_type'] == 1]


# In[27]:


#group by day
dfusers14 = dfusers14.groupby(['spent_date','user_id']).agg({'hours':'sum'}).reset_index()


# ## Create DF for all users

# In[28]:


dftask4all = dftask4.groupby(['spent_date','user_id']).agg({'hours':'sum'}).reset_index()


# ## Run t test

# In[33]:


#Run the T-test for the mean of ONE group of scores. See at: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
stats.ttest_1samp(a = dfusers14['hours'], popmean = dftask4all['hours'].mean())


# ## Run correlation test

# In[34]:


dftask4['user_type'].corr(dftask4['hours'])

