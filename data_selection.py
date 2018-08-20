# script to select basins from MChiSegmented.csv
# uses an AllBasins.csv file with source_name added to source data
# all csv files must be in the same directory
import csv
import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt



# defined by argparse from terminal line

parser = argparse.ArgumentParser()
parser.add_argument("-dir", "--base_directory", type=str, help="The base directory with the m/n analysis. If this isn't defined I'll assume it's the same as the current directory.")
parser.add_argument("-name","--name",type=str,default='',help="Output prefix name")
parser.add_argument("-burned_MChi","--burned_MChi",type=bool,default=False,help="Use if merging MChi with burned raster data")
parser.add_argument("-TRMM_basin", "--TRMM_basin",type=bool,default=False,help="use when merging output from TRMM anlaysis")
parser.add_argument("-litho_elevation", "--litho_elevation",type=bool,default=False,help="use when merging litho_elevation.csv files")
parser.add_argument("-merge_csv","--merge_csv",type=bool,default=False,help="merge AllBasin, MChi and litho_elevation csv files")
parser.add_argument("-no_summary", "--no_summary", type=bool, default = False, help="use if all AllBasin and MChiSegmented csvs are in same directory and no summary_AllBasins.csv is present.")
parser.add_argument("-stats", "--stats", type=bool, default = False, help="creates basic stats file to make results easier to manage")
inputs = parser.parse_args()

if inputs.name:
  name = inputs.name
else:
  name = ""

if inputs.no_summary:
  sorting_column = "source_name"
else:
  sorting_column = "source_prefix"

path = inputs.base_directory

path_log = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'

mchi = "_MChiSegmented"

if inputs.burned_MChi:
  mchi = mchi + "_burn"
  
#print mchi
  

#checking directory
if not path:
  path = os.getcwd()
  


#basin tracker
x_i = 0



#function to generate output csv files with the correct column headers
def writeHeader(file_name,target_name):
  with open(path+file_name+'.csv','r') as sourceheader_csv:
    pandasDF=pd.read_csv(sourceheader_csv,delimiter=',')
    header_list = pandasDF.columns.values.tolist()
  
    with open(path+name+'_output'+target_name+'.csv','wb') as writeheader_csv:
      csvWriter = csv.writer(writeheader_csv,delimiter = ',')
      csvWriter.writerow(header_list)


#allows merging of csv files output by multiple runs of this script when a summary csv file is not present.
#this creates a summary file following the same format.
if inputs.no_summary:
  with open(path+'summary_AllBasins.csv','wb') as csvfile:
    csvWriter = csv.writer(csvfile, delimiter = ',')
    csvWriter.writerow(('latitude','longitude','outlet_longitude','outlet_longitude','outlet_junction','basin_key','source_name'))

  for file in os.listdir(path):
    if file.endswith("AllBasinsInfo.csv"):
      print file
      with open(path+file, 'r') as csvfile:
        csvReader = csv.reader(csvfile, delimiter = ',')
        
        next(csvReader)
        #stripping file string
        file = file.replace('_AllBasinsInfo.csv','')
        print file
        
        for row in csvReader:
          row.append(file)
          with open(path+'summary_AllBasins.csv','a') as csvfile:
            csvWriter = csv.writer(csvfile,delimiter = ',')
            csvWriter.writerow((row))
  #this step prevents the file being read again by the loop
  os.rename(path+'summary_AllBasins.csv',path+'summary_AllBasinsInfo.csv')
  
            
