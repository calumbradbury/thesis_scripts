import gdal
import os
import osr

TRMM = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/TRMM_data/trmm2b31_annual_mm_per_year.tif' #source of the TRMM dataset


summary_directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_27.0_summary/'
fname = 'himalaya_27.0_12' 

#getting target srs from current DEM
ds = gdal.Open(summary_directory+fname+'.bil')
ds = ds.GetProjection()
ds = osr.SpatialReference(ds)
ds = ds.ExportToProj4()
print ds
print TRMM

extents = ['559222.8139456750359386','2931191.5925779701210558','659392.8139456750359386', '3042881.5925779701210558']

#translate raster
python = "gdalwarp -of ENVI -tr 90 90 -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te_srs '"+ds   +"' -te %s %s %s %s %s %s%s_LITHRAST.bil" %(extents[0],extents[1],extents[2],extents[3],TRMM,summary_directory,fname)
print python
os.system(python)


#reference gdal command which works in command line
#gdalwarp -of ENVI -s_srs 'EPSG:4326'  -t_srs '+proj=utm +zone=46 +datum=WGS84 +units=m +no_defs' -te 559222.8139456750359386 2931191.5925779701210558 659392.8139456750359386 3042881.5925779701210558 
#-te_srs '+proj=utm +zone=46 +datum=WGS84 +units=m +no_defs' -tr 30 30 /exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/TRMM_data/trmm2b31_annual_mm_per_year.tif 
#/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_27.0_summary/himalaya_27.0_12_30_trmm.bil


  def getTRMM(self,SRTM90,extents = []): #clips and rasterizes GLIM extents for current DEM. Saves to summary_directory
    
    #converting extents to UTM
    bottom_corner = utm.from_latlon(extents[1],extents[0])
    top_corner = utm.from_latlon(extents[3],extents[2])
    extent_utm = [bottom_corner[0],bottom_corner[1],top_corner[0],top_corner[1]]
    
    
    #source of the TRMM dataset
    TRMM = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/TRMM_data/trmm2b31_annual_mm_per_year.tif' 
    ds = gdal.Open(self.summary_directory+self.fname+'.bil')
        
    #getting target srs from current DEM
    ds = ds.GetProjection()
    ds = osr.SpatialReference(ds)
    ds = ds.ExportToProj4()
    
    #clipping raster, reprojecting, and setting resolution
    res_90 = "gdalwarp -of ENVI -tr 90 90 -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te_srs '"+ds   +"' -te %s %s %s %s %s %s%s_LITHRAST.bil" %(extent_utm[0],extent_utm[1],extent_utm[2],extent_utm[3],TRMM,self.summary_directory,self.fname)
    #print res_90
    res_30 = "gdalwarp -of ENVI -tr 30 30 -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -te_srs '"+ds   +"' -te %s %s %s %s %s %s%s_LITHRAST.bil" %(extent_utm[0],extent_utm[1],extent_utm[2],extent_utm[3],TRMM,self.summary_directory,self.fname)
    
        res_90 = "gdalwarp -ot Float64 -of ENVI -tr 90 90 -s_srs 'EPSG:4326' -t_srs"+" '"+ds+"' -cutline %s -crop_to_cutline %s %s%s_LITHRAST.bil" %(self.summary_directory+self.fname+'_index.shp',TRMM,self.summary_directory,self.fname)
    
    print 'srtm 90  is ...s...', SRTM90
    if SRTM90:
      os.system(res_90)
      print res_90
    else:
      os.system(res_30) 
      print res_30       
  




