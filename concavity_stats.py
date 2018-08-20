#m/n full dataset stats        
#gets basin list and median concavities for each tile
#appends to new csv
import pandas as pd
import csv
import os
import sys

#LSDTopoTools specific imports
#Loading the LSDTT setup configuration
setup_file = open('chi_automation.config','r')
LSDMT_PT = setup_file.readline().rstrip()
LSDMT_MF = setup_file.readline().rstrip()
Iguanodon = setup_file.readline().rstrip() 
setup_file.close()

sys.path.append(LSDMT_PT)
sys.path.append(LSDMT_MF)
sys.path.append(Iguanodon)

from LSDPlottingTools import LSDMap_MOverNPlotting as MN
from LSDMapFigure import PlottingHelpers as Helper

#target = os.path.join('R:\\','LSDTopoTools','Topographic_projects','full_himalaya')
target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/'
#output = os.path.join('C:\\output2\\')

remove_GLIMS = True

def pathCollector(path,name):
    #returns lists of paths and names
    path = os.path.join(path,name+'.csv')
    with open(path) as csvfile:
        csvReader = csv.reader(csvfile,delimiter=',')
        next(csvReader)
        full_paths = []
        dem_names = []
        write_names = []
        for row in csvReader:
            max_basin = (int(row[6])/2)+int(row[5])
          
            part_1 = str(row[0])
            part_1 = part_1.replace('.','_')
            part_2 = str(("%.2f" %float(row[2])))+'_'+str(("%.2f" %float(row[3])))
            part_2 = part_2.replace('.','_')
      
            full_path = os.path.join(target,part_1,part_2+'_'+part_1+'_'+str(row[1]),str(row[5]))

            dem_name = part_1+'_'+str(row[1])
            write_name = str(row[1])+str(row[5])+'_'+str((int(row[6])/2)+int(row[5]))

            full_paths.append(full_path)       
            dem_names.append(dem_name)
            write_names.append(write_name)
        return full_paths,dem_names,write_names

def concavityCatcher(full_path,write_name):
    #returns the basin_key and median concavity
    write_name = '/'+write_name
    #reading in the basin info
    BasinDF = Helper.ReadMCPointsCSV(full_path,write_name)  
    #Getting mn data
    PointsDF = MN.GetMOverNRangeMCPoints(BasinDF,start_movern=0.25,d_movern=0.05,n_movern=8)
    #extract basin key and concavity as list
    basin_series = PointsDF["basin_key"]
    concavity_series = PointsDF["Median_MOverNs"]
    basin_key = basin_series.tolist()
    basin_keys = []
    for x in basin_key:
        x = int(x)
        basin_keys.append(x)
    
    concavities = concavity_series.tolist()
    #print basin_keys
    return basin_keys,concavities
    
def getBasinLatLon(full_path,write_name):
    #print "opened function"
    #print full_path+write_name+'_AllBasinsInfo.csv'
    with open(full_path+'/'+write_name+'_AllBasinsInfo.csv','r') as basinInfo:
        #print "opened csv"
        basinDF = pd.read_csv(basinInfo,delimiter=',')
        lat = basinDF['outlet_latitude']
        lon = basinDF['outlet_longitude']
        lat_list = lat.tolist()
        lon_list = lon.tolist()
        #print lat_list,lon_list
        return lat_list,lon_list

def getDisorderConcavity(full_path,write_name):
    with open(full_path+'/'+write_name+'_fullstats_disorder_uncert.csv','r') as disorderInfo:
        disorderDF = pd.read_csv(disorderInfo,delimiter=',')
        disorderConcavity = disorderDF[' best_fit_for_all_tribs']
        disorder_list = disorderConcavity.tolist()
        corrected_disorder = []
        for x in disorder_list:
            correct = "%.2f" %float(x)
            corrected_disorder.append(correct) 
        return corrected_disorder
    
