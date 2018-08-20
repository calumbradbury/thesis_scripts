import pandas as pd

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/himalaya_27_5/27_50_86_70_himalaya_27_5_10/20000/1020000_35000_AllBasinsInfo.csv'




DF = pd.read_csv(target,delimiter = ',')

list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]

listSeries = pd.Series(list)
listDF = pd.DataFrame({'new_keys':list})
mergedDF = pd.merge(left=DF,right=listDF, left_index=True,right_index=True) 

mergedDF = mergedDF.rename(columns={"basin_key": "old_key","new_keys":"basin_key"})
print mergedDF
                                                         
                                                        