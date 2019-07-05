#Libraries Used.......................
import numpy as np
import sklearn
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split as TTS
from sklearn.linear_model import LinearRegression,Ridge
'''
We are going to predict the values with the models such as ['LinearRegression','Ridge','Lasso'] and also with the Support Vectors available in sklearn.svm ['linear','poly','rbf','sigmoid']
Developer may just need to use the desired classifier at the place of Line Numbers ['','']
'''
def predict(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER,CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS):

    forecast_point=(len(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER)//2)
    '''
    We set the Forecast point as to seperate Training and Test Datasets
    '''
    CATEGORIES_WITH_AMOUNT=np.array(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.iloc[:-1][CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[0:]])
    '''
    DataFrame before Pre-Processing
    '''
    CATEGORIES_WITH_AMOUNT=preprocessing.scale(CATEGORIES_WITH_AMOUNT)
    '''
    DataFrame after Pre-Processing
    '''
    CATEGORIES_WITH_AMOUNT_TO_BE_TESTED=CATEGORIES_WITH_AMOUNT[-forecast_point:]
    '''
    DataFrame after Pre-Processing from Forecast point to rest, intended for testing purposes
    '''
    CATEGORIES_WITH_AMOUNT_TO_BE_TRAINED=CATEGORIES_WITH_AMOUNT[:-forecast_point]
    '''
    DataFrame after Pre-Processing from start to Forecast point, intended for training purposes
    '''
    CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.dropna(inplace=True)
    '''
    Removing nan values from DataFrame
    '''
    CATEGORIES_WITHOUT_AMOUNT=np.array(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.iloc[:-forecast_point-1][CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[-1]])
    AMOUNT_WITHOUT_CATEGORIES=np.array(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.iloc[:-forecast_point-1][CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[:-1]])
    '''
    The Two other DataFrames for processing against.
    Look into the slices for limits of DataFrames.
    '''
    
    CAT_WITH_AMO_train,CAT_WITH_AMO_test,CAT_WITHOUT_AMO_train,CAT_WITHOUT_AMO_test,AMO_WITHOUT_CAT_train,AMO_WITHOUT_CAT_test = TTS( CATEGORIES_WITH_AMOUNT_TO_BE_TRAINED,CATEGORIES_WITHOUT_AMOUNT,AMOUNT_WITHOUT_CATEGORIES,test_size=0.25 )
    '''
    Training with train_test_split from sklearn.model_selection script.
    '''
    classifier1 = LinearRegression()
    classifier1.fit(CAT_WITH_AMO_train, CAT_WITHOUT_AMO_train)
    '''
    The First Classifier .
    '''
    classifier2 = LinearRegression()
    classifier2.fit(CAT_WITH_AMO_train,AMO_WITHOUT_CAT_train)
    '''
    The Second Classifier .
    '''
    confidence1 = classifier1.score(CAT_WITH_AMO_test, CAT_WITHOUT_AMO_test)
    confidence2 = classifier2.score(CAT_WITH_AMO_test, AMO_WITHOUT_CAT_test)
    #print("confidence score1:",confidence1)
    #print("confidence score2:",confidence2)
    
    '''
    The accuracy scores.
    1.0> accuracy > 0.95 ---> perfect
    0.95> accuracy > 0.65 ---> best
    0.65> accuracy > 0.50 ---> reliable
    0.50> accuracy > =0.0 ---> the model gave a try, not-reliable
    0.0> accuracy > -nan ---> worst
    '''
    forecast_classifier1 = list(classifier1.predict(CATEGORIES_WITH_AMOUNT_TO_BE_TESTED))
    forecast_classifier2 = list(classifier2.predict(CATEGORIES_WITH_AMOUNT_TO_BE_TESTED))
    '''
    Predicting the values.
    '''
    return(forecast_classifier1,forecast_classifier2)

if __name__=="__main__":
    print("DELPHI PREDICTOR SCRIPT")
