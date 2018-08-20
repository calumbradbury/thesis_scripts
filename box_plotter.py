# boxplots

import matplotlib
from scipy import stats as stats
matplotlib.use("Agg")

from matplotlib import pyplot as plt
import pandas as pd

path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'
filename = 'lithology_bins_MChiSegmented_pandas'

with open(path+filename+'.csv','r') as csvfile:
  df = pd.read_csv(csvfile,delimiter=',')

#  data_to_plot = []
#  name = []
  
  header_list = df.columns.values.tolist()
#  data_to_plot = df.values.tolist()
#  print header_list
  labels = []
  
  for column in header_list:
    label = column.replace(' ','\n')
    label = label.replace('count:','')
    label = label.replace('_','\n')
    df.rename(columns={column:label},inplace=True)
    
  new_labels = df.columns.values.tolist()
  print new_labels

  
#  print data_to_plot
  # Create a figure
  fig = plt.figure(1, figsize=(15,9))

  # Create an axes
  ax = fig.add_subplot(111)
  plt.ylabel("KSN", fontsize = 24)
  plt.title("KSN - lithology", fontsize = 32)
  
  # Create the boxplot
  #bp = ax.boxplot(data_to_plot, labels=header_list, showfliers=False)
  bp = df.boxplot(showfliers=False)
  
  plt.tick_params(axis='both', which='major', labelsize=18)
  # Save the figure
  fig.savefig(path+filename+'.png', bbox_inches='tight')
  
