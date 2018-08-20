# small tutorial to use pandas to create box and whisker plots
import matplotlib
matplotlib.use("Agg")

from matplotlib import pyplot as plt
import pandas as pd

# first step: read the file you want the information
## you'll have to adapt the path of your file
#df = pd.read_csv("/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/full_year_350_TRMM_100_140k/himalaya_all/_output_basin_TRMM_new.csv")
#df = pd.read_csv("/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/full_year_350_TRMM_100_140k/himalaya_all/_output_MChiSegmented_export.csv")
df = pd.read_csv("/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/_merged_MN_arc.csv")
#df = pd.read_csv("/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/TRMM_data/annual.csv")                  
#df = pd.read_csv("/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/full_year_350_TRMM_100_140k/himalaya_all/_merged_MN.csv")
#plotting column

#column = "Median_MOverNs"
#column="chi"

#column_a = "burned_data"
#column_a = "raster_point"
#column_a = "mean annual rainfall (mm)"
#column_a = "mean annual rainfall (mm)_y"
#column_a = "mean jun/jul/aug rainfall (mm)"


#column = "chi"

# your df (dataframe) now contains all the column and data of your csv file. 
# if you need to check the following command print the name of each columns:
#print(df.columns.values)

# I assume you have your file with all the geology correspondances ?
# you need to isolate the data bins you want
# imagine I want to plot the m_chi repartition for my lithologies 5, 11 and 13/15 grouped together: I need a list of the arrays

def count_total(dataframe):
  count = dataframe.basin_key.count()
  print count
  return count


div_500 = False
div_1000 = False
m_over_n = True

x = 0.9     

if div_500:
  column_a = "burned_data"
  column = "chi"
  
  df = df_original[df_original["Median_MOverNs"]==x]
  df_1 = df[df[column_a].isin(range(0,500))] # the logic is: df_5 is equal to the entire df WHERE the column "geology" is 5
  df_2 = df[df[column_a].isin(range(501,1000))]
  df_3 = df[df[column_a].isin(range(1001,1500))] # the logic is: df_5 is equal to the entire df WHERE the column "geology" is 5
  df_4 = df[df[column_a].isin(range(1501,2000))]
  df_5 = df[df[column_a].isin(range(2001,2500))]
  df_6 = df[df[column_a].isin(range(2501,3000))]
  df_7 = df[df[column_a].isin(range(3001,3500))]
  df_8 = df[df[column_a].isin(range(3501,4000))]
  df_9 = df[df[column_a].isin(range(4001,4500))]
  df_10 = df[df[column_a].isin(range(4501,5000))]
  df_11 = df[df[column_a].isin(range(5001,5500))]
  df_12 = df[df[column_a].isin(range(5501,6000))]
  df_13 = df[df[column_a].isin(range(6001,6500))]
  df_14 = df[df[column_a].isin(range(6501,7000))]


    # I want now to gather everything in a "list of arrays" to plot:
    #data_to_plot = [df_1[column], df_2[column], df_3[column],df_4[column], df_5[column], df_6[column],df_7[column], df_8[column], df_9[column],df_10[column],df_11[column],df_12[column],df_13[column],df_14[column]] # I only want the column m_chi
  data_to_plot = [df_1[column], df_2[column], df_3[column],df_4[column], df_5[column], df_6[column],df_7[column]] # I only want the column m_chi
    # you want to name it as well, in the same order
    #names = ["0-500", "500-1000", "1000-1500", "1500-2000","2000-2500", "2500-3000","3000-3500", "3500-4000","4000-4500", "4500-5000","5000-5500","5500-6000","6000-6500","6500-7000"]
  names = ["0-500", "500-1000", "1000-1500", "1500-2000","2000-2500", "2500-3000","3000-3500"]
    #df_x = df["burned_data"]
    #df_y = df["chi"]
    # ok now we are ready to plot:
    # Create a figure
  fig = plt.figure(1, figsize=(15, 15))
    # Create an axes
  ax = fig.add_subplot(111)
    # Create the boxplot
  bp = ax.boxplot(data_to_plot, labels = names)
    #bp = ax.scatter(df_x,df_y,marker='.')
  
  fig.savefig('%s_average_basin_chi_20_35k_monsoon.png'%(x), bbox_inches='tight')

if m_over_n:
  column = "Median_MOverNs"
  column_a = "RASTERVALU"
  df_1 = df[df[column] == 0.1] # the logic is: df_5 is equal to the entire df WHERE the column "geology" is 5
  df_2 = df[df[column] == 0.2]
  df_3 = df[df[column] == 0.3]
  df_4 = df[df[column] == 0.4]
  df_5 = df[df[column] == 0.5]
  df_6 = df[df[column] == 0.6]
  df_7 = df[df[column] == 0.7]
  df_8 = df[df[column] == 0.8]
  df_9 = df[df[column] == 0.9]


  #.ge(0) removes nodata values
  # I want now to gather everything in a "list of arrays" to plot:
  data_to_plot = [df_1[column_a], df_2[column_a], df_3[column_a],df_4[column_a], df_5[column_a], df_6[column_a],df_7[column_a],df_8[column_a],df_9[column_a]] # I only want the column m_chi
  # you want to name it as well, in the same order
  names = ["0.1 \n count:\n %s" %(count_total(df_1)),"0.2 \n count:\n %s" %(count_total(df_2)),"0.3 \n count:\n %s" %(count_total(df_3)),"0.4 \n count:\n %s" %(count_total(df_4)),"0.5 \n count:\n %s" %(count_total(df_5)),
  "0.6 \n count:\n %s" %(count_total(df_6)),"0.7 \n count:\n %s" %(count_total(df_7)),"0.8 \n count:\n %s" %(count_total(df_8)),"0.9 \n count:\n %s" %(count_total(df_9))]

  #df_x = df["burned_data"]

  #df_y = df["chi"]

  # ok now we are ready to plot:

  # Create a figure
  fig = plt.figure(1, figsize=(10, 10))

  # Create an axes
  ax = fig.add_subplot(111)
  
  # Create the boxplot
  bp = ax.boxplot(data_to_plot, labels = names)
  #bp = ax.scatter(df_x,df_y,marker='.')
  
  #adding labeling
  plt.ylabel("latitude", fontsize = 18)   
  plt.xlabel("M/N", fontsize = 18)
  plt.title("Monsoon average - 20 to 35k", fontsize = 24)
  #plt.ylim(ymin=0)
  fig.savefig('average_basin_lat_20_35k_monsoon.png', bbox_inches='tight')
  



if div_1000:
  df_1 = df[df[column_a].isin(range(0,1000))] # the logic is: df_5 is equal to the entire df WHERE the column "geology" is 5
  df_2 = df[df[column_a].isin(range(1001,2000))]
  df_3 = df[df[column_a].isin(range(2001,3000))]
  df_4 = df[df[column_a].isin(range(3001,4000))]
  df_5 = df[df[column_a].isin(range(4001,5000))]
  df_6 = df[df[column_a].isin(range(5001,6000))]
  df_7 = df[df[column_a].isin(range(6001,7000))]



  # I want now to gather everything in a "list of arrays" to plot:
  data_to_plot = [df_1[column], df_2[column], df_3[column],df_4[column], df_5[column], df_6[column],df_7[column]] # I only want the column m_chi
  # you want to name it as well, in the same order
  names = ["0-1000", "1000-2000", "2000-3000", "3000-4000","4000-5000", "5000-6000","6000-7000"]

  #df_x = df["burned_data"]

  #df_y = df["chi"]

  # ok now we are ready to plot:

  # Create a figure
  fig = plt.figure(1, figsize=(20, 20))                                            

  # Create an axes
  ax = fig.add_subplot(111)
  
  # Create the boxplot
  bp = ax.boxplot(data_to_plot, labels = names)
  #bp = ax.scatter(df_x,df_y,marker='.')

# Save the figure
fig.savefig('average_basin_MN_20_35k_monsoon.png', bbox_inches='tight')
