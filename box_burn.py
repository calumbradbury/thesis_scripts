# boxplots

import matplotlib
from scipy import stats as stats
matplotlib.use("Agg")

from matplotlib import pyplot as plt
import pandas as pd

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/'
name = 'mchi_pandas_output.csv'
#target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/precip_driven_chi_20_35k/himalaya_all/'
#name = 'precipitation_output_MChiSegmented_burn.csv'

lithology = True
precipitation = False
export = True

def counter(df):
  list_a = df["m_chi"]
  list_a = list_a.tolist()

  count = len(list_a)
  print count
  return str(count)  


with open(target+name,'r') as csvfile:
  #reading target
  df = pd.read_csv(csvfile,delimiter=',')
  #separate into pandasDF for each bin
  

  
  

  
  

  
  # I only want the column m_chi
  column = "m_chi"
  #column = "burned_data"
  #column = "secondary_burned_data"
  bins = 500
  #bins = 1000 

  
  if precipitation:
    #starting with precipitation values. 0 to 10000
    #start with bins of 500
    if bins == 500:
      df_1 = df[df["secondary_burned_data"].isin(range(0,500))]
      df_2 = df[df["secondary_burned_data"].isin(range(501,1000))]  
      df_3 = df[df["secondary_burned_data"].isin(range(1001,1501))]
      df_4 = df[df["secondary_burned_data"].isin(range(1501,2000))]  
      df_5 = df[df["secondary_burned_data"].isin(range(2001,2500))]
      df_6 = df[df["secondary_burned_data"].isin(range(2501,3000))]  
      df_7 = df[df["secondary_burned_data"].isin(range(3001,3500))]
      df_8 = df[df["secondary_burned_data"].isin(range(3501,4000))]  
      df_9 = df[df["secondary_burned_data"].isin(range(4001,4500))]
      df_10 = df[df["secondary_burned_data"].isin(range(4501,5000))]  
      df_11 = df[df["secondary_burned_data"].isin(range(5001,5500))]
      df_12 = df[df["secondary_burned_data"].isin(range(5501,6000))]  
      df_13 = df[df["secondary_burned_data"].isin(range(6001,6500))]
      df_14 = df[df["secondary_burned_data"].isin(range(6501,7000))]  
      df_15 = df[df["secondary_burned_data"].isin(range(7001,7500))]
      df_16 = df[df["secondary_burned_data"].isin(range(7501,8000))]  
      df_17 = df[df["secondary_burned_data"].isin(range(8001,8500))]
      df_18 = df[df["secondary_burned_data"].isin(range(8501,9000))]  
      df_19 = df[df["secondary_burned_data"].isin(range(9001,9500))]
      df_20 = df[df["secondary_burned_data"].isin(range(9501,10000))]  
    
    if bins == 1000:
      df_1 = df[df["secondary_burned_data"].isin(range(0,1000))]
      df_2 = df[df["secondary_burned_data"].isin(range(1001,2000))]  
      df_3 = df[df["secondary_burned_data"].isin(range(2001,3000))]
      df_4 = df[df["secondary_burned_data"].isin(range(3001,4000))]  
      df_5 = df[df["secondary_burned_data"].isin(range(4001,5000))]
      df_6 = df[df["secondary_burned_data"].isin(range(5001,6000))]  
      df_7 = df[df["secondary_burned_data"].isin(range(6001,7000))]
   
    if export:
      #df_1 = df_1["m_chi"]
      #df_1 = df_1.rename(columns={'m_chi' : '1000'},inplace=True)
      if bins ==1000:
      
        df_1.rename(columns={column:'0_1000'},inplace=True)
        df_1=df_1["0_1000"]
      
        df_2.rename(columns={column:'1000_2000'},inplace=True)
        df_2 = df_2["1000_2000"]
      
        df_3.rename(columns={column:'2000_3000'},inplace=True)
        df_3 = df_3["2000_3000"]    
      
        df_4.rename(columns={column:'3000_4000'},inplace=True)
        df_4 = df_4["3000_4000"]
      
        df_5.rename(columns={column:'4000_5000'},inplace=True)      
        df_5 = df_5["4000_5000"]
      
        df_6.rename(columns={column:'5000_6000'},inplace=True)      
        df_6 = df_6["5000_6000"]
      
        df_7.rename(columns={column:'6000_7000'},inplace=True)
        df_7 = df_7["6000_7000"]
      
        df_1.reset_index(drop=True, inplace=True)
        df_2.reset_index(drop=True, inplace=True)
        df_3.reset_index(drop=True, inplace=True)
        df_4.reset_index(drop=True, inplace=True)
        df_5.reset_index(drop=True, inplace=True)
        df_6.reset_index(drop=True, inplace=True)
        df_7.reset_index(drop=True, inplace=True)

        export_df = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_7],axis=1)
      #export_df = export_df.join(df_3)
      #export_df = export_df.join(df_4)
      #export_df = export_df.join(df_5)
      #export_df = export_df.join(df_6)
      #export_df = export_df.join(df_7)
      
      
        export_df.to_csv(target+column+"precipitation_bins_MChiSegmented_pandas.csv", mode="w",header=True,index=False)
      
      if bins ==500:
      
        df_1.rename(columns={column:'0_500'},inplace=True)
        df_1=df_1["0_500"]
      
        df_2.rename(columns={column:'500_1000'},inplace=True)
        df_2 = df_2["500_1000"]
      
        df_3.rename(columns={column:'1000_1500'},inplace=True)
        df_3 = df_3["1000_1500"]    
      
        df_4.rename(columns={column:'1500_2000'},inplace=True)
        df_4 = df_4["1500_2000"]
      
        df_5.rename(columns={column:'2000_2500'},inplace=True)      
        df_5 = df_5["2000_2500"]
      
        df_6.rename(columns={column:'2500_3000'},inplace=True)      
        df_6 = df_6["2500_3000"]
      
        df_7.rename(columns={column:'3000_3500'},inplace=True)
        df_7 = df_7["3000_3500"]
        
        df_8.rename(columns={column:'3500_4000'},inplace=True)
        df_8=df_8["3500_4000"]
      
        df_9.rename(columns={column:'4000_4500'},inplace=True)
        df_9 = df_9["4000_4500"]
      
        df_10.rename(columns={column:'4500_5000'},inplace=True)
        df_10 = df_10["4500_5000"]    
      
        df_11.rename(columns={column:'5000_5500'},inplace=True)
        df_11 = df_11["5000_5500"]
      
        df_12.rename(columns={column:'5500_6000'},inplace=True)      
        df_12 = df_12["5500_6000"]
      
        df_13.rename(columns={column:'6000_6500'},inplace=True)      
        df_13 = df_13["6000_6500"]
      
        df_14.rename(columns={column:'6500_7000'},inplace=True)
        df_14 = df_14["6500_7000"]      
        
        df_1.reset_index(drop=True, inplace=True)
        df_2.reset_index(drop=True, inplace=True)
        df_3.reset_index(drop=True, inplace=True)
        df_4.reset_index(drop=True, inplace=True)
        df_5.reset_index(drop=True, inplace=True)
        df_6.reset_index(drop=True, inplace=True)
        df_7.reset_index(drop=True, inplace=True)
        df_8.reset_index(drop=True, inplace=True)
        df_9.reset_index(drop=True, inplace=True)
        df_10.reset_index(drop=True, inplace=True)
        df_11.reset_index(drop=True, inplace=True)
        df_12.reset_index(drop=True, inplace=True)
        df_13.reset_index(drop=True, inplace=True)
        df_14.reset_index(drop=True, inplace=True)


        export_df = pd.concat([df_1,df_2,df_3,df_4,df_5,df_6,df_7,df_8,df_9,df_10,df_11,df_12,df_13,df_14],axis=1)
      #export_df = export_df.join(df_3)
      #export_df = export_df.join(df_4)
      #export_df = export_df.join(df_5)
      #export_df = export_df.join(df_6)
      #export_df = export_df.join(df_7)
      
      
        export_df.to_csv(target+column+"precipitation_500_bins_MChiSegmented.csv", mode="w",header=True,index=False)      
      #df_1.to_csv(target+"0_1000_MChiSegmented.csv", mode="w",header=True,index=False)
      #df_2.to_csv(target+"1000_2000_MChiSegmented.csv", mode="w",header=True,index=False)
      #df_3.to_csv(target+"2000_3000_MChiSegmented.csv", mode="w",header=True,index=False)  
    
    #read all precipitation bins
    
    ### This didn't work because the isin method cannot select float values, so these were all missed out.
    #removing isolated outlying results
    #df_3 = df_3[df_3["m_chi"].isin(range(0,4000))]
    
    #data_to_plot = [df_1[column], df_2[column], df_3[column],df_4[column],
    #                df_5[column], df_6[column],df_7[column],df_8[column],
    #                df_9[column], df_10[column],df_11[column], df_12[column],
    #                df_13[column], df_14[column]]
                    #, df_15[column], df_16[column],
                    #df_17[column],df_18[column], df_19[column], df_20[column]]
    
    names = ["0-500","500-1000","1000-1500","1500-2000","2000-2500","2500-3000",
              "3000-3500","3500-4000","4000-4500","4500-5000","5000-5500",
              "5500-6000","6000-6500","6500-7000"]
            #,"15","16","17","18","19","20"]  
    
  if lithology:
    #reading into lithology bins
    lf_1 = df[df["burned_data"].isin(range(10000,19999))]
    lf_2 = df[df["burned_data"].isin(range(20000,29999))]  
    lf_3 = df[df["burned_data"].isin(range(30000,39999))]
    lf_4 = df[df["burned_data"].isin(range(40000,49999))]  
    lf_5 = df[df["burned_data"].isin(range(50000,59999))]
    lf_6 = df[df["burned_data"].isin(range(60000,69999))]  
    lf_7 = df[df["burned_data"].isin(range(70000,79999))]
    lf_8 = df[df["burned_data"].isin(range(80000,89999))]  
    lf_9 = df[df["burned_data"].isin(range(90000,99999))]
    lf_10 = df[df["burned_data"].isin(range(100000,109999))]  
    lf_11 = df[df["burned_data"].isin(range(110000,119999))]
    lf_12 = df[df["burned_data"].isin(range(120000,129999))]  
    lf_13 = df[df["burned_data"].isin(range(130000,139999))]
    lf_14 = df[df["burned_data"].isin(range(140000,149999))]  
    lf_15 = df[df["burned_data"].isin(range(150000,159999))]
    lf_16 = df[df["burned_data"].isin(range(160000,169999))]  

    #if export:
      #lf_1.to_csv(target+"Evaporites_MChiSegmented.csv", mode="w",header=True,index=False)
      #lf_2.to_csv(target+"IceandGlaciers_MChiSegmented.csv", mode="w",header=True,index=False)
      #lf_3.to_csv(target+"Metamorphics_MChiSegmented.csv", mode="w",header=True,index=False)  

    #removing isolated outlying results
    #lf_3 = lf_3[lf_3["m_chi"].isin(range(0,4000))] 
    
    data_to_plot = [lf_1[column], lf_2[column], lf_3[column],lf_4[column],
                    lf_5[column], lf_6[column],lf_7[column],lf_8[column],
                    lf_9[column], lf_10[column],lf_11[column], lf_12[column],
                    lf_13[column], lf_14[column],lf_15[column], lf_16[column]]
  
  


    names = ["Evaporites","Ice \n and \n Glaciers","Metamorphics","NoData",
             "Acid \n Plutonic \n Rocks","Basin \n Plutonic \n Rocks",
             "Intermediate \n Plutonic \n Rocks","Pyroclastics","Carbonate \n Sedimentary \n Rocks",
             "Mixed \n Sedimentary \n Rocks","Siliciclastic \n Sedimentary \n Rocks",
             "Unconsolidated \n Sediments","Acid \n Volcanic \n Rocks","Basic \n Volcanic \n Rocks",
             "Intermediate \n Volcanic \n Rocks","Water \n Bodies"]
          #,"17","18","19","20"]
    
    if export:
      #df_1 = df_1["m_chi"]
      #df_1 = df_1.rename(columns={'m_chi' : '1000'},inplace=True)
      count_lf_3 = counter(lf_3)
      #print(lf_3)
      lf_3.rename(columns={column:'Metamorphics count:'+count_lf_3},inplace=True)
