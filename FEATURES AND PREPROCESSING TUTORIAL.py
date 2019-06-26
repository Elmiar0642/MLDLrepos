import os,random
import sklearn as skl
from sklearn.preprocessing import OneHotEncoder as OHE
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.preprocessing import MinMaxScaler as MMS
from sklearn.preprocessing import StandardScaler as SS
from sklearn.preprocessing import RobustScaler as RS
from sklearn.preprocessing import MinMaxScaler as MMS
from sklearn.preprocessing import StandardScaler as SS
import pandas as pd
import numpy as np
structure=[]*0
genecode=[]*0
difference=[]*0
A=[i*random.randint(1,5)for i in range(10)]#ord(os.urandom(1))
B=[chr(ord(os.urandom(1))%random.randint(ord('a'),ord('z')))*random.randint(1,5)for i in range(10)]
print(A,B)
for i,j in zip(A[:-1],A[1:]):
    if((j-i)%2==0):
        difference.append(2)
    elif((j-i)%3==0):
        difference.append(3)
    elif((j-i)%4==0):
        difference.append(4)
    elif((j-i)%5==0):
        difference.append(5)
    else:
        difference.append((j-i))
BB=np.array(B)
BBB=BB.reshape(-1,1)
print(BBB)
differences=np.array(difference)
diff=differences.reshape(-1,1)
print(diff)
#FEAT=list(zip(A,difference))
#print(FEAT)
input()
enc1=MMS()
print(enc1.fit(diff))
print(enc1.transform(diff))
enc2=SS()
print(enc2.fit(diff))
print(enc2.transform(diff))
enc3=RS()
print(enc3.fit(diff))
print(enc3.transform(diff))
for x in difference:
    print(np.log(1+x))
enc4=OHE()
print(enc4.fit(BBB))
print(enc4.transform(BBB))
enc5=LE()
print(enc5.fit(BB))
print(enc5.transform(BB))
print(pd.factorize(BB))
#DIFF=np.matrix(difference)
#for a in set(A):
    #print(a,A.count(a))
#    structure.append(A.count(a))
#    genecode.append(A.count(a)%2)
    
#print("{}\n{}\n{}\n{}\n{}\n{}\n".format(A,len(A),set(A),len(set(A)),structure,genecode))
#GENE=np.matrix(genecode).T
#print(GENE,GENE.shape)
#X=GENE @ DIFF
#for i in range(len(X)):
#    print(X[i])
