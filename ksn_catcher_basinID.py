#VERSION INCLUDING BASIN KEY MODIFICATION

#20/06
#adding control to check csv exports maintain the same number of headers
#error checking

#matplotlib pyplot hist2D
#windows concavity catcher test
import pandas as pd
import csv
import os
import sys
import glob

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

#====================
##  User Variables ##
#====================

delta_m_n = 0.1
start_m_n = 0.1
target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/0_1_5000m/'
export_suffix = '_MChiSegmented_Full.csv'

#====================
## /User Variables ##
#====================

total_iterations = (1.0-start_m_n)/delta_m_n
#must be integer???
total_iterations = float(total_iterations)



#For operations in Windows
#target = os.path.join('C:\\','Users','calum','Desktop','LSDTopoTools','Topographic_projects','full_himalaya')
#output = os.path.join('C:\\output2\\')

#=======================
## Removing old files ##
#=======================

try:
    remove_a = glob.glob(target+'*'+export_suffix)
    remove_b = glob.glob(target+'*'+'AllBasinsInfo.csv')
except:
    #will return empty list if no files are present
    print("Directory Error, exiting")
    sys.exit()

to_remove =[]

if remove_a:
    for x in remove_a:
        to_remove.append(x)
        
if remove_b:
    for x in remove_b:
        to_remove.append(x)

print to_remove

if not remove_a and not remove_b:
    print("Nothing to remove.")
        
for path in to_remove:
    print("removing...",path)
    try:
        os.remove(path)
    except:
        print("Error removing - ",path)
try:
    os.remove(target+'errorLog.txt')
except:
    print("no error log to remove.")    
    
try:
    os.remove(target+'concavity_bootstrap_basins_summary_processed.csv')
except:
    print("no concavity bootstrap to remove")
    
try:
    os.remove(target+'0.1_disorder.csv')
except:
    print("no 0.1_disorder to remove")

try:
    os.remove(target+'0.1_low_disorder_stat_ex_MChiSegmented_burned.csv')
except:
    print("no disorder_stat_ex to remove")
    
try:
    os.remove(target+'concavity_bootstrap_summary.csv')
except:
    print("no concavity_bootstrap_summary to remove")
    

    
disorder = True

#defined globally to ensure continuity
basin_tracker = 0

def logWriter(to_write):
    with open(target+'errorLog.txt','a') as log:
        write_log = log.write(str(to_write)+'\n')

logWriter(total_iterations)

def getHeaderList(to_open):
    with open(to_open,'r') as csvFile:
        csv = pd.read_csv(csvFile,delimiter=',')
        return csv.columns.values.tolist()
                                                                                                                                     
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


def compareColumns(df,max_column):
    #tests whether the column is the max in the DF. Testing MLE assignment of 0.1 concavity.
    print "opened compareColumns"
    print df
    print max_column
    series = df[max_column]
    print series
    to_list = series.tolist()
    
    if to_list[0] > float(50):
        print "logic success"
        #sys.exit()
        return False
        
    print "logic success"
    print to_list[0]
    return True

def getDisorder(full_path,write_name):

    suffix = '_disorder_basinstats.csv'
    #suffix = '_movernstats_basinstats.csv'
    fname = write_name+suffix
    # read in the dataframe using pandas
    df = pd.read_csv(full_path+'/'+fname)
    return df


        
