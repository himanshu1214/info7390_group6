from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import pandas as pd
import zipfile
import requests
from io import BytesIO
import logging
import os
import sys
import shutil
import boto3
from configparser import ConfigParser

# check directory    
outdir = './problem2_result'
if not os.path.exists(outdir):
    os.mkdir(outdir)
if os.path.exists(outdir + '/compiled_result.csv'):
    os.remove(outdir + '/compiled_result.csv')
    
# remove all handlers associated with the toot logger object
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
# set up logging to file
logging.basicConfig(filename= outdir + '/missing_data_log.log', filemode='w', level=logging.INFO,
                   format = '%(asctime)s%(levelname)-8s%(message)s')

# opening and parse EDGAR Log File Data Set html
edgarLogUrl = 'https://www.sec.gov/dera/data/edgar-log-file-data-set.html'
edgarLogPage = BeautifulSoup(urlopen(edgarLogUrl),'lxml')
logging.info('Opening and parse EDGAR Log File Data Set html.')

# get log file html of specified year
year = '2010'
try:
    for link in edgarLogPage.findAll('a'):
        if link.text == year:
            edgarLogFiles = BeautifulSoup(urlopen('https://www.sec.gov' + link.get('href')),'lxml')
            logging.info('Get log file html of specified year.')
            break
except Exception:
    loggint.warning('####Error, no ',year,'log file data set found')
    sys.exit('####Error, no ',year,'log file data set found')

# get url of each month
monthList=[]
for i, link in enumerate(edgarLogFiles.findAll('a')):
    if(re.match(r'.*01.zip$',link.text)):
        monthList.insert(12-i,link.get('href'))
logging.info('Get url of each month.')

# define a function, use box plot concept
# lower inner fence: Q1-1.5*IQ
# upper inner fence；Q3+1.5*IQ
# as fences to check anomalies.
# df, the dataframe of orignial dataset
# col_name, the column name to be checked
# return cleaned data (after removing anomalies) in a new dataframe
def remove_outlier(df,col_name):
    q1 = df[col_name].quantile(0.25)
    q3 = df[col_name].quantile(0.75)
    iqr = q3 -q1 #Interquartile range
    fence_low = q1 - 1.5 * iqr
    fence_high = q3 + 1.5 * iqr
    if(iqr == 0):
        df_out = df[df[col_name] == fence_low]
    else:
        df_out = df[(df[col_name] > fence_low) & (df[col_name] < fence_high)]
    return df_out

if len(monthList) != 12:
    loggint.warning('####Error, there is something wrong with each month log file in ',year,'.')
    sys.exit('####Error, there is something wrong with each month log file in ',year,'.')
    
for i in range(0, 12):
    # download zip and parse csv file
    content = requests.get(monthList[i])
    zf = zipfile.ZipFile(BytesIO(content.content))
    for name in zf.namelist():
        if (re.match(r'.*.csv$',name)):
            df = pd.read_csv(zf.open(name)) 
    logging.info('Download ' + year + '-' + str(i + 1) + '-01 zip and parse csv file')

    # fill 'unknown' for missing data in column 'browser'
    df['browser'].fillna('unknown', inplace = True)
    logging.info('Fill \'unknown\' for missing data in column \'browser\'')

    # fill average for missing data in column 'size'
    df['size'].fillna(df['size'].mean(), inplace = True)
    logging.info('Fill average for missing data in column \'size\'')

    # check for anomalies according column 'code' and remove anomalies
    df1 = remove_outlier(df, 'code')
    logging.info('Check for anomalies according column \'code\' and remove anomalies.')
    
    # compute summary metrics
    summary = df1.describe()
    logging.info('Compute summary metrics.')
    
    # compile data and summary into one file
    df1.to_csv(outdir + '/compiled_result.csv', mode = 'a',index = False, header = None)
    summary.to_csv(outdir + '/compiled_result.csv', mode = 'a')
    logging.info('Compile data and summary into one file.')

# zip the tables and log file in result.zip
logging.info('Zip the tables and log file in result.zip')
resultPath = os.path.join(os.getcwd(),'problem2_result')
shutil.make_archive(resultPath,'zip',resultPath)

# use AWS S3
config = ConfigParser()
config.read('config.ini')
aws_key = config.get('aws','aws_key')
aws_secret = config.get('aws','aws_secret')
session = boto3.Session(
    aws_access_key_id = aws_key,
    aws_secret_access_key = aws_secret,)
# before using AWS S3 bucket, make sure configuring aws credentials
try:
    s3 = session.resource('s3')
except Exception:
    logging.warn('######Error, please check aws configuration.')
    sys.exit('######Error, please check aws configuration.')

# create new bucket
bucketName = 'info7390-group6-missing-data'
s3.create_bucket(Bucket = bucketName)

# upload result.zip to S3 bucket
s3.meta.client.upload_file(os.path.join(os.getcwd(),'problem2_result.zip'),bucketName,'problem2_result.zip')

    