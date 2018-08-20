#matplotlib pyplot hist2D
#windows concavity catcher test
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
                                                                                                                                        
def writeHeader(file_name,target_name):
    with open(file_name,'r') as sourceheader_csv:
        pandasDF=pd.read_csv(sourceheader_csv,delimiter=',')
        header_list = pandasDF.columns.values.tolist()
  
    with open(target_name,'wb') as writeheader_csv:
        csvWriter = csv.writer(writeheader_csv,delimiter = ',')
        csvWriter.writerow(header_list)


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

def concavityCatcher(full_path,write_name,processed=False,basins_not_glaciated=[]):
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
    
    if not processed:
        return basin_keys,concavities
    
    if processed:
        #processed_concavities = []
        #for x in basins_not_glaciated:
        processedDF = PointsDF[PointsDF.basin_key.isin(basins_not_glaciated)]
        print("this is the processed DF")
        print processedDF
        if basin_key != basins_not_glaciated:
            sys.exit()        
  
  
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
    with open(target+'/'+'concavity_summary.csv','a') as csvwrite:
        csvWriter = csv.writer(csvwrite,delimiter=',')
        csvWriter.writerow((concavity,len(to_list),len(disorder_list)))
    print "There are bootstrap %s, disorder %s basins with a concavity of %s"%(len(to_list),len(disorder_list),concavity)





def glaciatedTest(pandasSeries):
    list = pandasSeries.tolist()
    for x in list:
        if x == 1:
            print("glaciation detected")
            return True
    print("no glaciation detected")
    return False
            

def ksnCatcher(full_path,dem_name,basin_key,concavity,basins_not_glaciated):
  #returns dataframe with mchi(ksn) for each basin based on the correct concavity
    try:
        with open(full_path+'/'+dem_name+str(concavity)+'_MChiSegmented_burned.csv','r') as mChicsv:
       
            mchiPandas = pd.read_csv(mChicsv,delimiter=',')
            selected_DF = mchiPandas.loc[mchiPandas['basin_key'] == int(basin_key)]
            glimsSeries = selected_DF['glaciated']
            #glims_glaciated = glimsSeries.loc[glimsSeries['glaciated'] == 1] 
            #glims_list = glims_glaciated.tolist()
            #print len(glims_list)
            #print glims_glaciated
            glaciated = glaciatedTest(glimsSeries)
            if not glaciated:
                basins_not_glaciated.append(basin_key)
                return basins_not_glaciated,selected_DF
      
    except:
        print("Error, fault in KSN catcher, this tile is probably missing %s %s\n"%(full_path,dem_name))           
        print full_path+dem_name+str(concavity)+'_MChiSegmented_burned.csv'


x_i = 0 

names = ['himalaya_processed','himalaya_b_processed','himalaya_c_processed']

for name in names:

    full_paths,dem_names,write_names = pathCollector(target,name)
    #testing to see if output files exist:
    m_n_list = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
    #m_n_list = [0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6]

    for c in m_n_list:
        c = str(c)
        c = c.replace('.','_')
        for d,e in zip(full_paths,dem_names):
            if not os.path.isfile(target+'/'+c+'_ex_MChiSegmented_burned.csv'):
                try:
                    writeHeader(file_name=d+'/'+e+c+'_MChiSegmented_burned.csv',target_name=target+c+'_ex_MChiSegmented_burned.csv')
                except:
                    print("source for headers not found, looping through lists until one is.",d+'/'+e+c+'_MChiSegmented_burned.csv')

    for x,y,z in zip(full_paths,dem_names,write_names):
        try:
            full_glaciated = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/himalaya_27_5/27_50_88_20_himalaya_27_5_14/20000/' 
            name_glaciated = 'himalaya_27_5_14'
            
            basins_not_glaciated = [] 
            #basin_keys,concavities = concavityCatcher(x,z)
            basin_keys,concavities = concavityCatcher(full_glaciated,name_glaciated)
            
            #testing length of strings provides a basic error control
            if len(basin_keys) == len(concavities):
                print("got basin key list and concavity list, lengths match so going ahead and collecting corresponding ksn data")
                for a,b in zip(basin_keys,concavities):
                    b = str(b)
                    b = b.replace('.','_')
                    #basins_not_glaciated, ksnDF = ksnCatcher(x,y,a,b,basins_not_glaciated)
                    basins_not_glaciated, ksnDF = ksnCatcher(full_glaciated,y,a,b,basins_not_glaciated)
                    #print basins_not_glaciated
                    #print ksnDF["basin_key"]
                    try:
                        ksnDF.to_csv(target+b+'_ex_MChiSegmented_burned.csv',mode='a',header=False,index=False)
                        print("saving to...",target+b+'_ex_MChiSegmented_burned.csv')
                        print("got data for %s %s %s"%(y,a,b))
                    except:
                        print("ERROR: problem exporting dataframe to csv at %s %s %s"%(y,a,b))
            else:
              print("basin key/concavity strings are not an equal length")
            print x_i
            x_i+=1
            try:
                print basins_not_glaciated
            except:
                print "printing error"
        except:
            print("ERROR: Problem getting source concavity/basin data. Skipping tile... %s"%(y))
            
            
        try: 
         #   print x,z
            #corrected_disorder = getDisorderConcavity(x,z)
            #basin_lat,basin_lon = getBasinLatLon(x,z)
            
            corrected_disorder = getDisorderConcavity(full_glaciated,name_glaciated)
            basin_lat,basin_lon = getBasinLatLon(full_glaciated,name_glaciated)
            
            
            #concavities = concavityCatcher(x,z,processed=True,basins_not_glaciated=basins_not_glaciated)
            concavities = concavityCatcher(full_glaciated,name_glaciated,processed=True,basins_not_glaciated=basins_not_glaciated)
            
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
            DF.to_csv(target+'concavity_basins_summary_processed.csv',mode='a',header=False,index=False)                                       
        except:
            print("No data at %s %s"%(full_glaciated,name_glaciated))
            
with open(target+'concavity_basins_summary.csv','r') as summaryCSV:
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
            