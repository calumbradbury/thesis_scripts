import pandas as pd
import csv

#aim is to separate stats into separate csvs for each concavity

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/10_20k_TRMM_monsoon/himalaya_all/_merged_MN_nodata.csv'
target_2 = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/10_20k_TRMM_monsoon/himalaya_all/stats/'


m_n = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]

with open(target,'r') as csvfile:
  df=pd.read_csv(csvfile,delimiter=',') 
  for x in m_n:
    #x = str(x)
    df_selected = df[df["Median_MOverNs"] == x]  
    df_selected.to_csv(target_2+str(x)+'_merged.csv',mode = "w", header = True, index = False)

