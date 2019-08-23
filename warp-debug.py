#debug of warp

import argparse
import subprocess as sub      
import shutil
import os
import geopandas as gpd
import pandas as pd
from time import sleep
import csv
import sys
import  ogr
import gdal
import osr

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

import LSDPlottingTools as LSDPT

directory = "/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/basin_shapefiles/"

rasterDS  = gdal.Open(directory+'output5.tif')
print gdal.Info(rasterDS)

srs = osr.SpatialReference()
###problematic - get from input file directly
srs.ImportFromEPSG(4326)

#outputDS =  gdal.Open(directory+'output6.tif')

gdal.Warp(directory+'outputDS.tif',rasterDS,dstSRS=srs)

#print gdal.Info(outputDS)