import pandas as pd
import os
target_a = 'C:\\output\\'
target_b = 'C:\\output2\\'
target_c = 'R:\\LSDTopoTools\\Topographic_projects\\full_himalaya\\'

output = 'C:\\pandas_in\\full_himalaya\\'
paths = ['0_1_MChiSegmented_burned.csv','0_2_MChiSegmented_burned.csv','0_3_MChiSegmented_burned.csv','0_4_MChiSegmented_burned.csv','0_5_MChiSegmented_burned.csv','0_6_MChiSegmented_burned.csv','0_7_MChiSegmented_burned.csv','0_8_MChiSegmented_burned.csv','0_9_MChiSegmented_burned.csv','0_15_MChiSegmented_burned.csv','0_25_MChiSegmented_burned.csv','0_35_MChiSegmented_burned.csv','0_45_MChiSegmented_burned.csv','0_55_MChiSegmented_burned.csv','0_65_MChiSegmented_burned.csv','0_75_MChiSegmented_burned.csv','0_85_MChiSegmented_burned.csv','0_95_MChiSegmented_burned.csv']

def pandas(source):
    with open(source,'r') as csvfile:
        DF = pd.read_csv(csvfile,delimiter=',')
        return DF

def merger(name):
    merge_a = pandas(target_a+name)
    merge_b = pandas(target_b+name)
    merge_c = pandas(target_c+name)
    #to_export = [merge_a,merge_b,merge_c]
    #exportDF = pd.concat(to_export,ignore_index=True,sort=False)
    #exportDF.to_csv(output+name,mode='w',index=False,header=True)
    merge_a.to_csv(output+name,mode='a',index=False,header=False)
    merge_b.to_csv(output+name,mode='a',index=False,header=False)
    merge_c.to_csv(output+name,mode='a',index=False,header=False)
        
for path in paths:
    merger(path)
