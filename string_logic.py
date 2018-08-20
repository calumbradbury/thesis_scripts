#string logic

glim_keys = ['Evaporites','Ice and Glaciers','Metamorphics','No Data',
               'Acid plutonic rocks','Basic plutonic rocks',
               'Intermediate plutonic rocks','Pyroclastics',
               'Carbonate sedimentary rocks','Mixed sedimentary rocks',
               'Siliciclastic sedimentary rocks','Unconsolidated sediments',
               'Acid volcanic rocks','Basic volcanic rocks',
               'Intermediate volcanic rocks','Water Bodies']
  
  
column_keys = ['10000_20000','20000_30000','30000_40000','40000_50000',
                 '50000_60000','60000_70000','70000_80000','80000_90000',
                 '90000_100000','100000_110000','110000_120000','120000_130000',
                 '130000_140000','140000_150000','150000_160000','160000_170000']
                 
column_to_replace = ['10000_20000','20000_30000','30000_40000','40000_50000',
                 '50000_60000','60000_70000','70000_80000','80000_90000',
                 '90000_100000','100000_110000','110000_120000','120000_130000',
                 '130000_140000','140000_150000','150000_160000','160000_170000']     
                 
                 
#for x in column_to_replace:
#  for y in column_keys:
#    try:
#      a = x.replace(y,'done')
#      print(a)
#    except:
#      print("error")
#  
#print(column_to_replace)

#for x,y in zip(column_keys,column_to_replace):

for x in column_keys:
  column_to_replace = [a.replace(x,'done') for a in column_to_replace]
  
#success!!!!
print(column_to_replace)              
                 
                 
                 
                 
