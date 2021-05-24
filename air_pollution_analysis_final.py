# -*- coding: utf-8 -*-
"""Air_Pollution_Analysis_final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WSRrdo11Ek-35jvT4oDuew104r47CkFT
"""



"""# Air Pollution Analysis """

# Import useful libraries

import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
import geopandas as gpd 

import netCDF4 as nc
import hd5y
import metis

pip install geopandas

import pandas as pd 
from google.colab import files

uploaded = files.upload()

df = pd.read_csv("data.csv", encoding = "ISO-8859-1")
df.head()

df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d') # date parse
df['year'] = df['date'].dt.year # year
df['year'] = df['year'].fillna(0.0).astype(int)
df = df[df['year']>0]

df.shape

df.dtypes.value_counts()

df.isnull().sum()

printNullValues(df)

"""### Affected Sectors """

df["type"].value_counts()

sns.catplot(x = "type", kind = "count",  data = df, height=5, aspect = 4)

"""* As We can see in the Histogram Analysis, Residential and Rural Areas are worst affected by Pollution.

## Sectors wise using different Pollutants
"""

grp = df.groupby(["type"]).mean()["so2"].to_frame()
grp.plot.bar(figsize = (20,10))

"""###                                                                                          NO2"""

grp = df.groupby(["type"]).mean()["no2"].to_frame()

grp.plot.bar(figsize = (20,10))

"""## State Wise Analysis for different Pollutants

### SO2 ( Sulfur dioxide )
"""

df[['so2', 'state']].groupby(['state']).median().sort_values("so2", ascending = False).plot.bar(figsize=(20,10))

df[['so2','year','state']].groupby(["year"]).median().sort_values(by='year',ascending=False).plot(figsize=(20,10))

"""### NO2 ( Nitrogen dioxide )"""

df[['no2', 'state']].groupby(['state']).median().sort_values("no2", ascending = False).plot.bar(figsize=(20,10))

df[['no2','year','state']].groupby(["year"]).median().sort_values(by='year',ascending=False).plot(figsize=(20,10))

"""### SPM ( Suspended Particulate Matter )"""

df[['spm', 'state']].groupby(['state']).median().sort_values("spm", ascending = False).plot.bar(figsize=(20,10))

df[['spm','year','state']].groupby(["year"]).median().sort_values(by='year',ascending=False).plot(figsize=(20,10))

"""## State vs Year Analysis for different Pollutants

### SO2
"""

fig, ax = plt.subplots(figsize=(20,10))      
sns.heatmap(df.pivot_table('so2', index='state',columns=['year'],aggfunc='median',margins=True),ax = ax,annot=True, linewidths=.5)

"""### NO2"""

fig, ax = plt.subplots(figsize=(20,10))      
sns.heatmap(df.pivot_table('no2', index='state',columns=['year'],aggfunc='median',margins=True),ax = ax,annot=True, linewidths=.5)

"""### SPM"""

fig, ax = plt.subplots(figsize=(20,10))      
sns.heatmap(df.pivot_table('spm', index='state',columns=['year'],aggfunc='median',margins=True),ax = ax,annot=False, linewidths=.5)

Year wise and States Wise Graph

"""### NO2"""

temp = df.pivot_table('no2', index='year',columns=['state'],aggfunc='median',margins=True).reset_index()
temp = temp.drop("All", axis = 1)
temp = temp.set_index("year")
temp.plot(figsize=(20,10))

"""### SPM"""

temp = df.pivot_table('spm', index='year',columns=['state'],aggfunc='median',margins=True).reset_index()
temp = temp.drop("All", axis = 1)
temp = temp.set_index("year")
temp.plot(figsize=(20,10))

upload = files.upload()

!pip install sentinelsat
!pip install geopandas
!pip install folium

import geopandas as gpd
import folium 
from sentinelsat import SentinelAPI

india = gpd.read_file(r"Indian_States.shp")
india.info()

india.plot()

# Matching the names of states between the two datasets

india["st_nm"] = india["st_nm"].apply(lambda x: x.lower())
india = india.set_index("st_nm")
df["state"] = df["state"].apply(lambda x: x.lower())

