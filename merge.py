import pandas as pd
import csv

target = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/annual.csv"
target_2 = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/_output_basin_TRMM_new.csv"
target_3 = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/_merged_MN_arc.csv"

with open(target,'r') as csvfile:
  pandas_a = pd.read_csv(csvfile,delimiter=',')
  with open(target_2,'r') as csvfile_b:
    pandas_b = pd.read_csv(csvfile_b,delimiter=',')
    pandas_a = pandas_a.merge(pandas_b, on=["basin_key"])
    pandas_a.to_csv(target_3, mode = "w", header = True, index = False)
