#joyplot

import joyplot
import pandas as pd
import scipy

joyplot.plt.switch_backend('agg')

target = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/Himalayan_front/ksn_concavity_0.5/'
directory = '/exports/csce/datastore/geos/users/s1134744/LSDTopoTools/Topographic_projects/full_himalaya/'


name_list = ['0_1_ex_MChiSegmented_burned','0_15_ex_MChiSegmented_burned',
             '0_2_ex_MChiSegmented_burned','0_25_ex_MChiSegmented_burned',
             '0_3_ex_MChiSegmented_burned','0_35_ex_MChiSegmented_burned',
             '0_4_ex_MChiSegmented_burned','0_45_ex_MChiSegmented_burned',
             '0_5_ex_MChiSegmented_burned','0_55_ex_MChiSegmented_burned',
             '0_6_ex_MChiSegmented_burned','0_65_ex_MChiSegmented_burned',
             '0_7_ex_MChiSegmented_burned','0_75_ex_MChiSegmented_burned',
             '0_8_ex_MChiSegmented_burned','0_85_ex_MChiSegmented_burned',
             '0_9_ex_MChiSegmented_burned','0_95_ex_MChiSegmented_burned']
             
def getSeries(name):
    with open(directory+name+'.csv','r') as csvfile:
        dataFrame = pd.read_csv(csvfile,delimiter=',')
        prefix = name.replace('_ex_MChiSegmented_burned','')
        dataFrame.rename(columns={'glaciated':prefix},inplace=True)
        series = dataFrame[prefix]                
        series.reset_index(drop=True, inplace=True)
        print "got data for %s"%(prefix)
        return series

mm_0_1 = getSeries('0_1_ex_MChiSegmented_burned')
mm_0_15 = getSeries('0_15_ex_MChiSegmented_burned')
mm_0_2 = getSeries('0_2_ex_MChiSegmented_burned')
mm_0_25 = getSeries('0_25_ex_MChiSegmented_burned')
mm_0_3 = getSeries('0_3_ex_MChiSegmented_burned')
mm_0_35 = getSeries('0_35_ex_MChiSegmented_burned')
mm_0_4 = getSeries('0_4_ex_MChiSegmented_burned')
mm_0_45 = getSeries('0_45_ex_MChiSegmented_burned')
mm_0_5 = getSeries('0_5_ex_MChiSegmented_burned')
mm_0_55 = getSeries('0_55_ex_MChiSegmented_burned')
mm_0_6 = getSeries('0_6_ex_MChiSegmented_burned')
mm_0_65 = getSeries('0_65_ex_MChiSegmented_burned')
mm_0_7 = getSeries('0_7_ex_MChiSegmented_burned')
mm_0_75 = getSeries('0_75_ex_MChiSegmented_burned')
mm_0_8 = getSeries('0_8_ex_MChiSegmented_burned')
mm_0_85 = getSeries('0_85_ex_MChiSegmented_burned')
mm_0_9 = getSeries('0_9_ex_MChiSegmented_burned')
mm_0_95 = getSeries('0_95_ex_MChiSegmented_burned')

new_DF = pd.concat([mm_0_1,mm_0_15,mm_0_2,mm_0_25,mm_0_3,mm_0_35,mm_0_4,mm_0_45,mm_0_5,mm_0_55,mm_0_6,mm_0_65,mm_0_7,mm_0_75,mm_0_8,mm_0_85,mm_0_9,mm_0_95],axis=1)
new_DF.to_csv(directory+'_merged_burned_glaciated.csv',mode='w',header=True,index=False)

#m_n = [0.8,0.9]
#x_spacing = 500
#for x in m_n:
with open(directory+'_merged_burned_glaciated.csv','r') as csvfile:
  df = pd.read_csv(csvfile,delimiter=',')
  #header_list = df.columns.values.tolist()
  #for name in header_list:
  #  count = counter(name,df)
  #  df.rename(columns={name:(name+' count: '+str(count))},inplace=True)  
  #df = df["secondary_burned_data"]
  #df = df.astype(int)
  #df = df.tolist()
  #print df
  #df = df['burned_data']
  fig,axes=joyplot.joyplot(df,figsize=(100,100),title='Lithology')
  #fig,axes=joyplot.joyplot(df,column=['0_1000 count: 33279','1000_2000 count: 2127','2000_3000 count: 1141','3000_4000 count: 600'],figsize=(20,10),x_range=[0,2000],title='Ice_and_Glacier')
  #fig,axes=joyplot.joyplot(df,column=['no_precip_MLE','precip_MLE'],figsize=(20,10),x_range=[-10,50])  
  #fig,axes=joyplot.joyplot(df,column=['burned_data'],figsize=(20,10))  
  #fig,axes=joyplot.joyplot(df,column=['difference(no_precip - precip)'],figsize=(20,5),x_range=[-10,10])
  fig.savefig(directory+'_joy_glaciated_all.png', bbox_inches='tight')
