import pymysql
from sqlalchemy import create_engine
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
    
print("size of list:customer\t",len(customer))
cust_id=list(set(customer))
print("size of list:cust_id\t",len(cust_id))
input()

#PREDICTION_PART

for ids in cust_id:
    df=pd.io.sql.read_sql('SELECT ordered_quantity,brand_id,ticket_id,length_id,finish_id,shade_id FROM coats_wba_p4i_hk.dbo.coats_bulk_order_lines p LEFT JOIN coats_wba_p4i_hk.dbo.coats_bulk_orders o  ON o.id = p.order_id where o.customer_id={} ORDER BY customer_id'.format(ids),conn)
    print(df.head(),len(df),len(df.head()),df.iloc[-1:-5],df.columns)
    cols=list(df.columns)
    empty=[[0] for i in range(1)]
    for k in zip(cols[:-1],empty):
        print(k)
    input()
    print(dict(zip(cols[:-1],empty)))
    input()
    df2=pd.DataFrame(dict(zip(cols[:-1],empty)))
    print(df2.head())
    print(df2.head())
    input()
    df=df.append(df2,sort=True,ignore_index=True)
    print(len(df),df.iloc[-1])
    input()
    #df=dict(df)
    for colsi in cols:
        df[colsi].fillna(value=-99999,inplace=True)
    forecast=int(math.ceil(0.01*len(df)))
    print(df.iloc[-1],forecast)
    input()
    df.iloc[-1]=df.iloc[-1].shift(-forecast)
    input()
    for i in range(1,len(cols[1:])):
        X=np.array(df.iloc[:-1][cols[0:i+1:i]]).T
        print(X,X.shape)
        input()
        X=preprocessing.scale(X)
        print(X,X.shape)
        input()
        X_lately=X[-forecast:]
        #X=X[:-forecast]
        print(X,X.shape)
        input()
        df.dropna(inplace=True)
        y=np.array(df.iloc[-1][cols[0:i+1:i]])
        print(y,y.shape)
        input()
        X_train,X_test,y_train,y_test=TTS(X,y,test_size=0.50)
        for k in ['linear','poly','rbf','sigmoid']:
            clf1 = svm.SVR(kernel=k)
            clf1.fit(X_train, y_train)
            confidence = clf1.score(X_test, y_test)
            print("{} PREDICTION BASED ON {}\n\nCONFIDENCE={}".format(k,cols[0:i+1:i],confidence))
                
            forecast_set1 = clf1.predict(X_lately)

            #df.iloc[-1] = np.nan

            last = df.iloc[-1][[cols[0]]]
            #df = df.append(df2)

            for j in forecast_set1:
                df.iloc[-1] = [np.nan for _ in range(len(df.columns)-1)]+[j]

            x_axis,y_axis=list(set(df[[cols[i]]])),list(set(df[[cols[0]]]))
            input()
            last.plot()
            input()
            df[:-1][[cols[0]]].plot()
            tick_marks = np.arange(len(x_axis))
            plt.xticks(tick_marks, x_axis)
            #plt.yticks(tick_marks, target_names)
            plt.legend(loc=4)
            plt.xlabel('TYPES')
            plt.ylabel('Orders')
            plt.show()
            
        
