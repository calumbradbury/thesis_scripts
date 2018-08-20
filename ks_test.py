#ks testing

from scipy import stats
import os
import csv
import pandas as pd

directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'

file = 'precipitation_500_bins_MChiSegmented.csv'

def getHeaderList():
  with open(directory+file,'r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    header_list = pandasDF.columns.values.tolist()
    #print header_list
    return header_list

def getPandasSeries(column_A,column_B):
  with open(directory+file,'r') as csvfile:
    pandasDF = pd.read_csv(csvfile,delimiter=',')
    pandasSeries_A = pandasDF[column_A]
    pandasSeries_B = pandasDF[column_B]  
    return pandasSeries_A,pandasSeries_B

def ks_2sample_test(pandasSeries_A,pandasSeries_B):
  list_A = pandasSeries_A.tolist()
  list_B = pandasSeries_B.tolist()
  statistic,p_value = stats.ks_2samp(list_A,list_B)
  return statistic,p_value
  
def exportResult(combination,statistic,p_value):
  if not os.path.isfile(directory+'ks_precipitation_results.csv'):
    with open(directory+'ks_precipitation_results.csv','wb') as write_csv:
      csvWrite = csv.writer(write_csv,delimiter=',')
      csvWrite.writerow(('combination','statistic','p_value'))
  
  with open(directory+'ks_precipitation_results.csv','a') as write_csv_b:
    csvWriter = csv.writer(write_csv_b,delimiter=',')
    csvWriter.writerow((combination,statistic,p_value))
  
header_list = getHeaderList()

for x in header_list:
  column_A = str(x)
  for y in header_list:
    column_B = str(y)
    combination = column_A+' '+column_B
    print combination
    pandasSeries_A,pandasSeries_B=getPandasSeries(column_A,column_B)
    statistic,p_value = ks_2sample_test(pandasSeries_A,pandasSeries_B)
    exportResult(combination,statistic,p_value)
    
#print header_list  
#combination = column_A+' '+column_B
#statistic,p_value = ks_2sample_test(pandasSeries_A,pandasSeries_B)
  
#exportResult(combination,statistic,p_value)