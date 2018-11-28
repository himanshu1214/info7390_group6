import os
import pandas as pd
import csv
from pandas.core.frame import DataFrame
from builtins import int

#get all types from the data set
data = pd.read_csv("/Users/YYY/Downloads/all/train.csv")
type = data['species']

typeCaptured = csv.reader(type,delimiter=',',skipinitialspace=True,)
print(typeCaptured)

categ = []
for row in typeCaptured:
    
    #if row[0] not in categ:
        categ.append(row[0])
        
print(categ[1])

dataarray = []
gcloudpath = 'gs://firsttry-220818-vcm/images'
for i in range(len(categ)):
    dataarray.append(('gs://firsttry-220818-vcm/images' + '/' + str(i+1) + '.jpg' , categ[i]))
    
print(dataarray[0])

dataframe = pd.DataFrame(dataarray)
dataframe.to_csv('all_data.csv',index=False, header=False)
