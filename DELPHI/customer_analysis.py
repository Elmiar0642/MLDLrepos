from customer_id_generator import *
from connection import *
from categorical_data_encoder import *
from predictor import *
import pandas as pd
import numpy as np
import statistics,warnings
from statistics import mode,StatisticsError
'''
'''

def delphi():
    DETAIL={}
    for ids in customer_id_list('SELECT DISTINCT customer_id FROM coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS ORDER BY customer_id;'):
        DETAIL.update({ids:{}})
        DATAFRAME_DATA_OF_CUSTOMER = pd.io.sql.read_sql( ' select article_id,brand_id,ordered_quantity from coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS where ordered_quantity IS NOT NULL AND brand_id IS NOT NULL AND  article_id IS NOT NULL AND customer_id={} ; ' .format( ids ) , make_connection() )
        COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER = list( DATAFRAME_DATA_OF_CUSTOMER.columns )

        #print( COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER )

        for column_name in COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[ : -1 ] :
            DATAFRAME_DATA_OF_CUSTOMER[column_name] = DATAFRAME_DATA_OF_CUSTOMER[column_name].astype( str )

                    
            CATEGORIES = DATAFRAME_DATA_OF_CUSTOMER[ column_name ]
            CATEGORIES_CLASSIFICATION = sorted( set( list( CATEGORIES ) ) )
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER = pd.DataFrame(encode().fit_transform(DATAFRAME_DATA_OF_CUSTOMER[[column_name]]).toarray(),columns=CATEGORIES_CLASSIFICATION)
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER[[COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[-1]]]=DATAFRAME_DATA_OF_CUSTOMER[[COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[-1]]]
            #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.head())
            DETAIL[ids].update({column_name:[]})
            empty=[[0] for a in range(len(list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns)))]
            EMPTY_DATAFRAME=pd.DataFrame(dict(zip(list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns),empty)))
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER=CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.append(EMPTY_DATAFRAME,sort=True,ignore_index=True)
            #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.tail())
                
            for b in list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns):
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER[ b ].fillna( value = -99999,inplace = True )
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS = list( CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns )
            
            
            FORECAST_OF_COLUMN_NAME={}
            TYPE,AMOUNT=predict(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER,CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS)
            #print(TYPE,AMOUNT,len(TYPE),len(AMOUNT))
            for c in range(len(AMOUNT)):
                FORECAST_OF_COLUMN_NAME.update({c:( mode(AMOUNT[c]) ,CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[AMOUNT[c].tolist().index(mode(AMOUNT[c]))] ) }) # CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS.index(mode(AMOUNT[c])) ,
            #print(FORECAST_OF_COLUMN_NAME.values(),"\n\n",FORECAST_OF_COLUMN_NAME.keys())
            FORECAST_OF_COLUMN_NAME_LIST=list(FORECAST_OF_COLUMN_NAME.values())
            FORECAST_OF_COLUMN_NAME_LIST_2=[]*0
            for d in FORECAST_OF_COLUMN_NAME_LIST:
                FORECAST_OF_COLUMN_NAME_LIST_2.append(d[0])
            #print(FORECAST_OF_COLUMN_NAME_LIST,"\n\n")
            #print(FORECAST_OF_COLUMN_NAME_LIST_2)
            AMOUNT_ORDERED,TYPE_ORDERED=mode(TYPE),0
                            
                    
            try:
                #print(mode(FORECAST_OF_COLUMN_NAME_LIST_2))
                try:
                    for e in FORECAST_OF_COLUMN_NAME_LIST:
                        if (e[0]==mode(FORECAST_OF_COLUMN_NAME_LIST_2)):
                            TYPE_ORDERED=e[1]
                    #print("AMOUNT_ORDERED={}\tTYPE_ORDERED={}\n".format(AMOUNT_ORDERED,TYPE_ORDERED))
                    
                except statistics.StatisticsError:
                    print("{}->{} cant be found due to two or more equi probable value/n/nINITIATING SEARCH PROTOCOL...".format(ids,column_name))


                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY=CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.copy(deep=True)
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.at[len(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER)-1, CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS.index(TYPE_ORDERED)]]=float(1)
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.at[len(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER)-1, CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[-1]]=int(AMOUNT_ORDERED)
                #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.iloc[-1])
                #print("{}\n".format(column_name),CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.tail())
                DETAIL[ids][column_name].append(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS [z])
                print("{}->{} has been found".format(ids,column_name))
                    

            except ValueError:
                print("{}->{} cant be found due to insufficient features".format(ids,column_name))

        try:
            with open('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv', 'w+') as f:
                for keys in DETAIL.keys():
                    f.write("%s,%s\n"%(key,DETAIL[keys]))            
        except IOError:
            print("I/O error")

    return ('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv')

