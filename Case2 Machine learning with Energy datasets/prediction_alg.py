import numpy as np
import sklearn
from sklearn import datasets
import os
import pandas as pd
import csv
from pandas.core.frame import DataFrame
from builtins import int
from sklearn.metrics import *
from math import sqrt
from sklearn.neural_network.multilayer_perceptron import MLPClassifier


data01 = pd.read_csv('/Users/YYY/Downloads/energy_consumption.csv')

#give the target variable, the outcome(energy consumption)
y = data01['Appliances']

#give the predictor variables
x = data01.drop(['Appliances','week_of_day','week_status','date'], axis=1)

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)

#funtion for mean_absolute_percentage_error
def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

#fit random tree model
#Import Random Forest Model
from sklearn.ensemble import RandomForestClassifier

#Create a Gaussian Classifier
clf=RandomForestClassifier(n_estimators=100)

#Train the model using the training sets y_pred=clf.predict(X_test)
clf.fit(X_train,y_train)
print('Random Forest model:')

train_pred_rf = clf.predict(X_train)
print('train data model estimation')

#Mean absolute error
print('MAE: ')
print(mean_absolute_error(y_train, train_pred_rf))

#ROOT MEAN SUARED ERROR
print('RMS: ')
print(sqrt(mean_squared_error(y_train, train_pred_rf)))

#R-squared score of this model
print('R2: ')
print(r2_score(y_train, train_pred_rf))

#MAPE
print('MAPE: ')
print(mean_absolute_percentage_error(y_train, train_pred_rf))

print('\n')


test_pred_rf=clf.predict(X_test)
print('test data model estimation')
#Mean absolute error
print('MAE: ')
print(mean_absolute_error(y_test, test_pred_rf))

#ROOTMEAN SUARED ERROR
print('RMS: ')
print(sqrt(mean_squared_error(y_test, test_pred_rf)))

#R-squared score of this model
print('R2: ')
print(r2_score(y_test, test_pred_rf))

#MAPE
print('MAPE: ')
print(mean_absolute_percentage_error(y_test, test_pred_rf))
from sklearn import metrics
# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, test_pred_rf))


#Fit a linear regression model
from sklearn import linear_model
lm=linear_model.LinearRegression()
lm.fit (X_train,y_train)
print('Linear regression model:')
train_pred = lm.predict(X_train)
print('train data model estimation')

#Mean absolute error
print('MAE: ')
print(mean_absolute_error(y_train, train_pred))

#ROOTMEAN SUARED ERROR
print('RMS: ')
print(sqrt(mean_squared_error(y_train, train_pred)))

#R-squared score of this model
print('R2: ')
print(r2_score(y_train, train_pred))

#MAPE
print('MAPE: ')
print( mean_absolute_percentage_error(y_train, train_pred))

print('\n')

#do prediction on test dataset
test_pred = lm.predict(X_test)

print('test data model estimation')
#Mean absolute error
print('MAE: ')
print(mean_absolute_error(y_test, test_pred))

#ROOTMEAN SUARED ERROR
print('RMS: ')
print(sqrt(mean_squared_error(y_test, test_pred)))

#R-squared score of this model
print('R2: ')
print(r2_score(y_test, test_pred))

#MAPE
print('MAPE: ')
print(mean_absolute_percentage_error(y_test, test_pred))

#Neural network model
from sklearn.preprocessing import StandardScaler
scaler= StandardScaler()
#fit only to the training data
scaler.fit(X_train)

StandardScaler(copy=True, with_mean=True, with_std=True)

#now apply the transformations to the data:
x_train_nn = scaler.transform(X_train)
x_test_nn = scaler.transform(X_test)

nn = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(5, 2), random_state=1)
print(nn.fit(x_train_nn,y_train))
print('Neural network model:')
nn_pred_train = nn.predict(x_train_nn)
print('train data model estimation')

#Mean absolute error
print('MAE: ')
print(mean_absolute_error(y_train, nn_pred_train))

#ROOTMEAN SUARED ERROR
print('RMS: ')
print(sqrt(mean_squared_error(y_train, nn_pred_train)))

#R-squared score of this model
print('R2: ')
print(r2_score(y_train, nn_pred_train))

#MAPE
print('MAPE: ')
print( mean_absolute_percentage_error(y_train, nn_pred_train))

print('\n')


nn_pred_test = nn.predict(x_test_nn)
print('test data model estimation')
#Mean absolute error
print('MAE: ')
print(mean_absolute_error(y_test, nn_pred_test))

#ROOTMEAN SUARED ERROR
print('RMS: ')
print(sqrt(mean_squared_error(y_test, nn_pred_test)))

#R-squared score of this model
print('R2: ')
print(r2_score(y_test, nn_pred_test))

#MAPE
print('MAPE: ')
print(mean_absolute_percentage_error(y_test, nn_pred_test))











