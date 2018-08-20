#no data correction
#replacing all values <0 with 0

import pandas as pd

target = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/_merged_MN.csv"
target2 = "/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/_merged_MN_nodata.csv"

with open(target,'r') as csvfile:
  pandasDF = pd.read_csv(csvfile,delimiter=',')
  pandasDF.loc[pandasDF['burned_data'] < 0, 'burned_data'] = 0
  print pandasDF
  pandasDF.to_csv(target2, mode = "w", header = True, index = False)