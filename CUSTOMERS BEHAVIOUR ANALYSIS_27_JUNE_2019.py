from sklearn.preprocessing import OneHotEncoder as OHE
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.preprocessing import MinMaxScaler as MMS
from sklearn.preprocessing import StandardScaler as SS
from sklearn.preprocessing import RobustScaler as RS
from sklearn.preprocessing import MinMaxScaler as MMS
from sklearn.preprocessing import StandardScaler as SS
from sklearn.feature_selection import SelectKBest as SKB
from sklearn.feature_selection import chi2 as CHI2
from sklearn.feature_selection import f_classif as FCF
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
from sqlalchemy import create_engine
import pyodbc,math
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split as TTS
from sklearn.linear_model import LinearRegression,Ridge
import matplotlib.pyplot as plt
from matplotlib import style
import datetime

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=ASINMDLB6P5T72;'
                      'Database=coats_wba_p4i_hk;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('select distinct customer_id from coats_wba_p4i_hk.dbo.coats_bulk_orders')
customer=[]*0
BEHAVIOUR={}
for row in cursor:
    customer.append(row[0])
    BEHAVIOUR.update({row[0]:[]})
print("size of list:customer\t",len(customer))



for ids in customer:
    try:
        df=pd.io.sql.read_sql('SELECT article_id,brand_id,ticket_id,length_id,finish_id,shade_id,ordered_quantity FROM coats_wba_p4i_hk.dbo.coats_bulk_order_lines  p LEFT JOIN coats_wba_p4i_hk.dbo.coats_bulk_orders o  ON o.id = p.order_id WHERE o.customer_id={} AND customer_material_no IS NOT NULL AND article_id IS NOT NULL AND  brand_id IS NOT NULL AND  ticket_id IS NOT NULL AND  length_id IS NOT NULL AND  finish_id IS NOT NULL AND  shade_id IS NOT NULL AND  ordered_quantity IS NOT NULL ORDER BY customer_id;'.format(ids),conn)
        cols=list(df.columns)
        X=df.iloc[:,:len(cols)-1]
        y=df.iloc[:,-1]
        bestfeatures=SKB(score_func=FCF,k=len(cols)-1)
        fit=bestfeatures.fit(X,y)
        dfscores=pd.DataFrame(fit.scores_)
        dfcolumns=pd.DataFrame(X.columns)
        featureScores=pd.concat([dfcolumns,dfscores],axis=1)
        featureScores.columns=['features','orders']
        feat=pd.DataFrame(featureScores.nlargest(10,'orders'))
        feat.set_index("features",drop=True,inplace=True)
        BEHAVIOUR[ids].append(dict(feat))
        #feat.plot(kind='barh')
        #plt.title('Order Placing Behaviour of Customer {}'.format(ids))
        #plt.show()
    except (ValueError):
        print("VALUEERROR")
        

'''
try:
    with open("C:/Users/muthuselvam.m/Desktop/INTERN/CUSTOMERBEHAVIOUR.txt", 'w+') as csvfile:
        csvfile.write(str(BEHAVIOUR))
        
except IOError:
    print("I/O error") 
'''
try:
    with open('C:/Users/muthuselvam.m/Desktop/INTERN/ORDERPREDICTION1.csv', 'w+') as f:
        for key in BEHAVIOUR.keys():
            f.write("%s,%s\n"%(key,BEHAVIOUR[key]))
except IOError:
    print("I/O error") 

print(len(BEHAVIOUR))
