#!/usr/bin/env python
# coding: utf-8

# # Test whether: programmers who created entries and spent more than 3 hours in the same entry are those who have more entries without notes.

# ## Read df with users "any notes"

# In[160]:


import pandas as pd


# In[161]:


#read df with only users with one or more entries "without any notes"
dfusers1 = pd.read_csv(r"C:\Users\marin\Downloads\jupyter\users1_before_groupby")
dfusers1


# In[162]:


#groupby user
dfusers1 = dfusers1.groupby(['user_id']).agg({'hours':'sum'}).reset_index()


# In[163]:


#get only users ids
dfusers1 = dfusers1[['user_id']].copy()


# ## Read database and clean it up

# In[164]:


#read database
df = pd.read_csv(r"C:\Users\marin\Downloads\rls-trainee-data-engineer_sample-data.csv")


# In[165]:


#clean database
#nan values
df = df.dropna(how="any", axis=0) 
#values equal to 0
df = df[(df != 0).all(1)]


# In[166]:


#create new df with important columns 
dftask3 = df[['user_id', 'brokenruledescription', 'hours', 'spent_date']].copy()


# In[167]:


dftask3['month'] = pd.to_datetime(df['spent_date']).dt.month
dftask3 = dftask3.drop(['spent_date'], axis = 1)


# ## Classify users with one or more entries "Time entry bigger than 3 hours"

# In[168]:


#filter the users with at least one "Time entry bigger than 3 hours."
dftask3 = dftask3.groupby(['month','user_id','brokenruledescription']).agg({'hours':'mean'}).reset_index()


# In[169]:


#classify entry type. Type 1 is for those who entered one or more "Time entry bigger than 3 hours.", else, type -1.
dftask3['bigger'] = [1 if d == 'Time entry bigger than 3 hours.' else -1 for d in dftask3['brokenruledescription']] 


# In[170]:


#classify users by entrys classification
dftask3 = dftask3.sort_values(["month", "user_id","bigger"], ascending=[True, False,False])

user_temp = ''

for i in dftask3.index: 
    if(dftask3["user_id"][i] == user_temp):
        tipoUser = dftask3["bigger"][i]
        dftask3["bigger"][i] = tipoUserTemp

    user_temp = dftask3["user_id"][i]
    tipoUserTemp = dftask3["bigger"][i]
    


# In[171]:


dfbigger = dftask3.groupby(['user_id']).agg({'hours':'sum'}).reset_index().drop(['hours'], axis = 1)


# ## Compare dfusers1 to dfbigger 

# In[172]:


#if user id in dfusers1 is also in dfbigger then column "exist" is filled with True, else, "False" 
dfusers1['exist'] = dfusers1['user_id'].isin(dfbigger['user_id'])


# In[173]:


#True and False percentages  in dataframe
dfusers1['exist'].value_counts(normalize=True) * 100


# In[ ]:




