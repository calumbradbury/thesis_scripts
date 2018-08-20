import pandas as pd
import matplotlib
matplotlib.use("Agg")
from scipy import stats

from matplotlib import pyplot as plt

import numpy as np
import matplotlib.cm as cm



target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/raw/'
source = '0_35_ex_MChiSegmented_burned.csv'
source_list = ['0_1_ex_MChiSegmented_burned.csv','0_15_ex_MChiSegmented_burned.csv','0_2_ex_MChiSegmented_burned.csv',
              '0_25_ex_MChiSegmented_burned.csv','0_3_ex_MChiSegmented_burned.csv','0_35_ex_MChiSegmented_burned.csv',
              '0_4_ex_MChiSegmented_burned.csv','0_45_ex_MChiSegmented_burned.csv','0_5_ex_MChiSegmented_burned.csv',
              '0_55_ex_MChiSegmented_burned.csv','0_6_ex_MChiSegmented_burned.csv','0_65_ex_MChiSegmented_burned.csv',
              '0_7_ex_MChiSegmented_burned.csv','0_75_ex_MChiSegmented_burned.csv','0_8_ex_MChiSegmented_burned.csv',
              '0_85_ex_MChiSegmented_burned.csv','0_9_ex_MChiSegmented_burned.csv','0_95_ex_MChiSegmented_burned.csv']
#
source_list = ['full_data.csv']  

#source_list=[1,2,3,4]            


hist2d = False
box = False
glacial = False       
pandas_hist = True

def toSeries(DF,target,values,tectonics=False):
    if not tectonics:
        selectedDF = DF[DF[target].isin(range(values[0],values[1]))]
    if tectonics:
        selectedDF = DF[DF[target] == values]
    selectedDF = selectedDF[selectedDF['m_chi'] > 0]
    series = selectedDF['m_chi']
    if hist2d:
        return selectedDF
    return series


def ks_2sample_test(pandasSeries_A,pandasSeries_B):
    list_A = pandasSeries_A.tolist()
    list_B = pandasSeries_B.tolist()
    statistic,p_value = stats.ks_2samp(list_A,list_B)
    return statistic,p_value

if glacial:
    for x in source_list:
        with open(target+x,'r') as csvfile:
            pandasDF = pd.read_csv(csvfile,delimiter=',')
            #print x
            glacial_1 = toSeries(pandasDF,'glaciated',0,tectonics=True)
            glacial_2 = toSeries(pandasDF,'glaciated',1,tectonics=True)

            list_1 = glacial_1.tolist()
            list_2 = glacial_2.tolist()
            
            list_1 = len(list_1)
            list_2 = len(list_2)
            
            proportion = float(list_2)/float(list_1)
            #except:
            #    print "error"
            #    proportion = 0
            
            print proportion






