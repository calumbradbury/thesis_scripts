import sys
import os
import pandas as pd
import csv

#LSDTopoTools specific imports
#Loading the LSDTT setup configuration
setup_file = open('chi_automation.config','r')
LSDMT_PT = setup_file.readline().rstrip()
LSDMT_MF = setup_file.readline().rstrip()
Iguanodon = setup_file.readline().rstrip() 
setup_file.close()

sys.path.append(LSDMT_PT)
sys.path.append(LSDMT_MF)
sys.path.append(Iguanodon)

from LSDPlottingTools import LSDMap_MOverNPlotting as MN
from LSDMapFigure import PlottingHelpers as Helper

current_path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/precip_test/27.00_90.35_himalaya_27.0_13/100000/'
writing_prefix = '13100000_120000'

BasinDF = Helper.ReadMCPointsCSV(current_path,writing_prefix)
PointsDF = MN.GetMOverNRangeMCPoints(BasinDF,start_movern=0.1,d_movern=0.1,n_movern=9)
PointsDF.to_csv(current_path+writing_prefix+'mn_stats.csv', mode="w",header=True,index=False)