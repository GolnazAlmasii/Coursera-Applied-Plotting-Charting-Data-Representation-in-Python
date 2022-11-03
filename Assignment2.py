
# coding: utf-8

# # Assignment 2
# 
# Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to **Preview the Grading** for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.
# 
# An NOAA dataset has been stored in the file `data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv`. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) [Daily Global Historical Climatology Network](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt) (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.
# 
# Each row in the assignment datafile corresponds to a single observation.
# 
# The following variables are provided to you:
# 
# * **id** : station identification code
# * **date** : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
# * **element** : indicator of element type
#     * TMAX : Maximum temperature (tenths of degrees C)
#     * TMIN : Minimum temperature (tenths of degrees C)
# * **value** : data value for element (tenths of degrees C)
# 
# For this assignment, you must:
# 
# 1. Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
# 2. Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
# 3. Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
# 4. Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.
# 
# The data you have been given is near **Ann Arbor, Michigan, United States**, and the stations the data comes from are shown on the map below.

# In[3]:

import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8,8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


# In[30]:

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
df = pd.read_csv("data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")
df.head(10)


# In[32]:

df["Data_Value"]=df["Data_Value"]/10
df["Year"] = df["Date"].apply(lambda x: x[:4])
df["Day"] = df["Date"].apply(lambda x: x[-5:])
df = df[df["Day"] != '02-29']
df2 = df[df["Year"]!="2015"]
df2015 = df[df["Year"]=="2015"]
#print(df.shape)
#print(df2.shape)
df2015


# In[45]:

maxdf4_14 = df2.groupby("Day").agg({"Data_Value" : np.max})
mindf4_14 = df2.groupby("Day").agg({"Data_Value" : np.min})
max15 = df2015.groupby("Day").agg({"Data_Value" : np.max})
min15 = df2015.groupby("Day").agg({"Data_Value" : np.min})
maxdf = pd.merge(maxdf4_14.reset_index(), max15.reset_index(), left_index=True, on = "Day")
mindf = pd.merge(mindf4_14.reset_index(), min15.reset_index(), left_index=True, on = "Day")
maxrec = maxdf[maxdf["Data_Value_y"] > maxdf["Data_Value_x"]]
minrec = mindf[mindf["Data_Value_y"] < mindf["Data_Value_x"]]
minrec


# In[104]:

get_ipython().magic('matplotlib inline')
plt.figure(figsize=(20,15))
plt.xlabel("Days", fontsize=15)
plt.ylabel("temperature", fontsize=15)
plt.plot(maxdf4_14.values, color = "red", alpha=0.35, label = "dacade high record")
plt.plot(mindf4_14.values, color = "blue", alpha=0.35, label = "decade low record")

plt.gca().fill_between(range(len(maxdf4_14)), 
                       np.array(maxdf4_14.values.reshape(len(mindf4_14.values),)), 
                       np.array(mindf4_14.values.reshape(len(mindf4_14.values),)), 
                       facecolor="808080", 
                       alpha=0.12)

plt.scatter(maxrec.index.tolist(), maxrec['Data_Value_y'].values, color = "red", label = "High record broken in 2015")
plt.scatter(minrec.index.tolist(), minrec['Data_Value_y'].values, color = "blue", label = "Low record broken in 2015")


for pos in ['right', 'top']:
    plt.gca().spines[pos].set_visible(False)
    
plt.legend(loc = 8, fontsize=15, frameon = False)


# In[ ]:



