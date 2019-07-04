import numpy as np
import sklearn
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split as TTS
from sklearn.linear_model import LinearRegression,Ridge
'''
'''
def predict(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER,CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS):

    forecast_point=(len(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER)//2)
    '''
    '''
    CATEGORIES_WITH_AMOUNT=np.array(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.iloc[:-1][CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[0:]])
    '''
    '''
    CATEGORIES_WITH_AMOUNT=preprocessing.scale(CATEGORIES_WITH_AMOUNT)
    '''
    '''
    CATEGORIES_WITH_AMOUNT_TO_BE_TESTED=CATEGORIES_WITH_AMOUNT[-forecast_point:]
    '''
    '''
    CATEGORIES_WITH_AMOUNT_TO_BE_TRAINED=CATEGORIES_WITH_AMOUNT[:-forecast_point]
    '''
    '''
    CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.dropna(inplace=True)
    '''
    '''
    CATEGORIES_WITHOUT_AMOUNT=np.array(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.iloc[:-forecast_point-1][CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[-1]])
    AMOUNT_WITHOUT_CATEGORIES=np.array(CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER.iloc[:-forecast_point-1][CLASSIFIED_DATAFRAME_DATA_OF_CUSTOMER_COLUMNS[:-1]])
    '''
    '''
    
    CAT_WITH_AMO_train,CAT_WITH_AMO_test,CAT_WITHOUT_AMO_train,CAT_WITHOUT_AMO_test,AMO_WITHOUT_CAT_train,AMO_WITHOUT_CAT_test = TTS( CATEGORIES_WITH_AMOUNT_TO_BE_TRAINED,CATEGORIES_WITHOUT_AMOUNT,AMOUNT_WITHOUT_CATEGORIES,test_size=0.25 )
    '''
    '''
    classifier1 = LinearRegression()
    classifier1.fit(CAT_WITH_AMO_train, CAT_WITHOUT_AMO_train)
    '''
    '''
    classifier2 = LinearRegression()
    classifier2.fit(CAT_WITH_AMO_train,AMO_WITHOUT_CAT_train)
    '''
    '''
    confidence1 = classifier1.score(CAT_WITH_AMO_test, CAT_WITHOUT_AMO_test)
    confidence2 = classifier2.score(CAT_WITH_AMO_test, AMO_WITHOUT_CAT_test)
    #print("confidence score1:",confidence1)
    #print("confidence score2:",confidence2)
    
    '''
    '''
    forecast_classifier1 = list(classifier1.predict(CATEGORIES_WITH_AMOUNT_TO_BE_TESTED))
    forecast_classifier2 = list(classifier2.predict(CATEGORIES_WITH_AMOUNT_TO_BE_TESTED))
    '''
    '''
    return(forecast_classifier1,forecast_classifier2)

if __name__=="__main__":
    print("DELPHI PREDICTOR SCRIPT")
