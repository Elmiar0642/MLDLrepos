import quandl, math
import pyodbc
import pickle
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split as TTS
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import datetime

style.use('ggplot')

df = quandl.get("WIKI/GOOGL")
print(df.head())
df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Close'] * 100.0
df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
forecast_col = 'Adj. Close'
df.fillna(value=-99999, inplace=True)
forecast_out = int(math.ceil(0.01 * len(df)))
df['label'] = df[forecast_col].shift(-forecast_out)

X = np.array(df.drop(['label'], 1))
print(X)
input()
X = preprocessing.scale(X)
print(X)
input()
X_lately = X[-forecast_out:]
X = X[:-forecast_out]
print(X,X.shape)
input()

df.dropna(inplace=True)

y = np.array(df['label'])
print(y,y.shape)
input()
X_train, X_test, y_train, y_test = TTS(X, y, test_size=0.80)

for k in ['linear','poly','rbf','sigmoid']:
    clf1 = svm.SVR(kernel=k)
    clf1.fit(X_train, y_train)
    confidence = clf1.score(X_test, y_test)
    print(k,confidence)
    #pickle_in=open('{}.pickle'.format(k),'rb')
    #clf=pickle.load(pickle_in)
    
    forecast_set1 = clf1.predict(X_lately)
    print(forecast_set1,X_lately)
'''
    df['Forecast'] = np.nan

    last_date = df.iloc[-1].name
    last_unix = last_date.timestamp()
    one_day = 86400
    next_unix = last_unix + one_day

    for i in forecast_set1:
        next_date = datetime.datetime.fromtimestamp(next_unix)
        next_unix += 86400
        df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]

    df['Adj. Close'].plot()
    df['Forecast'].plot()
    plt.legend(loc=4)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.show()

clf2 = LinearRegression()
clf2.fit(X_train, y_train)
confidence = clf2.score(X_test, y_test)
print(k,confidence)

forecast_set2 = clf2.predict(X_lately)

df['Forecast'] = np.nan

last_date = df.iloc[-1].name
last_unix = last_date.timestamp()
one_day = 86400
next_unix = last_unix + one_day

for i in forecast_set2:
    next_date = datetime.datetime.fromtimestamp(next_unix)
    next_unix += 86400
    df.loc[next_date] = [np.nan for _ in range(len(df.columns)-1)]+[i]

df['Adj. Close'].plot()
df['Forecast'].plot()
plt.legend(loc=4)
plt.xlabel('Date')
plt.ylabel('Price')
plt.show()
'''