def delphi_on_id(ids):
    DETAIL={}
    if ids in customer_id_list('SELECT DISTINCT customer_id FROM coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS ORDER BY customer_id;'):
        DETAIL.update({ids:{}})
        DATAFRAME_DATA_OF_CUSTOMER = pd.io.sql.read_sql( ' select article_id,brand_id,ordered_quantity from coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS where ordered_quantity IS NOT NULL AND brand_id IS NOT NULL AND  article_id IS NOT NULL AND customer_id={} ; ' .format( ids ) , make_connection() )
        COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER = list( DATAFRAME_DATA_OF_CUSTOMER.columns )

        #print( COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER )

        for column_name in COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[ : -1 ] :
            DATAFRAME_DATA_OF_CUSTOMER[column_name] = DATAFRAME_DATA_OF_CUSTOMER[column_name].astype( str )

                    
            CATEGORIES = DATAFRAME_DATA_OF_CUSTOMER[ column_name ]
            CATEGORIES_CLASSIFICATION = sorted( set( list( CATEGORIES ) ) )
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER = pd.DataFrame(encode().fit_transform(DATAFRAME_DATA_OF_CUSTOMER[[column_name]]).toarray(),columns=CATEGORIES_CLASSIFICATION)
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER[[COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[-1]]]=DATAFRAME_DATA_OF_CUSTOMER[[COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[-1]]]
            #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.head())
            DETAIL[ids].update({column_name:[]})
            empty=[[0] for a in range(len(list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns)))]
            EMPTY_DATAFRAME=pd.DataFrame(dict(zip(list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns),empty)))
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER=CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.append(EMPTY_DATAFRAME,sort=True,ignore_index=True)
            #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.tail())
                
            for b in list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns):
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER[ b ].fillna( value = -99999,inplace = True )
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS = list( CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns )
            
            
            FORECAST_OF_COLUMN_NAME={}
            TYPE,AMOUNT=predict(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER,CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS)
            #print(TYPE,AMOUNT,len(TYPE),len(AMOUNT))
            for c in range(len(AMOUNT)):
                FORECAST_OF_COLUMN_NAME.update({c:( mode(AMOUNT[c]) ,CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[AMOUNT[c].tolist().index(mode(AMOUNT[c]))] ) }) # CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS.index(mode(AMOUNT[c])) ,
            #print(FORECAST_OF_COLUMN_NAME.values(),"\n\n",FORECAST_OF_COLUMN_NAME.keys())
            FORECAST_OF_COLUMN_NAME_LIST=list(FORECAST_OF_COLUMN_NAME.values())
            FORECAST_OF_COLUMN_NAME_LIST_2=[]*0
            for d in FORECAST_OF_COLUMN_NAME_LIST:
                FORECAST_OF_COLUMN_NAME_LIST_2.append(d[0])
            #print(FORECAST_OF_COLUMN_NAME_LIST,"\n\n")
            #print(FORECAST_OF_COLUMN_NAME_LIST_2)
            AMOUNT_ORDERED,TYPE_ORDERED=mode(TYPE),0
                            
                    
            try:
                #print(mode(FORECAST_OF_COLUMN_NAME_LIST_2))
                try:
                    for e in FORECAST_OF_COLUMN_NAME_LIST:
                        if (e[0]==mode(FORECAST_OF_COLUMN_NAME_LIST_2)):
                            TYPE_ORDERED=e[1]
                    #print("AMOUNT_ORDERED={}\tTYPE_ORDERED={}\n".format(AMOUNT_ORDERED,TYPE_ORDERED))
                    
                except statistics.StatisticsError:
                    print("{}->{} cant be found due to two or more equi probable value/n/nINITIATING SEARCH PROTOCOL...".format(ids,column_name))


                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY=CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.copy(deep=True)
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.at[len(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER)-1, CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS.index(TYPE_ORDERED)]]=float(1)
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.at[len(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER)-1, CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[-1]]=int(AMOUNT_ORDERED)
                #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.iloc[-1])
                #print("{}\n".format(column_name),CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.tail())
                DETAIL[ids][column_name].append(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS [z])
                print("{}->{} has been found".format(ids,column_name))
                    

            except ValueError:
                print("{}->{} cant be found due to insufficient features".format(ids,column_name))

        try:
            with open('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI ON {} - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv'.format(ids), 'w+') as f:
                for keys in DETAIL.keys():
                    f.write("%s,%s\n"%(key,DETAIL[keys]))            
        except IOError:
            print("I/O error")

    return ('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI ON {} - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv'.format(ids))


if __name__=="__main__":
    print("DELPHI SCRIPT")
