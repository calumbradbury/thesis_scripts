#extacting variables
import pandas as pd
import csv

source = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/himalaya_27.0_summary/'
name = 'testing'


def writeHeader(file_name,target_name):
  with open(source+file_name+'.csv','r') as sourceheader_csv:
    pandasDF=pd.read_csv(sourceheader_csv,delimiter=',')
    header_list = pandasDF.columns.values.tolist()
  
    with open(source+name+'_output'+target_name+'.csv','wb') as writeheader_csv:
      csvWriter = csv.writer(writeheader_csv,delimiter = ',')
      csvWriter.writerow(header_list)

writeHeader(file_name="120000_35000_MChiSegmented_burn",target_name="_MChiSegmented_burn")
#writeHeader("1820000_35000_basin_TRMM")



#with open(source+'27_output_MChiSegmented_burn.csv','r') as csvfile:
#  pandasDF = pd.read_csv(csvfile,delimiter=',')
#  #getting column names as list
#  header_list = pandasDF.columns.values.tolist()
#  print header_list
  


#with open (source+"himalaya_27.0_2_upper_right.txt", "r") as myfile:
#    data=myfile.read().replace(',', '')
#    data = data.replace('(','')
#    data = data.replace(')','')
#    test = data.split()
#    print test[2]
#    print test[3]

#one = True
#two = True

#if one and not two:
#  print "correct"

#list = []
#print len(list)

#print bool(list)