with open(target+source,'r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    #pandasDF = pandasDF[pandasDF['segmented_elevation'] > 1000]
    #pandasDF = pandasDF[pandasDF['segmented_elevation'] < 4000]
    
    box_1 = toSeries(pandasDF,'secondary_burned_data',[0,500])
    box_2 = toSeries(pandasDF,'secondary_burned_data',[500,1000])
    box_3 = toSeries(pandasDF,'secondary_burned_data',[1000,1500])
    box_4 = toSeries(pandasDF,'secondary_burned_data',[1500,2000])
    box_5 = toSeries(pandasDF,'secondary_burned_data',[2000,2500])
    box_6 = toSeries(pandasDF,'secondary_burned_data',[2500,3000])
    box_7 = toSeries(pandasDF,'secondary_burned_data',[3000,3500]) 
    box_8 = toSeries(pandasDF,'secondary_burned_data',[3500,4000])
    box_9 = toSeries(pandasDF,'secondary_burned_data',[4000,4500])
    box_10 = toSeries(pandasDF,'secondary_burned_data',[4500,5000])
    box_11 = toSeries(pandasDF,'secondary_burned_data',[5000,5500])
    box_12 = toSeries(pandasDF,'secondary_burned_data',[5500,6000])
    box_13 = toSeries(pandasDF,'secondary_burned_data',[6000,6500])
    box_14 = toSeries(pandasDF,'secondary_burned_data',[6500,7000]) 
    
    #tect_1 = toSeries(pandasDF,'tectonics',1,tectonics=True)
    #tect_2 = toSeries(pandasDF,'tectonics',2,tectonics=True)
    #tect_3 = toSeries(pandasDF,'tectonics',3,tectonics=True)
    #tect_4 = toSeries(pandasDF,'tectonics',4,tectonics=True)
    
    litho_1 = toSeries(pandasDF,'burned_data',[10000,20000])
    litho_2 = toSeries(pandasDF,'burned_data',[20000,30000])
    litho_3 = toSeries(pandasDF,'burned_data',[30000,40000])
    litho_4 = toSeries(pandasDF,'burned_data',[40000,50000])
    litho_5 = toSeries(pandasDF,'burned_data',[50000,60000])
    litho_6 = toSeries(pandasDF,'burned_data',[60000,70000])
    litho_7 = toSeries(pandasDF,'burned_data',[70000,80000])
    litho_8 = toSeries(pandasDF,'burned_data',[80000,90000])
    litho_9 = toSeries(pandasDF,'burned_data',[90000,100000])
    litho_10 = toSeries(pandasDF,'burned_data',[100000,110000])
    litho_11 = toSeries(pandasDF,'burned_data',[110000,120000])
    litho_12 = toSeries(pandasDF,'burned_data',[120000,130000])
    litho_13 = toSeries(pandasDF,'burned_data',[130000,140000])
    litho_14 = toSeries(pandasDF,'burned_data',[140000,150000])
    litho_15 = toSeries(pandasDF,'burned_data',[150000,160000])
    litho_16 = toSeries(pandasDF,'burned_data',[160000,170000])
    
    glacial_1 = toSeries(pandasDF,'glaciated',0,tectonics=True)
    glacial_2 = toSeries(pandasDF,'glaciated',1,tectonics=True)
    
    if box:    
        fig = plt.figure(1, figsize=(20, 20))                                            

        # Create an axes
        ax   = fig.add_subplot(111)
  
        # Create the boxplot
        #bp = ax.boxplot([litho_1,litho_2,litho_3,litho_4,litho_5,litho_6,litho_7,litho_8,litho_9,litho_10,litho_11,litho_12,litho_13,litho_14,litho_15,litho_16])
        bp = ax.boxplot([box_1,box_2,box_3,box_4,box_5,box_6,box_7,box_8,box_9,box_10,box_11,box_12,box_13,box_14])
        #bp = ax.boxplot([glacial_1,glacial_2])
        #bp = ax.scatter(df_x,df_y,marker='.')
          
        #  Save the figure
        fig.savefig(target+'0.35_precip_box_elevation_clipped_low.png', bbox_inches='tight')
    
        #print ks_2sample_test(litho_9,litho_10)
        print ks_2sample_test(tect_1,tect_4)
        print ks_2sample_test(tect_1,tect_3)
        print ks_2sample_test(tect_1,tect_2)
        print ks_2sample_test(tect_2,tect_4)
        print ks_2sample_test(tect_2,tect_3)
        print ks_2sample_test(tect_3,tect_4)
 
        
    
    if hist2d:
        #lith_mins = [10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000,130000,140000,150000,160000]
        #lith_maxs = [20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000,130000,140000,150000,160000,170000]
        lith_range = [litho_1,litho_2,litho_3,litho_4,litho_5,litho_6,litho_7,litho_8,litho_9,litho_10,litho_11,litho_12,litho_13,litho_14,litho_15,litho_16]
        precip_range = [box_1,box_2,box_3,box_4,box_5,box_6,box_7,box_8,box_9,box_10,box_11,box_12,box_13,box_14]
        tecto_range = [tect_1,tect_2,tect_3,tect_4]
        iterator = 1
        for data in tecto_range:
            x_Series = data['tectonics']
            y_Series = data['m_chi']      
            print x_Series
            print y_Series
    
            #x_list = x_Series.tolist()
            #y_list = y_Series.tolist()
            #DF = pd.concat([x_Series,y_Series],axis=1)
            #print x_list,y_list     
            fig = plt.figure(1, figsize=(18,18))
            ax = fig.add_subplot(111)
            ax.hist2d(x_Series,y_Series,bins=(5,50),range=((0,5),(0,200)))
            #plt.ylim(0,200)                                                  
            fig.savefig(target+'tect_%s_ksn_hist2d_0.35.png'%(str(iterator)), bbox_inches='tight')  
            #required to clear the axes. Each call of this function wouldn't do that otherwise.
            plt.cla()
            iterator += 1
    
    bin_range_lower = range(0,140,10)
    bin_range_upper = range(10,150,10)
    
    #bin_range_lower = range(0,160000,10000)
    #bin_range_upper = range(10000,170000,10000)    
    
    #bin_range_lower = [10000,20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000,130000,140000,150000,160000]
    #bin_range_upper = [20000,30000,40000,50000,60000,70000,80000,90000,100000,110000,120000,130000,140000,150000,160000,170000]
    
    #bin_range_lower = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3]
    
    #bin_range_upper = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4]     
    
             
    if pandas_hist:
        
        median_full = []
        value_full = []
        
        

        #source_list = ['segmented_elevation','quaternary_burned_data','secondary_burned_data','monsoon']
        for x in source_list:
            #with open(target+x,'r') as csvfile:
            with open(target+'0_35_ex_MChiSegmented_burned.csv','r') as csvfile:
                medians = []
                values = []
                weights = []
                list_of_series = []
                pandasDF = pd.read_csv(csvfile,delimiter=',')
                
                #for y,z in zip(bin_range_lower,bin_range_upper):
                for y in [1,2,3,4]:
                #    
                    selectedDF = pandasDF[pandasDF['second_inv'] > 0]
                    #selectedDF = selectedDF[selectedDF['second_inv'] <= 100]
                    #selectedDF = selectedDF[selectedDF['segmented_elevation'] > y]
                    #selectedDF = selectedDF[selectedDF['segmented_elevation'] < z]
                    selectedDF = selectedDF[selectedDF['quaternary_burned_data'] == y]
                    #selectedDF = selectedDF[selectedDF['tectonics'] == y]
                    #selectedDF = selectedDF[selectedDF['strain_ezz'] >= y]
                    
                    #selectedDF = selectedDF[selectedDF['strain_ezz'] < z]                          
                    
                    series = selectedDF['second_inv']
                    #series = selectedDF['secondary_burned_data']
                    
                    lister = series.tolist()
                    list_of_series.append(lister)
                    value=1
                    #value = z+((z-y)/2)
                    values.append(value)
                    
                    medians.append(series.median())
                
                    #weighting
                    weighter = selectedDF['secondary_burned_data'].median()
                    weights.append(weighter)
                    
                
                
                median_full.append(medians)
                value_full.append(values)
                
            fig = plt.figure(1, figsize=(24,9))
            ax = fig.add_subplot(111)
            #plt.yscale('log')
            #plt.xlabel("segmented elevation in 50m bins")
            #plt.ylabel("median Ksn - log scale")        
            
            plt.ylabel("Strain")
            plt.xlabel("Tectonic zones")
            #plt.scatter(values,medians,c=weights,cmap=cm.Blues)
            #plt.colorbar()
            plt.boxplot(list_of_series)
            
                
                
                #    hs = series.hist(bins=200)
            write_name = x.replace('_ex_MChiSegmented_burned.csv','')
            
            #plt.title("concavity "+write_name)
            fig.savefig(target+'0.35_strain_2nd_tectonics_box.png', bbox_inches='tight')
            #fig.savefig(target+'elevation_concavity_scatter_%s.png'%(x), bbox_inches='tight')
                #fig.savefig(target+'longitude_scatter_precip_%s.png'%(write_name), bbox_inches='tight')
            plt.cla()
        x = np.arange(18)
        ys = [i+x+(i*x)**2 for i in range(18)]

        colors = cm.Reds(np.linspace(0, 1, len(ys)))

        #median_full = median_full[:9]
        #value_full = value_full[:9]
        
        for median,value,colour in zip(median_full,value_full,colors):
            plt.scatter(value,median,color=colour)
            
        plt.yscale('log')
        plt.xlabel("segmented elevation in 50m bins")
        plt.ylabel("median Ksn - log scale") 
        
        #fig.savefig(target+'full_scatter.png', bbox_inches='tight')                
                #plt.cla()

                #selectDF = pandasDF[pandasDF['m_chi'] > 0]
                #selectedDF = selectDF[selectDF['segmented_elevation'] > 350]
                #selectedDF = selectedDF[selectedDF['segmented_elevation'] < 600] 
                #elevation_series_1 = selectedDF['m_chi'] 
                
                #selectedDF = selectDF[selectDF['segmented_elevation'] > 600]
                #selectedDF = selectedDF[selectedDF['segmented_elevation'] < 850] 
                #elevation_series_2 = selectedDF['m_chi'] 
                
                #selectedDF = selectDF[selectDF['segmented_elevation'] > 850]
                #selectedDF = selectedDF[selectedDF['segmented_elevation'] < 1100] 
                #elevation_series_3 = selectedDF['m_chi']
                
                #selectedDF = selectDF[selectDF['segmented_elevation'] > 1100]
                #selectedDF = selectedDF[selectedDF['segmented_elevation'] < 1350] 
                #elevation_series_4 = selectedDF['m_chi']
                
                
                #print elevation_series_1.median()
                #print elevation_series_2.median()
                #print elevation_series_3.median()
                #print elevation_series_4.median()
                
                
                #print ks_2sample_test(elevation_series_1,elevation_series_2)                 
                #print ks_2sample_test(elevation_series_1,elevation_series_3)
                #print ks_2sample_test(elevation_series_1,elevation_series_4) 
                #print ks_2sample_test(elevation_series_2,elevation_series_3)
                #print ks_2sample_test(elevation_series_2,elevation_series_4) 
                #print ks_2sample_test(elevation_series_3,elevation_series_4) 