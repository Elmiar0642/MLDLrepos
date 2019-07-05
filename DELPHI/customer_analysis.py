#Libraries Used.......................
from customer_id_generator import *
from connection import *
from categorical_data_encoder import *
from predictor import *
import pandas as pd
import numpy as np
import statistics,warnings
from statistics import mode,StatisticsError
'''
The columns/index of the table are, ['customer_id','id','order_id','ordered_quantity','article_id','brand_id','ticket_id','length_id','finish_id','shade_id'].
These are the top 10 features (['customer_material_no','coats_material_no'] are at 11th and 12th position for now ),that could be useful for our predictions.
The data of delivery and ordering dates, can be added in future versions, if needed.
'''
def delphi():
    DETAIL={}
    '''
    We pass the query to the "customer_id_list()" function of the "customer_id_generator.py" script, which would return a list of customer id.
    '''
    for ids in customer_id_list('SELECT distinct customer_id\
                                           FROM coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS\
                                           GROUP BY brand_id , article_id, customer_id\
                                            HAVING COUNT(article_id)>=7 and COUNT(brand_id)>=7 and COUNT(customer_id)>3\
                                             ORDER BY customer_id;'):
        #The 'DETAIL' Dictionary is created for the sake of saving the predicted results and to write them into files
        DETAIL.update({ids:{}})
        #The ' DATAFRAME_DATA_OF_CUSTOMER ' is a Pandas DataFrame object,which reads the sql directly from its in_built ' pd.io.read_sql() '
        DATAFRAME_DATA_OF_CUSTOMER = pd.io.sql.read_sql( ' select article_id,brand_id,ordered_quantity from coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS where ordered_quantity IS NOT NULL AND brand_id IS NOT NULL AND  article_id IS NOT NULL AND customer_id={} ; ' .format( ids ) , make_connection() )
        #The ' COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER ' is a List, which has the indices of the DataFrame
        COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER = list( DATAFRAME_DATA_OF_CUSTOMER.columns )
        #Suppressing the Warnings that could occur while executing
        warnings.simplefilter(action='ignore', category=Warning)
        
        #print( COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER )

        '''
        We have tried to encode each types in features we have selected using Categorical Encoding Technique.
        We have certainly used only One Hot Encoding as the Label Encoding is not so important.
        The One Hot Encoding is done when we pass the DataFrame with each feature selected, and its length into the 'predict()' function of 'predictor.py' script.
        '''
        for column_name in COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[ : -1 ] :

            #Converting the datatype of the selected feature set
            DATAFRAME_DATA_OF_CUSTOMER[column_name] = DATAFRAME_DATA_OF_CUSTOMER[column_name].astype( str )
            
            CATEGORIES = DATAFRAME_DATA_OF_CUSTOMER[ column_name ]

            CATEGORIES_CLASSIFICATION = sorted( set( list( CATEGORIES ) ) )

            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER = pd.DataFrame(encode().fit_transform(DATAFRAME_DATA_OF_CUSTOMER[[column_name]]).toarray(),columns=CATEGORIES_CLASSIFICATION)

            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER[[COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[-1]]]=DATAFRAME_DATA_OF_CUSTOMER[[COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER[-1]]]
            #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.head())

            #updating the customers data in dictionary with a new dictionary containing the feature name and a empty place for its result
            DETAIL[ids].update({column_name:[]})
            #generating dummies to append to the last row to be predicted on the ' CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER '
            empty=[[0] for a in range(len(list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns)))]
            EMPTY_DATAFRAME=pd.DataFrame(dict(zip(list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns),empty)))
            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER=CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.append(EMPTY_DATAFRAME,sort=True,ignore_index=True)
            #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.tail())

            #filling the nan values at the appended row in DataFrame    
            for b in list(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns):
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER[ b ].fillna( value = -99999,inplace = True )

            CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS = list( CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.columns )

            try:
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
                
                #print(mode(FORECAST_OF_COLUMN_NAME_LIST_2))
                try:
                    for e in FORECAST_OF_COLUMN_NAME_LIST:
                        if (e[0]==mode(FORECAST_OF_COLUMN_NAME_LIST_2)):
                            TYPE_ORDERED=e[1]
                    #print("AMOUNT_ORDERED={}\tTYPE_ORDERED={}\n".format(AMOUNT_ORDERED,TYPE_ORDERED))
                    
                except statistics.StatisticsError:
                    print("{}->{} cant be found due to two or more equi probable value/n/nINITIATING SEARCH PROTOCOL...".format(ids,column_name))

                #In-order to prevent any harm to the OG DataFrame we make a copy and print the result from it
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY=CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.copy(deep=True)
                #The nominal is kinda filled at the feature type column that is predicted
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.at[len(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER)-1, CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS.index(TYPE_ORDERED)]]=float(1)
                #The amount predicted to be ordered in that quantity is added to the DataFrame
                CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.at[len(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER)-1, CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[-1]]=int(AMOUNT_ORDERED)
                #print(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.iloc[-1])
                #print("{}\n".format(column_name),CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COPY.tail())
                #The ' DETAIL ' dictionary is filled with the new predicted value of the feature
                DETAIL[ids][column_name].append(TYPE_ORDERED)
                print("{}->{} has been found".format(ids,column_name))
                    

            except ValueError:
                print("{}->{} cant be found due to insufficient features".format(ids,column_name))

    try:
        with open('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI/DELPHI - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv', 'w+') as f:
            for keys in DETAIL.keys():
                f.write("%s,%s\n"%(key,DETAIL[keys]))            
    except IOError:
        print("I/O error")
        
    print ('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI/DELPHI - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv')

    return ('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI/DELPHI - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv')

'''
The same process we do above is followed here, except for , the intended customer's data can be predicted here.
'''
def delphi_on_id(ids):
    DETAIL={}
    DETAIL.update({ids:{}})
    DATAFRAME_DATA_OF_CUSTOMER = pd.io.sql.read_sql( ' select article_id,brand_id,ordered_quantity from coats_wba_p4i_hk.dbo.TABLE_FOR_ANALYTICS where ordered_quantity IS NOT NULL AND brand_id IS NOT NULL AND  article_id IS NOT NULL AND customer_id={} ; ' .format( str(ids) ) , make_connection() )
    COLUMNS_IN_DATAFRAME_DATA_OF_CUSTOMER = list( DATAFRAME_DATA_OF_CUSTOMER.columns )

    warnings.simplefilter(action='ignore', category=Warning)
        
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
            DETAIL[ids][column_name].append(TYPE_ORDERED)
            print("{}->{} has been found".format(ids,column_name))
                    

        except ValueError:
            print("{}->{} cant be found due to insufficient features".format(ids,column_name))

    try:
        with open('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI/DELPHI ON {} - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv'.format(ids), 'w+') as f:
            f.write("%s,%s\n"%(ids,DETAIL[ids]))            
    except IOError:
        print("I/O error")
    print("done!!")
    print ('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI/DELPHI ON {} - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv'.format(ids))

    return ('C:/Users/muthuselvam.m/Desktop/INTERN/july/DELPHI/DELPHI ON {} - ORDER QUANTITY PREDICTION BASEDON ARTICLEID+BRANDID+SHADEID.csv'.format(ids))


if __name__=="__main__":
    print("DELPHI SCRIPT")
