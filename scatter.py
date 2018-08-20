#scatter
import matplotlib 
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import pandas as pd           
import sys
import matplotlib.cm as cm


target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/raw/'

source_list = ['0_1_ex_MChiSegmented_burned.csv','0_15_ex_MChiSegmented_burned.csv','0_2_ex_MChiSegmented_burned.csv',
              '0_25_ex_MChiSegmented_burned.csv','0_3_ex_MChiSegmented_burned.csv','0_35_ex_MChiSegmented_burned.csv',
              '0_4_ex_MChiSegmented_burned.csv','0_45_ex_MChiSegmented_burned.csv','0_5_ex_MChiSegmented_burned.csv',
              '0_55_ex_MChiSegmented_burned.csv','0_6_ex_MChiSegmented_burned.csv','0_65_ex_MChiSegmented_burned.csv',
              '0_7_ex_MChiSegmented_burned.csv','0_75_ex_MChiSegmented_burned.csv','0_8_ex_MChiSegmented_burned.csv',
              '0_85_ex_MChiSegmented_burned.csv','0_9_ex_MChiSegmented_burned.csv','0_95_ex_MChiSegmented_burned.csv']
              
def openPandas(source):
    df = pd.read_csv(target+source)
    return df 

for source in source_list:
    df = openPandas(source)
    #print pandasDF
    df.to_csv(target+'full_data.csv',mode='a',index=False,header=False)

#with open(target+'0_35_ex_MChiSegmented_burned.csv','r') as csvfile:
with open(target+'full_data.csv','r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    pandasDF = pandasDF[pandasDF['m_chi'] > 0]
    #pandasDF = pandasDF[pandasDF['longitude'] > 85]
    #pandasDF = pandasDF[pandasDF['longitude'] < 90]
    #pandasDF = pandasDF[pandasDF['distance_along'] < 1000]
    #pandasDF = pandasDF[pandasDF['distance_along'] > 150]    
    
    x_Series = pandasDF['distance_along']
    y_Series = pandasDF['distance']
    weight = pandasDF['secondary_burned_data']
    
    #lister = weight.tolist()
    

    #color = [str(item/255.) for item in lister]

    
    #x_list = x_Series.tolist()
    #y_list = y_Series.tolist()
    #DF = pd.concat([x_Series,y_Series],axis=1)
    #print x_list,y_list     
    fig = plt.figure(1, figsize=(18,6))
    ax = fig.add_subplot(111)
    
    plt.scatter(x_Series,y_Series,marker='.', c=weight, cmap=cm.Blues)
    plt.gca().invert_xaxis()
    #matplotlib.axes.Axes.invert_xaxis 
    
    #ax.hist2d(x_Series,y_Series,bins=(40,40),range=((150,1000),(0,3000)))
    #plt.ylim(0,200)                                                  
    fig.savefig(target+'distance_along_secondary_burn_scatter_full_data_map_plot.png', bbox_inches='tight')  
    #required to clear the axes. Each call of this function wouldn't do that otherwise.
