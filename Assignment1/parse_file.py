from urllib.request import urlopen
from bs4 import BeautifulSoup
import unicodedata
import csv
import pandas as pd

#company ID
CIK = '51143' 
#document accession number
acc_no = '0000051143-13-000007'

# #company ID
# CIK = '1288776' 
# #document accession number
# acc_no = '0001288776-15-000046'

# replace '_' in accession number
string1 = acc_no.replace('-','')

# generate index url
indexUrl = 'https://www.sec.gov/Archives/edgar/data/' + CIK + '/' + string1 + '/' + acc_no + '-index.html'

def file_from_url(url):
    # get the html document from the url
    response = urlopen(url)
    # import beautiful soup to represent the document as a nested data structure
    page = BeautifulSoup(response,'lxml')
    return page

indexPage = file_from_url(indexUrl)
# extract second row in the table 'tableFile'
table = indexPage.find('table', class_= 'tableFile')
row = table.findAll('tr')
url = 'https://www.sec.gov' + row[1].a.get('href')

# page_10Q = file_from_url(url)
# tables = page_10Q.findAll('table')

df = pd.read_html(url)
df = pd.DataFrame(df[4])
df.to_csv('out.csv',index = False)

# df.to_csv('out.csv',index = False)

# with open('out.csv','w') as f:
#     wr = csv.writer(f)
#     wr.writerow(df[0][:])

# for row in tables[4].findAll('tr'):
#     A=[]
#     for cell in row.findAll('td'):
#         text = cell.get_text()
#         text = text.replace('\xc2','')
#         text = text.replace('\xa0','')
#         A.append(text)
#     print(A)

# with open('out.csv','w') as f:
#     wr = csv.writer(f)
#     for row in tables[4].findAll('tr'):
#         A = []
#         for cell in row.findAll('td'):
#             text = cell.get_text()
#             text = text.replace('\xc2','')
#             text = text.replace('\xa0','')
#             A.append(text)
#         wr.writerow(A)
