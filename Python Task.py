#!/usr/bin/env python
# coding: utf-8

# # Python Task

# In[1]:


import numpy as np
import pandas as pd
from datetime import datetime
from scipy import stats
import missingno as msno
import seaborn as sns
import matplotlib.pyplot as plt


# ## Flow data

# In[2]:


# Load the flow daata files and combine them in one dataframe
xlsx_flow_file_list = ["flow_1.xlsx", "flow_2.xlsx", "flow_3.xlsx", "flow_4.xlsx"]

list_of_flow_data = []

for filename in xlsx_flow_file_list:
    list_of_flow_data.append(pd.read_excel(filename))

flow_data = pd.concat(list_of_flow_data)

flow_data.head()


# #### The time column is in unix time format, which needs to be converted.

# In[3]:


# Check the data type and missing values
flow_data.info()


# #### It shows the dataframe has null values from both columns.

# In[4]:


# Convert the time column
flow_data['time'] = pd.to_datetime(flow_data['time'],unit='s')
flow_data = flow_data.rename({'value': 'flow'}, axis=1)
flow_data.head(15)


# In[5]:


# Visualize the count of the missing values
time_missing = len(flow_data[flow_data['time'].isnull()])
value_missing = len(flow_data[flow_data['flow'].isnull()])

plt.bar(['time', 'flow'], [time_missing, value_missing], align='center')
plt.ylabel('Count')
plt.title('Missing value count by columns for flow data')

plt.show()


# In[6]:


plt.figure(figsize=(150,20))
sns.heatmap(flow_data.isna().transpose(),
            cmap="YlGnBu",
            cbar_kws={'label': 'Missing Data'})


# #### Another problem here is that there are duplicates of timestamps with different flow values.

# In[7]:


# Visualize the duplicates of the timestamps
flow_data['Count'] = 1
flow_duplicate = flow_data.groupby(['time']).Count.count().reset_index()
# Sample the timestamps randomly to make the axis more clear
flow_duplicate.sample(n=150, random_state=1).plot.line(x='time', y='Count', figsize=(60,20), title='Count of timestamp')
flow_duplicate.head()


# #### According to the random sampling of the timestamps, most of the timestamps have more than 1 different values of flow data.

# ## Rain data

# In[8]:


# Load the rain daata files and combine them in one dataframe
xlsx_rain_file_list = ["rain_1.xlsx", "rain_2.xlsx"]

list_of_rain_data = []

for filename in xlsx_rain_file_list:
    list_of_rain_data.append(pd.read_excel(filename))

rain_data = pd.concat(list_of_rain_data)

rain_data.head()


# In[9]:


rain_data.info()


# #### There are no missing values for rain data, but the time column still needs to be converted.

# In[10]:


rain_data['time'] = pd.to_datetime(rain_data['time'],unit='s')
rain_data.head(15)


# #### Similar to the flow data, timestamp duplication is also a problem for the rain data.

# In[11]:


rain_data['Count'] = 1
rain_duplicate = rain_data.groupby(['time']).Count.count().reset_index()
rain_duplicate.plot.line(x='time', y='Count', figsize=(60,20), 
                                                       title='Count of timestamp for rain')
rain_duplicate.head()


# In[12]:


rain_duplicate[rain_duplicate['Count'] > 1].count()


# #### 383 records of timestamps have duplicated rain values.

# ## Relatonship between flow and rain

# #### Assuming the rain is the explanatory variable and the flow is the response variable, the first step is to drop the missing values of the flow data. And then, in order to combine these two dataframes together, the timestamps need to be unique from both dataframes. For rain data, assuming the value is aggregated by mode. For flow data, assuming the value is aggregated by maximum.

# In[13]:


# Drop the missing values for flow data
flow_data = flow_data.dropna()
flow_data.info()


# In[14]:


# Join these two dataframes by column time
rain_flow = pd.merge(rain_data.groupby(rain_data.time)['rain'].agg(lambda x: tuple(stats.mode(x)[0])[0]), 
                     flow_data.groupby(flow_data.time).max('flow'), on=['time','time'])[['flow', 'rain']]
rain_flow.info()


# #### Check the distribution pattern of rain and flow

# In[15]:


rain_flow['rain'].plot.kde()


# In[16]:


rain_flow['flow'].plot.kde()


# #### For the flow data, the distribution is a little bit right-skewed, which means the mean of the flow data is to the right of the median.

# In[17]:


plt.scatter((rain_flow["rain"]), rain_flow["flow"])


# #### The scatter plot doesn't show any clear relationship.

# In[18]:


print(rain_flow['rain'].value_counts())


# #### For the rain data, the values are not continuous. They are discrete, which means boxplots can be used to show the relationship.

# In[19]:


bp = rain_flow.boxplot(by='rain', column='flow', figsize=(15, 10), grid=False)
bp.set_ylabel('flow')
plt.suptitle('')
bp.set_title('Flow distribution based om different rain values')


# #### According to the boxplots based on different rain values, the distribution pattern is clear for flow data. As the rain increases, the flow also increases.
# #### One thing to notice is that when the rain value is 10, the flow data decreases siginificantly, which is abnormal. Moreover, compared to other rain data values, the value 10 is quite large. There could be possibility that 10.0 should be 1.0. The gap from 0.8 to 10.0 is too large.
