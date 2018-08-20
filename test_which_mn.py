# box plot to visualise testing correct median m/n for landscape

import matplotlib
matplotlib.use("Agg")
from matplotlib import pyplot as plt
import csv
import pandas as pd
import os

path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'

with open(path+'disorder_out.csv') as csvfile:
  pandasDF = pd.read_csv(csvfile,delimiter=',')
  #selecting columns to plot
  #data_to_plot = [pandasDF["no_precip_mn"],pandasDF["precip_mn"]]
  data_to_plot = [pandasDF["no_precip_mn"]]
  #defining data labels
  #names = ["no_precip_mn","precip_mn"]
  names = ["no_precip_mn"]
  
  # Create a figure
  fig = plt.figure(1, figsize=(15,9))

  # Create an axes
  ax = fig.add_subplot(111)
  plt.ylabel("Concavity", fontsize = 24)
  plt.title("Concavity result - no chi precipitation, d = 0.05, iterations = 18, m_over_n = 0.3", fontsize = 32)
  
  # Create the boxplot
  bp = ax.boxplot(data_to_plot, labels = names)
  plt.tick_params(axis='both', which='major', labelsize=18)
  # Save the figure
  fig.savefig(path+'test_which_mn.png', bbox_inches='tight')
  
  print(pandasDF["no_precip_mn"].median())#,pandasDF["precip_mn"].median())