"""### Splitting Data in Before and After 2001 for Analysis """

df_before_2001 = df[df["year"] < 2001]
df_before_2001 = df_before_2001.groupby("state").mean()
df_before_2001.head()

df_after_2001 = df[df["year"] >= 2001]
df_after_2001 = df_after_2001.groupby("state").mean()

"""### SO2"""

result = pd.concat([df_before_2001, india], axis=1, sort=False)
result = result [result["geometry"] != None]

from geopandas import GeoDataFrame
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(result, crs=crs, geometry=result ["geometry"])
gdf['centroid'] = gdf.geometry.centroid
fig,ax = plt.subplots(figsize=(20,10))
gdf.plot(column='so2',ax=ax,alpha=0.4,edgecolor='black',cmap='cool', legend=True)
plt.title("Mean So2 before 2001")
plt.axis('off')

for x, y, label in zip(gdf.centroid.x, gdf.centroid.y, gdf.index):
    ax.annotate(label, xy=(x, y), xytext=(3,3), textcoords="offset points",color='gray')

result = pd.concat([df_after_2001, india], axis=1, sort=False)
result = result [result["geometry"] != None]

from geopandas import GeoDataFrame
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(result, crs=crs, geometry=result ["geometry"])
gdf['centroid'] = gdf.geometry.centroid
fig,ax = plt.subplots(figsize=(20,10))
gdf.plot(column='so2',ax=ax,alpha=0.4,edgecolor='black',cmap='cool', legend=True)
plt.title("Mean So2 after 2001")
plt.axis('off')

for x, y, label in zip(gdf.centroid.x, gdf.centroid.y, gdf.index):
    ax.annotate(label, xy=(x, y), xytext=(3,3), textcoords="offset points",color='gray')

"""### NO2"""

result = pd.concat([df_before_2001, india], axis=1, sort=False)
result = result [result["geometry"] != None]

from geopandas import GeoDataFrame
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(result, crs=crs, geometry=result ["geometry"])
gdf['centroid'] = gdf.geometry.centroid
fig,ax = plt.subplots(figsize=(20,10))
gdf.plot(column='no2',ax=ax,alpha=0.4,edgecolor='black',cmap='cool', legend=True)
plt.title("Mean NO2 before 2001")
plt.axis('off')

for x, y, label in zip(gdf.centroid.x, gdf.centroid.y, gdf.index):
    ax.annotate(label, xy=(x, y), xytext=(3,3), textcoords="offset points",color='gray')

result = pd.concat([df_after_2001, india], axis=1, sort=False)
result = result [result["geometry"] != None]


from geopandas import GeoDataFrame
crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(result, crs=crs, geometry=result ["geometry"])
gdf['centroid'] = gdf.geometry.centroid
fig,ax = plt.subplots(figsize=(20,10))
gdf.plot(column='no2',ax=ax,alpha=0.4,edgecolor='black',cmap='cool', legend=True)
plt.title("Mean NO2 after 2001")
plt.axis('off')

for x, y, label in zip(gdf.centroid.x, gdf.centroid.y, gdf.index):
    ax.annotate(label, xy=(x, y), xytext=(3,3), textcoords="offset points",color='gray')

"""# Time Series Analysis for Long-term Air Pollution Levels and changes.

### SO2 ( Sulfur dioxide )
"""

uploaded1 = files.upload()

AQIdf = pd.read_csv("meanAQI.csv")
AQIdf['date'] = pd.to_datetime(AQIdf['date'],format='%Y-%m-%d') # date parse
AQIdf.head()

AQIdf.isna().sum()

AQIdf=AQIdf.set_index('date')
AQIdf.reset_index()
AQIdf.resample(rule="M")
AQIdf.head()

AQIdf.index

AQIdf.plot(figsize = (20,10))

"""Using Exponentially Weighted Moving Average (EWMA) for SO2"""

AQIdf["EWMA_8"] = AQIdf["AQI"].ewm(span=8).mean()

AQIdf.plot(figsize = (25,10))

from statsmodels.tsa.seasonal import seasonal_decompose
result = seasonal_decompose(AQIdf["AQI"], model = "multiplicative",period=8)

