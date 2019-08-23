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
target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya_5000/'
#output = os.path.join('C:\\output2\\')

disorder = True

#defined globally to ensure continuity
basin_tracker = 0


                                                                                                                                     
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
            

def ksnCatcher(full_path,dem_name,write_name,basin_key,concavity,basins_not_glaciated,new_ID):
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
            print "testing %s %s %s"%(full_path,dem_name,basin_key)
            glaciated = glaciatedTest(glimsSeries)
            
            if glaciated:
                #this should always result in an empty DF
                returnDF = mchiPandas.loc[mchiPandas['glaciated'] == 2]
                return basins_not_glaciated,returnDF
            
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
                    print "\n \n \n \n \n \n",e,"\n \n \n \n \n \n \n"

            if not glaciated:
                basins_not_glaciated.append(basin_key)
                print("got here")
                lister =  selected_DF["node"].tolist()
                print("got here")
                length = len(lister)
                print("got here")
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
                return basins_not_glaciated,selected_DF

    except Exception as e:
        print e
        print("Error, fault in KSN catcher, this tile is probably missing %s %s\n"%(full_path,dem_name))           
        print full_path+dem_name+str(concavity)+'_MChiSegmented_burned.csv'


x_i = 0 

names = ['himalaya_processed','himalaya_b_processed','himalaya_c_processed']

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
    
    m_n_list = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
    #m_n_list = [0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6]
    

    
    for c in m_n_list:
        c = str(c)
        c = c.replace('.','_')
        for d,e in zip(full_paths,dem_names):
            if not os.path.isfile(target+'/'+c+'unique_MChiSegmented_burned.csv'):
                try:
                    writeHeader(file_name=d+'/'+e+c+'_MChiSegmented_burned.csv',target_name=target+c+'unique_MChiSegmented_burned.csv')
                except:
                    print("source for headers not found, looping through lists until one is.",d+'/'+e+c+'_MChiSegmented_burned.csv')

    for x,y,z in zip(full_paths,dem_names,write_names):

        basins_not_glaciated = []
        
        try:
            #full_glaciated = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/himalaya_27_5/27_50_88_20_himalaya_27_5_14/20000/' 
            #name_glaciated = 'himalaya_27_5_14'
            

            basin_keys,concavities,new_IDs = concavityCatcher(x,z)
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
                    basins_not_glaciated,ksnDF = ksnCatcher(x,y,z,a,b,basins_not_glaciated,c)
                    #basins_not_glaciated, ksnDF = ksnCatcher(full_glaciated,y,a,b,basins_not_glaciated)
                    print basins_not_glaciated
                    #print ksnDF["basin_key"]
                    #if ksnDF:
                        #print("Glaciated is %s, exporting basin data"%(glaciated))
                    try:
                        ksnDF.to_csv(target+b+'unique_MChiSegmented_burned.csv',mode='a',header=False,index=False)
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
        except Exception as e:
            print e
            print("ERROR: Problem getting source concavity/basin data. Skipping tile... %s"%(y))
            

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
            