import requests
from robobrowser import RoboBrowser
from bs4 import BeautifulSoup
import re
from lxml import html
import pathlib
import time
import zipfile
from io import BytesIO
import pandas as pd
import glob
import os
import numpy as np

import warnings
warnings.filterwarnings('ignore')

import missingno as msno
from matplotlib import pyplot as plt
import seaborn as sns

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
    regex = re.findall('historical_data1_'+ filename, str(link))
    
        #download zip file
    url = "https://freddiemac.embs.com/FLoan/Data/" + link.get('href')
    #year = regex[0].split('_')[1][:4]
    #print(year,'|',url)
    content = requests.get(url, cookies = cookie) 
    zf = zipfile.ZipFile(BytesIO(content.content))
        #download txt file, add headers, convert to csv and save in zipfile directory
    for name in zf.namelist():
            
        df = pd.read_csv(zf.open(name), sep='|', header=None)
        df.to_csv(filepath+'/'+filename+'.csv',index=False, header=header_perf)
          
 
df = pd.read_csv(filename+'.csv') 
df['delinquency'] = df['delinquency'].astype(str)           
for row in df:
    if row['delinquency'] == '0' :
        row['Y'] = 'N'
else:
   row['Y'] = 'Y'
   
   
   