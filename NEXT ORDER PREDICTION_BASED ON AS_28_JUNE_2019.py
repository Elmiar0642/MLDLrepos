import pymysql,pyodbc,math,csv
import numpy as np
import pandas as pd
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split as TTS
from sklearn.linear_model import LinearRegression,Ridge
import matplotlib.pyplot as plt
from matplotlib import style
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
    df=pd.io.sql.read_sql('select brand_id,article_id,ordered_quantity,ticket_id,length_id,finish_id,shade_id from coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS where customer_id IS NOT NULL AND id IS NOT NULL AND ordered_quantity IS NOT NULL AND brand_id IS NOT NULL AND ticket_id IS NOT NULL AND length_id IS NOT NULL AND finish_id IS NOT NULL AND shade_id IS NOT NULL AND article_id IS NOT NULL AND customer_id={};'.format(ids),conn)
    cols=list(df.columns)
    for i in cols:
        if(i=='brand_id'):
            DETAIL[ids].update({i:[]})
        else:
            DETAIL[ids].update({i:0})
    
    empty=[[0] for i in range(1)]
    df2=pd.DataFrame(dict(zip(cols[:-1],empty)))
    df=df.append(df2,sort=True,ignore_index=True)
    for colsi in cols:
        df[colsi].fillna(value=-99999,inplace=True)
    forecast=int(math.ceil(0.01*len(df)))
    for i in range(1,len(cols[1:])+1,1):
        #df.iloc[-1][cols[0:i+1:i]]=df.iloc[-1][cols[0:i+1:i]].shift(-forecast)
        try:
            X=np.array(df.iloc[:-1][cols[0:i+1:i]])
            X=preprocessing.scale(X)
            X_lately=X[-forecast:]
            X=X[:-forecast]
            df.dropna(inplace=True)
            y1=np.array(df.iloc[:-forecast-1][cols[0]])
            y2=np.array(df.iloc[:-forecast-1][cols[i]])        
            X_train,X_test,y1_train,y1_test,y2_train,y2_test=TTS(X,y1,y2,test_size=0.80)
            clf1 = LinearRegression()
            clf1.fit(X_train, y1_train)
            clf2 = LinearRegression()
            clf2.fit(X_train,y2_train)
            confidence1 = clf1.score(X_test, y1_test)
            confidence2 = clf1.score(X_test, y2_test)
            forecast_set1 = list(clf1.predict(X_lately))
            forecast_set2 = list(clf2.predict(X_lately))
            x,y=int(forecast_set1[-1]),int(forecast_set2[-1])
            df1=df.copy(deep=True)
            df1.at[len(df)-1, cols[0]]=x
            DETAIL[ids][cols[0]].append(x)
            df1.at[len(df)-1, cols[i]]=y
            DETAIL[ids][cols[i]]+=y
            #print(ids)
        except ValueError:
            print("the {} is skipped".format(ids))
        '''
        df1[cols[i]]=df1[cols[i]].astype(str)
        df1.set_index('{}'.format(cols[i]),drop=True,inplace=True)
        print(df1.index)
        df1[cols[0]].plot()
        plt.legend(loc=4)
        plt.xlabel('{}'.format(cols[i]))
        plt.ylabel('ORDER QUANTITY')
        plt.show()'''
    #print(ids,"\n\n",DETAIL[ids],"\n\n")
print(DETAIL)

csv_columns = list(DETAIL[customer[0]].keys())
'''
try:
    with open("C:/Users/muthuselvam.m/Desktop/INTERN/ORDERPREDICTION1.txt", 'w+') as csvfile:
        csvfile.write(str(DETAIL))
except IOError:
    print("I/O error") 
'''
try:
    with open('C:/Users/muthuselvam.m/Desktop/INTERN/NEXT BRAND ORDER PREDICTION BASED ON BTLFSA.csv', 'w+') as f:
        for key in DETAIL.keys():
            f.write("%s,%s\n"%(key,DETAIL[key]))            
except IOError:
    print("I/O error") 

print(len(DETAIL))    
