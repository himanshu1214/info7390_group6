import pathlib
from robobrowser import RoboBrowser
import re
import requests
import zipfile
import pandas as pd
from io import BytesIO
import glob
import os

import warnings
warnings.filterwarnings('ignore')

print(' ---> Start to download orignation and performation data ...')
filepath = './zipfile'
#creating the folder for zipfiles
pathlib.Path(filepath).mkdir(parents=True, exist_ok=True) 

#account parameters
print(' ---> Please input your acount credentials ...')
username = input(' ---> Please enter your username: ')
password = input(' ---> Please enter your password: ')

#Intializing browser
br = RoboBrowser()
#open website
br.open('https://freddiemac.embs.com/FLoan/secure/login.php?pagename=download')  

#Getting form from browser
form = br.get_form()
form['username'] = username
form['password'] = password
br.submit_form(form)

#accept the form
form1 = br.get_form()
form1['accept'] = 'Yes'
br.submit_form(form1)

#get all the file links and cookie
links = br.find_all('a')
cookie = br.session.cookies.get_dict()
print(' ---> Your cookie: ', cookie)

# set the headers for origination and performance data
header_perf = ['seq_no', 'MM_report', 'act_UPB','delinquency','load_age','MM_remain','repurch','modify',
              'zero_code','zero_date','interest_rate','defer_UPB','DDLPI','MI_recover','sale_proceed','Non_MI_recover',
              'expense','legal_cost','mainten','tax','mix_expense','loss','modify_cost','step_modify','defer_modify','ELTV']
header_orig = ['score','pay1_date','homebuyer','maturity_date','MSA','MI%','unit','occupancy','CLTV','DTI_rat','UPB','LTV',
               'interest_rate','channel','PPM','prod_type','prop_state','prop_type','post_code','seq_no','purpose','term',
              'borrowers','seller','service','sup_conform']
print(' ---> Start to download data ...')
for link in links:
    regex = re.findall('sample_\d+.zip', str(link))
    if(regex and (int)(re.findall('\d+', str(regex))[0]) > 2005):
        #download zip file
        url = "https://freddiemac.embs.com/FLoan/Data/" + link.get('href')
        year = regex[0].split('_')[1][:4]
        print(year,'|',url)
        content = requests.get(url, cookies = cookie) 
        zf = zipfile.ZipFile(BytesIO(content.content))
        #download txt file, add headers, convert to csv and save in zipfile directory
        for name in zf.namelist():
            if re.findall('svcg',name):
                df = pd.read_csv(zf.open(name), sep='|', header=None)
                df.to_csv(filepath+'/'+str(year)+'_perf.csv',index=False, header=header_perf)
            if re.findall('orig',name):
                df = pd.read_csv(zf.open(name), sep='|', header=None)
                df.to_csv(filepath+'/'+str(year)+'_orig.csv',index=False, header=header_orig)
print(' ---> Download finished ...')

# file path of the summary of origination and performance data
orig_summary = './summary/orig.csv'
perf_summary = './summary/perf.csv'

# check the summary directory
if not os.path.exists('./summary'):
    os.mkdir('./summary')

for csv_name in glob.glob("./zipfile/*.csv"):
    # aggregate origination summary
    if re.findall('orig', csv_name):
        year = re.findall('\d+',csv_name)[0]
        df = pd.read_csv(csv_name)
        metrix = df.describe().T.dropna()
        metrix['year'] = year
        if not os.path.exists(orig_summary):
            metrix.to_csv(orig_summary)
        else:
            metrix.to_csv(orig_summary,mode='a',header=False)
    # aggregate performance summary
    if re.findall('perf', csv_name):
        year = re.findall('\d+',csv_name)[0]
        df = pd.read_csv(csv_name)
        metrix = df.describe().T.dropna()
        metrix['year'] = year
        if not os.path.exists(perf_summary):
            metrix.to_csv(perf_summary)
        else:
            metrix.to_csv(perf_summary,mode='a',header=False)

# trends over time
summary_orig = pd.read_csv(orig_summary)
summary_orig.rename(columns={'Unnamed: 0':'attribute'}, inplace=True)
summary_orig.groupby(['attribute','year']).mean().to_csv('./summary/orig_year.csv')

summary_perf = pd.read_csv(perf_summary)
summary_perf.rename(columns={'Unnamed: 0':'attribute'}, inplace=True)
summary_perf.groupby(['attribute','year']).mean().to_csv('./summary/perf_year.csv')