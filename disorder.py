#script to search through disorder stats by basin. I can't be sure that basin 
#number continuity has been preserved between the two runs of the anlaysis.

import pandas as pd
import csv
import os
                                                                                                                  
directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'
sub = '../50_100k_basins_precip_chi/'

def writeHeader(file_name,target_name):
  with open(directory+file_name,'r') as sourceheader_csv:
    pandasDF=pd.read_csv(sourceheader_csv,delimiter=',')
    header_list = pandasDF.columns.values.tolist()
  
    with open(directory+target_name,'wb') as writeheader_csv:
      csvWriter = csv.writer(writeheader_csv,delimiter = ',')
      csvWriter.writerow(header_list)


def output(x,y,z,a,b,c,d):
  if not os.path.isfile(directory+'disorder_out.csv'):
    with open(directory+'disorder_out.csv','wb') as csvfile:
      csvWriter = csv.writer(csvfile,delimiter=',')
      csvWriter.writerow(('no_precip_basin_key','precip_basin_key','no_precip_mn','precip_mn','no_precip_MLE','precip_MLE','difference(no_precip - precip)'))
  
  with open(directory+'disorder_out.csv',"a") as csvfile_out:
    csvWriter = csv.writer(csvfile_out,delimiter=',')
    csvWriter.writerow((x,y,z,a,b,c,d))

def output_basic(x,y,z):
  if not os.path.isfile(directory+'disorder_out.csv'):
    with open(directory+'disorder_out.csv','wb') as csvfile:
      csvWriter = csv.writer(csvfile,delimiter=',')
      csvWriter.writerow(('no_precip_basin_key','no_precip_mn','no_precip_MLE'))
  
  with open(directory+'disorder_out.csv',"a") as csvfile_out:
    csvWriter = csv.writer(csvfile_out,delimiter=',')
    csvWriter.writerow((x,y,z))

    
def outputMChi(x,y,z,a):
  with open(directory+'MChi_out.csv',"a") as csvfile_out:
    csvWriter = csv.writer(csvfile_out,delimiter=',')
    csvWriter.writerow((x,y,z,a))  

def fileLog(file_path):
  with open(directory+'disorder_log.txt','a') as param:
    param.write(file_path+'\n')

#function to fetch median MN. Uses the final path only.
#returns MN for both datasets
def getMN(path,basin_key):
  with open(directory+path+'_basin_TRMM_MN.csv','r') as csvfile_MN:
    basin_key = int(basin_key)
    pandasDF = pd.read_csv(csvfile_MN,delimiter=',')
    pandasDF = pandasDF.loc[pandasDF['basin_key']==basin_key]
    pandasDF = pandasDF['Median_MOverNs']
    pandasDF = pandasDF.tolist()
    try:
      precip_mn = pandasDF[0]
      #print (precip_mn)
      return precip_mn
    except IndexError:
      print("I couldn't find the basin")
      return 0
      
def columnSelector(mn):
  #rounding mn to nearest 1dp
  #print mn
  mn = "%.1f" %float(mn)
  mn = float(mn)
  if mn == 0.1:
    return 2
  if mn == 0.2:
    return 3
  if mn == 0.3:
    return 4
  if mn == 0.4:
    return 5
  if mn == 0.5:
    return 6
  if mn == 0.6:
    return 7
  if mn == 0.7:
    return 8
  if mn == 0.8:
    return 9
  if mn == 0.9:
    return 10
  else:
    print("invalid concavity!")

def getMLEcolumn(path):
  with open(directory+path+'_disorder_basinstats.csv','r') as mleSource:
    csvReader = csv.reader(mleSource, delimiter = ',')
    #skipping header
    next(csvReader)
    mleStore = []
    x_basin_key = []
    x_mn = []
    for row in csvReader:
      basin_key = row[0]
      mn = getMN(path,basin_key)
      column = columnSelector(mn)
      mle = row[column]
      mleStore.append(row[column])
      x_basin_key.append(basin_key)
      x_mn.append(mn)
    #returning all mle values
    return mleStore,x_basin_key,x_mn

#function to return MChiSegmented data as lists. I think this will be more efficient than previous method.
#return basin_key, burned_data, secondary_burned_data and mchi    

#fast at checking list, ie, node length. V.slow at writing.
#use pandas instead
#try and move all to pandas. This relies on the same output format. A more robust method would select by column header.

def getMChiSegmented(path):
  with open(directory+path+'_MChiSegmented_burned.csv') as mChiSource:
    csvReader = csv.reader(mChiSource,delimiter=',')
    #skipping header
    next(csvReader)
    x_basin_key = []
    x_burned_data = []
    x_secondary_burned_data = []
    x_mchi = []
    #reading data into lists
    for row in csvReader:
      basin_key = row[14]
      burned_data = row[0]
      secondary_burned_data = row[1]
      mchi = row[11]
      x_basin_key.append(basin_key)
      x_burned_data.append(burned_data)
      x_secondary_burned_data.append(secondary_burned_data)
      x_mchi.append(mchi)
    return x_basin_key,x_burned_data,x_secondary_burned_data,x_mchi  

