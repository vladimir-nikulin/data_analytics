#!/usr/bin/env python
# coding: utf-8

# In[22]:


import numpy as np
import pandas as pd

from geopy.distance import vincenty
import datetime
import time


# ### Введение

# #### Загрузите csv файл в датафрейм

# In[11]:


citybike = pd.read_csv('201809-citibike-tripdata.csv')


# In[8]:


citybike.head()


# 1. Найти общее количество строк и столбцов в датасете - указать первым число строк, вторым - число столбцов

# In[12]:


citybike.shape


# Найти среднюю длину поездок в минутах(столбец tripduration) c точностью до 2 знака

# In[13]:


citybike['tripduration'] = citybike['tripduration']/60
round(citybike.describe()['tripduration']['mean'], 2)


# Сколько поездок начались и закончились в той же самой станции?

# In[14]:


citybike[(citybike['start station id'] == citybike['end station id'])].shape


# Сколько поездок начались и закончились в той же самой станции? Указать количество уникальных байков

# In[43]:


citybike[(citybike['start station id'] == citybike['end station id'])]['bikeid'].unique().shape


# Какой самый используемый байк(bikeid) в городе по количеству поездок? 

# In[19]:


citybike['bikeid'].value_counts()[:1]


# Найдите байк(bikeid), у которого в среднем продолжительность поездок выше, чем у всех остальных

# In[15]:


citybike.groupby('bikeid')['tripduration'].mean().sort_values(ascending=False)[:1]


# Найдите количество строк, в которых отсутствуют данные о start station id

# In[17]:


citybike[citybike['start station id'].isnull()].shape


# Какова средняя продолжительность поездки в зависимости от типа подписки c точностью до 2 знака? 

# In[18]:


round(citybike.groupby('usertype')['tripduration'].mean(),2)


# Для каждой станции найдите расстояние между станциями, а затем найдите среднее расстояние по всем поездкам, предварительно выкинув замкнутые траектории(те у которых совпадают start station id = end station id). 
# 
# Hint: можно воспользоваться библиотекой geopy и взять расстояние vincenty(минимальное расстояние между точками)
# 

# In[12]:


citybike['distance_km'] = citybike.apply(lambda x: vincenty((x['start station latitude'], x['start station longitude']),
                                                            (x['end station latitude'], x['end station longitude'])).kilometers, axis=1)

print(citybike['distance_km'].mean())


# In[15]:


citybike['end station name'].value_counts()[:5]


# Выберите станцию (start station id) с максимальным количеством отправлений с 18 до 20 вечера

# In[24]:


citybike['end_hour'] = citybike['stoptime'].apply(lambda x: datetime.datetime.fromtimestamp(
            time.mktime(datetime.datetime.strptime(x.strip(), "%Y-%m-%d %H:%M:%S.%f").timetuple())).hour)


# In[25]:


citybike['start_hour'] = citybike['starttime'].apply(lambda x: datetime.datetime.fromtimestamp(
                                        time.mktime(datetime.datetime.strptime(x.strip(), "%Y-%m-%d %H:%M:%S.%f").timetuple())).hour)


# In[33]:


citybike[(citybike.start_hour.isin([18, 19, 20]))]['start station id'].value_counts().head()


# Выберите станции(end station id), в которые приезжают с 6 до 10 утра
# 

# In[29]:


end_stations = [3140, 3106, 3116, 369]


# In[30]:


citybike[(citybike.end_hour.isin([6,7,8,9,10])) &
         (citybike['end station id'].isin(end_stations))]['end station id'].unique()

