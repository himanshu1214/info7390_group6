import h2o
from h2o.automl import H2OAutoML

h2o.init()

# Import a sample binary outcome train/test set into H2O
train = h2o.import_file("https://s3.amazonaws.com/erin-data/higgs/higgs_train_10k.csv")
test = h2o.import_file("https://s3.amazonaws.com/erin-data/higgs/higgs_test_5k.csv")

# Identify predictors and response
x = train.columns
y = "response"
x.remove(y)

# For binary classification, response should be a factor
train[y] = train[y].asfactor()
test[y] = test[y].asfactor()

# Run AutoML for 20 base models (limited to 1 hour max runtime by default)
aml = H2OAutoML(max_models=20, seed=1)
aml.train(x=x, y=y, training_frame=train)

# View the AutoML Leaderboard
lb = aml.leaderboard
lb.head(rows=lb.nrows)  # Print all rows instead of default (10 rows)

# model_id                                                    auc    logloss    mean_per_class_error      rmse       mse
# -----------------------------------------------------  --------  ---------  ----------------------  --------  --------
# StackedEnsemble_AllModels_AutoML_20181022_213938       0.787952   0.553121                0.326584  0.432972  0.187465
# StackedEnsemble_BestOfFamily_AutoML_20181022_213938    0.786665   0.554442                0.326707  0.433626  0.188031
# XGBoost_grid_1_AutoML_20181022_213938_model_3          0.782557   0.559853                0.332668  0.435851  0.189966
# XGBoost_1_AutoML_20181022_213938                       0.781066   0.560126                0.331227  0.436328  0.190382
# XGBoost_3_AutoML_20181022_213938                       0.780847   0.561162                0.324008  0.436482  0.190516
# XGBoost_grid_1_AutoML_20181022_213938_model_4          0.780624   0.560661                0.322992  0.43656   0.190585
# XGBoost_2_AutoML_20181022_213938                       0.780052   0.561374                0.336129  0.436646  0.19066
# GBM_5_AutoML_20181022_213938                           0.77983    0.561488                0.326767  0.436813  0.190805
# GBM_1_AutoML_20181022_213938                           0.777228   0.562825                0.340895  0.437694  0.191576
# GBM_2_AutoML_20181022_213938                           0.775152   0.564562                0.335697  0.438741  0.192494
# GBM_3_AutoML_20181022_213938                           0.771208   0.568808                0.341364  0.440754  0.194264
# GBM_4_AutoML_20181022_213938                           0.77009    0.571766                0.361497  0.441974  0.195341
# GBM_grid_1_AutoML_20181022_213938_model_1              0.766161   0.575801                0.339059  0.444005  0.19714
# XGBoost_grid_1_AutoML_20181022_213938_model_2          0.765121   0.586489                0.352089  0.447558  0.200309
# GBM_grid_1_AutoML_20181022_213938_model_2              0.749166   0.942444                0.362949  0.49916   0.24916
# XGBoost_grid_1_AutoML_20181022_213938_model_1          0.733602   0.596321                0.380896  0.454024  0.206137
# XRT_1_AutoML_20181022_213938                           0.732968   0.603421                0.365632  0.456439  0.208337
# DRF_1_AutoML_20181022_213938                           0.732963   0.607233                0.367129  0.456443  0.208341
# DeepLearning_grid_1_AutoML_20181022_213938_model_2     0.729144   0.612294                0.37187   0.460569  0.212124
# GLM_grid_1_AutoML_20181022_213938_model_1              0.685316   0.636626                0.393665  0.47177   0.222567
# DeepLearning_1_AutoML_20181022_213938                  0.684702   0.643051                0.40708   0.474047  0.224721
# DeepLearning_grid_1_AutoML_20181022_213938_model_1     0.67466    0.694187                0.407733  0.488307  0.238443
#
# [22 rows x 6 columns]


# The leader model is stored here
aml.leader

# If you need to generate predictions on a test set, you can make
# predictions directly on the `"H2OAutoML"` object, or on the leader
# model object directly

preds = aml.predict(test)

# or:
preds = aml.leader.predict(test)
