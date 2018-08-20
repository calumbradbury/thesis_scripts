#write_raster_point driver

import subprocess as sub
import os
import csv

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
    command = "nohup nice python write_raster_point.py %s&"%(row[1])
    os.system(command)
    print command
    