def getDisorderConcavity(full_path,write_name,basins_not_glaciated=[],fromConcavityCatcher=False,alter_ID=True):
    global basin_tracker
    with open(full_path+'/'+write_name+'_fullstats_disorder_uncert.csv','r') as disorderInfo:
        
        #part of glacier removal
        inputDF = pd.read_csv(disorderInfo,delimiter=',')
        if basins_not_glaciated:
            disorderDF = inputDF[inputDF.basin_key.isin(basins_not_glaciated)]              
        if not basins_not_glaciated:
            disorderDF = inputDF
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
            new_ID=[]
            basin_keys = []
            #for x in basin_key:
            #    x = int(x)
            #    basin_keys.append(x)
            for x in basin_key:
                x = int(x)
                #y = new_ID[-1]
                #y = y+1
                if alter_ID:
                    try:
                        y = x+basin_tracker
                
                    except:
                        print basin_tracker
                        print("basin_tracker error")
                        sys.exit()
                    basin_keys.append(x)
                    new_ID.append(y)
                else:
                    basin_keys.append(x)
            if alter_ID:
                basin_tracker = new_ID[-1]
                #need to add one for debug
                basin_tracker = basin_tracker+1
                return basin_keys, corrected_disorder, new_ID
            else:
                return basin_keys, corrected_disorder
        
def concavityCatcher(full_path,write_name,processed=False,basins_not_glaciated=[],alter_ID = True):
    #returns the basin_key and median concavity
    write_name = '/'+write_name
    #reading in the basin info

    try:
        BasinDF = Helper.ReadMCPointsCSV(full_path,write_name)  
    except Exception as e:
        logWriter("ReadMCPointsCSV error at..."+full_path)
        logWriter(repr(e))
        return
    
    #Getting mn data
    try:
        PointsDF = MN.GetMOverNRangeMCPoints(BasinDF,start_movern=float(start_m_n),d_movern=float(delta_m_n),n_movern=float(total_iterations))
    except Exception as e:
        logWriter("GetMOverNRangeMCPoints error at..."+full_path)
        logWriter(repr(e))
        print(BasinDF)
        sys.exit()
    
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
        print "got to disorder"
        print full_path,write_name
        if not alter_ID:
            basin_keys,concavities = getDisorderConcavity(full_path,write_name,fromConcavityCatcher = True,alter_ID=False)
        else:
            basin_keys,concavities,new_IDs = getDisorderConcavity(full_path,write_name,fromConcavityCatcher = True)
    if not processed:
        print concavities
        return basin_keys,concavities,new_IDs
    
    if processed:
        print "got to processed"
        
        #processed_concavities = []
        #for x in basins_not_glaciated:
        try:
            processedDF = PointsDF[PointsDF.basin_key.isin(basins_not_glaciated)]
        
        except Exception as e:
            print e
            print "error in processed section of concavity catcher"
            
        
        #print("this is the processed DF")

        processed_basin = processedDF["basin_key"]
        processed_concavity = processedDF["Median_MOverNs"]
        basin_list = processed_basin.tolist()
        concavity_list = processed_concavity.tolist()
              
        return basin_list,concavity_list
  
  
def getBasinLatLon(full_path,write_name,basins_not_glaciated):
    #print "opened function"
    #print full_path+write_name+'_AllBasinsInfo.csv'
    with open(full_path+'/'+write_name+'_AllBasinsInfo.csv','r') as basinInfo:

        #part of glacier removal
        inputDF = pd.read_csv(basinInfo,delimiter=',')
        basinDF = inputDF[inputDF.basin_key.isin(basins_not_glaciated)]       
        
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





def glaciatedTest(pandasSeries):
    list = pandasSeries.tolist()
    for x in list:
        if x == 1:
            print("glaciation detected")
            return True
            
    print("no glaciation detected")
    return False

