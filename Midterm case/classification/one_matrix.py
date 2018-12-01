import pandas as pd
import numpy as np
from sklearn import preprocessing
import csv
from sklearn import metrics


filename = 'Q12005'
data1 = pd.read_csv('splitaa.csv',header=0)
testdata = pd.read_csv('test_splitaa.csv',header=0,na_values=" NaN")
testdata = testdata.replace([np.inf, -np.inf], np.nan)
testdata = testdata.replace([np.inf, -np.inf], np.nan).dropna(subset=['MM_report', 'act_UPB', 'load_age', 'MM_remain','interest_rate','defer_UPB'], how="all")
X = data1.Y.value_counts()

print(data1.Y.value_counts())

w,h = 5,1;
Matrix = [[0 for x in range(w)] for y in range(h)]
 
Matrix[0][0] = filename
Matrix[0][1] = data1.Y.value_counts()[1]
Matrix[0][2] = data1.count()[0]

import numpy as np

feature_cols = ['MM_report', 'act_UPB', 'load_age', 'MM_remain','interest_rate','defer_UPB']
y=data1.Y
X=data1[feature_cols]
#testdata
y_test = testdata.Y
X_test = testdata[feature_cols]
X = data1[feature_cols]
Y = data1.Y
from sklearn.naive_bayes import BernoulliNB
clf = BernoulliNB()
clf.fit(X, Y)
BernoulliNB(alpha=1.0, binarize=0.0, fit_prior=True)
y_pred = clf.predict(X_test)
print (y_pred)

tn, fp, fn, tp  = metrics.confusion_matrix(y_test, y_pred)
print(tn, fp, fn, tp )

Matrix[0][3] = tp
Matrix[0][4] = fp
print(Matrix)



