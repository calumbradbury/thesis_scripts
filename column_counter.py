#litho_counter
#independent script to verify lithology counts

import pandas as pd

def counter(df):
  series = df["burned_data"]
  list_a = series.tolist()
  return len(list_a)
  
def writer(name,count):
  with open('/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/litho_counting.txt','a') as param:
    param.write(name+' count is '+str(count)+'\n')
  

with open('/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/mchi_pandas_output.csv','r') as csvfile:
  data = pd.read_csv(csvfile,delimiter=',')
  columns = data.columns.values.tolist()
  series = data["burned_data"]
  list_b = series.tolist()
  writer('total',len(list_b))
  #df = data[data["burned_data"].isin(range(30000,39999))]
  count_evaporites = counter(data[data["burned_data"].isin(range(10000,19999))])
  writer('Evaporites',count_evaporites)
  
  count_iceglacier = counter(data[data["burned_data"].isin(range(20000,29999))])
  writer('Ice and Glacier',count_iceglacier)
  
  count_metamorphic = counter(data[data["burned_data"].isin(range(30000,39999))])
  writer('Metamorphic',count_metamorphic)
  
  count_nodata = counter(data[data["burned_data"].isin(range(40000,49999))])
  writer('NoData',count_nodata)
  
  count_acidplutonic = counter(data[data["burned_data"].isin(range(50000,59999))])
  writer('Acid plutonic rocks',count_acidplutonic)
  
  count_basicplutonic = counter(data[data["burned_data"].isin(range(60000,69999))])
  writer('Basic plutonic rocks',count_basicplutonic)

  count_intermediateplutonic = counter(data[data["burned_data"].isin(range(70000,79999))])
  writer('Intermediate plutonic rocks',count_intermediateplutonic)
  
  count_pyro = counter(data[data["burned_data"].isin(range(80000,89999))])
  writer('Pyroclastics',count_pyro)
  
  count_carbsed = counter(data[data["burned_data"].isin(range(90000,99999))])
  writer('Carbonate sedimentary rocks',count_carbsed)

  count_mixsed = counter(data[data["burned_data"].isin(range(100000,109999))])
  writer('Mixed sedimentary rocks',count_mixsed)
  
  count_silised = counter(data[data["burned_data"].isin(range(110000,119999))])
  writer('Siliciclastic sedimentary rocks',count_silised)
  
  count_unconsed = counter(data[data["burned_data"].isin(range(120000,129999))])
  writer('Unconsolidated sediments',count_unconsed)

  count_acidvolcanic = counter(data[data["burned_data"].isin(range(130000,139999))])
  writer('Acid volcanic rocks',count_acidvolcanic)
  
  count_basicvolcanic = counter(data[data["burned_data"].isin(range(140000,149999))])
  writer('Basic volcanic rocks',count_basicvolcanic)
  
  count_intvolcanic = counter(data[data["burned_data"].isin(range(150000,159999))])
  writer('Intermediate volcanic rocks',count_intvolcanic)
  
  count_water = counter(data[data["burned_data"].isin(range(160000,169999))])
  writer('Water Bodies',count_water)
  
  count_precambrian = counter(data[data["burned_data"].isin(range(170000,179999))])
  writer('Precambrian rocks',count_precambrian)
  
  count_complex = counter(data[data["burned_data"].isin(range(180000,189999))])
  writer('Complex lithology',count_complex)
