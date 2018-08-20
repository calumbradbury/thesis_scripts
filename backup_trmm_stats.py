#backup stats writer
#recalculates basin average and writes output to all_basins_trmmm
import csv
import pandas as pd
import sys

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/'

#LSDTopoTools specific imports
#Loading the LSDTT setup configuration
setup_file = open('/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Git_projects/LSDAutomation/chi_analysis_automation/chi_automation.config','r')
LSDMT_PT = setup_file.readline().rstrip()
LSDMT_MF = setup_file.readline().rstrip()
Iguanodon = setup_file.readline().rstrip() 
setup_file.close()

sys.path.append(LSDMT_PT)
sys.path.append(LSDMT_MF)
sys.path.append(Iguanodon)

from LSDPlottingTools import LSDMap_MOverNPlotting as MN
from LSDMapFigure import PlottingHelpers as Helper
import Iguanodon31 as Ig

#creating csv with rainfall averaged over basin segments, and including MN data
with open(target+"_output_basin_TRMM_recalculated.csv","wb") as csvfile:
  csvWriter = csv.writer(csvfile,delimiter=',')
  csvWriter.writerow(("basin_key","mean jun/jul/aug rainfall (mm)"))

  #opening source of climate data
with open(target+'_output_MChiSegmented_nodata.csv','r') as csvfile:
  pandasDF = pd.read_csv(csvfile,delimiter=',')
      
        #opening basin directory
  with open(target+'_output_AllBasinsInfo.csv','r') as csvfile_2:
    csvReader = csv.reader(csvfile_2,delimiter=',')
    next(csvReader)
        
    for row in csvReader:
      basin_number = int(row[5])
      selected_DF = pandasDF.loc[pandasDF['basin_key'] == basin_number]
      #getting burned data series for the basin
      pandas_list = selected_DF['burned_data']
      #print pandas_list
      mean_rainfall = pandas_list.mean()
        
      with open(target+'_output_basin_TRMM_recalculated.csv', 'a') as csvfile_3:
        csvWriter = csv.writer(csvfile_3,delimiter=',')
        csvWriter.writerow((basin_number,mean_rainfall))

with open(target+'_output_basin_TRMM.csv','r') as csvfile:
  pandas_a = pd.read_csv(csvfile,delimiter=',')
  with open(target+'_output_basin_TRMM_recalculated.csv','r') as csvfile_b:
    pandas_b = pd.read_csv(csvfile_b,delimiter=',')
    pandas_a = pandas_a.merge(pandas_b, on=["basin_key"])
    pandas_a.to_csv(target+'_output_basin_TRMM_new.csv', mode = "w", header = True, index = False)
