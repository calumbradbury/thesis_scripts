#shapefile sorting development

#plan
#load basins - make sure have area attribute for sorting by largest to smallest
# shapefiles aleady have area attribute - good
# geologic_maps_modify_shapefile facilitates adding geological code for GLIM etc...

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

target = '/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/basin_shapefiles/s016_basins_webmercator.shp'
target_b = '/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/basin_shapefiles/s027_basins_webmercator.shp'


# Set the directory where the input files are stored
directory = "/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/basin_shapefiles/"


#creating output
driver = ogr.GetDriverByName("ESRI Shapefile")
data_source = driver.CreateDataSource(directory+"output.shp")

srs = osr.SpatialReference()
srs.ImportFromEPSG(3857)

layer = data_source.CreateLayer("output", srs, ogr.wkbPolygon)

 
dataSource = ogr.Open(target)
#print(daShapefile)
daLayer = dataSource.GetLayer(0)


# Get the list of input files
fileList = os.listdir(directory)
 
# Copy the features from all the files in a new list
#print fileList

#listing features appears to work, but how to write to shapefile?
features = []

for file in fileList:
    
		if file.endswith('.shp'):
				#print file
				tempSource = ogr.Open(directory+file)
				#print(tempSource)
				tempLayer = tempSource.GetLayer(0)
			
				for feat in tempLayer:
						#daLayer.CreateFeature(feat)
						#print feat.GetField("EBE_MMKYR")
						#print daLayer.GetFeatureCount()
						features.append(feat)

definitions = []
area_list = []

layerDefinition_b = daLayer.GetLayerDefn()
print layerDefinition_b.GetFieldCount()
for i in range(layerDefinition_b.GetFieldCount()):
		definition = layerDefinition_b.GetFieldDefn(i)
		definitions.append(definition)
		print("executing")
		print(layerDefinition_b.GetFieldDefn(i).GetName())

### appears to work if fields are pre-defined
for definition in definitions:
	layer.CreateField(definition)

for feature in features:
	area = feature.GetField("AREA")
	area_list.append(area)
	layer.CreateFeature(feature)
  #print(feature.GetFieldCount())
  
#for feature in layer:
#	print feature.GetField("EBE_MMKYR")




layerDefinition = layer.GetLayerDefn()
###no fields
print layerDefinition.GetFieldCount()
for i in range(layerDefinition.GetFieldCount()):
		print("executing")
		print(layerDefinition.GetFieldDefn(i).GetName())
		

                                                        

#print dataSource
#dataSource.SyncToDisk()

####CAUTION####
#no duplicates#
###############
area_list.sort(reverse=True)

# Create the destination data source
inGridSize=float(400)
xMin, xMax, yMin, yMax = layer.GetExtent()
#print layer.GetExtent()

#setting up raster output
xRes = int((xMax - xMin) / inGridSize)
yRes = int((yMax - yMin) / inGridSize)
rasterDS =  gdal.GetDriverByName('GTiff'.encode('utf-8')).Create(directory+"output.tif", xRes, yRes, 1,  gdal.GDT_Float32)

# Define spatial reference
NoDataVal = -9999
rasterDS.SetProjection(layer.GetSpatialRef().ExportToWkt())
rasterDS.SetGeoTransform((xMin, inGridSize, 0, yMax, 0, -inGridSize))
rBand = rasterDS.GetRasterBand(1)
rBand.SetNoDataValue(NoDataVal)
rBand.Fill(NoDataVal)

x_i = 0

						 
for area in area_list:
	if area != -9999.99:
		# Rasterize     
		if x_i < 5:
			#Execute queries(SQL)
			testSQL = "SELECT * FROM output WHERE AREA='%s'" %(area)
			#print area
			temp = data_source.ExecuteSQL(testSQL)
			#print temp
			burn_values = []
			for feature in temp:
				burn_values.append(feature.GetField("EBE_MMKYR"))
			burn = burn_values[0]
			
			layer.SetAttributeFilter('AREA={}'.format(area))
			#gdal.RasterizeLayer(rasterDS, [1], layer, options = ["ATTRIBUTE=EBE_MMKYR"])
			gdal.RasterizeLayer(rasterDS, [1], temp,burn_values=[burn])
			
			layer.SetAttributeFilter('')
			print x_i
			x_i =x_i+1

print len(area_list)

#print area_list

data_source = None
