#node counter
#average stats

import pandas as pd
import os
import csv
import numpy as np

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya_5000/raw/'

files = ['0_1_ex_MChiSegmented_burned','0_15_ex_MChiSegmented_burned','0_2_ex_MChiSegmented_burned','0_25_ex_MChiSegmented_burned',
          '0_3_ex_MChiSegmented_burned','0_35_ex_MChiSegmented_burned','0_4_ex_MChiSegmented_burned','0_45_ex_MChiSegmented_burned',
          '0_5_ex_MChiSegmented_burned','0_55_ex_MChiSegmented_burned','0_6_ex_MChiSegmented_burned','0_65_ex_MChiSegmented_burned',
          '0_7_ex_MChiSegmented_burned','0_75_ex_MChiSegmented_burned','0_8_ex_MChiSegmented_burned','0_85_ex_MChiSegmented_burned',
          '0_9_ex_MChiSegmented_burned','0_95_ex_MChiSegmented_burned']



          
def getStats(source,column):
    df = pd.read_csv(target+source+'.csv')
    series = df[column]
    list = series.tolist()
    length = len(list)
    median = np.median(list)
    mean = np.mean(list)
    return length,median,mean
    
def writeOutput(name,output_1='',output_2='',output_3=''):       
    name = name.replace('_ex_MChiSegmented_burned','')
    with open(target+'output_node_calculations_precip.csv','a') as csvfile:
        csvWriter = csv.writer(csvfile,delimiter=',')
        csvWriter.writerow((name,output_1,output_2,output_3))
      
  
        
node_lengths = []

with open(target+'output_node_calculations.csv','w') as csvfile:
    csvWriter = csv.writer(csvfile,delimiter=',')
    csvWriter.writerow(('concavity','total_nodes','median','mean'))       

for file in files:
    length,median,mean = getStats(file,'secondary_burned_data')
    print "there are %s nodes in %s"%(length,file)
    node_lengths.append(length)
    writeOutput(file,length,median,mean)
    
print node_lengths
print sum(node_lengths)
writeOutput('total_nodes',sum(node_lengths))
    