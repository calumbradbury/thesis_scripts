#burn raster driver
import os
import csv
import pandas as pd
import gdal
import osr
import subprocess as sub
import sys
import shutil
import utm

#plan: use processed csv to rasterize a new source raster, and run the raster burner hack of the chi_mapping_tool



#directory = 'R:\\LSDTopoTools\\Topographic_projects\\full_himalaya\\'
directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/0_05_concavity/'

#data_source = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/TRMM_data/full_data/non_monsoon_trans.tif' 

#data_source = 'R:\\exhumation\\0_2.tif'#source of the rasterized exhumation data
data_source_exhumation = '/exports/csce/datastore/geos/users/s1134744/exhumation/0_2.tif'
data_source_glaciated = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/glims_ice/ice_100.bil'
data_source_cosmo = '/exports/csce/datastore/geos/groups/LSDTopoData/Himalayan_Ksn_Concavity/cosmo_data/basin_shapefiles/outputDS.tif'
data_source_distance = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/simplified_distance.tif'
data_source_distance_km = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/distance_km.tif'
data_source_distance_along = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/euc_allocation_6.tif'
data_source_strain = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/strain/second_invariant.tif'

data_source_tectonics = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/fault_zones/digitized.bil'#source of digitized shapefile

def utmExtents(summary_directory,fname,corner):
  with open (summary_directory+fname+corner+".txt", "r") as text:
    data = text.read().replace(',', '')
    data = data.replace('(','')
    data = data.replace(')','')
    data = data.split()
    coordinates = [data[2],data[3]]
    return coordinates
    
def utmToLatLon(coordinate,proj4):
  zone = proj4.split(' ')
  zone = zone[1]
  zone = zone.replace('+zone=','')
  easting = float(coordinate[0])
  northing = float(coordinate[1])
  lat_lon_coordinate = utm.to_latlon(int(easting),int(northing),int(zone),northern = True)
  return lat_lon_coordinate
    
def getGlaciers(full_directory,summary_directory,fname,write_name,SRTM90=False):

  #these are in UTM, needs to be lat lon
  LL = utmExtents(summary_directory,fname,corner="_lower_left")
  UR = utmExtents(summary_directory,fname,corner="_upper_right")   

  simplified_geology = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/fault_zones/digitized.shp' #source of digitized shapefile  
  glaciers = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/glims_ice/clipped_exists.shp'

  ds = gdal.Open(summary_directory+fname+'.bil')
  #getting target srs from current DEM
  ds = ds.GetProjection()
  ds = osr.SpatialReference(ds)
  ds = ds.ExportToProj4()
  
  try:
    LL_lat_lon = utmToLatLon(LL,ds)
    UR_lat_lon = utmToLatLon(UR,ds)
  except:
    sys.exit()        
      
  #clipping                   
  try:
    print('ogr2ogr -f "ESRI Shapefile" %s.shp %s -clipsrc %s %s %s %s' %(summary_directory+fname+'_glaciers',glaciers,LL_lat_lon[0],LL_lat_lon[1],UR_lat_lon[0],UR_lat_lon[1]))                                                     
    sys.exit()
  except:
    sys.exit()
  os.system(('ogr2ogr -f "ESRI Shapefile" %s.shp %s -clipsrc %s %s %s %s') %(summary_directory+fname+'_glaciers',glaciers,LL_lat_lon[0],LL_lat_lon[1],UR_lat_lon[0],UR_lat_lon[1]))
  #transform crs and rasterize
  os.system('ogr2ogr -t_srs'+" '"+ds+"' "+summary_directory+fname+'_glaciers_utm'+'.shp '+summary_directory+fname+'_glaciers.shp')
  
  if os.path.isfile(full_directory+fname+'_glaciated.bil'):
    try:
      os.remove(full_directory+fname+'_glaciated.bil')  
      os.remove(full_directory+fname+'_glaciated.hdr')
    except:
      print("Error removing raster files. Forcing exit to prevent unseen errors")
      sys.exit()  
  
  if SRTM90:
    os.system('gdal_rasterize -of ENVI -a exists -a_nodata 0 -tr 90 90 -l '+fname+'_glaciers_utm'+' '+summary_directory+fname+'_glaciers_utm'+'.shp '+full_directory+write_name+'_glaciated'+'.bil')      
  else:
    os.system('gdal_rasterize -of ENVI -a exists -a_nodata 0 -tr 30 30 -l '+fname+'_glaciers_utm'+' '+summary_directory+fname+'_glaciers_utm'+'.shp '+full_directory+write_name+'_glaciated'+'.bil')





