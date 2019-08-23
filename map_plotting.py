#scatter
import matplotlib 
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import pandas as pd           
import sys
import matplotlib.cm as cm


#target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya_5000/raw/'
target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya_5000/'
#source_list = ['0_1_ex_MChiSegmented_burned.csv','0_15_ex_MChiSegmented_burned.csv','0_2_ex_MChiSegmented_burned.csv',
#              '0_25_ex_MChiSegmented_burned.csv','0_3_ex_MChiSegmented_burned.csv','0_35_ex_MChiSegmented_burned.csv',
#              '0_4_ex_MChiSegmented_burned.csv','0_45_ex_MChiSegmented_burned.csv','0_5_ex_MChiSegmented_burned.csv',
#              '0_55_ex_MChiSegmented_burned.csv','0_6_ex_MChiSegmented_burned.csv','0_65_ex_MChiSegmented_burned.csv',
#              '0_7_ex_MChiSegmented_burned.csv','0_75_ex_MChiSegmented_burned.csv','0_8_ex_MChiSegmented_burned.csv',
#              '0_85_ex_MChiSegmented_burned.csv','0_9_ex_MChiSegmented_burned.csv','0_95_ex_MChiSegmented_burned.csv']
              
source_list = ['0_1cosmo_MChiSegmented_burned.csv','0_15cosmo_MChiSegmented_burned.csv','0_2cosmo_MChiSegmented_burned.csv',
              '0_25cosmo_MChiSegmented_burned.csv','0_3cosmo_MChiSegmented_burned.csv','0_35cosmo_MChiSegmented_burned.csv',
              '0_4cosmo_MChiSegmented_burned.csv','0_45cosmo_MChiSegmented_burned.csv','0_5cosmo_MChiSegmented_burned.csv',
              '0_55cosmo_MChiSegmented_burned.csv','0_6cosmo_MChiSegmented_burned.csv','0_65cosmo_MChiSegmented_burned.csv',
              '0_7cosmo_MChiSegmented_burned.csv','0_75cosmo_MChiSegmented_burned.csv','0_8cosmo_MChiSegmented_burned.csv',
              '0_85cosmo_MChiSegmented_burned.csv','0_9cosmo_MChiSegmented_burned.csv','0_95cosmo_MChiSegmented_burned.csv']
              
def openPandas(source):
    df = pd.read_csv(target+source)
    return df 

for source in source_list:
    df = openPandas(source)
    #print pandasDF
    df.to_csv(target+'cosmo_full_data.csv',mode='a',index=False,header=False)

#with open(target+'0_35_ex_MChiSegmented_burned.csv','r') as csvfile:

weights = ['cosmo_EBE_MMKYR']#,'tectonics','monsoon','burned_data','secondary_burned_data','exhumation','segmented_elevation']

with open(target+'cosmo_full_data.csv','r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    #print pandasDF
    pandasDF = pandasDF[pandasDF['m_chi'] > 0]
    #pandasDF = pandasDF[pandasDF['longitude'] > 85]
    #pandasDF = pandasDF[pandasDF['longitude'] < 90]
    #pandasDF = pandasDF[pandasDF['distance_along'] < 1000]
    #pandasDF = pandasDF[pandasDF['distance_along'] > 150]    
    
    x_Series = pandasDF['longitude']
    y_Series = pandasDF['latitude']
    
    for x in weights:
        weight = pandasDF[x]
        #reducing nodata
        #pandasDF = pandasDF[pandasDF[x] > 0]
        #lister = weight.tolist()
    

        #color = [str(item/255.) for item in lister]

    
        #x_list = x_Series.tolist()
        #y_list = y_Series.tolist()
        #DF = pd.concat([x_Series,y_Series],axis=1)
        #print x_list,y_list     
        try:
            fig = plt.figure(1, figsize=(18,6))
            ax = fig.add_subplot(111)
    
            plt.scatter(x_Series,y_Series,marker='.', c=weight, cmap=cm.Blues)
            #plt.gca().invert_xaxis()
            #matplotlib.axes.Axes.invert_xaxis 
    
            #ax.hist2d(x_Series,y_Series,bins=(40,40),range=((150,1000),(0,3000)))
            #plt.ylim(0,200)                                                  
            cb = plt.colorbar()
            fig.savefig(target+'lat_lon_%s_full_data_map_plot.png'%(x), bbox_inches='tight')
            plt.cla()
        except:
            print("error in %s"%(x))  