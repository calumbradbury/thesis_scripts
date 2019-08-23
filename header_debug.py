import pandas as pd

def getDF(source):
    with open('/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya_5000/'+source,'r') as csvFile:
        csv = pd.read_csv(csvFile,delimiter=',')
        return csv

csv_a = getDF('0_1unique_MChiSegmented_burned.csv')
print csv_a.columns

csv_b = getDF('0_6_AllBasinsInfo.csv')
list_b = csv_b.columns.values.tolist()
list_a = csv_a.columns.values.tolist()

if list_b==list_a:
    print('equal')
    
else:
    print('not-equal')
