from sklearn.preprocessing import OneHotEncoder as OHE
import numpy as np
'''
'''
def  encode():
    return(OHE(dtype=np.int,sparse=True,categories="auto"))
    '''
    '''
if __name__=="__main__":
    print("DELPHI CATEGORICAL DATA ENCODER SCRIPT")
    
