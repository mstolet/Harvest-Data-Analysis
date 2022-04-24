#!/usr/bin/env python
# coding: utf-8

# # Create a list classifying projects considering the amount of work done by task names.

# ## Read database and clean it up

# In[36]:


import pandas as pd


# In[37]:


#read database
df = pd.read_csv(r"C:\Users\marin\Downloads\rls-trainee-data-engineer_sample-data.csv")


# In[38]:


#clean database
#nan values
df = df.dropna(how="any", axis=0) 
#values equal to 0
df = df[(df != 0).all(1)]


# In[39]:


#create new df with important columns 
dftask2 = df[['user_id', 'task_name', 'hours']].copy()
dftask2


# ## Classify tasks by groups 

# In[40]:


#Group Recruitment tasks
dftask2.loc[((dftask2.task_name == 'Candidate Screening') | (dftask2.task_name == 'Candidates reviews and updates') | (dftask2.task_name == 'Interview') | (dftask2.task_name == 'Onboarding') | (dftask2.task_name == 'RLS: review')), "task_group"] = "Recruitment"
#Group Development tasks
dftask2.loc[((dftask2.task_name == 'Backend') | (dftask2.task_name == 'Dev: Development') | (dftask2.task_name == 'Dev: Pair Programming') | (dftask2.task_name == 'Dev: Planning') | (dftask2.task_name == 'Dev: Testing') | (dftask2.task_name == 'Gamification') | (dftask2.task_name == 'Programming')), "task_group"] = "Development"
#Group Self improving tasks
dftask2.loc[((dftask2.task_name == 'Learning') | (dftask2.task_name == 'Studying')), "task_group"] = "Self improving"
#Group Management tasks
dftask2.loc[((dftask2.task_name == 'Project Management') | (dftask2.task_name == 'BizTech') | (dftask2.task_name == 'Business Development') | (dftask2.task_name == 'Documentation') | (dftask2.task_name == 'Copywriting') | (dftask2.task_name == 'Meeting: 101') | (dftask2.task_name == 'Meeting: Approving') | (dftask2.task_name == 'Meeting: ATDD') | (dftask2.task_name == 'Meeting: Automation') | (dftask2.task_name == 'Meeting: Bug Fix') | (dftask2.task_name == 'Meeting: Client Bug') | (dftask2.task_name == 'Meeting: Client Scope') | (dftask2.task_name == 'Meeting: Client SSO / API') | (dftask2.task_name == 'Meeting: Demo') | (dftask2.task_name == 'Meeting: Feedback') | (dftask2.task_name == 'Meeting: Formulation') | (dftask2.task_name == 'Meeting: Retro') | (dftask2.task_name == 'Meeting: Scope') | (dftask2.task_name == 'Meeting: Sprint Planning') | (dftask2.task_name == 'Meeting: SUP') | (dftask2.task_name == 'Meeting: Tech Talk') | (dftask2.task_name == 'Meeting: Ticket Review') | (dftask2.task_name == 'Meetings')), "task_group"] = "Management"
#Group DevOps tasks
dftask2.loc[((dftask2.task_name == 'DevOps')), "task_group"] = "DevOps"
#Group Marketing tasks
dftask2.loc[((dftask2.task_name == 'Marketing')), "task_group"] = "Marketing"
#Group UI/UX Design tasks
dftask2.loc[((dftask2.task_name == 'UI') | (dftask2.task_name == 'UX') | (dftask2.task_name == 'UX/UI: High-end Fidelity Design') | (dftask2.task_name == 'UX/UI: Prototyping') | (dftask2.task_name == 'UX/UI: Research / Ideation') | (dftask2.task_name == 'Graphic Design')), "task_group"] = "UI/UX Design"
#Group Prod Work tasks
dftask2.loc[((dftask2.task_name == 'Prod: Approving') | (dftask2.task_name == 'Prod: Bulk Uploads / Deletes') | (dftask2.task_name == 'Prod: Create / Run Reports') | (dftask2.task_name == 'Prod: Cycle Planning') | (dftask2.task_name == 'Prod: Dashboard Creation / Update') | (dftask2.task_name == 'Prod: Discovery') | (dftask2.task_name == 'Prod: Process Scope / Optimization') | (dftask2.task_name == 'Prod: Research') | (dftask2.task_name == 'Prod: Scope') | (dftask2.task_name == 'Prod: SecurityQuestionnaires') | (dftask2.task_name == 'Prod: SSO Setup') | (dftask2.task_name == 'Prod: Tech Requests') | (dftask2.task_name == 'Prod: Testing') | (dftask2.task_name == 'Prod: Testing / Approving') | (dftask2.task_name == 'Prod: User Stories')), "task_group"] = "Prod Work"
#Group Quality Assurance tasks
dftask2.loc[((dftask2.task_name == 'QA') | (dftask2.task_name == 'QA: Code Review') | (dftask2.task_name == 'QA: Exploratory Tests') | (dftask2.task_name == 'QA: Manual Tests') | (dftask2.task_name == 'QA: Test Automation') | (dftask2.task_name == 'QA: Test Devops') | (dftask2.task_name == 'QA: Test Scenarios Conception') | (dftask2.task_name == 'QA: Tests Formulation')), "task_group"] = "Quality Assurance"


# ## Show amount of hours worked by task group

# In[41]:


dftask2 = dftask2.groupby(['task_group']).agg({'hours':'sum'}).sort_values(['hours'], ascending=False)


# In[42]:


dftask2


# In[ ]:




