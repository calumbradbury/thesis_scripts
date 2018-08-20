#split into simplified geology
import pandas as pd

directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'
name = 'mchi_pandas_output_simplified.csv'

with open(directory+name,'r') as csvfile:
  pandasDF = pd.read_csv(csvfile,delimiter=',')
  df1 = pandasDF.loc[pandasDF['digitized']==1] 
  df2 = pandasDF.loc[pandasDF['digitized']==2] 
  df3 = pandasDF.loc[pandasDF['digitized']==3] 
  df4 = pandasDF.loc[pandasDF['digitized']==4] 
  df5 = pandasDF.loc[pandasDF['digitized']<1]
  print df5
  
  #df1.to_csv(directory+'mchi_pandas_output_sub.csv',mode='w',header=True,index=False)
  #df2.to_csv(directory+'mchi_pandas_output_lesser.csv',mode='w',header=True,index=False)
  #df3.to_csv(directory+'mchi_pandas_output_greater.csv',mode='w',header=True,index=False)
  #df4.to_csv(directory+'mchi_pandas_output_tethyan.csv',mode='w',header=True,index=False)
  
  