# script to add raster point data to csvs
import os
import pandas as pd
import csv
import subprocess as sub
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("current_name",nargs='?',default="none")
inputs = parser.parse_args()

current_name = inputs.current_name

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/'
raster = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/TRMM_data/annual.tif'

with open(target+current_name+'_output_MChiSegmented_export.csv','wb') as csvfile:
  csvWriter = csv.writer(csvfile)
  csvWriter.writerow(["burned_data","latitude","longitude","node","row","col","chi","elevation","flow_distance","drainage_area","m_chi","b_chi","source_key","basin_key","segmented_elevation","raster_point"])

def write_row(string):
  with open(target+current_name+'_output_MChiSegmented_export.csv','a') as writefile:
    csvWriter = csv.writer(writefile,delimiter=',')
    csvWriter.writerow((string))

#setting up output file  


#tracker
x_i = 0

with open(target+current_name+"_output_MChiSegmented_burn.csv",'r') as csvfile:
  csvReader = csv.reader(csvfile,delimiter=',')
  #pandasDF = pd.read_csv(csvfile,delimiter=',')
  next(csvReader)
  for row in csvReader:
    string = [row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]]
    #sampling target raster using gdallocationinfo
    gdal = ['gdallocationinfo', '-wgs84', '-valonly', raster, row[2], row[1]]
    locate = sub.Popen(gdal, stdout=sub.PIPE)
    value = locate.stdout.read()
    value = int(value)
    string.append(value)
    write_row(string)
    print value,x_i
    x_i+=1
    
  
  