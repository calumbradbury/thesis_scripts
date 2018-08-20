#hist2D

import matplotlib 
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import pandas as pd           
import sys


target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/raw/'

source_list = ['0_1_ex_MChiSegmented_burned.csv','0_15_ex_MChiSegmented_burned.csv','0_2_ex_MChiSegmented_burned.csv',
              '0_25_ex_MChiSegmented_burned.csv','0_3_ex_MChiSegmented_burned.csv','0_35_ex_MChiSegmented_burned.csv',
              '0_4_ex_MChiSegmented_burned.csv','0_45_ex_MChiSegmented_burned.csv','0_5_ex_MChiSegmented_burned.csv',
              '0_55_ex_MChiSegmented_burned.csv','0_6_ex_MChiSegmented_burned.csv','0_65_ex_MChiSegmented_burned.csv',
              '0_7_ex_MChiSegmented_burned.csv','0_75_ex_MChiSegmented_burned.csv','0_8_ex_MChiSegmented_burned.csv',
              '0_85_ex_MChiSegmented_burned.csv','0_9_ex_MChiSegmented_burned.csv','0_95_ex_MChiSegmented_burned.csv']
              
#def openPandas(source):
#    df = pd.read_csv(target+source)
#    return df 

#for source in source_list:
#    df = openPandas(source)
#    #print pandasDF
#    df.to_csv(target+'full_data.csv',mode='a',index=False,header=False)

with open(target+'0_35_ex_MChiSegmented_burned.csv','r') as csvfile:
#with open(target+'full_data.csv','r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    pandasDF = pandasDF[pandasDF['m_chi'] > 0]
    #pandasDF = pandasDF[pandasDF['tectonics'] == 4]
    y_Series = pandasDF['second_inv']
    #y_Series = pandasDF['m_chi']
    x_Series = pandasDF['quaternary_burned_data']
    #x_Series = pandasDF['tectonics']    
    #weight = pandasDF['secondary_burned_data']
    
    #x_list = x_Series.tolist()
    #y_list = y_Series.tolist()
    #DF = pd.concat([x_Series,y_Series],axis=1)
    #print x_list,y_list     
    fig = plt.figure(1, figsize=(18,18))
    ax = fig.add_subplot(111)
    #plt.scatter(x_Series,y_Series,marker='.')
    ax.hist2d(x_Series,y_Series,bins=(4,100),range=((0,5),(0,250)))
    #plt.ylim(0,200)                                                  
    fig.savefig(target+'tectonics_strain_hist2d_0.35.png', bbox_inches='tight')
    print target+'strain_2nd_m_chi_hist2d_0.35.png'
    #fig.savefig(target+'distance_monsoon_scatter_0.35.png', bbox_inches='tight')  
    #required to clear the axes. Each call of this function wouldn't do that otherwise.
