#litho bin processing

import pandas as pd
import joyplot
joyplot.plt.switch_backend('agg')


directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'
file_name = 'mchi_pandas_output.csv'

def counter(pandasDF):
  list_a = pandasDF["m_chi"]
  list_a = list_a.tolist()
  count = len(list_a)
  return count

def binSelector(bin_min,bin_max,pandasDF,columns_for_joy):
  #selecting precipitation bin
  pandasDF = pandasDF[pandasDF["secondary_burned_data"].isin(range(bin_min,bin_max))]
  #counting data for labeling in joy
  count = counter(pandasDF)
  if count >= 10:
    columns_for_joy.append(str(bin_min)+'_'+str(bin_max)+' count: '+str(count))
  #renaming header  
  pandasDF.rename(columns={'m_chi':(str(bin_min)+'_'+str(bin_max)+' count: '+str(count))},inplace=True)
  pandasSeries = pandasDF[(str(bin_min)+'_'+str(bin_max)+' count: '+str(count))]
  #preparing to concat to new dataframe
  pandasSeries.reset_index(drop=True, inplace=True)
  return pandasSeries,columns_for_joy

def joyPlotter(pandasDF,litho_name,columns_for_joy):
  fig,axes=joyplot.joyplot(pandasDF,column=columns_for_joy,figsize=(10,10),x_range=[0,100],title='%s precipitation bin'%(litho_name))  
  fig.savefig(directory+'_joy_%s_precip_bin.png'%(litho_name), bbox_inches='tight')

def litho_to_precip(litho_name,litho_min,litho_max,pandasDF):
  
  #selection will only work if litho_keys have been adapted in the source shapefile
  selectedDF = pandasDF[pandasDF["burned_data"].isin(range(litho_min,litho_max))]
  
  #if result is empty, try using basic litho_key to select data.
  if selectedDF.empty:
    #fixing litho_min to represent original litho_key
    original_litho_key = litho_min/10000
    print(litho_min,original_litho_key)
    print("Failed to find any data in your csv. Attempting to use the original glim_litho_key")
    selectedDF = pandasDF[pandasDF["burned_data"] == original_litho_key]
    if selectedDF.empty:
      print("Still can't find any data, I guess it's not there after all...")
  
  columns_for_joy = []
  bin_1,columns_for_joy = binSelector(0,1000,selectedDF,columns_for_joy)
  bin_2,columns_for_joy = binSelector(1000,2000,selectedDF,columns_for_joy)
  bin_3,columns_for_joy = binSelector(2000,3000,selectedDF,columns_for_joy)
  bin_4,columns_for_joy = binSelector(3000,4000,selectedDF,columns_for_joy)
  bin_5,columns_for_joy = binSelector(4000,5000,selectedDF,columns_for_joy)
  bin_6,columns_for_joy = binSelector(5000,6000,selectedDF,columns_for_joy)
  bin_7,columns_for_joy = binSelector(6000,7000,selectedDF,columns_for_joy)
  print columns_for_joy
  export_DF = pd.concat([bin_1,bin_2,bin_3,bin_4,bin_5,bin_6,bin_7],axis=1)
  export_DF.to_csv(directory+litho_name+"_precipitation_bins.csv", mode="w",header=True,index=False)  
  try:
    joyPlotter(export_DF,litho_name,columns_for_joy)
  except:
    print("Error in generating %s joyplot"%(litho_name))  
with open(directory+file_name,'r') as csvfile:
  pandasDF=pd.read_csv(csvfile,delimiter=',')
  litho_to_precip("Evaporites",10000,19999,pandasDF)
  litho_to_precip("Ice_and_Glaciers",20000,29999,pandasDF)
  litho_to_precip("Metamorphics",30000,39999,pandasDF)
  litho_to_precip("NoData",40000,49999,pandasDF)
  litho_to_precip("Acid_Plutonic_Rocks",50000,59999,pandasDF)
  litho_to_precip("Basin_Plutonic_Rocks",60000,69999,pandasDF)
  litho_to_precip("Intermediate_Plutonic_Rocks",70000,79999,pandasDF)
  litho_to_precip("Pyroclastics",80000,89999,pandasDF)
  litho_to_precip("Carbonate_Sedimentary_Rocks",90000,99999,pandasDF)
  litho_to_precip("Mixed_Sedimentary_Rocks",100000,109999,pandasDF)
  litho_to_precip("Siliciclastic_Sedimentary_Rocks",110000,119999,pandasDF)
  litho_to_precip("Unconsolidated_Sediments",120000,129999,pandasDF)
  litho_to_precip("Acid_Volcanic_Rocks",130000,139999,pandasDF)
  litho_to_precip("Basic_Volcanic_Rocks",140000,149999,pandasDF)
  litho_to_precip("Intermediate_Volcanic_Rocks",150000,159999,pandasDF)
  litho_to_precip("Water_Bodies",160000,169999,pandasDF)
