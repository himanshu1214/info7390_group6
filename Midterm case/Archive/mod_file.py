import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt 

import csv

with open('splitaa.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('splitaa.csv', 'w') as out_file:
        writer = csv.writer(out_file)
    
        writer.writerows(lines)
        
with open('splitab.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('splitab.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('seq_no', 'MM_report', 'act_UPB','delinquency','load_age','MM_remain','repurch','modify',
              'zero_code','zero_date','interest_rate','defer_UPB','DDLPI','MI_recover','sale_proceed','Non_MI_recover',
              'expense','legal_cost','mainten','tax','mix_expense','loss','modify_cost','step_modify','defer_modify','ELTV','Y'))
        writer.writerows(lines)
with open('splitac.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('splitac.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('seq_no', 'MM_report', 'act_UPB','delinquency','load_age','MM_remain','repurch','modify',
              'zero_code','zero_date','interest_rate','defer_UPB','DDLPI','MI_recover','sale_proceed','Non_MI_recover',
              'expense','legal_cost','mainten','tax','mix_expense','loss','modify_cost','step_modify','defer_modify','ELTV','Y'))
        writer.writerows(lines)
        
 
with open('test_splitaa.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(",") for line in stripped if line)
    with open('test_splitaa.csv', 'w') as out_file:
        writer = csv.writer(out_file)
    
        writer.writerows(lines)       

