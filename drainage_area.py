#drainage area
#needs to get max drainage area for each basin

import pandas as pd
import os
import csv


target = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/_output_AllBasinsInfo.csv"
target2 = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/_output_MChiSegmented_nodata.csv" 
target3 =  "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/_output_basin_drainage_area.csv"  
cell_size = 30

with open(target3,'wb') as csvfile:
  csvWriter = csv.writer(csvfile,delimiter=',')
  csvWriter.writerow(("basin_key","drainage_area"))

with open(target,'r') as csvfile:
  csvReader = csv.reader(csvfile,delimiter=',')
  next(csvReader)
  for row in csvReader:
    basin_key = row[5]
    with open(target2,'r') as csvfile2:
      pandasDF = pd.read_csv(csvfile2,delimiter=',')
      #selecting data for basin
      pandasDF = pandasDF[pandasDF["basin_key"] == int(basin_key)]
      pandasDF = pandasDF["drainage_area"]
      drainage_area = pandasDF.max()
      with open(target3,'a') as csvfile3:
        csvWriter = csv.writer(csvfile3,delimiter=',')
        csvWriter.writerow((basin_key,drainage_area))
      print basin_key
      #print pandasDF.max()
      #print pandasDF    
    
