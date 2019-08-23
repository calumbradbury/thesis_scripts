#matplotlib pyplot hist2D
#windows concavity catcher test
import pandas as pd
import csv
import os
import sys

import matplotlib
matplotlib.use('Agg')



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

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/raw/'


                                                                                                                                        
def writeHeader(file_name,target_name):
    with open(file_name,'r') as sourceheader_csv:
        pandasDF=pd.read_csv(sourceheader_csv,delimiter=',')
        header_list = pandasDF.columns.values.tolist()
  
    with open(target_name,'wb') as writeheader_csv:
        csvWriter = csv.writer(writeheader_csv,delimiter = ',')
        csvWriter.writerow(header_list)

def countLength(DF):
    #counts length of DF, usefull to get number of nodes
    series=DF['basin_key']
    series_list = series.tolist()
    length = len(series_list)
    return length

def exportBasinDF(DF,basin_key,export_to,count_nodes=False):
    print("opened export function")
    #exports basin data from desired DF to output
    selectedDF = DF[DF['basin_key'] == basin_key]
    print("selected DF")
    print target+export_to+'.csv'
    #print selectedDF
    try:
        selectedDF.to_csv(export_to+'.csv',mode='a',header=False,index=False)
    except Exception as e:
        print e
    print "exported"
    if count_nodes:
        length = countLength(selectedDF)
        return length
    
def openPandas(path,name):
    #opens and returns pandasDF
    dataFrame = pd.read_csv(path+'/'+name+'.csv',delimiter=',')
    return dataFrame
    
def basinsWithDesiredConcavity(full_path,write_name,concavity):
    #returns a list of basins with the desired concavity
    write_name = '/'+write_name
    #reading in the basin info
    BasinDF = Helper.ReadMCPointsCSV(full_path,write_name)  
    #Getting mn data
    PointsDF = MN.GetMOverNRangeMCPoints(BasinDF,start_movern=0.1,d_movern=0.05,n_movern=18)
    #selecting by concavity
    selectedDF = PointsDF[PointsDF["Median_MOverNs"] == concavity]
    concavitySeries = selectedDF["basin_key"]
    concavityList = concavitySeries.tolist()
    return concavityList
    
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
        
def addNewBasinKey(DF,basin_list,to_export):
    basinDF = pd.DataFrame({'new_keys':basin_list})
    mergedDF = pd.merge(left=DF,right=basinDF, left_index=True,right_index=True) 
    mergedDF = mergedDF.rename(columns={"basin_key": "old_key","new_keys":"basin_key"})
    mergedDF = mergedDF.drop(['old_key'],axis=1)
    mergedDF.to_csv(to_export+'.csv',mode='w',index=False,header=True)



names = ['himalaya_processed','himalaya_b_processed','himalaya_c_processed']

basin_tracker = 0
new_basin_list = []
movern_node_counter = []
fullstats_node_counter = []


for name in names:

    full_paths,dem_names,write_names = pathCollector(target,name)    
    
    c = '0.4'    
    for d,e in zip(full_paths,write_names):
        if not os.path.isfile(target+'/'+c+'_burned_movern.csv'):
            try:
                writeHeader(file_name=d+'/'+e+'_burned_movern.csv',target_name=target+'/'+c+'_burned_movern.csv')
            except:
                print("source for headers not found, looping through lists until one is.",d+'/'+e+'_burned_movern.csv')

        if not os.path.isfile(target+'/'+c+'_movernstats_basinstats.csv'):
            try:
                writeHeader(file_name=d+'/'+e+'_movernstats_basinstats.csv',target_name=target+'/'+c+'_movernstats_basinstats.csv')
            except:
                print("source for headers not found, looping through lists until one is.",d+'/'+e+'_movernstats_basinstats.csv')
                
        if not os.path.isfile(target+'/'+c+'_movernstats_0.35_fullstats.csv'):
            try:
                writeHeader(file_name=d+'/'+e+'_movernstats_0.35_fullstats.csv',target_name=target+'/'+c+'_movernstats_0.35_fullstats.csv')
            except:
                print("source for headers not found, looping through lists until one is.",d+'/'+e+'_movernstats_0.35_fullstats.csv')

    for x,y,z in zip(full_paths,dem_names,write_names):
        try:
            basin_list = basinsWithDesiredConcavity(x,z,float(c))
            print basin_list
            for basin in basin_list:
                new_basin_list.append(basin_tracker)
                basin_tracker+=1
            print new_basin_list
                
            
            try:
                movernDF = openPandas(x,z+'_burned_movern')
            except:
                print("error opening",x,z+'_burned_movern')
            
            try:
                basinstatsDF = openPandas(x,z+'_movernstats_basinstats')
            except:
                print("error opening",x,z+'_movernstats_basinstats')
                       
            try:
                fullstatsDF = openPandas(x,z+'_movernstats_%s_fullstats'%(float(c)))    
            except:
                print("error opening",x,z+'_movernstats_0.35_fullstats')                
            
            for basin in basin_list:
                try:
                    node_count = exportBasinDF(movernDF,basin,target+'/'+c+'_burned_movern',count_nodes=True)  
                    exportBasinDF(basinstatsDF,basin,target+'/'+c+'_movernstats_basinstats')                      
                    test_count = exportBasinDF(fullstatsDF,basin,target+'/'+c+'_movernstats_0.35_fullstats',count_nodes=True)  
                    fullstats_node_counter.append(test_count)
                    movern_node_counter.append(node_count)
                except:
                    print("error exporting data")        
        
        
        except:
            print("problem at %s %s %s concavity %s"%(x,y,z,float(c)))

print len(movern_node_counter)
print len(new_basin_list)
print sum(movern_node_counter)

movern_new_list = []
fullstats_new_list = []

for x,y in zip(new_basin_list,movern_node_counter):
    new_list = [x]*y

    movern_new_list.extend(new_list)
        
    print movern_new_list[-1]

for x,y in zip(new_basin_list,fullstats_node_counter):
    new_list = [x]*y

    fullstats_new_list.extend(new_list)
        
    print fullstats_new_list[-1]
print movern_new_list
print len(movern_new_list)
        

movernDF = openPandas(target,'/'+c+'_burned_movern')
basinstatsDF = openPandas(target,'/'+c+'_movernstats_basinstats')
fullstatsDF = openPandas(target,'/'+c+'_movernstats_0.35_fullstats')


addNewBasinKey(movernDF,movern_new_list,target+'/'+c+'_burned_movern')
addNewBasinKey(basinstatsDF,new_basin_list,target+'/'+c+'_movernstats_basinstats')
addNewBasinKey(fullstatsDF,fullstats_new_list,target+'/'+c+'_movernstats_0.35_fullstats')          
        
               

#for x in new_basin_list:
MN.MakeChiPlotsMLE(target,'0.35',basin_list=new_basin_list, start_movern=0.35, d_movern=0.05, n_movern=1,size_format='ESURF', FigFormat='png',keep_pngs=True,animate=True)



            
            