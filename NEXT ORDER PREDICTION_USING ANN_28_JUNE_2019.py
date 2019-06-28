import pymysql,pyodbc,math,csv
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split as TTS
from sklearn.linear_model import LinearRegression,Ridge
import matplotlib.pyplot as plt
from matplotlib import style
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import EarlyStopping
model = Sequential()

style.use('ggplot')

'''
'''
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ASINMDLB6P5T72;'
                      'Database=coats_wba_p4i_hk;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()

'''
'''
cursor.execute('SELECT DISTINCT customer_id FROM coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS ORDER BY customer_id;')
customer=[]*0
DETAIL={}
for row in cursor:
    customer.append(row[0])
    DETAIL.update({row[0]:{}})
print(len(customer))
'''PREDICTION_PART
'''
for ids in customer:
    '''
    '''
    df=pd.io.sql.read_sql('select ordered_quantity,article_id,brand_id,ticket_id,length_id,finish_id,shade_id from coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS where customer_id IS NOT NULL AND id IS NOT NULL AND ordered_quantity IS NOT NULL AND brand_id IS NOT NULL AND ticket_id IS NOT NULL AND length_id IS NOT NULL AND finish_id IS NOT NULL AND shade_id IS NOT NULL AND article_id IS NOT NULL AND customer_id={};'.format(ids),conn)
    cols=list(df.columns)
    for i in cols:
        if(i=='ordered_quantity'):
            DETAIL[ids].update({i:[]})
        else:
            DETAIL[ids].update({i:0})
    
    train_X = df.iloc[:-1][cols[1:len(cols)]]
    train_y = df[:-1][cols[0]]
    print(train_X.head(),"\n\n",train_y.head())

    model.add(Dense(200, activation='relu', input_shape=(len(cols)-1,)))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(200, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    early_stopping_monitor = EarlyStopping(patience=3)
    model.fit(train_X, train_y, validation_split=0.2, epochs=30, callbacks=[early_stopping_monitor])
    print(model.fit(train_X, train_y, validation_split=0.2, epochs=30, callbacks=[early_stopping_monitor]))
    empty=[[0] for i in range(1)]
    df2=pd.DataFrame(dict(zip(cols,empty)))
    df=df.append(df2,sort=True,ignore_index=True)
    test_y_predictions = model.predict(df.iloc[:-1][cols[:-1]])
    print(test_y_predictions)
    input()
