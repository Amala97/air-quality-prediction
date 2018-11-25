import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from matplotlib.pylab import rcParams
from sklearn.linear_model import LinearRegression
linreg=LinearRegression()
from statsmodels.tsa.arima_model import ARIMA
import seaborn as sns
from pandas.plotting import autocorrelation_plot
color = sns.color_palette()
from pandas import datetime
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score

df=pd.read_csv('AirQualityUCI1.csv')

df=df[['Date','Time','CO(GT)','C6H6(GT)','NO2(GT)','PT08.S5(O3)','T','RH','AH']]
v=df['CO(GT)'].mean()
df['CO(GT)'].fillna(v,inplace=True)
v=df['C6H6(GT)'].mean()
df['C6H6(GT)'].fillna(v,inplace=True)
v=df['NO2(GT)'].mean()
df['NO2(GT)'].fillna(v,inplace=True)
v=df['PT08.S5(O3)'].mean()
df['PT08.S5(O3)'].fillna(v,inplace=True)
v=df['T'].mean()
df['T'].fillna(v,inplace=True)
v=df['RH'].mean()
df['RH'].fillna(v,inplace=True)
v=df['AH'].mean()
df['AH'].fillna(v,inplace=True)

df['O3']=df['PT08.S5(O3)']/10
df['AQI(CO)']=df['CO(GT)']*100/10.31
df['AQI(NO2)']=df['NO2(GT)']*100/226.04
df['AQI(O3)']=df['O3']*100/196
df['AQI(C6H6)']=df['C6H6(GT)']*100/5
df['AQI']=(df['AQI(CO)']+df['AQI(NO2)']+df['AQI(O3)']+df['AQI(C6H6)'])/4
def func(row):
    if row['AQI'] <= 50:
        return 'Excellent'
    elif row['AQI'] <= 100:
        return 'Good' 
    elif row['AQI'] <= 150:
        return 'Lightly Polluted' 
    elif row['AQI'] <= 200:
        return 'Moderately Polluted'
    elif row['AQI'] <= 300:
        return 'Heavily Polluted'
    else:
        return 'Severely Polluted'


df['class'] = df.apply(func, axis=1)

af=df[['Date', 'AQI']].drop_duplicates()
df['Date']=pd.to_datetime(df['Date'],infer_datetime_format=True)
indexeddata=df.set_index(['Date'])
#df.head()

AQI_date=df[['Date', 'AQI']].drop_duplicates()
AQI_date_count = AQI_date.groupby(['Date'])['AQI'].aggregate('mean').reset_index().sort_values(by='Date', ascending=0)
date=list(AQI_date_count['Date'])
aqi=list(AQI_date_count['AQI'])
date_aqi = pd.DataFrame({'dates': date, 'aqi':aqi})
date_aqi=date_aqi.set_index(['dates'])
date_aqi['aqi'] = date_aqi['aqi'].map(lambda x: float(x))
date_aqi.head()

date_aqi.plot()
plt.show()
autocorrelation_plot(date_aqi)
plt.show()


sum=0
aqi = date_aqi.values
size = int(len(aqi) * 0.84)
train, test = aqi[0:size], aqi[size:len(aqi)]
history = [x for x in train]
predictions = list()
for t in range(len(test)):
    model = ARIMA(history, order=(2 ,1 ,0))
    model_fit = model.fit(disp=0)
    output = model_fit.forecast()
    yhat = output[0]
    predictions.append(yhat[0])
    obs = test[t]
    history.append(obs)
    print('predicted=%f, expected=%f' % (yhat, obs))
    v=yhat-obs
    sum=sum+v*v
    pred = np.array(predictions)
e=sum/len(test)

error = mean_squared_error(test, predictions)
print('Test MSE: %.3f' % error)
print e


# plot
plt.plot(test,label='Actual')
plt.plot(predictions, color='red',label='ARIMA')
plt.show()


from sklearn.externals import joblib
joblib.dump(model_fit,'model.json')