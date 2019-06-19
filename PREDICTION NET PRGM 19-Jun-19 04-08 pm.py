######################
#import quandl, math##
#import pickle      ##
######################

import pyodbc,math
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
    
de=pd.DataFrame(cursor)
print(de)


print("size of list:customer\t",len(customer))
cust_id=list(set(customer))
print("size of list:cust_id\t",len(cust_id))
input()
#PREDICTION_PART
for ids in cust_id:
    cursor_for_b_t_l_f_plus_shade=conn.cursor()
    cursor_for_b_t_l_f_plus_shade.execute('SELECT brand_id,ticket_id,length_id,finish_id,shade_id,ordered_quantity FROM coats_wba_p4i_hk.dbo.coats_bulk_order_lines p LEFT JOIN coats_wba_p4i_hk.dbo.coats_bulk_orders o  ON o.id = p.order_id where o.customer_id={} ORDER BY customer_id'.format(ids))

    df=pd.DataFrame(cursor_for_b_t_l_f_plus_shade)
    print(df.head(),len(df))
    df.extend(()*0)
    for i in range(len(df)+1,len(df)+2):
        df[i].fillna(value=-99999,inplace=True)
        forecast=int(math.ceil(0.01*len(df)))
        #print(df,df[5])
        #input()
        df[5]=df[0:4].shift(-forecast)
        print(df[5])
        input()
        X=np.array(df.drop([5]))
        print(X)
        input()
        X=preprocessing.scale(X)
        print(X)
        input()
        X_lately=A[-forecast:]
        X=X[:-forecast]
        print(X)
        input()
        df.dropna(inplace=True)
        y=np.array(df[5])
        X_train,X_test,y_train,y_test=TTS(X,y,test_size=0.80)
        for k in ['linear','poly','rbf','sigmoid']:
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
        
        
