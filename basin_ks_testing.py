#BASIN  STATS INCLUDING KS

from scipy import stats
import os
import csv
import pandas as pd

directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/'

files = ['full_himalaya/full_concavity_basins_summary.csv','full_himalaya/concavity_bootstrap_basins_summary_processed.csv',
         'full_himalaya_5000/full_concavity_basins_summary.csv','full_himalaya_5000/concavity_bootstrap_basins_summary_processed.csv']
         
def returnSeries(source):
    DF = pd.read_csv(source,delimiter=',')
    series = DF['concavity_bootstrap']
    return series

def ks_2sample_test(pandasSeries_A,pandasSeries_B):
    list_A = pandasSeries_A.tolist()
    list_B = pandasSeries_B.tolist()
    statistic,p_value = stats.ks_2samp(list_A,list_B)
    return statistic,p_value

    
full_full_DF = returnSeries(directory+files[0]) 
full_GLIMS_DF = returnSeries(directory+files[1]) 
clip_full_DF = returnSeries(directory+files[2]) 
clip_GLIMS_DF = returnSeries(directory+files[3])

print "full DEM/full DEM",ks_2sample_test(full_full_DF,full_full_DF) 
print "full DEM/FULL-GLIMS",ks_2sample_test(full_full_DF,full_GLIMS_DF) 
print "full DEM/Clip-Full",ks_2sample_test(full_full_DF,clip_full_DF) 
print "full DEM/Clip-GLIMS",ks_2sample_test(full_full_DF,clip_GLIMS_DF) 
print ".............\n"
print "full GLIMS/full DEM",ks_2sample_test(full_GLIMS_DF,full_full_DF) 
print "full GLIMS/FULL-GLIMS",ks_2sample_test(full_GLIMS_DF,full_GLIMS_DF) 
print "full GLIMS/Clip-Full",ks_2sample_test(full_GLIMS_DF,clip_full_DF) 
print "full GLIMS/Clip-GLIMS",ks_2sample_test(full_GLIMS_DF,clip_GLIMS_DF) 
print ".............\n"
print "clip FULL/full DEM",ks_2sample_test(clip_full_DF,full_full_DF) 
print "clip FULL/FULL-GLIMS",ks_2sample_test(clip_full_DF,full_GLIMS_DF) 
print "clip FULL/Clip-Full",ks_2sample_test(clip_full_DF,clip_full_DF) 
print "clip FULL/Clip-GLIMS",ks_2sample_test(clip_full_DF,clip_GLIMS_DF) 
print ".............\n"
print "clip GLIMS/full DEM",ks_2sample_test(clip_GLIMS_DF,full_full_DF) 
print "clip GLIMS/FULL-GLIMS",ks_2sample_test(clip_GLIMS_DF,full_GLIMS_DF) 
print "clip GLIMS/Clip-Full",ks_2sample_test(clip_GLIMS_DF,clip_full_DF) 
print "clip GLIMS/Clip-GLIMS",ks_2sample_test(clip_GLIMS_DF,clip_GLIMS_DF) 
