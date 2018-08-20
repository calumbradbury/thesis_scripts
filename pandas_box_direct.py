#pandas direct boxer
import matplotlib

matplotlib.use("Agg")
import pandas as pd
import csv
import os
from matplotlib import pyplot as plt

###windows switch###

#windows = False
windows = False

#sub_path = 'full_himalaya'

if windows:
    sub_path = '25_65\\'
    target = os.path.join('R:\\','LSDTopoTools','Topographic_projects',sub_path,'\\') 
    #temp_path = os.path.join('C:\\','pandas_in',sub_path)
    #temp_out = os.path.join('C:\\','pandas_out',sub_path) 

else:
    target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/'+sub_path

def counter(pandasDF):
    list_a = pandasDF["m_chi"]
    list_a = list_a.tolist()
    count = len(list_a)
    return count

def renameToSeries(dataFrame,column_name):
    column = "m_chi"
    dataFrame.rename(columns={column:column_name},inplace=True)      
    series = dataFrame[column_name]
    return series 

def boxPlot(dataFrame,m_n,fig_name):
    
    if windows:
        target_path = temp_out+'concavity_boxplots\\'
    else:
        target_path = target+'concavity_boxplots/'
    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
  
    # Create a figure
    fig = plt.figure(1, figsize=(18,9))

    # Create an axes
    ax = fig.add_subplot(111)
    plt.ylabel("KSN", fontsize = 24)
    plt.title(("KSN "+fig_name+m_n), fontsize = 32)
  
    # Create the boxplot
    #bp = ax.boxplot(data_to_plot, labels=header_list, showfliers=False)
    bp = dataFrame.boxplot(showfliers=False)
  
    plt.tick_params(axis='both', which='major', labelsize=18)
    # Save the figure
    fig.savefig(target_path+fig_name+m_n+'_box.png', bbox_inches='tight')  
    #required to clear the axes. Each call of this function wouldn't do that otherwise.
    plt.cla()
  
#function to select data by column range
def selector(dataFrame,column,range_min,range_max,columns_for_joy=[],return_series=False):
    #dataFrame.sort_values(by=[column])
    print column,range_min,range_max
    selected = dataFrame[dataFrame[column].isin(range(range_min,range_max))]

    if return_series: 
        count = counter(selected)
        if count >= 100:
            columns_for_joy.append(str(range_min)+'_'+str(range_max)+'_count:'+str(count)) 
        series = renameToSeries(selected,str(range_min)+'_'+str(range_max)+'_count:'+str(count))
        return series,columns_for_joy 
    return selected 