#sorting summary_AllBasinsInfo csv by source name to maintain consistency in basin_key assigniment
if inputs.merge_csv:
  #if not inputs.no_summary:
  with open(path+'summary_AllBasinsInfo.csv','r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    outputDF = pandasDF.sort_values(by=[sorting_column,"basin_key"])
    #enable to help debug
    #print outputDF
    outputDF.to_csv(path+"summary_sorted_AllBasinsInfo.csv", mode="w",header=True,index=False)
    
  #opening AllBasins.csv to generate matching MChiSegmented 
  with open(path+'summary_sorted_AllBasinsInfo.csv', 'r') as csvfile_C:
    csvReader_C = csv.reader(csvfile_C, delimiter = ',')
    next(csvReader_C)
    for row in csvReader_C:                                           
    # use row[6] to open MChiSegmented  
      latitude = row[0]
      longitude = row[1]
      outlet_latitude = row[2]
      outlet_longitude = row[3]
      outlet_junction = row[4]
      basin_key = row[5]
      basin_key = int(basin_key)
      source_name = row[6]
    
      #checking all required files are present:
      
      MChiSegmented = os.path.isfile(path+source_name+mchi+'.csv')
      #print path+source_name+mchi+'.csv'
      litho_elevation = os.path.isfile(path+source_name+'_litho_elevation.csv')
      #checking if disorder stats csvs are present
      fullstats_disorder = os.path.isfile(path+source_name+'_fullstats_disorder_uncert.csv')
      disorder_basinstats = os.path.isfile(path+source_name+'_disorder_basinstats.csv')

      if inputs.TRMM_basin:
        litho_elevation = True       

      if MChiSegmented and litho_elevation and fullstats_disorder and disorder_basinstats:
        
        with open(path_log+'merge_log.txt', 'a') as param:
          param.write(source_name+' OK, starting to merge \n')
        
        #checking for/generating output files
        if not os.path.isfile(path+name+'_output'+mchi+'.csv'):
          writeHeader(file_name=source_name+mchi,target_name=mchi) 
        
        if not os.path.isfile(path+name+'_output_fullstats_disorder_uncert.csv'):
          writeHeader(file_name=source_name+'_fullstats_disorder_uncert',target_name='_fullstats_disorder_uncert')                                                                                                 
        
        if not os.path.isfile(path+name+'_output_disorder_basinstats.csv'):
          writeHeader(file_name=source_name+'_disorder_basinstats',target_name='_disorder_basinstats')           
        
        if not os.path.isfile(path+name+'_output_AllBasinsInfo.csv'):
          writeHeader(file_name='summary_AllBasinsInfo',target_name='_AllBasinsInfo')     
        
                  
        #read into pandas dataframe to allow easy selection using column value
        with open(path+source_name+mchi+'.csv', 'r') as csvfile_D:
          pandasDF = pd.read_csv(csvfile_D, delimiter = ',')
          selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_key]
          #reassigning basin_key
          selected_DF.loc[selected_DF.basin_key == basin_key, 'basin_key'] = x_i
          #append to MChiSegemnted.csv
          #print selected_DF
          selected_DF.to_csv(path+name+'_output'+mchi+'.csv',mode='a',header=False,index=False)     
          with open(path_log+'merge_log.txt', 'a') as param:
            param.write(source_name+' OK, merged MChi \n')
    
        #write corrected output_AllBasins.csv
        with open(path+name+'_output_AllBasinsInfo.csv', 'a') as csvfile_E:
          csvReader_D = csv.writer(csvfile_E, delimiter = ',')
          csvReader_D.writerow((latitude,longitude,outlet_latitude,outlet_longitude,outlet_junction,x_i))
      
        ##INCORPORATING DISORDER STATS####
        if fullstats_disorder:
          #print source_name+'_fullstats_disorder_uncert.csv present, attempting to merge'
          #read into pandas dataframe to allow easy selection using column value
          with open(path+source_name+'_fullstats_disorder_uncert.csv', 'r') as csvfile_F:
            pandasDF = pd.read_csv(csvfile_F, delimiter = ',')
            selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_key]
            #reassigning basin_key
            selected_DF.loc[selected_DF.basin_key == basin_key, 'basin_key'] = x_i
            #append to _fullstats_disorder_uncert.csv
            #print selected_DF
            selected_DF.to_csv(path+name+'_output_fullstats_disorder_uncert.csv',mode='a',header=False,index=False)   
            
            with open(path_log+'merge_log.txt', 'a') as param:
              param.write(source_name+' OK, merged _fullstats_disorder_uncert \n')
           
        if disorder_basinstats:
          #print source_name+'_disorder_basinstats.csv present, attempting to merge'
          #read into pandas dataframe to allow easy selection using column value
          with open(path+source_name+'_disorder_basinstats.csv', 'r') as csvfile_G:
            pandasDF = pd.read_csv(csvfile_G, delimiter = ',')        
            selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_key]
            #reassigning basin_key
            selected_DF.loc[selected_DF.basin_key == basin_key, 'basin_key'] = x_i
            #append to _disorder_basinstats.csv
            #print selected_DF
            selected_DF.to_csv(path+name+'_output_disorder_basinstats.csv',mode='a',header=False,index=False)           
            
            with open(path_log+'merge_log.txt', 'a') as param:
              param.write(source_name+' OK, merged _disorder_basinstats \n')
        
        
        #writing litho_elevation.csv
    
        if inputs.litho_elevation:
          
          #checking/generating output csv file
          if not os.path.isfile(path+name+'_output_litho_elevation.csv'):
            writeHeader(file_name=source_name+'_litho_elevation',target_name='_litho_elevation')   
        
          with open(path+source_name+'_litho_elevation.csv','r') as csvfile:
            pandasDF = pd.read_csv(csvfile,delimiter=',')
            selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_key]
            #reassigning basin_key
            selected_DF.loc[selected_DF.basin_key == basin_key, 'basin_key'] = x_i
            selected_DF.to_csv(path+name+'_output_litho_elevation.csv',mode='a',header=False,index=False)
            with open(path_log+'merge_log.txt', 'a') as param:
              param.write(source_name+' OK, merged _litho_elevation \n')
         
        if inputs.TRMM_basin:
          
          #checking/generating output csv file
          if not os.path.isfile(path+name+'_basin_TRMM.csv'):
            writeHeader(file_name=source_name+'_basin_TRMM',target_name='_basin_TRMM')           
          
          with open(path+source_name+'_basin_TRMM.csv','r') as csvfile:
            pandasDF = pd.read_csv(csvfile,delimiter=',')
            selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_key]
            #reassigning basin_key
            selected_DF.loc[selected_DF.basin_key == basin_key, 'basin_key'] = x_i
            selected_DF.to_csv(path+name+'_output_basin_TRMM.csv',mode='a',header=False,index=False)  
            with open(path_log+'merge_log.txt', 'a') as param:
              param.write(source_name+' OK, merged basin_TRMM \n')
          
          #csvReader = csv.reader(csvfile,delimiter = ',')
          #next(csvReader)
          #for row in csvReader:
            #removing old basin_key
          #  data = row[:-1]
          #  data.append(x_i)
            #writing output data
          #  with open(path+str(name)+'_output_litho_elevation.csv','a') as csvfile:
          #    csvWriter = csv.writer(csvfile,delimiter = ',')
          #    csvWriter.writerow(data)
        print x_i
        x_i += 1
      
      else:
        print "MChiSegmented is ", MChiSegmented
        print "litho_elevation is ", litho_elevation
        
        with open(path_log+'merge_log.txt', 'a') as param:
          param.write(path+source_name+' ERROR FAILED TO BEGIN MERGE \n')
        
                     
      #maintains correct basin labelling  
    

