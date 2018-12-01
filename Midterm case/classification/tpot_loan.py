
from tpot import TPOTClassifier

from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd



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
tpot = TPOTClassifier(generations=1, population_size=50, verbosity=2)
tpot.fit(X, y)
#print(tpot.score(X_test, y_test))
tpot.export('tpot_loan_pipeline.py')

