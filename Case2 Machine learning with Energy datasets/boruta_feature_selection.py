import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from boruta import BorutaPy
import numpy as np


# load X and y
# NOTE BorutaPy accepts numpy arrays only, hence the .values attribute
X = pd.read_csv('/Users/YYY/Downloads/energy_consumption_x.csv', index_col=0).values
y = pd.read_csv('/Users/YYY/Downloads/energy_consumption_y.csv', index_col=0).values
y = y.ravel()



# define random forest classifier, with utilising all cores and
# sampling in proportion to y labels
rf = RandomForestClassifier(n_jobs=-1, class_weight='balanced', max_depth=5)

# define Boruta feature selection method
feat_selector = BorutaPy(rf, n_estimators='auto', verbose=2, random_state=1)

# find all relevant features - 5 features should be selected
feat_selector.fit(X,y)

# check selected features - first 5 features are selected
feat_selector.support_

# check ranking of features
feat_selector.ranking_

# call transform() on X to filter it down to selected features
X_filtered = feat_selector.transform(X)


# check selected features
print(feat_selector.support_)
#select the chosen features from our dataframe.
selected = X[:,feat_selector.support_]
print ("")
print ("Selected Feature Matrix Shape")
print (selected.shape)