#code to append complete allBasinInfo csv 
def allBasinsInfo(full_path,dem_name,concavity,basin_key,new_ID,glaciated = False):
    
    #skipping append of basin data, this removes glaciated basins from the output AllBasinsInfo.csv
    if glaciated:
        return
    
    try:
        tile = dem_name.split("_")
        print tile

        if os.path.isfile(full_path+'/'+tile[-1]+'20000_35000_AllBasinsInfo.csv'):
            print("AllBasins Exists")
        else:
            print('error in: \n'+full_path+'/'+tile[-1]+'20000_35000_AllBasinsInfo.csv')
        
        with open(full_path+'/'+tile[-1]+'20000_35000_AllBasinsInfo.csv','r') as basinInfo:
            basinPandas = pd.read_csv(basinInfo,delimiter=',')
            
            basinInfoDF = basinPandas.loc[basinPandas['basin_key'] == int(basin_key)]
            basinInfoDF["new_ID"] = new_ID
            print basinInfoDF
            #sys.exit()
    
    
            if os.path.isfile(target+'/'+str(concavity)+'_AllBasinsInfo.csv'): 
                basinInfoDF.to_csv(target+'/'+str(concavity)+'_AllBasinsInfo.csv',mode='a',header=False,index=False)
            else:
                basinInfoDF.to_csv(target+'/'+str(concavity)+'_AllBasinsInfo.csv',mode='a',header=True,index=False)
    except Exception as e:
        print('failed to open AllBasinsInfo')
        logWriter("allBasinsInfo error")
        logWriter(repr(e))  
        sys.exit()  
    ##nothing to return##                  

def ksnCatcher(full_path,dem_name,write_name,basin_key,concavity,basins_not_glaciated,new_ID):
  #returns dataframe with mchi(ksn) for each basin based on the correct concavity
    try:
        with open(full_path+'/'+dem_name+str(concavity)+'_MChiSegmented_burned.csv','r') as mChicsv:         
            mchiPandas = pd.read_csv(mChicsv,delimiter=',')
            selected_DF = mchiPandas.loc[mchiPandas['basin_key'] == int(basin_key)]
            print("here")
            #print(selected_DF)
            #sys.exit()                                                 
            
            try:
                glimsSeries = selected_DF['Glaciated']
            except:
                print("Could not selected Glaciated series. Exiting Process")
                sys.exit()
                
            #print glimsSeries
            #sys.exit()
            #glims_glaciated = glimsSeries.loc[glimsSeries['glaciated'] == 1] 
            #glims_list = glims_glaciated.tolist()
            #print len(glims_list)
            #print glims_glaciated
            print "testing %s %s %s"%(full_path,dem_name,basin_key)
            glaciated = glaciatedTest(glimsSeries)
            try:
                allBasinsInfo(full_path,dem_name,concavity,basin_key,new_ID,glaciated)
            except:
                print("allBasinsError")
                sys.exit()
            
            
            #deprecating
            #if glaciated:
            #   #this should always result in an empty DF
            #    returnDF = mchiPandas.loc[mchiPandas['glaciated'] == 2]
            #    return basins_not_glaciated,returnDF
            
            concavity_float = concavity.replace('_','.')
            
            #attempting to remove anomolous 0.1 concavity basins

            if float(concavity_float) == 0.1:
                try:
                    disorderStatsDF = getDisorder(full_path,str(write_name))
                    selectDisDF = disorderStatsDF.loc[disorderStatsDF['basin_key'] == int(basin_key)]
                    selectDisDF.to_csv(target+'0.1_disorder.csv',mode='a',header=False,index=False)
                    #should be false if a discontinuity in disorder is detected
                    is_real_concavity = compareColumns(selectDisDF,'m_over_n = 0.1')
                    if not is_real_concavity:
                        print "False"
                        selected_DF.to_csv(target+'0.1_low_disorder_stat_ex_MChiSegmented_burned.csv',mode='a',header=False,index=False)
                        
                except Exception as e:
                    #old exception argument, leave as is.
                    print "\n \n \n \n \n \n",e,"\n \n \n \n \n \n \n"

            if not glaciated:
                basins_not_glaciated.append(basin_key)
                #print("got here")
                lister =  selected_DF["basin_key"].tolist()
                #print("got here")
                length = len(lister)
                print("got here")
                print selected_DF["basin_key"]
                print lister
                new_IDs = []
                print length
                for x in range(0,length):
                    #print x
                    
                    new_IDs.append(new_ID)

                #add_ID = [new_ID]
                selected_DF["new_ID"] = new_IDs
                #print("got here")
                #print selected_DF
                #print new_IDs
                #sys.exit()
                #insert code for allbasinsinfo here
                
            return basins_not_glaciated,selected_DF,glaciated

    except Exception as e:
        #old exception argument, leave as is.
        print e
        print("Error, fault in KSN catcher, this tile is probably missing %s %s\n"%(full_path,dem_name))           
        print full_path+dem_name+str(concavity)+'_MChiSegmented_burned.csv'

          

