#selection automator
import csv
import os
import shutil

directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'

target_csv = 'himalaya_b.csv'

name = 'himalaya_all'

current_path = directory+name+'/'

if not os.path.exists(current_path):
  os.makedirs(current_path)

with open(directory+target_csv,'r') as csvfile:
  csvReader = csv.reader(csvfile,delimiter=',')
  next(csvReader)
  for row in csvReader:
   
    command = 'python data_selection.py -dir %s -name %s -burned_MChi True -merge_csv True -TRMM_basin True -litho_elevation True' %(directory+row[0]+'_summary/',row[1])
    os.system(command)      
    
    
    print directory+row[0]+'_summary/'+row[1]+'_output_AllBasinsInfo.csv'
    shutil.copy(directory+row[0]+'_summary/'+row[1]+'_output_AllBasinsInfo.csv',current_path+row[1]+'_output_AllBasinsInfo.csv')
    shutil.copy(directory+row[0]+'_summary/'+row[1]+'_output_MChiSegmented_burn.csv',current_path+row[1]+'_output_MChiSegmented_burn.csv')    
    shutil.copy(directory+row[0]+'_summary/'+row[1]+'_output_basin_TRMM.csv',current_path+row[1]+'_output_basin_TRMM.csv')
    #incorporating new disorder stats
    shutil.copy(directory+row[0]+'_summary/'+row[1]+'_output_fullstats_disorder_uncert.csv',current_path+row[1]+'_output_fullstats_disorder_uncert.csv')    
    shutil.copy(directory+row[0]+'_summary/'+row[1]+'_output_disorder_basinstats.csv',current_path+row[1]+'_output_disorder_basinstats.csv')
    shutil.copy(directory+row[0]+'_summary/'+row[1]+'_output_litho_elevation.csv',current_path+row[1]+'_output_litho_elevation.csv')
    

    
        
command_2 = 'python data_selection.py -dir %s -burned_MChi True -merge_csv True -TRMM_basin True -no_summary True' %(current_path)

#os.system(command_2)

