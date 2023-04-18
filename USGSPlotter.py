# -*- coding: utf-8 -*-
"""
Spyder Editor

This Script was created to deal with the USGS water data needed for Table 3
in the PFAS PMR report 2021. It will automatically pull the necessary tables 
and estimate max and min discharge for USGS 04133501
"""
import hydrofunctions as hf

#inputs

SiteCode = '04133501'

'''
If you want to run this code for different dates, please change the start & end values, make sure to keep 
the format as YYYY-MM-DD or code will not work
'''

start = '2020-11-23'
end = '2021-12-31'


#%% Read in the Discharge data and rework it for table 3 in the 2021 PFAS PMR

ThunderBay = hf.NWIS(SiteCode, 'dv', start, end)

dfFlow = ThunderBay.df()

dfMax = dfFlow.resample('W-SUN',kind='period').max()
dfMax = dfMax.replace('A','') 
droplist = list(dfMax.columns)
dfMax['Max'] = dfMax['USGS:04133501:00060:00003'].astype(int).astype(str) + ' ' +  dfMax['USGS:04133501:00060:00003_qualifiers']
dfMax = dfMax.drop(droplist,axis=1)

dfMin = dfFlow.resample('W-SUN',kind='period').min()
dfMin = dfMin.replace('A','') 
dfMin['Min'] = dfMin['USGS:04133501:00060:00003'].astype(int).astype(str) + ' ' + dfMin['USGS:04133501:00060:00003_qualifiers']
dfMin = dfMin.drop(droplist,axis=1)

dfDischarge = dfMax.join(dfMin)

dfDischarge.to_csv(r'Save Location.csv'+start+'to'+end+'.csv')
