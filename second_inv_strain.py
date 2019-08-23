### Script to calculate second invariant of strain based on global strain rate model data ###
### Exports as csv for rasterisation ###


import csv
import sys
import math
import os

def write_row(x,y,a,b,c):
  with open('/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/strain/strain_full.csv','a') as csvfile:
        csvWriter = csv.writer(csvfile,delimiter = ',')
        csvWriter.writerow((x,y,a,b,c))

try:
  os.remove('/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/strain/strain_full.csv')
except:
  print("nothing to remove")
  
write_row('lat','lon','e1','e2','second_inv')

#iterator for skip control
x_i = 0

with open('/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/strain/kreemer/GSRM_strain.txt','r') as textfile:
#with open('/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/strain/global_strain_rate.txt','r') as textfile:
     for line in textfile:
        x_i+=1
        #skipping header
        if x_i <= 25:
          continue
        
        #cumbersom method for dealing with multiple spaces
        line = line.replace('....',' ')
        line = line.replace('   ',' ')
        line = line.replace('  ',' ')
        line = line.replace('  ',' ')
        line = line.split(' ')
        print(line)
        #adding some error management
        try:
          e1 = float(line[8])
          e2 = float(line[9])
          lat = float(line[0])
          lon = float(line[1])
        
        except:
          if not line[0]:
            e1 = float(line[9])
            e2 = float(line[10])
            lat = float(line[1])
            lon = float(line[2])            
        
        
        if lat >= 11.0 or lat <=-57.0:
          continue
        if lon >= -59.0 or lon <= -82.0:
          continue
        
        second_inv = math.sqrt((e1**2)+(e2**2))
        
        print(e1,e2,second_inv)
        write_row(lat,lon,e1,e2,second_inv)