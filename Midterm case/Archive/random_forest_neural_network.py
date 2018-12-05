import pandas as pd
import numpy as np
from sklearn import preprocessing
import csv
from sklearn.metrics import *
from math import sqrt
from sklearn.neural_network.multilayer_perceptron import MLPClassifier

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

y_binary = np.where(y=='N',0,1)

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

#fit random tree model
#Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier

#Create a Gaussian Classifier
clf=RandomForestClassifier(n_estimators=100)

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X,y)
print('Random Forest model:')


test_pred_rf=clf.predict(X_test)

print(test_pred_rf)

#compute confusion matrix
from sklearn import metrics
cnf_matrix = metrics.confusion_matrix(y_test, test_pred_rf)
print(cnf_matrix)

#compute roc cureve
import matplotlib.pyplot as plt
y_pred_proba = clf.predict_proba(X_test)[::,1]
y_binary = np.where(y=='N',0,1)
fpr, tpr, _ = metrics.roc_curve(y_binary,  y_pred_proba)
auc = metrics.roc_auc_score(y_binary, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()

#Neural network model
print("Neural network")

#Neural network model
from sklearn.preprocessing import StandardScaler
scaler= StandardScaler()
#fit only to the training data
scaler.fit(X)

StandardScaler(copy=True, with_mean=True, with_std=True)

#now apply the transformations to the data:
x_train_nn = scaler.transform(X)
x_test_nn = scaler.transform(X_test)

nn = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)
print(nn.fit(x_train_nn,y))
print('Neural network model:')
nn_pred_test = nn.predict(x_test_nn)
#compute confusion matrix
from sklearn import metrics
#pred_obj = np.where(predictions==predictions[0],'N','Y')
#print(pred_obj)

cnf_matrix = metrics.confusion_matrix(y_test, nn_pred_test)
print(cnf_matrix)

#compute roc cureve
import matplotlib.pyplot as plt
y_pred_proba =nn.predict_proba(X_test)[::,1]
y_binary = np.where(y=='N',0,1)
fpr, tpr, _ = metrics.roc_curve(y_binary,  y_pred_proba)
auc = metrics.roc_auc_score(y_binary, y_pred_proba)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.show()