x_i = 0 

names = ['himalaya_processed','himalaya_b_processed','himalaya_c_processed']
#Windows Edit
#names = ['himalaya_b_processed']

with open(target+'concavity_bootstrap_basins_summary_processed.csv','wb') as writeCSV:
    csvWriter = csv.writer(writeCSV,delimiter=',')
    csvWriter.writerow(['latitude','longitude','basin_key','concavity_bootstrap','concavity_disorder'])

ID_dict = []
for name in names:

    full_paths,dem_names,write_names = pathCollector(target,name)
    #testing to see if output files exist:
    
    #full_paths = ['/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/himalaya_27_5/27_50_88_20_himalaya_27_5_14/20000/']
    #dem_names = ['himalaya_27_5_14']
    #write_names = ['1420000_35000']
    
    for x,y,z in zip(full_paths,dem_names,write_names):
        logWriter(y)
        basins_not_glaciated = []
        
        try:
            #full_glaciated = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/himalaya_27_5/27_50_88_20_himalaya_27_5_14/20000/' 
            #name_glaciated = 'himalaya_27_5_14'
            try:
                basin_keys,concavities,new_IDs = concavityCatcher(x,z)
            except Exception as e:
                logWriter("concavityCatcher Error at..."+y)
                logWriter(repr(e))
                logWriter("skipping")
                continue
            print("new ids are:")
            print(new_IDs)
            ID_dict.append(new_IDs)
            #relict#
            #basin_keys,concavities = concavityCatcher(full_glaciated,name_glaciated)
            
            #testing length of strings provides a basic error control
            if len(basin_keys) == len(concavities):
                print("got basin key list and concavity list, lengths match so going ahead and collecting corresponding ksn data")
                for a,b,c in zip(basin_keys,concavities,new_IDs):
                    b = str(b)
                    b = b.replace('.','_')
                    try:
                        basins_not_glaciated,ksnDF,glaciated = ksnCatcher(x,y,z,a,b,basins_not_glaciated,c)
                        #adding logic to skip if glaciation is true.
                        if glaciated:
                            print("Skipping")
                            
                            # for debug #
                            #logWriter(str(glaciated)+'_'+str(a)+'_'+str(c)+'_'+str(b))
                            #print basins_not_glaciated,ksnDF,glaciated
                            # for debug #
                            
                            continue
                    except Exception as e:    
                        logWriter("ksnCatcher Error at..."+y)   
                        logWriter(repr(e))
                        #ksnCatcher errors are not acceptable.
                        #adding logic to continue only if glaciation is true.
                        sys.exit()
                    
                    # for debug #
                    #logWriter(str(glaciated)+'_'+str(a)+'_'+str(c)+'_'+str(b))
                    #sys.exit()
                    
                    #basins_not_glaciated, ksnDF = ksnCatcher(full_glaciated,y,a,b,basins_not_glaciated)
                    print basins_not_glaciated
                    #print ksnDF["basin_key"]
                    #if ksnDF:
                        #print("Glaciated is %s, exporting basin data"%(glaciated))
                    try:
                        #notes 17/3/19
                        #more efficient logic for making sure headers are correct#
                        #this should really have some form of error checking to ensure headers match#
                        #/notes 17/3/19
                        #note 20/06
                        #adding test to check headers match
                        #/notes 20/06
                        if os.path.isfile(target+'/'+b+export_suffix): 
                            print("Exporting to existing csv")
                            #test to check if headers are equal as a list
                            targetCSV = getHeaderList(target+'/'+b+export_suffix)
                            if targetCSV == ksnDF.columns.values.tolist():
                                print("Headers match")
                                ksnDF.to_csv(target+'/'+b+export_suffix,mode='a',header=False,index=False)
                                #sys.exit()
                            else:
                                print("Headers do not match, skipping basin")
                                #sys.exit()
                          
                        else:
                            ksnDF.to_csv(target+'/'+b+export_suffix,mode='a',header=True,index=False)
                        
                        print("saving to...",target+b+export_suffix)
                        print("got data for %s %s %s"%(y,a,b))
                       
                       
                    except Exception as e:                        
                        print("ERROR: problem exporting dataframe to csv at %s %s %s"%(y,a,b))
                        print e
                        sys.exit()
            else:
              print("basin key/concavity strings are not an equal length")
            print x_i
            x_i+=1
            try:
                print basins_not_glaciated
            except:
                print "printing error"
        except Exception as e:
            print e
            logWriter(y)
            print("ERROR: Problem getting source concavity/basin data. Skipping tile... %s"%(y))
            logWriter("ERROR: Problem getting source concavity/basin data."+y)
            logWriter("Exception is:  "+repr(e))
            #logic to force exit if an error unexplained by a failed chi tile occurs.
            if os.path.isfile(x+'/'+y+'0_1_MChiSegmented_burned.csv'):
                print("KSN catcher failed, but chi tile did not. Exiting.")
                sys.exit()
            
        try: 
            print x,z
            
            corrected_disorder = getDisorderConcavity(x,z,basins_not_glaciated,alter_ID = False)
            basin_lat,basin_lon = getBasinLatLon(x,z,basins_not_glaciated)
            
            #corrected_disorder = getDisorderConcavity(full_glaciated,name_glaciated)
            #basin_lat,basin_lon = getBasinLatLon(full_glaciated,name_glaciated)
            
            print "getting concavities"
            basins,concavities = concavityCatcher(x,z,processed=True,basins_not_glaciated=basins_not_glaciated,alter_ID = False)
            print basins,concavities
            
            #concavities = concavityCatcher(full_glaciated,name_glaciated,processed=True,basins_not_glaciated=basins_not_glaciated)
        #except:
        #  print("Failed to find basin keys and concavities...")
            lat_Series = pd.Series(basin_lat)
            lon_Series = pd.Series(basin_lon)
            basin_Series = pd.Series(basins)
            concavity_Series = pd.Series(concavities)  
            disorder_Series = pd.Series(corrected_disorder)  
            #print basin_Series
            #print concavity_Series
            
            #basin_Series.reset_index(drop=True, inplace=True)
            #concavity_Series.reset_index(drop=True, inplace=True)
            
            DF = pd.concat([lat_Series,lon_Series,basin_Series,concavity_Series,disorder_Series],axis=1)
            DF.to_csv(target+'concavity_bootstrap_basins_summary_processed.csv',mode='a',header=False,index=False)                                       
        except Exception as e:
            print e
            
            #print("No data at %s %s"%(x,z))
            
    ##Begin working with AllBasinsInfo files##        
    #cannot be placed here. Must be appended to after each basin!
    #for x,y,z in zip(full_paths,dem_names,write_names):
    

print ID_dict
sys.exit()


with open(target+'concavity_bootstrap_basins_summary_processed.csv','r') as summaryCSV:
  summary_DF = pd.read_csv(summaryCSV,delimiter=',')
  concavity_series = summary_DF["concavity_bootstrap"]
  dis_series = summary_DF["concavity_disorder"]
  print concavity_series.median()
  print dis_series.median()
  lister = concavity_series.tolist()
  lister_b = dis_series.tolist()
  print len(lister) 
  print len(lister_b)
  
  #range has to be integer#
  for m_over_n in range(int(start_m_n*100),100,int(delta_m_n*100)):
      #recasting to float
      m_n = float(m_over_n)/100
      countConcavity(summary_DF,float(m_n))