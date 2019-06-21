import pymysql
from sqlalchemy import create_engine
import pyodbc,math
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split as TTS
from sklearn.linear_model import LinearRegression,Ridge
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
    print("HEAD:{}\n\nTOTAL LENGTH OF DATAFRAME:{}\n\nTAIL:{}\n\nLABELS:{}\n\n".format(df.head(),len(df),len(df.head()),df.tail(),df.columns))
    cols=list(df.columns)
    empty=[[0] for i in range(1)]
    df2=pd.DataFrame(dict(zip(cols[:-1],empty)))
    df=df.append(df2,sort=True,ignore_index=True)
    print("TOTAL LENGTH OF DATAFRAME:{}\n\nRECENTLY ADDED:{}\n\n".format(len(df),df.iloc[-1]))
    for colsi in cols:
        df[colsi].fillna(value=-99999,inplace=True)
    forecast=int(math.ceil(0.01*len(df)))
    for i in range(1,len(cols[1:])):
        #df.iloc[-1][cols[0:i+1:i]]=df.iloc[-1][cols[0:i+1:i]].shift(-forecast)
        X=np.array(df.iloc[:-1][cols[0:i+1:i]])
        print("FEATURE SET:{}\n\nFEATURE SET'S SHAPE:{}\n\n".format(X,X.shape))
        X=preprocessing.scale(X)
        print("AFTER PRE-PROCESSING(LIMITING EVERY VALUES BETWEEN THE LIMIT OF -1 TO +1)\n\nFEATURE SET:{}\n\nFEATURE SET'S SHAPE:{}\n\n".format(X,X.shape))
        X_lately=X[-forecast:]
        print("FORCAST TESTING SET:{}\n\n".format(X_lately[-1]))
        X=X[:-forecast]
        print("FEATURE TRAINING SET:{}\n\nFEATURE TRAINING SET'S SHAPE:{}\n\n".format(X,X.shape))
        df.dropna(inplace=True)
        y1=np.array(df.iloc[:-forecast-1][cols[0]])
        y2=np.array(df.iloc[:-forecast-1][cols[i]])
        print(y1,y1.shape,y2,y2.shape)
        input()
        X_train,X_test,y1_train,y1_test,y2_train,y2_test=TTS(X,y1,y2,test_size=0.80)
        clf1 = LinearRegression()
        clf1.fit(X_train, y1_train)
        clf2 = LinearRegression()
        clf2.fit(X_train,y2_train)
        confidence1 = clf1.score(X_test, y1_test)
        confidence2 = clf1.score(X_test, y2_test)
        print("{} PREDICTION BASED ON {}\n\nCONFIDENCE1={}\n\nCONFIDENCE2={}".format("LINEAR REGGRESSION",cols[0:i+1:i],confidence1,confidence2))             
        forecast_set1 = list(clf1.predict(X_lately))
        forecast_set2 = list(clf2.predict(X_lately))
        print(forecast_set1,"\n\n",forecast_set2)
        input()
        x,y=int(forecast_set1[-1]),int(forecast_set2[-1])
        print(df.iloc[-1])
        df1=df.copy(deep=True)
        print(df1[cols[0]].replace(to_replace = 0, value = x,inplace=True) )
        print(df1.replace(to_replace = -99999, value = y,inplace=True) )
        print(df1.iloc[-1])
        input()
        X_AXIS,y_axis=list(df1.iloc[0:][cols[i]]),list(set(df1[[cols[0]]]))
        df1[[cols[0]]].plot()
        df1[[cols[i]]].plot()
        plt.legend(loc=4)
        plt.xlabel('INDEX')
        plt.ylabel('ORDER QUANTITY/BRAND ID')
        plt.show()
        input()
        plt.plot(df1[[cols[0]]],label="ORDER QUANTITY")
        plt.plot(df1[[cols[i]]],label="BRAND ID")
        plt.legend(loc=4)
        plt.xlabel('ORDER QUANTITY/BRAND ID')
        plt.ylabel('INDEX')
        plt.show()
            
        
