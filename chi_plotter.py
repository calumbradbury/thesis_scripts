#matplotlib pyplot hist2D
#windows concavity catcher test
import pandas as pd
import csv
import os
import sys

import matplotlib
matplotlib.use('Agg')



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

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/'
MN.MakeChiPlotsMLE(target,'0.1',basin_list=[299], start_movern=0.1, d_movern=0.1, n_movern=1,size_format='ESURF', FigFormat='png',keep_pngs=True)