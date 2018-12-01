import pandas as pd
import numpy as np
from sklearn import preprocessing
import csv

data1 = pd.read_csv('splitaa.csv',header=0)

testdata = pd.read_csv('test_splitaa.csv',header=0,na_values=" NaN")
testdata = testdata.replace([np.inf, -np.inf], np.nan)
testdata = testdata.replace([np.inf, -np.inf], np.nan).dropna(subset=['MM_report', 'act_UPB', 'load_age', 'MM_remain','interest_rate','defer_UPB'], how="all")



print(data1.shape)
print(list(data1.columns))

feature_cols = ['MM_report', 'act_UPB', 'load_age', 'MM_remain','interest_rate','defer_UPB']
y=data1.Y
X=data1[feature_cols]
#testdata
y_test = testdata.Y
X_test = testdata[feature_cols]

# import the class
from sklearn.linear_model import LogisticRegression

# instantiate the model (using the default parameters)
logreg = LogisticRegression()

# fit the model with data
logreg.fit(X,y)

#
y_pred=logreg.predict(X_test)

print(y_pred)

#compute confusion matrix
from sklearn import metrics
cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
print(cnf_matrix)

#compute roc cureve
import matplotlib.pyplot as plt
y_pred_proba = logreg.predict_proba(X_test)[::,1]
y_binary = np.where(y=='N',0,1)
fpr, tpr, _ = metrics.roc_curve(y_binary,  y_pred_proba)
auc = metrics.roc_auc_score(y_binary, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()

























