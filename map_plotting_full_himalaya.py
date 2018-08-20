#scatter
import matplotlib 
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import pandas as pd           
import sys
import matplotlib.cm as cm


target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya_5000/'
#target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/figures_to_keep/full/'

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
    #print pandasDF
#    df.to_csv(target+'full_data.csv',mode='a',index=False,header=False)


weights = ['ksn']#'quaternary_burned_data','monsoon','burned_data','secondary_burned_data','tertiary_burned_data','segmented_elevation']

#weights = ['m_chi']
with open(target+'0_35_ex_MChiSegmented_burned.csv','r') as csvfile:
#with open(target+'full_data.csv','r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    #pandasDF = pandasDF[pandasDF['m_chi'] > 0]
    #pandasDF = pandasDF[pandasDF['strain_ezz'] >= 0]
    #pandasDF = pandasDF[pandasDF['longitude'] > 85]
    #pandasDF = pandasDF[pandasDF['longitude'] < 90]
    #pandasDF = pandasDF[pandasDF['distance_along'] < 1000]
    #pandasDF = pandasDF[pandasDF['distance_along'] > 150]    
    
    x_Series = pandasDF['longitude']
    y_Series = pandasDF['latitude']
    
    for x in weights:
        #weight = pandasDF[x]
        #reducing nodata
        #pandasDF = pandasDF[pandasDF["second_inv"] < 150]
        #lister = weight.tolist()
    

        #color = [str(item/255.) for item in lister]

    
        #x_list = x_Series.tolist()
        #y_list = y_Series.tolist()
        #DF = pd.concat([x_Series,y_Series],axis=1)
        #print x_list,y_list     
        try:
            fig = plt.figure(1, figsize=(30,9))
            ax = fig.add_subplot(111)
    
            weight_series = pandasDF["m_chi"]
            
            weight = weight_series.tolist()
            
            plt.scatter(x_Series,y_Series,marker='.', c=weight, cmap=cm.Reds)
            cb = plt.colorbar()
            #plt.gca().invert_xaxis()
            #matplotlib.axes.Axes.invert_xaxis 
    
            #ax.hist2d(x_Series,y_Series,bins=(40,40),range=((150,1000),(0,3000)))
            #plt.ylim(0,200)                                                  
            fig.savefig(target+'lat_lon_%s_full_data_map_plot.png'%(x), bbox_inches='tight')
            #plt.clf()
            #plt.cla()
            #plt.close()
            
            #pandasDF = pandasDF[pandasDF["glaciated"] == 1]
            #x_Series = pandasDF['longitude']
            #y_Series = pandasDF['latitude']
            #plt.scatter(x_Series,y_Series,marker='.', c='k')
            #fig.savefig(target+'lat_lon_elevation_glaciated_full_data_map_plot.png', bbox_inches='tight') 
        
        
        except Exception as e:
            print e
            print("error in %s"%(x))                      
