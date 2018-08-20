#ksn to correct concaivity
import os
import csv

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya_5000/'
name = 'himalaya_c_processed.csv'#,'himalaya_b_processed.csv','himalaya_c_processed.csv'

#for name in name_list:

with open(target+name,'r') as csvfile:
  csvReader = csv.reader(csvfile,delimiter=',')
  next(csvReader)
  for row in csvReader:
    max_basin = (int(row[6])/2)+int(row[5])
    
    part_1 = str(row[0])
    part_1 = part_1.replace('.','_')
    part_2 = str(("%.2f" %float(row[2])))+'_'+str(("%.2f" %float(row[3])))
    part_2 = part_2.replace('.','_')
    
    current_path = target+part_1+'/'+part_2+'_'+part_1+'_'+str(row[1])+'/'+str(row[5])+'/'
    fname = part_1+'_'+str(row[1]) 
    summary_directory = target+part_1+'_summary/'
    print current_path
    concavity_corrector = 'nohup nice python ./concavity_corrector_b.py %s %s %s&'%(current_path,fname,summary_directory)
    os.system(concavity_corrector)
    