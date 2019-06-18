#import quandl, math
import pyodbc
#import pickle
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split as TTS
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib import style
import datetime

style.use('ggplot')
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ASINMDLB6P5T72;'
                      'Database=coats_wba_p4i_hk;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()
cursor.execute('select customer_id from coats_wba_p4i_hk.dbo.coats_bulk_orders')
customer=[]*0
for row in cursor:
    customer.append(row[0])
print("size of list:customer\t",len(customer))
cust_id=list(set(customer))
print("size of list:cust_id\t",len(cust_id))

input()

id_dict,order_id_dict={},{}

for keys in cust_id:
    id_dict.update({keys:[]*0})
print(len(id_dict))
for ids in cust_id:
    #print(ids)
    cursor2 = conn.cursor()
    cursor2.execute('select id from coats_wba_p4i_hk.dbo.coats_bulk_orders where(customer_id = {})'.format(ids))
    for row in cursor2:
        id_dict[ids]+=[row[0]]
        order_id_dict.update({row[0]:[]*0})
        
    #print("size of list in key customer id {} of id_dict:{}\t".format((ids),len(id_dict[ids])),id_dict[ids][0])
input()
for ids in cust_id:
    for aiid in id_dict[ids]:
        cursor3 = conn.cursor()
        df = cursor3.execute('select * from coats_wba_p4i_hk.dbo.coats_bulk_order_lines where(order_id = {})'.format(aiid))
        print(df)#.head())
        #for row in cursor3:
        #    order_id_dict[aiid]+=[row[0]]
        #print("size of list in key auto-incremented id {} of order_id_dict:{}\t".format((aiid),len(order_id_dict[aiid])),order_id_dict[aiid][0])
'''
        cursor3 = conn.cursor()
        cursor3.execute('select * from coats_wba_p4i_hk.dbo.coats_bulk_order_lines where(order_id = {})'.format(row[0]))
        for row1 in cursor3:
            order_id_dict[row[0]].append(row1)
        print("size of list in key [{}] of order_id_dict:\t".format(row[0]),len(id_dict[row[0]]))
'''
#print(customer)

#df = quandl.get("WIKI/GOOGL")
#print(df.head())
#df = df[['Adj. Open',  'Adj. High',  'Adj. Low',  'Adj. Close', 'Adj. Volume']]
#df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Close'] * 100.0
#df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100.0

#df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
#forecast_col = 'Adj. Close'
#df.fillna(value=-99999, inplace=True)
#forecast_out = int(math.ceil(0.01 * len(df)))
#df['label'] = df[forecast_col].shift(-forecast_out)

#X = np.array(df.drop(['label'], 1))
#X = preprocessing.scale(X)
#X_lately = X[-forecast_out:]
#X = X[:-forecast_out]

#df.dropna(inplace=True)

#y = np.array(df['label'])

#X_train, X_test, y_train, y_test = TTS(X, y, test_size=0.80)

'''for k in ['linear','poly','rbf','sigmoid']:
    clf1 = svm.SVR(kernel=k)
    clf1.fit(X_train, y_train)
    confidence = clf1.score(X_test, y_test)
    print(k,confidence)
    #pickle_in=open('{}.pickle'.format(k),'rb')
    #clf=pickle.load(pickle_in)
    
    forecast_set1 = clf1.predict(X_lately)

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
