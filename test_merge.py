import pandas as pd

current_path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/350_3500/himalaya_27.0/27.00_86.22_himalaya_27.0_2/20000/'
writing_prefix = '220000_35000'




with open(current_path+writing_prefix+'_chi_data_map_burned.csv','r') as chi:
  pandasChi = pd.read_csv(chi, delimiter = ',')
  burned_data = pandasChi[["burned_data","latitude","longitude"]]
  burned_data[["latitude","longitude"]] = burned_data[["latitude","longitude"]].round(4)
  #print burned_data  
  with open(current_path+writing_prefix+'_MChiSegmented.csv','r') as mchi:
    pandasMChi = pd.read_csv(mchi, delimiter = ',')
    pandasMChi[["latitude","longitude"]] = pandasMChi[["latitude","longitude"]].round(4)
    burned_data = burned_data.merge(pandasMChi,on=["latitude","longitude"])
    #print pandasMChi
    #print burned_data
    
    burned_data.to_csv(current_path+writing_prefix+'_MChiSegmented_burn.csv', mode = "w", header = True, index = False)