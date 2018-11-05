from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, \
    load_robot_execution_failures
download_robot_execution_failures()

from sklearn.model_selection import train_test_split
import pandas as pd

data01 = pd.read_csv('/Users/YYY/Downloads/energy_consumption_tsfresh.csv')

#give the target variable, the outcome(energy consumption)
y = data01['Appliances']

#give the predictor variables
x = data01.drop(['Appliances','week_of_day','week_status','date'], axis=1)


X_train, X_test, y_train, y_test = train_test_split(x, y, random_state=0)
timeseries, y = load_robot_execution_failures()

from tsfresh import extract_features
extracted_features = extract_features(x, column_id="index")

from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute

impute(extracted_features)
features_filtered = select_features(extracted_features, y)

from tsfresh import extract_relevant_features

features_filtered_direct = extract_relevant_features(timeseries, y,
                                                     column_id='index')

