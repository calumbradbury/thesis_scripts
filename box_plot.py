# small tutorial to use pandas to create box and whisker plots
import matplotlib
matplotlib.use("Agg")

from matplotlib import pyplot as plt
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("number",nargs='?',default="none")
inputs = parser.parse_args()

number = inputs.number

# first step: read the file you want the information
## you'll have to adapt the path of your file
#df = pd.read_csv("/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/350_3500/himalaya_all/_output_litho_elevation.csv")
df = pd.read_csv("/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_all/burned_output_MChiSegmented.csv")
# your df (dataframe) now contains all the column and data of your csv file. 
# if you need to check the following command print the name of each columns:
#print(df.columns.values)

# I assume you have your file with all the geology correspondances ?
# you need to isolate the data bins you want
# imagine I want to plot the m_chi repartition for my lithologies 5, 11 and 13/15 grouped together: I need a list of the arrays



def write_box_wisker(number):
  number = int(number)
  df_meta = df[df["Metamorphics"] >= number] # the logic is: df_5 is equal to the entire df WHERE the column "geology" is 5
  # df_5 now contains all the information of my original file, but just when the column geology was 5
  #df_acid = df[df["Acid plutonic rocks"] >= perc]
  df_carb = df[df["Carbonate sedimentary rocks"] >= number] # same logic
  df_mix = df[df["Mixed sedimentary rocks"] >= number]
  df_sili = df[df["Siliciclastic sedimentary rocks"] >= number]
  
  #df_13_15 = df[df["geology"].isin([13,15])] # the logic is slightly different when you want to check several values


  # I want now to gather everything in a "list of arrays" to plot:
  data_to_plot = [df_meta["chi"],df_carb["chi"],df_mix["chi"],df_sili["chi"]] # I only want the column Median_MOv
  #data_to_plot = [df_meta["Median_MOv"],df_acid["Median_MOv"],df_carb["Median_MOv"],df_mix["Median_MOv"],df_sili["Median_MOv"]]
  #data_to_plot = [df_meta["Median_MOv"],df_carb["Median_MOv"],df_mix["Median_MOv"],df_sili["Median_MOv"]]
  # you want to name it as well, in the same order
  #names = ["Metamorphics", "Acid plutonic rocks", "Carbonate sedimentary rocks", "Mixed sedimentary rocks", "Siliciclastic sedimentary rocks"]
  names = ["Metamorphics", "Carbonate\n sedimentary rocks", "Mixed\n sedimentary rocks", "Siliciclastic\n sedimentary rocks"]
  # ok now we are ready to plot:

  # Create a figure
  fig = plt.figure(1, figsize=(15,9))

  # Create an axes
  ax = fig.add_subplot(111)
  #plt.rc('axes', titlesize=14) 
  #plt.rc('title', size=14) 
  plt.ylabel("m/n ratio", fontsize = 24)
  plt.title(("Lithology >= %s percent of basin")%(number), fontsize = 32)
  
  # Create the boxplot
  bp = ax.boxplot(data_to_plot, labels = names)
  plt.tick_params(axis='both', which='major', labelsize=18)
  # Save the figure
  print number
  fig.savefig('simple_test_'+str(number)+'_mchi_boxplot.png', bbox_inches='tight')

def box_wisker():
#  number = int(number)
  df_3 = df[df["burned_data"] == 3]
  df_5 = df[df["burned_data"] == 5]
  df_6 = df[df["burned_data"] == 6]
  df_9 = df[df["burned_data"] == 9]
#  print "total df_9:", df_9.chi.count()
  
  df_10 = df[df["burned_data"] == 10]
  df_11 = df[df["burned_data"] == 11]
  df_12 = df[df["burned_data"] == 12]
  df_14 = df[df["burned_data"] == 14]
  df_15 = df[df["burned_data"] == 15]
  # I want now to gather everything in a "list of arrays" to plot:
  data_to_plot = [df_3["chi"],df_5["chi"],df_6["chi"],df_9["chi"],df_10["chi"],df_11["chi"],df_12["chi"],df_14["chi"],df_15["chi"]] # I only want the column Median_MOv
  
  def count_total(dataframe):
     count = dataframe.chi.count()
     print count
     return count
    
  names = ["Metamorphics\n\n\n\n count: %s" %(count_total(df_3)), "Acid\n plutonic\n rocks\n\n count: %s" %(count_total(df_5)), "Basic\n plutonic\n rocks\n\n count: %s" %(count_total(df_6)),
   "Carbonate\n sedimentary\n rocks\n\n count: %s" %(count_total(df_9)),"Mixed\n sedimentary\n rocks\n\n count: %s" %(count_total(df_10)),"Siliciclastic\n sedimentary\n rocks\n\n count: %s" %(count_total(df_11)),
   "Unconsolidated\n sediments\n\n\n count: %s" %(count_total(df_12)),"Basic\n volcanic\n rocks\n\n count: %s" %(count_total(df_14)),"Intermediate\n volcanic\n rocks\n\n count: %s" %(count_total(df_15))]

  # ok now we are ready to plot:

  # Create a figure
  fig = plt.figure(1, figsize=(21,9))

  # Create an axes
  ax = fig.add_subplot(111)
  #plt.rc('axes', titlesize=14) 
  #plt.rc('title', size=14) 
  plt.ylabel("K_sn", fontsize = 24)
  #plt.title(("Lithology >= %s percent of basin"), fontsize = 32)
  
  # Create the boxplot
  bp = ax.boxplot(data_to_plot, labels = names)
  plt.tick_params(axis='both', which='major', labelsize=18)
  # Save the figure
  fig.savefig('simple_test__mchi_boxplot.png', bbox_inches='tight')

box_wisker()
#write_box_wisker(number)