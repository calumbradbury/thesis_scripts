#concavity boxplotting
import matplotlib 
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import pandas as pd           
import sys
import matplotlib.cm as cm


target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/raw/'
target_b = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/figures_to_keep/' 

source_list = ['0_1_ex_MChiSegmented_burned.csv','0_15_ex_MChiSegmented_burned.csv','0_2_ex_MChiSegmented_burned.csv',
              '0_25_ex_MChiSegmented_burned.csv','0_3_ex_MChiSegmented_burned.csv','0_35_ex_MChiSegmented_burned.csv',
              '0_4_ex_MChiSegmented_burned.csv','0_45_ex_MChiSegmented_burned.csv','0_5_ex_MChiSegmented_burned.csv',
              '0_55_ex_MChiSegmented_burned.csv','0_6_ex_MChiSegmented_burned.csv','0_65_ex_MChiSegmented_burned.csv',
              '0_7_ex_MChiSegmented_burned.csv','0_75_ex_MChiSegmented_burned.csv','0_8_ex_MChiSegmented_burned.csv',
              '0_85_ex_MChiSegmented_burned.csv','0_9_ex_MChiSegmented_burned.csv','0_95_ex_MChiSegmented_burned.csv']
                                                                                      
def getSeriesList(source,column):
    df = pd.read_csv(target+source)
    df = df[df[column]>0]
    #df = df[df[column]<400]
    #print df
    series = df[column]
    lister = series.tolist()
    return lister

for_box = []
labels = []
    
for source in source_list:
    name = source.replace('_ex_MChiSegmented_burned.csv','')
    name = name.replace('_','.')
    #source = source.replace('ex','0.45')
    data = getSeriesList(source,'segmented_elevation')
    for_box.append(data)
    labels.append(name)

    
fig = plt.figure(1, figsize=(15,8))
ax = fig.add_subplot(111)
       
            
plt.ylabel("Elevation",fontsize=16)
plt.xlabel("Concavity",fontsize=16)
#plt.ylim(ymax=400,ymin=0)
plt.boxplot(for_box,labels=labels,medianprops=dict(linestyle='-', linewidth=2.5, color='k'))
            
            
fig.savefig(target_b+'elevation_concavity_box.png', bbox_inches='tight')