def getRaster(full_directory,summary_directory,fname,write_name,raster_source,raster_name='to_burn',SRTM90=False): 
  LL = utmExtents(summary_directory,fname,corner="_lower_left")
  UR = utmExtents(summary_directory,fname,corner="_upper_right")    
  
  #getting target srs from current DEM  
  try:
    print full_directory+fname+'.bil'
    ds = gdal.Open(full_directory+fname+'.bil')
    ds = ds.GetProjection()
    ds = osr.SpatialReference(ds)
    ds = ds.ExportToProj4()
  except:
    print("error getting burn raster, skipping...")
    return
  
         
  #clipping raster, reprojecting, and setting resolution 
  #setting nodata values to ensure preservation
  #changing from filename to writename
  res_90 = "gdalwarp -ot Float64 -of ENVI -tr 90 90 -srcnodata '-9999' -dstnodata '-9999' -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te %s %s %s %s %s %s%s_%s.bil" %(LL[0],LL[1],UR[0],UR[1],raster_source,full_directory,write_name,raster_name)
  res_30 = "gdalwarp -ot Float64 -of ENVI -tr 30 30 -srcnodata '-9999' -dstnodata '-9999' -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te %s %s %s %s %s %s%s_%s.bil" %(LL[0],LL[1],UR[0],UR[1],raster_source,full_directory,write_name,raster_name)    
  
  #before rasterising, check if raster is already present in directory, remove if it is
  if os.path.isfile(full_directory+write_name+'_'+raster_name+'.bil'):
    try:
      os.remove(full_directory+write_name+'_'+raster_name+'.bil')
      os.remove(full_directory+write_name+'_'+raster_name+'.hdr')
    except:
      print("Error removing raster files. Forcing exit to prevent unseen errors")
      sys.exit()
      
  print 'srtm 90  is ...s...', SRTM90
  if SRTM90:
    os.system(res_90)
    print res_90
  else:
    os.system(res_30) 
    print res_30       




#opening processed source file to access directory structure

name_list = ['himalaya_processed','himalaya_b_processed','himalaya_c_processed']

