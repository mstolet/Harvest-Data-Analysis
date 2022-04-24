#!/usr/bin/env python
# coding: utf-8

# # Create and test three hypothesis:
1) People who spend more hours working are the same that enter programming tasks. 
2) People work more hours when the client's currency is GBP.
3) People work less hours in december.
# ## Read database and clean it up

# In[22]:


import pandas as pd
import numpy as np
import scipy.stats as stats
import math


# In[23]:


#read database
df = pd.read_csv(r"C:\Users\marin\Downloads\rls-trainee-data-engineer_sample-data.csv")


# In[24]:


#clean database
#nan values
df = df.dropna(how="any", axis=0) 
#values equal to 0
df = df[(df != 0).all(1)]


# In[25]:


df


# # Hypothesys one: People who enter programming tasks enter more hours.
Programming tasks:
    -UX/UI: Prototyping
        -Dev: Pair Programming
        -Programming
# ## Create dataframe

# In[26]:


#create new df with important columns 
dftask51 = df[['user_id', 'task_name', 'hours']].copy()


# In[27]:


dftask51 = dftask51.groupby(['user_id', 'task_name']).agg({'hours':'sum'}).reset_index()


# ## Classify user by programmers and not programmers

# In[28]:


#fill user type column with "programmer" if task name is Programming or Dev: Pair Programming
dftask51.loc[(dftask51['task_name'] == 'Dev: Pair Programming') | (dftask51['task_name'] == 'Programming'), 'user_type'] = 'programmer'  
dftask51.loc[(dftask51['task_name'] != 'Dev: Pair Programming') & (dftask51['task_name'] != 'Programming'), 'user_type'] = 'not programmer'  


# In[29]:


#sort users
dftask51 = dftask51.sort_values(["user_id","user_type"], ascending=[True, False])


# In[30]:


# Classify users who have entered at least one programming task name as Programmer and those have not as not programmers
user_temp = ''

for i in dftask51.index: 
    if(dftask51["user_id"][i] == user_temp):
        tipoUser = dftask51["user_type"][i]
        dftask51["user_type"][i] = tipoUserTemp

    user_temp = dftask51["user_id"][i]
    tipoUserTemp = dftask51["user_type"][i]


# In[31]:


dftask51g = dftask51.groupby(['user_id','user_type']).agg({'hours':'mean'}).reset_index()


# ## create df for programmers

# In[32]:


dfprogrammer = dftask51[dftask51['user_type'] == 'programmer']


# ## Run t test

# In[33]:


#Run the T-test for the mean of ONE group of scores. See at: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
stats.ttest_1samp(a = dfprogrammer['hours'], popmean = dftask51g['hours'].mean())


# # Hypothesys two: People work more hours when the client's currency is GBP.

# In[34]:


#create new df with important columns 
dftask52 = df[['user_id', 'client_currency', 'hours']].copy()


# In[35]:


dftask52 = dftask52.groupby(['user_id', 'client_currency']).agg({'hours':'sum'}).reset_index()


# ## Create dataframe for GBP

# In[36]:


#create dataframe for GBP entered hours
dfgbp = dftask52[dftask52['client_currency'] == 'GBP']


# ## Run t test

# In[37]:


#Run the T-test for the mean of ONE group of scores. See at: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
stats.ttest_1samp(a = dfgbp['hours'], popmean = dftask52['hours'].mean())


# # Hypothesys three: People work less hours in december.

# In[38]:


#create new df with important columns 
dftask53 = df[['user_id', 'spent_date', 'hours']].copy()


# In[39]:


#get month from date_spent
dftask53['month'] = pd.to_datetime(df['spent_date']).dt.month
dftask53 = dftask53.drop(['spent_date'], axis = 1)


# ## Create df for december hours

# In[40]:


#create df for only for december
dfdec = dftask53[dftask53['month'] == 12]


# ## Run t test

# In[41]:


#Run the T-test for the mean of ONE group of scores. See at: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_1samp.html
stats.ttest_1samp(a = dfdec['hours'], popmean = dftask53['hours'].mean())


# ## Run correlation test

# In[42]:


dftask53['month'].corr(dftask53['hours'])


# In[ ]:


## Devsquad's harvest data analysis

## Description
Harvest is a time tracking and reporting software used by many companies, one of them being Devsquad. In this project a database from Devsquad's harvest account is being analyzed. The project is devided in five main tasks, in which mainly hypothesis are being tested. 

## Visuals
get_ipython().system('[image.png](./image.png)')

## Installation
All we need to have for this project is:
    Pandas (see how to install: https://pt.stackoverflow.com/questions/57487/como-instalar-a-biblioteca-pandas-no-python-3)
    Numpy (see how to install: https://numpy.org/install/)
    Statsmodels (see how to install: https://www.statsmodels.org/stable/install.html)
And a text editing program. I am using Jupyter Notebook, you can learn how to install it in: https://docs.jupyter.org/en/latest/install/notebook-classic.html

## Usage
This code is helpfull when it comes to running t-tests and correlations tests on a database to test whether a hypothesis is true or false.

## Tasks Descriptions

# Task 1
Test whether: People that register more hours monthly are the ones that also register time one or more entries with no description or notes.

# Task 2
Create a list classifying projects considering the amount of work done by task names.

# Task 3
Test whether: programmers who created entries and spent more than 3 hours in the same entry are those who have more entries without notes.

# Task 4
Test whether: people who create manual entries have a more even distributed work time during the week, i.e., they work in a regular pace every day, registering the same average amount of hours per day.

# Task 5
Create and test three hypothesis:
    1) People who spend more hours working are the same that enter more programming tasks. 
    2) People work more hours when the client's currency is USD.
    3) People work less hours in december.

## Tasks Results

# Task 1
The null hypothesis, people who registered one or more entries "without any notes" registered just as much hours than the rest, got rejected after receiving a p-value of 3.9371271521266196e-11 after a t-test. Also, if the correlation of 0.5034603801323787 is analyzed, it can be concluded that there are a positive moderated relation between entering more hours and not entering notes.

# Task 2
The most time demanding tasks are those in the Development group, a total of 24669.37 hours registered. Quality Assurance is the second (5926.63 hours) and, actually with a really close number (5177.65) is the DevOps group. After that it comes UI/UX Design, Management, Marketing, Prod Work, Recruitment and Self improving.

# Task 3
After descovering that not even 10% of those who entered at least one time "without any notes" are NOT in the list of those who created entries "bigger than 3 hours", it can stated that programmers who create time entries longer than three hours are probably the same who don't write notes.

# Task 4
Running a correlation test between a "hours only from users who create manual entries" dataframe and a "hours from all the users" dataframe, it can be found that probably, users who create manual entries have NOT a more even work pace during the week, since the number gotten is really close to zero, only -0.05853687472846683. If a t-test is also ran, the null hypothesis that people who create manual entries have a more even work pace during the week can be rejected, since the p-value is also really small: 3.5107658841576125e-08.

# Task 5
    1) People who spend more hours working are the same that enter more programming tasks.
H0: People who spend a higher number of hours than the mean working are the same that enter programming tasks.
Null hypothesis accepted for a p-value of 0.1791899767959702.

    2) People work more hours when the client's currency is USD.
H0: People spend more hours than the mean on projects which the clients currency is GBP.
Null hypothesis rejected for a p-value of 0.030391437008328866.

    3) People work less hours in december.
H0: People work less hours than the mean of the rest of the year in december.
Null hypothesis rejected for a p-value of 7.525432670171487e-07 and correlation of 0.022521589871756283
.