#      print(lf_3)
      lf_3=lf_3['Metamorphics count:'+count_lf_3]

      count_lf_5 = counter(lf_5)      
      lf_5.rename(columns={column:'Acid Plutonic count:'+count_lf_5},inplace=True)
      lf_5 = lf_5['Acid Plutonic count:'+count_lf_5]

      count_lf_6 = counter(lf_6)      
      lf_6.rename(columns={column:'Basic Plutonic count:'+count_lf_6},inplace=True)
      lf_6 = lf_6['Basic Plutonic count:'+count_lf_6]    

      count_lf_14 = counter(lf_14)      
      lf_14.rename(columns={column:'Basin Volcanic count:'+count_lf_14},inplace=True)
      lf_14 = lf_14['Basin Volcanic count:'+count_lf_14]

      count_lf_9 = counter(lf_9)
      lf_9.rename(columns={column:'carb_sed count:'+count_lf_9},inplace=True)
      lf_9=lf_9['carb_sed count:'+count_lf_9]
      
      count_lf_10 = counter(lf_10)
      lf_10.rename(columns={column:'mix_sed count:'+count_lf_10},inplace=True)
#      mixed_sed = lf_10[['mix_sed','secondary_burned_data']]
#      count_lf_10 = counter(lf_10)
#      mixed_sed.to_csv(target+'mixed_sed.csv',mode='w',header=True,index=False) 
      lf_10 = lf_10['mix_sed count:'+count_lf_10]      
      
      count_lf_11 = counter(lf_11)
      lf_11.rename(columns={column:'sili_sed count:'+count_lf_11},inplace=True)
      lf_11 = lf_11['sili_sed count:'+count_lf_11]    
      
      count_lf_12 = counter(lf_12)
      lf_12.rename(columns={column:'uncon_sed count:'+count_lf_12},inplace=True)
      lf_12 = lf_12['uncon_sed count:'+count_lf_12]
      
     
      lf_12.reset_index(drop=True, inplace=True)
      lf_9.reset_index(drop=True, inplace=True)
      lf_10.reset_index(drop=True, inplace=True)
      lf_11.reset_index(drop=True, inplace=True)
      lf_3.reset_index(drop=True, inplace=True)
      lf_5.reset_index(drop=True, inplace=True)
      lf_6.reset_index(drop=True, inplace=True)
      lf_14.reset_index(drop=True, inplace=True)
      #df_5.reset_index(drop=True, inplace=True)
      #df_6.reset_index(drop=True, inplace=True)
      #df_7.reset_index(drop=True, inplace=True)

      export_df = pd.concat([lf_12,lf_9,lf_10,lf_11,lf_3,lf_5,lf_6,lf_14],axis=1)
      #export_df = export_df.join(df_3)
      #export_df = export_df.join(df_4)
      #export_df = export_df.join(df_5)
      #export_df = export_df.join(df_6)
      #export_df = export_df.join(df_7)
      
      
      export_df.to_csv(target+column+"lithology_bins_MChiSegmented_pandas.csv", mode="w",header=True,index=False)  
  
  #ks stat testing
  #convert to list (array)
  #df_1 = df_1["m_chi"].tolist()
  #df_2 = df_2["m_chi"].tolist()
  #df_3 = df_3["m_chi"].tolist()
  #df_4 = df_4["m_chi"].tolist()
  #df_5 = df_5["m_chi"].tolist()
  #df_6 = df_6["m_chi"].tolist()
  #df_7 = df_7["m_chi"].tolist()
  #df_8 = df_8["m_chi"].tolist()
  #df_9 = df_9["m_chi"].tolist()
  #df_10 = df_10["m_chi"].tolist()
  #df_11 = df_11["m_chi"].tolist()
  #df_12 = df_12["m_chi"].tolist()
  #df_13 = df_13["m_chi"].tolist()
  #df_14 = df_14["m_chi"].tolist()  
  #df = df["m_chi"].tolist()
  #print stats.ks_2samp(df_1,df)
  #print stats.ks_2samp(df_2,df)
  #print stats.ks_2samp(df_3,df)
  #print stats.ks_2samp(df_4,df)
  #print stats.ks_2samp(df_5,df)
  #print stats.ks_2samp(df_6,df)
  #
  #print "one sided ks follows"
  #print stats.kstest(df_3,'norm',alternative='two-sided')
  #print stats.ks_2samp(df_7,df)
  #print stats.ks_2samp(df_8,df)
  #print stats.ks_2samp(df_9,df)
  #print stats.ks_2samp(df_10,df)
  #print stats.ks_2samp(df_12,df)
  #print stats.ks_2samp(df_13,df)
  #print stats.ks_2samp(df_14,df_14)

  
  # ok now we are ready to plot:
  # Create a figure
  fig = plt.figure(1, figsize=(20, 10))
  
  # Create an axes
  ax = fig.add_subplot(111)
  
  
  #df_x = df["secondary_burned_data"]

  #df_y = df["m_chi"]
  
  # Create the boxplot
  #if not export:
  #  bp = ax.boxplot(data_to_plot, labels = names)
  #bp = ax.scatter(df_x,df_y,marker='.')
  
  #plt.title("Precipitation bins \n no chi precipitation", fontsize = 24)
  #plt.title("Precipitation bins \n chi precipitation", fontsize = 24)
  plt.title("Lithology bins \n no chi precipitation", fontsize = 24)
  #plt.title("Lithology bins \n chi precipitation", fontsize = 24)
  
  if lithology and not export:
    fig.savefig(target+'lithology.png', bbox_inches='tight')         
  #if precipitation and not export:
    #fig.savefig(target+'precipiation-annual.png', bbox_inches='tight')