fig = result.plot()

"""## Using ARIMA and Seasonal ARIMA Model

"""

import multiprocessing as mp
from multiprocessing import Pool
import time

pool = mp.Pool(mp.cpu_count())

start=time.time()
p = Pool(1)

p.map(ADF_Test, df)
end= time.time()
print(end-start)

df.shape

from statsmodels.tsa.stattools import adfuller
def ADF_Test(df):
    result = adfuller(df)
    print('Augmented Dickey-Fuller Test:')
    labels = ['ADF Test Statistic','p-value','#Lags Used','Number of Observations Used']
    for value,label in zip(result,labels):
        print(label+' : '+str(value) )
    if result[1] <= 0.05:
        print("strong evidence against the null hypothesis, reject the null hypothesis. Data has no unit root and is stationary")
    else:
        print("weak evidence against null hypothesis, time series has a unit root, indicating it is non-stationary ")

import time

df

import random

ADF_Test(AQIdf['AQI'])

AQIdf['AQI_First_Diff']=AQIdf['AQI']-AQIdf['AQI'].shift(8)
AQIdf=AQIdf.dropna()
AQIdf.head()

ADF_Test(AQIdf['AQI_First_Diff'])

AQIdf["AQI_First_Diff"].plot(figsize = (20,10))

from pandas.plotting import autocorrelation_plot
autocorrelation_plot(AQIdf['AQI'])

from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
## p(number of months till shut-off)=3, d(how many times difference)=1, q(exponential decrease till)=2

fig = plt.figure(figsize=(15,10))
ax1 = fig.add_subplot(211)
fig = plot_acf(AQIdf["AQI_First_Diff"],lags=50,ax=ax1)
ax2 = fig.add_subplot(212)
fig = plot_pacf(AQIdf["AQI_First_Diff"],lags=50,ax=ax2)

"""## Using the ARIMA model"""

from statsmodels.tsa.arima.model import ARIMA

AQIdf.index = pd.DatetimeIndex(AQIdf.index).to_period('M')

model=ARIMA(AQIdf['AQI'],order=(3,1,2))
model_fit=model.fit()

print(model_fit.summary())
model_fit.resid.plot()

model_fit.resid.plot(kind='kde')

"""#### Checking with known data """

AQIdf['forecast'] = model_fit.predict(start = 285, end= 338, dynamic= True)  
AQIdf[['AQI','forecast']].plot(figsize=(20,10))

"""* As We can See from above graph ARIMA Model does not give good results, so we  should try Seasonal ARIMA

## Using the Seasonal ARIMA model
"""

import statsmodels.api as sm

seasonal_model = sm.tsa.statespace.SARIMAX(AQIdf["AQI"],order=(3,1,2), seasonal_order=(3,1,2,8))
results = seasonal_model.fit()
print(results.summary())
results.resid.plot()

results.resid.plot(kind='kde')

"""#### Check with known data """

AQIdf['Seasonal_forecast'] = results.predict(start = 284, end= 338, dynamic= True)  
AQIdf[['AQI','Seasonal_forecast']].plot(figsize=(20,10))

"""* Using Seasonal ARIMA, We are getting Pretty Good Results!**

# Forecast
"""

AQIdf.index=AQIdf.index.to_timestamp() # date parse
AQIdf.reset_index()
AQIdf.resample(rule="M")
AQIdf.head()

AQIdf.index.map(lambda t: t.replace(day=1))

from pandas.tseries.offsets import DateOffset
future_dates = [AQIdf.index[-1] + DateOffset(months=x) for x in range(0,63)]
future_AQIdf = pd.DataFrame(index=future_dates[1:],columns=AQIdf.columns)
Combined_AQIdf = pd.concat([AQIdf,future_AQIdf])
Combined_AQIdf.index = pd.DatetimeIndex(Combined_AQIdf.index).to_period('M')
Combined_AQIdf['AQI_Forecast'] = results.predict(start = 338, end = 400, dynamic= True)  
Combined_AQIdf[['AQI', 'AQI_Forecast']].plot(figsize=(20, 10))
