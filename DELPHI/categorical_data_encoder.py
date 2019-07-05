#Libraries Used.......................
from sklearn.preprocessing import OneHotEncoder as OHE
import numpy as np

'''
The 'OneHotEncoder' is used here to encode the categorical data.
The sparse matrix is produced and returned.
The nominals are binaries, and thus on attempting to reproduce the original DataFrame would be easier, by just dot producting it with the OG DataFrame.
This is because , on encoded DataFrame only one value can be present for each row according to the column value.
'''
def  encode():
    return(OHE(dtype=np.int,sparse=True,categories="auto"))
    
if __name__=="__main__":
    print("DELPHI CATEGORICAL DATA ENCODER SCRIPT")
    