for name in name_list:

    with open(directory+name+'.csv','r') as csvfile:
        csvReader = csv.reader(csvfile,delimiter=',')
        next(csvReader)
        for row in csvReader:
            #print(row)
            #generating target path
            #for writing output, will make it easier in handling the generated files with existing scripts
            part_1 = str(row[0])
            part_1 = part_1.replace('.','_')
            part_2 = str(("%.2f" %float(row[2])))+'_'+str(("%.2f" %float(row[3])))
            part_2 = part_2.replace('.','_')
        
            full_target = os.path.join(directory+part_1,part_2+'_'+part_1+'_'+str(row[1]),str(row[5])+'/')
            
            #print(full_target)
            
            #summary directory. This is where the extent.txt files are preserved from the original analysis
            summary_target = directory+part_1+'_summary/'
      
            fname = part_1+'_'+str(row[1])
              
            max_basin = (int(row[6])/2)+int(row[5])
      
            write_name = str(row[1])+str(row[5])+'_'+str(max_basin)
      
            #column_header = "digitized"
            #secondary_column_header = "tectonic_zone"
            #logic to rename source DEM files/make sure they exist
            
            if not os.path.isfile(full_target+write_name+'.bil'):
            
                if not os.path.isfile(full_target+fname+'.bil'):
                
                    try:
                        shutil.copy2(summary_target+fname+'.bil',full_target+fname+'.bil')
                        shutil.copy2(summary_target+fname+'.hdr',full_target+fname+'.hdr')                        
                    except:
                        print("cannot find the dem for %s"%(fname))                        
                        
                os.rename(full_target+fname+'.bil',full_target+write_name+'.bil')
                os.rename(full_target+fname+'.hdr',full_target+write_name+'.hdr')
            

          

    
            #adaptions for concavity catcher. Needs to get precipitation and litho rasters from summary directory
            #shutil.copy2(summary_target+fname+'_precipitation.bil',full_target+write_name+'_precipitation.bil')
            #shutil.copy2(summary_target+fname+'_precipitation.hdr',full_target+write_name+'_precipitation.hdr')
            #shutil.copy2(summary_target+fname+'_geology.bil',full_target+write_name+'_geology.bil')
            #shutil.copy2(summary_target+fname+'_geology.hdr',full_target+write_name+'_geology.hdr')
    
            #^^^ not necessary as rasters are sourced from the summary directory
    
            #getRaster(full_target,summary_target,fname,write_name,data_source_exhumation,raster_name='exhumation')
            #getRaster(full_target,summary_target,fname,write_name,data_source_glaciated,raster_name='glaciated')
            
            #getRaster(full_target,summary_target,fname,write_name,data_source_distance,raster_name='distance')            
            #getRaster(full_target,summary_target,fname,write_name,data_source_distance_along,raster_name='distance_along')
            
            getRaster(full_target,summary_target,fname,write_name,data_source_cosmo,raster_name='cosmo')
            getRaster(full_target,summary_target,fname,write_name,data_source_tectonics,raster_name='tectonics')            
            
            #getGlaciers(full_target,summary_target,fname,write_name)
            #print(full_target,summary_target,fname,write_name)
            #try:
            #getGeologyRaster(full_target,summary_target,fname,write_name)
            #  sys.exit()
            #except:                                                                                                    
            #  print("error")
            #sys.exit()
            #put into m_n list loop if adding to all concavity ksn calculations
    
            m_n_list = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95]
    
            for x in m_n_list:
                #print(x)
                x=str(x)
                x = x.replace('.','_')
    
                try:
                    os.rename(full_target+write_name+'.bil',full_target+write_name+x+'.bil')
                    os.rename(full_target+write_name+'.hdr',full_target+write_name+x+'.hdr')
    
                except(OSError):
                    print("ERROR! Probably a missing tile. Location: %s%s"%(full_target,fname))        
    
                with open(full_target+fname+"_Chiculations.param",'wb') as file:
                    file.write('# This is a parameter file for the chi_mapping_tool \n')
                    file.write('# One day there will be documentation. \n')
                    file.write(" \n")
                    file.write('# These are parameters for the file i/o \n')
                    file.write("# IMPORTANT: You MUST make the write directory: the code will not work if it doens't exist. \n")
                    file.write('read path: %s \n'%(full_target))
                    file.write('write path: %s \n'%(full_target))
      
                    file.write('read fname: %s \n'%(write_name+x))
                    file.write('write fname: %s \n'%(write_name+x))
      
                    #file.write('read fname: %s \n'%(write_name))
                    #file.write('write fname: %s \n'%(write_name))      
      
                    file.write("\n")
                    file.write('burn_raster_to_csv: True \n')
                    file.write('burn_raster_prefix: %s \n'%(fname+'_cosmo'))
                    #file.write('burn_raster_prefix: %s \n'%(fname+'_glaciated'))
                    #file.write('burn_data_csv_column_header: tertiary_burned_data \n')
                    file.write('burn_data_csv_column_header: cosmo_EBE_MMKYR \n')
                    file.write("\n")
                    file.write('secondary_burn_raster_to_csv: True \n')
                    file.write('secondary_burn_raster_prefix: %s \n'%(fname+'_tectonics'))
                    file.write('secondary_burn_data_csv_column_header: tectonic_zone \n')
                    file.close()
                        
                #os.remove(full_target+fname+"_Chiculations.param")
                
                #print("removed")
                    
                raster_burner_command = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Git_projects/LSDTT_Development/driver_functions_MuddChi2014/raster_burner.exe %s %s" %(full_target,fname+"_Chiculations.param")
                #print(raster_burner_command)
                
                try:
                    sub.call(raster_burner_command, shell = True)
                #print(full_target+fname+x+'_MChiSegmented_burned.csv')
                #target_dem = os.path.isfile(full_target+fname+x+'.bil')
                #target_MChi = os.path.isfile(full_target+fname+x+'_MChiSegmented_burned.csv')
                #target_burn = os.path.isfile(full_target+fname+'_to_burn.bil')
                #print(target_dem,target_MChi,target_burn)
                #if target_dem and target_MChi and target_burn:
                #    print("OK to run burn_raster")
                    
                except:
                    print("could not burn to csv!!!")
                    
                    #undoing rename to allow renaming in next step
                try:
                    os.rename(full_target+fname+x+'.bil',full_target+fname+'.bil')
                    os.rename(full_target+fname+x+'.hdr',full_target+fname+'.hdr')
                except:
                    print("error fixing rename")
        

      
      
    #clearing up
    #os.remove(full_target+write_name+'_precipitation.bil')
    #os.remove(full_target+write_name+'_precipitation.hdr')
    #os.remove(full_target+write_name+'_geology.bil')
    #os.remove(full_target+write_name+'_geology.hdr')