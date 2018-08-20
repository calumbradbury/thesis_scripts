#similar to chi driver script. Will call iguanodon to output only the mchiseg...
#csv in a loop through all concavitites. Output will be used to extract
#corrected KSN values for each basin
#to be run with nohup nice &

import argparse    
import shutil
import sys
import gdal          
import osr
import os

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

import Iguanodon31 as Ig

#parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("current_path",nargs='?',default="none")
parser.add_argument("fname",nargs='?',default="none")
parser.add_argument("summary_directory",nargs='?',default="none")

inputs = parser.parse_args()

current_path = inputs.current_path
fname = inputs.fname
summary_directory = inputs.summary_directory


data_source = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/shapefiles/fault_zones/digitized.bil' #source of digitized shapefile

def utmExtents(summary_directory,fname,corner):
  with open (summary_directory+fname+corner+".txt", "r") as text:
    data = text.read().replace(',', '')
    data = data.replace('(','')
    data = data.replace(')','')
    data = data.split()
    coordinates = [data[2],data[3]]
    return coordinates

def getRaster(full_directory,summary_directory,fname,write_name,SRTM90=False): 
  LL = utmExtents(summary_directory,fname,corner="_lower_left")
  UR = utmExtents(summary_directory,fname,corner="_upper_right")    
  
  #getting target srs from current DEM  
  try:
    ds = gdal.Open(full_directory+fname+'.bil')
    ds = ds.GetProjection()
    ds = osr.SpatialReference(ds)
    ds = ds.ExportToProj4()
  except:
    print("error getting burn raster, skipping...")
    return
  
         
  #clipping raster, reprojecting, and setting resolution 
  res_90 = "gdalwarp -ot Float64 -of ENVI -tr 90 90 -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te %s %s %s %s %s %s%s_to_burn.bil" %(LL[0],LL[1],UR[0],UR[1],data_source,full_directory,write_name)
  res_30 = "gdalwarp -ot Float64 -of ENVI -tr 30 30 -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te %s %s %s %s %s %s%s_to_burn.bil" %(LL[0],LL[1],UR[0],UR[1],data_source,full_directory,write_name)    
  #before rasterising, check if raster is already present in directory, remove if it is
  
  if os.path.isfile(full_directory+write_name+'_to_burn.bil'):
    print("to_burn exists")
    try:
      os.remove(full_directory+write_name+'_to_burn.bil')
      os.remove(full_directory+write_name+'_to_burn.hdr')
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



#moving raster files to current directory

#shutil.copy2(summary_directory+fname+'.bil', current_path)
#shutil.copy2(summary_directory+fname+'.hdr', current_path)
try:
  shutil.copy2(summary_directory+fname+'_precipitation.bil',current_path+fname+'_precipitation.bil')
  shutil.copy2(summary_directory+fname+'_precipitation.hdr',current_path+fname+'_precipitation.hdr')
  shutil.copy2(summary_directory+fname+'_geology.bil',current_path+fname+'_geology.bil')
  shutil.copy2(summary_directory+fname+'_geology.hdr',current_path+fname+'_geology.hdr')
except:
  print("error moving rasters to burn")
#current path is fine as the data can be written in the source directory

#getting simplified zone raster
try:
  getRaster(current_path,summary_directory,fname,fname)
except:
  print("error getting tertiary burn raster")
  
#run_list = [25,30,35,40,45,50,55,60]
run_list = [10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]

for x in run_list:
  x = float(x)
  m_over_n = (x/100)
  if m_over_n >= 1:
    print('error in m_over_n number')
  
  print m_over_n
  mn_for_name = str(m_over_n)
  mn_for_name = mn_for_name.replace('.','_')
  chi = Ig.Iguanodon31(current_path, fname, writing_path = current_path,
                       writing_prefix = fname+str(mn_for_name), data_source = 'ready', 
                       preprocessing_raster = False, UTM_zone = '', south = False)
                     
  Ig.Iguanodon31.mchi_only(chi,minimum_basin_size_pixels = 20000, maximum_basin_size_pixels = 35000, 
                           m_over_n = m_over_n, threshold_contributing_pixels = 1000,
                           minimum_elevation = 350, maximum_elevation= 30000,burn_raster_to_csv = True,
                           secondary_burn_raster_to_csv = True, burn_raster_prefix = fname+'_geology',
                           secondary_burn_raster_prefix = fname+'_precipitation')

try:
  os.remove(current_path+fname+'_precipitation.bil')
  os.remove(current_path+fname+'_precipitation.hdr')
  os.remove(current_path+fname+'_geology.bil')
  os.remove(current_path+fname+'_geology.hdr')
except:
  print("error removing rasters to burn")