#script to get results as pandas dataframe.
def getMChiSegmentedPandas(path):
  with open(directory+path+'_MChiSegmented_burned.csv') as mChiSource:
    pandasDF = pd.read_csv(mChiSource, delimiter=',')
    #pandasDF = pandasDF[['burned_data','secondary_burned_data','m_chi','basin_key']]
    return pandasDF
  
  
           
      
      


  
x_i = 0

#opening processed source file to access directory structure
with open(directory+'himalaya_processed.csv','r') as csvfile:
  csvReader = csv.reader(csvfile,delimiter=',')
  next(csvReader)
  for row in csvReader:
    #generating target path
    max_basin = (int(row[6])/2)+int(row[5])
    target = str(row[0])+'/'+("%.2f" %float(row[2]))+'_'+("%.2f" %float(row[3]))+'_'+str(row[0])+'_'+str(row[1])+'/'+str(row[5])+'/'+str(row[1])+str(row[5])+'_'+str(max_basin)
    #testing to make sure both files exist
    is_no_precip = os.path.isfile(directory+target+'_disorder_basinstats.csv')
    is_precip = os.path.isfile(directory+sub+target+'_disorder_basinstats.csv')
    
    #another test is needed to make sure that analaysis completed on the tile
    is_no_precip_mn = os.path.isfile(directory+target+'_basin_TRMM_MN.csv')
    is_precip_mn = os.path.isfile(directory+sub+target+'_basin_TRMM_MN.csv')
    
    #development testing
    #print(directory+target+'_disorder_basinstats.csv')
    #print(is_no_precip,is_precip)
    
    if not is_no_precip: #or not is_precip:
      print("found missing tile * %s!"%(x_i))
      x_i+=1 


    #if both files are present, open and append to the output file
    #need to get the MLE for the median concavity of each basin. TRMM_MN has this in its csv file so use that.
    #work on directly involving MN calculator if this method is successful
    
    if is_no_precip and is_no_precip_mn: # and is_precip  and is_precip_mn:
      #print(directory+target+'_disorder_basinstats.csv')
      #print(directory+sub+target+'_disorder_basinstats.csv')
      #print(is_no_precip,is_precip)
      #precip_mn = getMN(path=sub+target,basin_key=0)
      no_precip_mn = getMN(path=target,basin_key=0)
    
      get_disorder = False
      get_mchi = True
      disorder_basic = False
    
      #print columnSelector(mn=0.5)
      if get_disorder:
        no_precip_mle,no_precip_basin,no_precip_mn = getMLEcolumn(path=target)
        if not disorder_basic:
          precip_mle,precip_basin,precip_mn = getMLEcolumn(path=sub+target)
          print sub+target
      #print precip_basin
      #print no_precip_basin
      #print no_precip_mn
      #print precip_mn
      #print(no_precip_mle)
      #print(precip_mle)
      #testing to make sure that the returned lists are the same length. If they are different then a different number of basins has been analysed.
          if len(no_precip_mle) == len(precip_mle):
            print("Okie dokie")
          if len(no_precip_mle) != len(precip_mle):
            print("oh dear! There's an error somewhere")
          for x,y,z,a,b,c in zip(no_precip_basin,precip_basin,no_precip_mn,precip_mn,no_precip_mle,precip_mle):
            d = float(b)-float(c)
            output(x,y,z,a,b,c,d)
        if disorder_basic:
          for x,y,z in zip(no_precip_basin,no_precip_mn,no_precip_mle):
            output_basic(x,y,z)


      
      if get_mchi:
        #no list length testing required as only the disorder statistics can be compared between the two runs.
        #no_precip_basin,no_precip_burned,no_precip_secondary_burned,no_precip_mchi = getMChiSegmented(path=target)
        #precip_basin,precip_burned,precip_secondary_burned,precip_mchi = getMChiSegmented(path=sub+target)
        pandasDF = getMChiSegmentedPandas(path=target)
        #print pandasDF
        #if len(no_precip_basin) == len(precip_basin):
        if not pandasDF.empty:
          print("Okie dokie, getting data as pandasDF")
          pandasDF = getMChiSegmentedPandas(path=target)
          
          if not os.path.isfile(directory+'mchi_pandas_output_simplified.csv'):
            writeHeader(file_name=target+'_MChiSegmented_burned.csv',target_name='mchi_pandas_output_simplified.csv')
          
          pandasDF.to_csv(directory+'mchi_pandas_output_simplified.csv',mode='a',header=False,index=False)  

        #if len(no_precip_basin) != len(precip_basin):
        if pandasDF.empty:
          print("oh dear! There's an error somewhere")
        
        
          
        #for x,y,z,a in zip(no_precip_basin,no_precip_burned,no_precip_secondary_burned,no_precip_mchi):
        #  outputMChi(x,y,z,a)


      fileLog(file_path=target)
print("found total missing tiles * %s!"%(x_i))


#with open(directory+'disorder_out.csv',"a") as csvfile_out:
#  csvWriter = csv.reader(csvfile_out,delimiter=',')
      
    
    
    #with open(directory+)
    #print target
