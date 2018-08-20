#box plot precipitation in litho_bins

import matplotlib
from scipy import stats as stats
matplotlib.use("Agg")

from matplotlib import pyplot as plt
import pandas as pd

import joyplot
joyplot.plt.switch_backend('agg')

path = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'
filename = 'secondary_burned_datalithology_bins_MChiSegmented_pandas'

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
  plt.ylabel("Precipitation", fontsize = 24)
  plt.title("Lithology - precipitation", fontsize = 32)
  
  # Create the boxplot
  #bp = ax.boxplot(data_to_plot, labels=header_list, showfliers=False)
  bp = df.boxplot(showfliers=False)
  
  plt.tick_params(axis='both', which='major', labelsize=18)
  # Save the figure
  fig.savefig(path+filename+'.png', bbox_inches='tight')
  
with open(path+filename+'.csv','r') as csvfile:
  df = pd.read_csv(csvfile,delimiter=',')
  #header_list = df.columns.values.tolist()
  #for name in header_list:
  #  count = counter(name,df)
  #  df.rename(columns={name:(name+' count: '+str(count))},inplace=True)  
  #df = df["secondary_burned_data"]
  #df = df.astype(int)
  #df = df.tolist()
  #print df
  fig,axes=joyplot.joyplot(df,figsize=(20,10),x_range=[0,2500],title='Precipiation Lithology Bins')
  #fig,axes=joyplot.joyplot(df,column=['0_1000 count: 33279','1000_2000 count: 2127','2000_3000 count: 1141','3000_4000 count: 600'],figsize=(20,10),x_range=[0,2000],title='Ice_and_Glacier')
  #fig,axes=joyplot.joyplot(df,column=['no_precip_MLE','precip_MLE'],figsize=(20,10),x_range=[-10,50])  
  #fig,axes=joyplot.joyplot(df,column=['difference(no_precip - precip)'],figsize=(20,5),x_range=[-10,10])
  fig.savefig(path+'_joy_precip_lito.png', bbox_inches='tight')