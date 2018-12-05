import h2o
from h2o.automl import H2OAutoML
import pandas as pd
import numpy as np
from h2o.automl import H2OAutoML

h2o.init()


train = h2o.import_file("/Users/YYY/Desktop/INFO7390/midterm/splitaa.csv")
test = h2o.import_file("/Users/YYY/Desktop/INFO7390/midterm/test_splitaa.csv")

testdata = pd.read_csv('test_splitaa.csv',header=0,na_values=" NaN")
testdata = testdata.replace([np.inf, -np.inf], np.nan)
testdata = testdata.replace([np.inf, -np.inf], np.nan).dropna(subset=['MM_report', 'act_UPB', 'load_age', 'MM_remain','interest_rate','defer_UPB'], how="all")

# Identify predictors and response
x = train.columns
y = "Y"
x.remove(y)
x.remove('delinquency')
x.remove('seq_no')

# For binary classification, response should be a factor
train["Y"] = train["Y"].asfactor()
test["Y"] = test["Y"].asfactor()

# Run AutoML for 20 base models (limited to 1 hour max runtime by default)
aml = H2OAutoML(max_models=20, seed=1)
aml.train(x=x, y=y, training_frame=train)

# View the AutoML Leaderboard
lb = aml.leaderboard
lb.head(rows=lb.nrows)  # Print all rows instead of default (10 rows)



# The leader model is stored here
aml.leader

# If you need to generate predictions on a test set, you can make
# predictions directly on the `"H2OAutoML"` object, or on the leader
# model object directly

preds = aml.predict(test)




