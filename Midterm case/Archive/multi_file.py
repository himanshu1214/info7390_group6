import requests
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import re
from lxml import html
import pathlib

import zipfile
from io import BytesIO
import pandas as pd

import numpy as np

import warnings
warnings.filterwarnings('ignore')


from sklearn import metrics
filepath = './zipfile'
#creating the folder for zipfiles
pathlib.Path(filepath).mkdir(parents=True, exist_ok=True) 

#account parameters
username = 'xinglongjia715@gmail.com'
password = 'vKTk_;<J'

# username = input('Please enter your username: ')
# password = input('Please enter your password: ')

#Intializing browser
br = RoboBrowser()
#open website
br.open('https://freddiemac.embs.com/FLoan/secure/login.php?pagename=download')  

#Getting form from browser
form = br.get_form()
form['username'] = username
form['password'] = password
br.submit_form(form)

filename = input('Please enter filename: ')


#accept the form
form1 = br.get_form()
form1['accept'] = 'Yes'
br.submit_form(form1)

#get all the file links and cookie
links = br.find_all('a')
cookie = br.session.cookies.get_dict()
print(cookie)

# set the headers for origination and performance data
header_perf = ['seq_no', 'MM_report', 'act_UPB','delinquency','load_age','MM_remain','repurch','modify',
              'zero_code','zero_date','interest_rate','defer_UPB','DDLPI','MI_recover','sale_proceed','Non_MI_recover',
              'expense','legal_cost','mainten','tax','mix_expense','loss','modify_cost','step_modify','defer_modify','ELTV','Y']

#https://freddiemac.embs.com/FLoan/Data/download2.php
for link in links:
    regex = re.findall('historical_data1_', str(link))
    
        #download zip file
    url = "https://freddiemac.embs.com/FLoan/Data/" + link.get('href')
    year = regex[0].split('_')[4][:6]
    print(year,'|',url)
    content = requests.get(url, cookies = cookie) 
    zf = zipfile.ZipFile(BytesIO(content.content))
        #download txt file, add headers, convert to csv and save in zipfile directory
    for name in zf.namelist():
            
        df = pd.read_csv(zf.open(name), sep='|', header=None)
        df.to_csv(filepath+'/'+year+'.csv',index=False, header=header_perf)
        
import zipfile
with zipfile.ZipFile( '/Users/YYY/Desktop/INFO7390/midterm', 'r') as zip_ref:
    zip_ref.extractall('/Users/YYY/Desktop/INFO7390/midterm')    

w,h = 6,68;
Matrix = [[0 for x in range(w)] for y in range(h)]    
        
import glob
path = "/Users/YYY/Desktop/INFO7390/midterm/*.csv"
for i, fname in enumerate(glob.glob(path)):
    df = pd.read_csv(fname) 
    df['delinquency'] = df['delinquency'].astype(str)           
    for row in df:
        if row['delinquency'] == '0' :
            row['Y'] = 'N'
        else:
            row['Y'] = 'Y'
   
    data1 = pd.read_csv(fname,header=0)
    testdata = pd.read_csv(fname,header=0,na_values=" NaN")
    testdata = testdata.replace([np.inf, -np.inf], np.nan)
    testdata = testdata.replace([np.inf, -np.inf], np.nan).dropna(subset=['MM_report', 'act_UPB', 'load_age', 'MM_remain','interest_rate','defer_UPB'], how="all")
    X = data1.Y.value_counts()

    print(data1.Y.value_counts())

    
 
    Matrix[i][0] = filename
    Matrix[i][1] = data1.Y.value_counts()[1]

    Matrix[i][3] = data1.count()[0]

    import numpy as np

    feature_cols = ['MM_report', 'act_UPB', 'load_age', 'MM_remain','interest_rate','defer_UPB']
    y=data1.Y
    X=data1[feature_cols]
#testdata
    y_test = testdata.Y
    X_test = testdata[feature_cols]
    X = data1[feature_cols]
    Y = data1.Y
    from sklearn.naive_bayes import BernoulliNB
    clf = BernoulliNB(alpha=0.01, fit_prior=True)
    clf.fit(X, Y)

    y_pred = clf.predict(X_test)
    print (y_pred)

    cnf_matrix = metrics.confusion_matrix(y_test, y_pred)
    print(cnf_matrix)

    (cnf_matrix[0][0])

#print(tn, fp, fn, tp )
    Matrix[i][2] = cnf_matrix[1][1] + cnf_matrix[0][1]
    Matrix[i][4] = cnf_matrix[1][1]
    Matrix[i][5] = cnf_matrix[0][1]
    print(Matrix)
