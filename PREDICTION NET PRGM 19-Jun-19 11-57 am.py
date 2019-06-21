######################
#import quandl, math##
#import pickle      ##
######################

import pyodbc
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
i=0

cursor = conn.cursor()
cursor.execute('select customer_id from coats_wba_p4i_hk.dbo.coats_bulk_orders')
customer=[]*0

###########################
##de=pd.DataFrame(cursor)##
##print(de.head())       ##
###########################
input()
for row in cursor:
    i+=1
    customer.append(row[0])
print("size of list:customer\t",len(customer))
cust_id=list(set(customer))
print("size of list:cust_id\t",len(cust_id))
######################################
##btlfsd={}                         ##
##for ids in cust_id:               ##
##    btlfsd.update({ids:[]*0})     ##
######################################
for ids in cust_id:
    cursor_for_b_t_l_f_plus_shade=conn.cursor()
    cursor_for_b_t_l_f_plus_shade.execute('SELECT brand_id,ticket_id,length_id,finish_id,shade_id,ordered_quantity FROM coats_wba_p4i_hk.dbo.coats_bulk_order_lines p LEFT JOIN coats_wba_p4i_hk.dbo.coats_bulk_orders o  ON o.id = p.order_id where o.customer_id={} ORDER BY customer_id'.format(ids))
    df=pd.DataFrame(cursor_for_b_t_l_f_plus_shade)
    print(df.head())
    ################################################################################################################################################
    ##for row in cursor_for_b_t_l_f_plus_shade:                                                                                                   ##
    ##btlfsd[ids].append({'brand_id':row[0],'ticket_id':row[1],'length_id':row[2],'finish_id':row[3],'shade_id':row[4],'ordered_quantity':row[5]})##
    ################################################################################################################################################
        
################################
##print(btlfsd[cust_id[0]][0])##
################################


#PREDICTION_PART
