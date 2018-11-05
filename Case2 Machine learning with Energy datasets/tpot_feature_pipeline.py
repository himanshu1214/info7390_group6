import numpy as np

from sklearn.kernel_approximation import RBFSampler
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier

# NOTE: Make sure that the class is labeled 'class' in the data file
tpot_data = np.recfromcsv('/Users/YYY/Downloads/energy_consumption_TPOT.csv', delimiter=',', dtype=np.float64)
features = np.delete(tpot_data.view(np.float64).reshape(tpot_data.size, -1), tpot_data.dtype.names.index('class'), axis=1)
training_features, testing_features, training_classes, testing_classes = \
    train_test_split(features, tpot_data['class'], random_state=None)

exported_pipeline = make_pipeline(
    RBFSampler(gamma=0.8500000000000001),
    DecisionTreeClassifier(criterion="entropy", max_depth=3, min_samples_leaf=4, min_samples_split=9)
)

exported_pipeline.fit(training_features, training_classes)
results = exported_pipeline.predict(testing_features)



from tpot import TPOTClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

data01 = pd.read_csv('/Users/YYY/Downloads/energy_consumption.csv')

#give the target variable, the outcome(energy consumption)
y = data01['Appliances']

#give the predictor variables
x = data01.drop(['Appliances','week_of_day','week_status','date'], axis=1)


X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)
print(exported_pipeline.score(testing_features, testing_classes))


X_train.shape, X_test.shape, y_train.shape, y_test.shape

tpot = TPOTClassifier(verbosity=2, max_time_mins=2)
tpot.fit(X_train, y_train)
print(tpot.score(X_test, y_test))