def getStats(path,column_name):
  with open(path+name+"_output_litho_elevation.csv",'r') as csvfile_a:
    pandasDF = pd.read_csv(csvfile_a,delimiter=',')
    try:
      selectedDF = pandasDF.loc[pandasDF[column_name]>=90]
      mean_100 = selectedDF['Median_MOv'].mean()
      count_100 = len(selectedDF.index)
      std_100 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=80]
      mean_90 = selectedDF['Median_MOv'].mean()
      count_90 = len(selectedDF.index)
      std_90 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=80]
      mean_80 = selectedDF['Median_MOv'].mean()
      count_80 = len(selectedDF.index)
      std_80 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=70]
      mean_70 = selectedDF['Median_MOv'].mean()
      count_70 = len(selectedDF.index)
      std_70 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=60]
      mean_60 = selectedDF['Median_MOv'].mean()
      count_60 = len(selectedDF.index)
      std_60 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=50]
      mean_50 = selectedDF['Median_MOv'].mean()
      count_50 = len(selectedDF.index)
      std_50 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=40]
      mean_40 = selectedDF['Median_MOv'].mean()
      count_40 = len(selectedDF.index)
      std_40 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=30]
      mean_30 = selectedDF['Median_MOv'].mean()
      count_30 = len(selectedDF.index)
      std_30 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=20]
      mean_20 = selectedDF['Median_MOv'].mean()
      count_20 = len(selectedDF.index)
      std_20 = selectedDF['Median_MOv'].std()
      
      selectedDF = pandasDF.loc[pandasDF[column_name]>=10]
      mean_10 = selectedDF['Median_MOv'].mean()
      count_10 = len(selectedDF.index)
      std_10 = selectedDF['Median_MOv'].std()
      
      
      #get count and standar deviation too
      with open(path+'statistics.csv','a') as csvfile_b:
        csvWriter = csv.writer(csvfile_b, delimiter = ',')
        csvWriter.writerow((column_name,mean_100,mean_90,mean_80,mean_70,mean_60,mean_50,mean_40,mean_30,mean_20,mean_10,
        count_100,count_90,count_80,count_70,count_60,count_50,count_40,count_30,count_20,count_10,
        std_100,std_90,std_80,std_70,std_60,std_50,std_40,std_30,std_20,std_10))
    except KeyError:
      print "Incorrect column key: ", column_name
      return 

#def pyplot(path,column_name):
#  with open (path+name+'_output_litho_elevation.csv','r') as csvfile:
#    pandasDF = pd.read_csv(csvfile, delimiter = ',')
#    fig = plt.scatter(pandasDF[column_name],pandasDF['Median_MOv'])
#    fig.savefig(path+column_name+'.png',dpi=500)
  
if inputs.stats:
  with open(path+'statistics.csv','wb') as csvfile:
    csvWriter = csv.writer(csvfile, delimiter = ',')
    csvWriter.writerow(('lithology','mean 100','mean 90','mean 80','mean 70','mean 60','mean 50','mean 40','mean 30','mean 20','mean 10',
    'count 100','count 90','count 80','count 70','count 60','count 50','count 40','count 30','count 20','count 10',
    'standard_deviation 100','standard_deviation 90','standard_deviation 80','standard_deviation 70','standard_deviation 60',
    'standard_deviation 50','standard_deviation 40','standard_deviation 30','standard_deviation 20','standard_deviation 10'))
  
  with open(path+name+"_output_litho_elevation.csv",'r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    columns = pandasDF.columns.values
    for column_name in columns:
      getStats(path,column_name)
      #pyplot(path,column_name)
      print column_name
    full_mean = pandasDF['Median_MOv'].mean()
    with open(path+'statistics.csv','a') as csvfile_b:
      csvWriter = csv.writer(csvfile_b, delimiter = ',')
      csvWriter.writerow(('All Basins',full_mean))

      
       
      