def countConcavity(dataFrame,concavity):
    concavityFrame = dataFrame[dataFrame['concavity_bootstrap'] == concavity]
    concavitySeries = concavityFrame['concavity_bootstrap']
    to_list = concavitySeries.tolist()
    disorder_concavity = "%.2f" %float(concavity) 
    disorderFrame = dataFrame[dataFrame['concavity_disorder'] == concavity]
    disorderSeries = disorderFrame['concavity_disorder']
    disorder_list = disorderSeries.tolist()
    with open(target+'/'+'full_concavity_sumamry.csv','a') as csvwrite:
        csvWriter = csv.writer(csvwrite,delimiter=',')
        csvWriter.writerow((concavity,len(to_list),len(disorder_list)))
    print "There are bootstrap %s, disorder %s basins with a concavity of %s"%(len(to_list),len(disorder_list),concavity)
    
  

names = ['himalaya_processed','himalaya_b_processed','himalaya_c_processed']

if os.path.isfile(target+'full_concavity_basins_summary.csv'):
    os.remove(target+'full_concavity_basins_summary.csv')    

with open(target+'full_concavity_basins_summary.csv','wb') as writeCSV:
    csvWriter = csv.writer(writeCSV,delimiter=',')
    csvWriter.writerow(['latitude','longitude','basin_key','concavity_bootstrap','concavity_disorder'])

error_log = []

for name in names:

    full_paths,dem_names,write_names = pathCollector(target,name)
    
    for x,y,z in zip(full_paths,dem_names,write_names):
        try: 
         #   print x,z
            corrected_disorder = getDisorderConcavity(x,z)
            basin_lat,basin_lon = getBasinLatLon(x,z)
            
            
            basin_keys,concavities = concavityCatcher(x,z)
        #except:
        #  print("Failed to find basin keys and concavities...")
            lat_Series = pd.Series(basin_lat)
            lon_Series = pd.Series(basin_lon)
            basin_Series = pd.Series(basin_keys)
            concavity_Series = pd.Series(concavities)  
            disorder_Series = pd.Series(corrected_disorder)  
            #print basin_Series
            #print concavity_Series
            
            #basin_Series.reset_index(drop=True, inplace=True)
            #concavity_Series.reset_index(drop=True, inplace=True)
            
            DF = pd.concat([lat_Series,lon_Series,basin_Series,concavity_Series,disorder_Series],axis=1)
            #print("printing DF")
            print DF
            DF.to_csv(target+'full_concavity_basins_summary.csv',mode='a',header=False,index=False)                                       
        except:
            #logging error
            error_log.append(x+z)            
            print("No data at %s %s"%(x,z))

with open(target+'full_concavity_basins_summary.csv','r') as summaryCSV:
  summary_DF = pd.read_csv(summaryCSV,delimiter=',')
  concavity_series = summary_DF["concavity_bootstrap"]
  dis_series = summary_DF["concavity_disorder"]
  print concavity_series.median()
  print dis_series.median()
  lister = concavity_series.tolist()
  lister_b = dis_series.tolist()
  print len(lister) 
  print len(lister_b)
  countConcavity(summary_DF,0.1)
  countConcavity(summary_DF,0.15)
  countConcavity(summary_DF,0.2)
  countConcavity(summary_DF,0.25)
  countConcavity(summary_DF,0.3)
  countConcavity(summary_DF,0.35)
  countConcavity(summary_DF,0.4)
  countConcavity(summary_DF,0.45)
  countConcavity(summary_DF,0.5)
  countConcavity(summary_DF,0.55)
  countConcavity(summary_DF,0.6)
  countConcavity(summary_DF,0.65)
  countConcavity(summary_DF,0.7)
  countConcavity(summary_DF,0.75)
  countConcavity(summary_DF,0.8)
  countConcavity(summary_DF,0.85)
  countConcavity(summary_DF,0.9)
  countConcavity(summary_DF,0.95)
  #print summary_DF
  
print error_log