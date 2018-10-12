from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import pandas as pd
import os
import logging
from configparser import ConfigParser
import shutil
import boto3
import sys
from flask import Flask
import sys
import optparse
import time


app = Flask(__name__)

start = int(round(time.time()))

# check directory    
outdir = './result/cleaned_tables'
if not os.path.exists(outdir):
    os.makedirs(outdir)

# remove all handlers associated with the toot logger object
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
    
# set up logging to file
logging.basicConfig(filename='./result/parse_file_log.log', filemode='w', level=logging.INFO,
                   format = '%(asctime)s%(levelname)-8s%(message)s')

# read parameters CIK and acc_no from config file
config = ConfigParser()
config.read('config.ini')
CIK = config.get('default','CIK')
acc_no = config.get('default','acc_no')
logging.info('Read parameters CIK and acc_no from config file.')

# replace '_' in accession number
string1 = acc_no.replace('-','')

# generate index url and parse index html
indexUrl = 'https://www.sec.gov/Archives/edgar/data/' + CIK + '/' + string1 + '/' + acc_no + '-index.html'
indexPage = BeautifulSoup(urlopen(indexUrl),'lxml')
logging.info('Generate index url and parse index html.')

# find 10-Q url through checking the file type in each table row
url10Q = ''
for row in indexPage.findAll('tr'):
    cell = row.text.split('\n')
    if cell[4] == '10-Q':
        url10Q = 'https://www.sec.gov' + row.a.get('href')
        break
logging.info('Find 10-Q url through checking the file type in each table row.')

# extract all tables from 10-Q url and write the tables data in csv
try:
    df = pd.read_html(url10Q, header = None) 
except Exception:
    logging.warning('#######Error, wrong 10-Q url, fail to get 10-Q file.')
    sys.exit('#######Error, wrong 10-Q url, fail to get 10-Q file.')

# extrac raw tables, clean up the data, and write cleaned tables to cleaned directory
# since first four table has no useful data, start with table[4]
logging.info('Extract raw tables, start to clean up data.')
for i in range(4, len(df)):
    fullname = os.path.join(outdir, 'table' + str(i) + '.csv')    
    df1 = pd.DataFrame(df[i])
    
    logging.info('Start to clean up Table' + str(i))

    # replace the $ sign in the table
    df1 = df1.replace('$',None)
    
    # shift the row left whose firs column is empty
    s1 = df1[df1.columns[0]]
    for i,x in enumerate(s1):
        if pd.isnull(s1[i]) and i > 1:
            df1.iloc[i]=df1.iloc[i].shift(-1)

    # drop the rows and columns which only contains none 
    df1.dropna(how='all',inplace=True)
    df1.dropna(axis=1, how = 'all',inplace=True)

    # replace nan to blank
    df1.fillna('',inplace=True)

    # show the finished table and write to csv
    df1.to_csv(fullname,index=False, header=None) 
    logging.info('Write cleaned table' + str(i) + ' to csv.') 

# zip the tables and log file in result.zip
logging.info('Zip the tables and log file in result.zip')
resultPath = os.path.join(os.getcwd(),'result')
shutil.make_archive(resultPath,'zip',resultPath)

#boto3 connection

access_key = input("please input your access key")

secret_key = input("please input your secert_key")

#endpointurl = 'https://s3.US_EAST_1.amazonaws.com'




session = boto3.Session(
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
)

# use AWS S3
# before using AWS S3 bucket, make sure configuring aws credentials
try:
    s3 = session.resource('s3')
except Exception:
    logging.warning('######Error, please check aws configuration.')
    sys.exit('######Error, please check aws configuration.')

# create new bucket
bucketName = 'info7390-group6-parse-file'
s3.create_bucket(Bucket = bucketName)

# upload result.zip to S3 bucket
s3.meta.client.upload_file(os.path.join(os.getcwd(),'result.zip'),bucketName,'result.zip')

if __name__ == '__main__':
    parser = optparse.OptionParser(usage="python simpleapp.py -p ")
    parser.add_option('-p', '--port', action='store', dest='port', help='The port to listen on.')
    (args, _) = parser.parse_args()
    if args.port == None:
        print ("Missing required argument: -p/--port")
        sys.exit(1)
    app.run(host='0.0.0.0', port=int(args.port), debug=False)