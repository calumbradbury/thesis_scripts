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

remove_GLIMS = False

disorder = True
                                                                                                                                        
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


def getDisorderConcavity(full_path,write_name,fromConcavityCatcher=False):
    with open(full_path+'/'+write_name+'_fullstats_disorder_uncert.csv','r') as disorderInfo:
        
        #part of glacier removal
        disorderDF = pd.read_csv(disorderInfo,delimiter=',')
                     
        
        disorderConcavity = disorderDF[' best_fit_for_all_tribs']
        disorder_list = disorderConcavity.tolist()
        corrected_disorder = []
        for x in disorder_list:
            correct = "%.2f" %float(x)
            correct = correct.replace('0','')
            correct = correct.replace('.','0.')
            corrected_disorder.append(correct) 
            
        if not fromConcavityCatcher:
            return corrected_disorder

        if fromConcavityCatcher:            
            basin_series = disorderDF["basin_key"]
            basin_key = basin_series.tolist()
            basin_keys = []
            for x in basin_key:
                x = int(x)
                basin_keys.append(x)
            return basin_keys, corrected_disorder


def concavityCatcher(full_path,write_name,processed=False):
    #returns the basin_key and median concavity
    write_name = '/'+write_name
    #reading in the basin info
    BasinDF = Helper.ReadMCPointsCSV(full_path,write_name)  
    #Getting mn data
    PointsDF = MN.GetMOverNRangeMCPoints(BasinDF,start_movern=0.1,d_movern=0.05,n_movern=18)
    #extract basin key and concavity as list
    basin_series = PointsDF["basin_key"]
    concavity_series = PointsDF["Median_MOverNs"]
        
    if not disorder:    
        basin_key = basin_series.tolist()
        basin_keys = []
        for x in basin_key:
            x = int(x)
            basin_keys.append(x)
    
        concavities = concavity_series.tolist()
        
    if disorder:
        print full_path,write_name
        basin_keys,concavities = getDisorderConcavity(full_path,write_name,fromConcavityCatcher = True)
    
    if not processed:
        return basin_keys,concavities
    
    if processed:
        #processed_concavities = []
        #print("this is the processed DF")
        #print processedDF
        processed_basin = processedDF["basin_key"]
        processed_concavity = processedDF["Median_MOverNs"]
        basin_list = processed_basin.tolist()
        concavity_list = processed_concavity.tolist()
        return basin_list,concavity_list
  
  
def getBasinLatLon(full_path,write_name):
    #print "opened function"
    #print full_path+write_name+'_AllBasinsInfo.csv'
    with open(full_path+'/'+write_name+'_AllBasinsInfo.csv','r') as basinInfo:

        #part of glacier removal
        
        basinDF = pd.read_csv(basinInfo,delimiter=',')
           
        
        lat = basinDF['outlet_latitude']
        lon = basinDF['outlet_longitude']
        lat_list = lat.tolist()
        lon_list = lon.tolist()
        #print lat_list,lon_list
        return lat_list,lon_list


    
def countConcavity(dataFrame,concavity):
    concavityFrame = dataFrame[dataFrame['concavity_bootstrap'] == concavity]
    concavitySeries = concavityFrame['concavity_bootstrap']
    to_list = concavitySeries.tolist()
    disorder_concavity = "%.2f" %float(concavity) 
    disorderFrame = dataFrame[dataFrame['concavity_disorder'] == concavity]
    disorderSeries = disorderFrame['concavity_disorder']
    disorder_list = disorderSeries.tolist()
    with open(target+'/'+'concavity_bootstrap_summary.csv','a') as csvwrite:
        csvWriter = csv.writer(csvwrite,delimiter=',')
        csvWriter.writerow((concavity,len(to_list),len(disorder_list)))
    print "There are bootstrap %s, disorder %s basins with a concavity of %s"%(len(to_list),len(disorder_list),concavity)


            

def ksnCatcher(full_path,dem_name,basin_key,concavity):
  #returns dataframe with mchi(ksn) for each basin based on the correct concavity
    try:
        with open(full_path+'/'+dem_name+str(concavity)+'_MChiSegmented_burned.csv','r') as mChicsv:
       
            mchiPandas = pd.read_csv(mChicsv,delimiter=',')
            selectedDF = mchiPandas.loc[mchiPandas['basin_key'] == int(basin_key)]
            print "testing %s %s %s"%(full_path,dem_name,basin_key)
            return selectedDF
    except Exception as e: 
        print e
        print("Error, fault in KSN catcher, this tile is probably missing %s %s\n"%(full_path,dem_name))           
        print full_path+dem_name+str(concavity)+'_MChiSegmented_burned.csv'


x_i = 0 

names = ['himalaya_processed','himalaya_b_processed','himalaya_c_processed']
tiles_skipped =[]
tiles_error = []
for name in names:

    full_paths,dem_names,write_names = pathCollector(target,name)
    #testing to see if output files exist:
    
    #full_paths = ['/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/himalaya_27_5/27_50_88_20_himalaya_27_5_14/20000/']
    #dem_names = ['himalaya_27_5_14']
    #write_names = ['1420000_35000']
    
    
    
    m_n_list = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
    #m_n_list = [0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6]
    

    
    for c in m_n_list:
        c = str(c)
        c = c.replace('.','_')
        for d,e in zip(full_paths,dem_names):
            if not os.path.isfile(target+'/'+'raw/'+c+'_ex_MChiSegmented_burned.csv'):
                try:
                    writeHeader(file_name=d+'/'+e+c+'_MChiSegmented_burned.csv',target_name=target+'raw/'+c+'_ex_MChiSegmented_burned.csv')
                except:
                    print("source for headers not found, looping through lists until one is.",d+'/'+e+c+'_MChiSegmented_burned.csv')

    for x,y,z in zip(full_paths,dem_names,write_names):
        
        
        
        try:


            basin_keys,concavities = concavityCatcher(x,z)

            
            #testing length of strings provides a basic error control
            if len(basin_keys) == len(concavities):
                print("got basin key list and concavity list, lengths match so going ahead and collecting corresponding ksn data")
                for a,b in zip(basin_keys,concavities):
                    b = str(b)
                    b = b.replace('.','_')
                    ksnDF = ksnCatcher(x,y,a,b)


                    try:
                        ksnDF.to_csv(target+'raw/'+b+'_ex_MChiSegmented_burned.csv',mode='a',header=False,index=False)
                        print("saving to...",target+b+'_ex_MChiSegmented_burned.csv')
                        print("got data for %s %s %s"%(y,a,b))
                    except:
                        print("ERROR: problem exporting dataframe to csv at %s %s %s"%(y,a,b))
                        tiles_error.append(y)
            else:
              print("basin key/concavity strings are not an equal length")
            print x_i
            x_i+=1

        except:
            print("ERROR: Problem getting source concavity/basin data. Skipping tile... %s"%(y))
            tiles_skipped.append(y)
            
print tiles_skipped
print tiles_error
            
          