def precipLithoBins(dataFrame,step,max_value):
    #column = "m_chi"
    mins = []
    maxs = []
    #helps with managing empty columns in joy plotting
    columns_for_joy = []
    for x in range(0,int(max_value),int(step)):
        mins.append(x)
        maxs.append(x+step)
    if max_value == 7000:
        print("precipitation bins detected")
        #column = "secondary_burned_data"
        column = "secondary_burned_data"
        precip_1,columns_for_joy = selector(dataFrame,column,mins[0],maxs[0],columns_for_joy,return_series=True)
        precip_2,columns_for_joy = selector(dataFrame,column,mins[1],maxs[1],columns_for_joy,return_series=True)
        precip_3,columns_for_joy = selector(dataFrame,column,mins[2],maxs[2],columns_for_joy,return_series=True)
        precip_4,columns_for_joy = selector(dataFrame,column,mins[3],maxs[3],columns_for_joy,return_series=True)
        precip_5,columns_for_joy = selector(dataFrame,column,mins[4],maxs[4],columns_for_joy,return_series=True)
        precip_6,columns_for_joy = selector(dataFrame,column,mins[5],maxs[5],columns_for_joy,return_series=True)
        precip_7,columns_for_joy = selector(dataFrame,column,mins[6],maxs[6],columns_for_joy,return_series=True)
        precip_1.reset_index(drop=True, inplace=True)
        precip_2.reset_index(drop=True, inplace=True)
        precip_3.reset_index(drop=True, inplace=True)
        precip_4.reset_index(drop=True, inplace=True)
        precip_5.reset_index(drop=True, inplace=True)
        precip_6.reset_index(drop=True, inplace=True)
        precip_7.reset_index(drop=True, inplace=True)

        precip_bins = pd.concat([precip_1,precip_2,precip_3,precip_4,precip_5,precip_6,precip_7],axis=1)
        return precip_bins,columns_for_joy   
  
    if max_value == 170000:
        print("lithology bins detected")
        column = "burned_data"
        litho_3,columns_for_joy = selector(dataFrame,column,mins[3],maxs[3],columns_for_joy,return_series=True)
        litho_5,columns_for_joy = selector(dataFrame,column,mins[5],maxs[5],columns_for_joy,return_series=True)
        litho_6,columns_for_joy = selector(dataFrame,column,mins[6],maxs[6],columns_for_joy,return_series=True)
        litho_9,columns_for_joy = selector(dataFrame,column,mins[9],maxs[9],columns_for_joy,return_series=True)
        litho_10,columns_for_joy = selector(dataFrame,column,mins[10],maxs[10],columns_for_joy,return_series=True)
        litho_11,columns_for_joy = selector(dataFrame,column,mins[11],maxs[11],columns_for_joy,return_series=True)
        litho_12,columns_for_joy = selector(dataFrame,column,mins[12],maxs[12],columns_for_joy,return_series=True)
        litho_14,columns_for_joy = selector(dataFrame,column,mins[14],maxs[14],columns_for_joy,return_series=True)
    
        litho_3.reset_index(drop=True, inplace=True)
        litho_5.reset_index(drop=True, inplace=True)
        litho_6.reset_index(drop=True, inplace=True)
        litho_9.reset_index(drop=True, inplace=True)
        litho_10.reset_index(drop=True, inplace=True)
        litho_11.reset_index(drop=True, inplace=True)
        litho_12.reset_index(drop=True, inplace=True)
        litho_14.reset_index(drop=True, inplace=True)
    
        litho_bins = pd.concat([litho_3,litho_5,litho_6,litho_9,litho_10,litho_11,litho_12,litho_14],axis=1)
        
    
        return litho_bins,columns_for_joy
    
    if max_value == 4:
        print("simplified bins detected")
        column = "tertiary_burned_data"
        simplified_1,columns_for_joy = selector(dataFrame,column,mins[0],maxs[0],columns_for_joy,return_series=True)
        simplified_2,columns_for_joy = selector(dataFrame,column,mins[1],maxs[1],columns_for_joy,return_series=True)
        simplified_3,columns_for_joy = selector(dataFrame,column,mins[2],maxs[2],columns_for_joy,return_series=True)
        simplified_4,columns_for_joy = selector(dataFrame,column,mins[3],maxs[3],columns_for_joy,return_series=True)

        simplified_1.reset_index(drop=True, inplace=True)
        simplified_2.reset_index(drop=True, inplace=True)
        simplified_3.reset_index(drop=True, inplace=True)
        simplified_4.reset_index(drop=True, inplace=True)
    
        simplified_bins = pd.concat([simplified_1,simplified_2,simplified_3,simplified_4],axis=1)
        
    
        return simplified_bins,columns_for_joy
  
