#spatial variability
#bin data according to latitude/longitude

import matplotlib
from scipy import stats as stats
matplotlib.use("Agg")

from matplotlib import pyplot as plt
import pandas as pd
import csv

import joyplot
joyplot.plt.switch_backend('agg')
import os

#setting paths
target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'
name = 'mchi_pandas_output_extra_burn.csv'
subdirectory = 'annual_lon_bins_2_5_bins/'

## functions ##

#recast calculation
def multiply(x):
  return x*100 

#function to temporarily recast latitude and longitude data to integer values whilst retaining 2 decimal place 
def recastingLatLon(dataFrame):
  dataFrame[["latitude","longitude"]] = dataFrame[["latitude","longitude"]].apply(multiply)
  dataFrame[["latitude","longitude"]] = dataFrame[["latitude","longitude"]].astype(int)
  return dataFrame

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
  for x in range(0,max_value,step):
    mins.append(x)
    maxs.append(x+step)
  if max_value == 7000:
    print("precipitation bins detected")
    column = "secondary_burned_data"
    #column = "non_monsoon"
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

def boxPlot(dataFrame,fig_name):
  if not os.path.exists(target+subdirectory+'boxplots/'):
    os.makedirs(target+subdirectory+'boxplots/')
  
  # Create a figure
  fig = plt.figure(1, figsize=(18,9))

  # Create an axes
  ax = fig.add_subplot(111)
  plt.ylabel("KSN", fontsize = 24)
  plt.title(("KSN "+fig_name), fontsize = 32)
  
  # Create the boxplot
  #bp = ax.boxplot(data_to_plot, labels=header_list, showfliers=False)
  bp = dataFrame.boxplot(showfliers=False)
  
  plt.tick_params(axis='both', which='major', labelsize=18)
  # Save the figure
  fig.savefig(target+subdirectory+'/boxplots/'+fig_name+'_box.png', bbox_inches='tight')  
  #required to clear the axes. Each call of this function wouldn't do that otherwise.
  plt.cla()

def joyPlot(dataFrame,fig_name,columns_for_joy):
  if not os.path.exists(target+subdirectory+'/joyplots/'):
    os.makedirs(target+subdirectory+'/joyplots/')
  x_range = [0,100]
  fig,axes=joyplot.joyplot(dataFrame,column=columns_for_joy,figsize=(20,10),x_range=x_range,title=fig_name)
  fig.savefig(target+subdirectory+'/joyplots/'+fig_name+'_joy.png', bbox_inches='tight')


def columnLabeler(dataFrame,columns_for_joy,precipitation=False):
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


                                                                                                         
  if not precipitation:            
    
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

  return dataFrame,columns_for_joy 

## main ##
#reading csvfile
with open(target+name,'r') as csvfile:
  dataFrame = pd.read_csv(csvfile,delimiter=',')
  integerLatLon = recastingLatLon(dataFrame)
  print integerLatLon
  #lon varies 72 degrees to 95 degrees
  #lat varies 27 degrees to 31.5 degrees
  start = 7200
  end = 9700
  step = 250

  if not os.path.exists(target+subdirectory):
    os.makedirs(target+subdirectory)
  
  for x in range(start,end,step):
    bin = selector(integerLatLon,"longitude",x,x+step)
    x  = float(x)/100
    bin.to_csv(target+subdirectory+str(x)+'_'+name,mode="w",header=True,index=False)
    
    
    precip,columns_for_joy_precip = precipLithoBins(bin,1000,7000)
    litho,columns_for_joy_litho = precipLithoBins(bin,10000,170000)
    
    precip.to_csv(target+subdirectory+str(x)+'_precip_'+name,mode="w",header=True,index=False)    
    litho.to_csv(target+subdirectory+str(x)+'_litho_'+name,mode="w",header=True,index=False)
    
    litho,columns_for_joy_litho = columnLabeler(litho,columns_for_joy_litho)    
    precip,columns_for_joy_precip = columnLabeler(precip,columns_for_joy_precip,precipitation=True)
   
    boxPlot(litho,'litho_'+str(x))
    boxPlot(precip,'precip_'+str(x))
    try:
      joyPlot(litho,'litho_'+str(x),columns_for_joy_litho)
      joyPlot(precip,'precip_'+str(x),columns_for_joy_precip)   
    except:
      print("found an error in "+str(x)) 
    print x 
     


