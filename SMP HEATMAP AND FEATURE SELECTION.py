import os,random
import sklearn as skl
from sklearn.preprocessing import OneHotEncoder as OHE
from sklearn.preprocessing import LabelEncoder as LE
from sklearn.preprocessing import MinMaxScaler as MMS
from sklearn.preprocessing import StandardScaler as SS
from sklearn.preprocessing import RobustScaler as RS
from sklearn.preprocessing import MinMaxScaler as MMS
from sklearn.preprocessing import StandardScaler as SS
from sklearn.feature_selection import SelectKBest as SKB
from sklearn.feature_selection import chi2 as CHI2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data=pd.read_csv("C:/DATASET.csv")
print(data.head())
X=data.iloc[:,1:21]
y=data.iloc[:,-1]
bestfeatures=SKB(score_func=CHI2,k=10)
fit=bestfeatures.fit(X,y)
dfscores=pd.DataFrame(fit.scores_)
dfcolumns=pd.DataFrame(X.columns)
featureScores=pd.concat([dfcolumns,dfscores],axis=1)
featureScores.columns=['brides','probablity']
print(featureScores.nlargest(10,'probablity'))
input()
feat=pd.DataFrame(featureScores.nlargest(10,'probablity'))
feat.set_index("brides",drop=True,inplace=True)
print(feat,feat.index.values)

input()
feat.plot(kind='barh')
plt.show()