def columnLabeler(dataFrame,columns_for_joy,lithology=False,precipitation=False):   
    glim_keys = ['Evaporites','Ice and Glaciers','Metamorphics','No Data',
                 'Acid plutonic rocks','Basic plutonic rocks',
                 'Intermediate plutonic rocks','Pyroclastics',
                 'Carbonate sedimentary rocks','Mixed sedimentary rocks',
                 'Siliciclastic sedimentary rocks','Unconsolidated sediments',
                 'Acid volcanic rocks','Basic volcanic rocks',
                 'Intermediate volcanic rocks','Water Bodies']
  
  
    column_keys = ['10000_20000','20000_30000','30000_40000','40000_50000',
                   '50000_60000','60000_70000','70000_80000','80000_90000',
                   '90000_100000','100000_110000','110000_120000','120000_130000',
                   '130000_140000','140000_150000','150000_160000','160000_170000']


                                                                                                         
    if lithology or precipitation:            
    
        df_header = dataFrame.columns.values.tolist()
        new_headers = df_header
        for x,y in zip(column_keys,glim_keys):
            new_headers = [z.replace(x,y) for z in new_headers]
            
        for x,y in zip(df_header,new_headers):

            y = y.replace('_','\n')
            y = y.replace(' ','\n')
      
            try:             
    
                dataFrame.rename(columns={x:y},inplace=True)
                columns_for_joy = [a.replace(x,y) for a in columns_for_joy]
      
            except:
                print("Error in replacing the %s column with the %s glim key"%(x,y))
  
    if precipitation:
        header_list = dataFrame.columns.values.tolist()
        new_label = [b.replace('_','\n') for b in header_list]
    
        for c,d in zip(header_list,new_label):
            try:
                dataFrame.rename(columns={c:d},inplace=True)
                columns_for_joy = [a.replace(c,d) for a in columns_for_joy]       
            except:
                print("Error in replacing the %s column with the %s intended value"%(c,d))      
    
    if not precipitation and not lithology:
        
        df_header = dataFrame.columns.values.tolist()
        new_headers = df_header
        new_simplified_keys = ['Sub_Himalaya','Lesser_Himalaya','Greater_Himalaya','Tethyan_Himalaya'] 
        simplified_keys = ['0_1','1_2','2_3','3_4']
        for x,y in zip(simplified_keys,new_simplified_keys):
            new_headers = [z.replace(x,y) for z in new_headers]
            
        for x,y in zip(df_header,new_headers):

            y = y.replace('_','\n')
            y = y.replace(' ','\n')
      
            try:             
    
                dataFrame.rename(columns={x:y},inplace=True)
                columns_for_joy = [a.replace(x,y) for a in columns_for_joy]
      
            except:
                print("Error in replacing the %s column with the %s glim key"%(x,y))
                

    return dataFrame,columns_for_joy 
  
#script to get results as pandas dataframe.
def getMChiSegmented(path):
    
    #windows modifications#
    if windows:
        with open(temp_path+path+'_MChiSegmented_burned.csv') as mChiSource:
            pandasDF = pd.read_csv(mChiSource, delimiter=',')
    
    else:
        with open(target+path+'_MChiSegmented_burned.csv') as mChiSource:
            pandasDF = pd.read_csv(mChiSource, delimiter=',')        
    
    return pandasDF
    
#m_n_list = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
m_n_list = [0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6]
simplified = ['sub','lesser','greater','tethyan']

for x in m_n_list:
    x = str(x)
    x = x.replace('.','_')
    pandasDF = getMChiSegmented(x)  
    litho,columns_for_joy_litho = precipLithoBins(pandasDF,10000,170000)
    precip,columns_for_joy_precip = precipLithoBins(pandasDF,1000,7000)
    
    #print columns_for_joy_litho
    #print litho
    litho,columns_for_joy_litho = columnLabeler(litho,columns_for_joy_litho,lithology=True)
    precip,columns_for_joy_precip = columnLabeler(precip,columns_for_joy_precip,precipitation=True)  
    
    simplified_data,columns_for_joy_simplified = precipLithoBins(pandasDF,1,4)
    simplified_data,columns_for_joy_precip = columnLabeler(simplified_data,columns_for_joy_simplified)  
  
    boxPlot(litho,x,"litho")
    boxPlot(precip,x,"precip")
    boxPlot(simplified_data,x,"simplified_data")
    
    #selecting data using simplified fault zones
    for name in simplified:
        dataFrame = selector(pandasDF,'tertiary_burned_data',1,4)
        litho,columns_for_joy_litho = precipLithoBins(pandasDF,10000,170000)
        precip,columns_for_joy_precip = precipLithoBins(pandasDF,1000,7000)
    
        #print columns_for_joy_litho
        #print litho
        litho,columns_for_joy_litho = columnLabeler(litho,columns_for_joy_litho,lithology=True)
        precip,columns_for_joy_precip = columnLabeler(precip,columns_for_joy_precip,precipitation=True)  
  
        boxPlot(litho,x,"litho "+name)
        boxPlot(precip,x,"precip "+name)
        
        
    
    
    
  
  
  