#script to extract max/min precipitation from each basin. Used to calculate gradient
import matplotlib

matplotlib.use("Agg")
import pandas as pd
import csv
import os
from matplotlib import pyplot as plt

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'
#name = 'himalaya_processed.csv'

def getMaxMin(dataFrame,basin_key):
  basinDataFrame = dataFrame.loc[dataFrame["basin_key"] == basin_key]
  try:
    precipitationSeries = basinDataFrame["precipitation"]
  
  except:
    precipitationSeries = basinDataFrame["secondary_burned_data"]
  #print precipitationSeries
  
  #maxPrecip = precipitationSeries.max()
  #minPrecip = precipitationSeries.min()
  maxPrecip = precipitationSeries.first_valid_index()
  minPrecip = precipitationSeries.last_valid_index()
  
  
  return maxPrecip, minPrecip 


def pathCollector(path,name):
  #returns lists of paths and names
  with open(path+name+'.csv','r') as csvfile:
    csvReader = csv.reader(csvfile,delimiter=',')
    next(csvReader)
    full_paths = []
    dem_names = []
    write_names = []
    for row in csvReader:
          max_basin = (int(row[6])/2)+int(row[5])
          full_path = path+str(row[0])+'/'+("%.2f" %float(row[2]))+'_'+("%.2f" %float(row[3]))+'_'+str(row[0])+'_'+str(row[1])+'/'+str(row[5])+'/'
          dem_name = str(row[0])+'_'+str(row[1])
          write_name = str(row[1])+str(row[5])+'_'+str((int(row[6])/2)+int(row[5]))
          full_paths.append(full_path)
          dem_names.append(dem_name)
          write_names.append(write_name)
    return full_paths,dem_names,write_names  

def basinLists(path):
  with open(path+'_AllBasinsInfo.csv','r') as basincsv:
    basinPandas = pd.read_csv(basincsv,delimiter=',')
    basins = basinPandas["basin_key"]
    basin_list = basins.tolist()
    return basin_list

def getMChiSegmentedPandas(path):
  with open(path+'_MChiSegmented_burned.csv') as mChiSource:
    pandasDF = pd.read_csv(mChiSource, delimiter=',')
    return pandasDF

def mainOperation(full_paths,dem_names,write_names,dem_record,basins,maxs,mins):
  
  #looping through each tile
  for x,y,z in zip(full_paths,dem_names,write_names):
    #getting basin list for tile
    try:
      basin_list = basinLists(x+z)
      pandasDF = getMChiSegmentedPandas(x+z)  
      for a in basin_list:
        max_precip,min_precip = getMaxMin(pandasDF,a)
        dem_record.append(y)
        basins.append(a)
        maxs.append(max_precip)
        mins.append(min_precip)
    except(IOError):
      print("IOError, some info does not exist %s"%(y))
  
  return dem_record,basins,maxs,mins

def scatterPlot(dataFrame):
  
  # Create a figure
  fig = plt.figure(1, figsize=(18,9))

  # Create an axes
  ax = fig.add_subplot(111)
  #plt.ylabel("", fontsize = 24)
  plt.title(("precip_gradient"), fontsize = 32)
  
  # Create the boxplot
  #bp = ax.boxplot(data_to_plot, labels=header_list, showfliers=False)
  bp = dataFrame.plot.scatter(x=[2],y=[3],c='DarkBlue')
  
  plt.tick_params(axis='both', which='major', labelsize=18)
  # Save the figure
  fig.savefig(target+'precip_gradient_scatter.png', bbox_inches='tight')  
  #required to clear the axes. Each call of this function wouldn't do that otherwise.
  plt.cla()

#getting base lists

full_paths,dem_names,write_names = pathCollector(target,'himalaya_processed')
full_paths_b,dem_names_b,write_names_b = pathCollector(target,'himalaya_b_processed')

dem_record = []
basins = []
maxs = []
mins = []

dem_record,basins,maxs,mins = mainOperation(full_paths,dem_names,write_names,dem_record,basins,maxs,mins)

dem_record,basins,maxs,mins = mainOperation(full_paths_b,dem_names_b,write_names_b,dem_record,basins,maxs,mins)



demDF = pd.Series(dem_record)
basinDF = pd.Series(basins)
maxDF = pd.Series(maxs)
minDF = pd.Series(mins)

print demDF,basinDF,maxDF,minDF
export_DF = pd.concat([demDF,basinDF,maxDF,minDF],axis=1)
export_DF.to_csv(target+'precip_gradient_data_first_last.csv',mode='w',header=True,index=False)
scatterPlot(export_DF)