#ice scraper
import pandas as pd

directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/'
name_list = ['0_1_ex_MChiSegmented_burned','0_15_ex_MChiSegmented_burned',
             '0_2_ex_MChiSegmented_burned','0_25_ex_MChiSegmented_burned',
             '0_3_ex_MChiSegmented_burned','0_35_ex_MChiSegmented_burned',
             '0_4_ex_MChiSegmented_burned','0_45_ex_MChiSegmented_burned',
             '0_5_ex_MChiSegmented_burned','0_55_ex_MChiSegmented_burned',
             '0_6_ex_MChiSegmented_burned','0_65_ex_MChiSegmented_burned',
             '0_7_ex_MChiSegmented_burned','0_75_ex_MChiSegmented_burned',
             '0_8_ex_MChiSegmented_burned','0_85_ex_MChiSegmented_burned',
             '0_9_ex_MChiSegmented_burned','0_95_ex_MChiSegmented_burned']
             
for name in name_list:
    with open(directory+name+'.csv','r') as csvfile:
        pandasDF = pd.read_csv(csvfile,delimiter=',')
        glimsDF = pandasDF[pandasDF['glaciated'] == 0]
        prefix = name.replace('_ex_MChiSegmented_burned','')
        glimDF = pandasDF[pandasDF['burned_data'] != 20000]
        glimsDF.to_csv(directory+prefix+'_GLIMS_ice_removed.csv',mode="w",header=True,index=False)
        glimDF.to_csv(directory+prefix+'_GLiM_ice_removed.csv',mode="w",header=True,index=False)
        