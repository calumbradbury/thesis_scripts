#correct all csv file names. Need to remove periods
import os
import csv

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/'
name = 'himalaya_processed.csv'

with open(target+name,'r') as csvfile:
  csvReader = csv.reader(csvfile,delimiter=',')
  next(csvReader)
  for row in csvReader:
    max_basin = (int(row[6])/2)+int(row[5])
    current_path = target+str(row[0])+'/'+("%.2f" %float(row[2]))+'_'+("%.2f" %float(row[3]))+'_'+str(row[0])+'_'+str(row[1])+'/'+str(row[5])+'/'
    #current_path = target+str(row[0])+'/'
    current_path = current_path.replace('.','_')
    command = "find %s -type f -name '*0.*.csv' -exec bash -c 'mv %s %s ' {} \;"%(current_path,'"${0//0./_}"','"$0"')
    print command
    os.system(command) 
    #renamer(current_path+'files.txt')
    #os.remove(current_path+'files.txt')
    

