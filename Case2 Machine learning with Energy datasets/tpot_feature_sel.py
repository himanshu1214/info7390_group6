from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

data01 = pd.read_csv('/Users/YYY/Downloads/energy_consumption.csv')

#give the target variable, the outcome(energy consumption)
y = data01['Appliances']

#give the predictor variables
x = data01.drop(['Appliances','week_of_day','week_status','date'], axis=1)


X_train, X_test, y_train, y_test = train_test_split(x, y, train_size=0.75, test_size=0.25)


X_train.shape, X_test.shape, y_train.shape, y_test.shape
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

tpot = TPOTClassifier(generations=5,verbosity=2)


tpot = TPOTClassifier(verbosity=2, max_time_mins=50)
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))

tpot.export('tpot_feature_pipeline.py')