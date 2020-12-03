#The purpose of this program is to import data from the MLS to find the highest
#return on investment (ROI) in an assigned location.
#
#For this to be accomplished the property value (PV), Tax, and any HOA fees will
#need to be imported from the MLS.
#
#Then the average rent price per zip code must be found in order to assigned a
#base value for rent rate.
#
#Put together this should be able to calculate the ROI of properties in any area.
#
#ROI = (Rent - (Tax + Hoa + Ins)) // PV
#
#Pandas packet: https://www.anaconda.com/products/individual/download-success

import pandas as pd
import numpy as np
total = 0


df = pd.read_excel(r'C:\Users\Matt\Documents\Splitt\MLS ROI Calc.xlsx', sheet_name='MLS ROI Calc')
#Fill all blank spaces with 0s so that code may function correctly:
df.fillna(0, inplace=True)

#Calculate insurance premiums @ a 1% of asking price $100,000 = $1,000
#Actual numbers vary but this establishes a baseline
df['Annual Insurance'] = (df['CurrentPrice'] * .01)


#Calculate annual maintenance costs @ a .5% of asking price $100,000 = $500
#Actual numbers vary but this establishes a baseline
df['Maintenance'] = (df['CurrentPrice'] * .005)

#Calculate tax rate based off of property value and mileage rate

mults = pd.DataFrame([
    ['BELLEAIR BEACH', 15.9212],
    ['BELLEAIR BLUFFS', 19.9818],
    ['BELLEAIR', 21.1318],
    ['BELLEAIR SHORE', 14.4641],
    ['CLEARWATER', 20.5868],
    #Clearwater beach is entered as the same as clearwater 
    ['CLEARWATER BEACH', 20.5868],
    ['DUNEDIN', 18.7663],  
    ['EAST LAKE', 19.1825],
    ['FEATHER SOUND', 20.5875],
    ['GANDY', 18.3687],
    ['GULFPORT', 18.6708],
    ['HIGH POINT', 19.8875],
    ['SAFETY HARBOR', 18.5818],
    
    ['INDIAN ROCKS BEACH', 16.4644],
    ['INDIAN SHORES', 16.5018],
    ['KENNETH CITY', 19.3192],
    ['LARGO', 20.2518],
    ['LEALMAN', 22.9675],
    ['MADEIRA BEACH', 17.3818],
    ['NORTH REDINGTON BEACH', 15.6318],
    ['OLDSMAR', 18.6818],
    ['PINELLAS PARK', 20.1218],
    ['REDINGTON BEACH', 16.4467],
    ['REDINGTON SHORES', 16.3214],
    ['SEMINOLE', 17.1111],
    ['ST PETERSBURG', 23.2538],
    ['ST PETE BEACH', 17.0318],
    ['TREASURE ISLAND', 17.4947],
    ['TARPON SPRINGS', 20.0018],
    ['TIERRA VERDE', 18.3793],
    ['SOUTH PASADENA', 18.4124],

        ], columns=['City', 'Mil Rate'])
mults.fillna(0, inplace=True)

df = df.merge(mults, on='City', how='outer')
df['NewTaxAmount'] = df['CurrentPrice'].div(1000).mul(df['Mil Rate'])


    
#Calculate the sum of all expenses
df['Total'] = df['Annual Insurance'] + df['NewTaxAmount'] + df['Maintenance'] + (df['AssociationFee'] * 12) + (df['CondoFees'] * 12)

#Rental data feed by zip code
df['Multiplier'] = 1.69
df['Rent'] = df['LivingArea'] * df['Multiplier']
df['Monthly Rent'] = df['Rent'] 

print(df['Rent'])

#Set annual rent
df['Rent'] = df['Rent'] * 12
    
print(df[['UnparsedAddress', 'Total', 'Rent']])

#Find return on investment (ROI)
df['ROI'] = (df['Rent']) - df['Total']

df['ROI Percentage'] = df['ROI'] / df['CurrentPrice']
print(df[['ROI Percentage','ROI', 'UnparsedAddress', 'Total', 'NewTaxAmount', 'Annual Insurance', 'Maintenance']])

print("...")

df['Rent'] = round(df['Rent'],2)
df['Total'] = round(df['Total'],2)
df['Monthly Rent']= round(df['Monthly Rent'],2)
df['TaxAnnualAmount'] = round(df['TaxAnnualAmount'],2)
df['NewTaxAmount'] = round(df['NewTaxAmount'],2)
df['ROI'] = round(df['ROI'],2)


df = df.sort_values('ROI Percentage', ascending = False)
df = df[['ROI Percentage', 'ROI', 'CurrentPrice', 'UnparsedAddress', 'City', 'PostalCode','BedroomsTotal','Monthly Rent', 'Rent', 'Maintenance', 'Annual Insurance', 'NewTaxAmount', 'Mil Rate', 'TaxAnnualAmount', 'AssociationFee', 'CondoFees']]
df.to_excel(r'C:\Users\Matt\Documents\Splitt\MLS ROI Calc_complete.xlsx', index = False, header = True)
print("File successfully transferred")



##flag = True
##flag = (df['City'] == 'BELLEAIR BEACH') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 15.9212)
##    print('test')
##    print(df['TaxAnnualAmount'])
##else:
##    print('LOL!')
##flag = True
##flag = (df['City'] == 'Belleair Bluffs') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 19.9818)
##
##flag = True
##flag = (df['City'] == 'Belleair') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 21.1318)
##
##flag = True
##flag = (df['City'] == 'Belleair Shore') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 14.4641)
##
##flag = True
##flag = (df['City'] == 'Clearwater') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 20.5868)
##
##flag = True
##flag = (df['City'] == 'Dunedin') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 18.7663)
##
##flag = True
##flag = (df['City'] == 'East Lake') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 19.1825)
##
##flag = True
##flag = (df['City'] == 'Feather Sound') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 20.5875)
##
##
##flag = True
##flag = (df['City'] == 'Gandy') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 18.3687)
##
##flag = True
##flag = (df['City'] == 'Gulfport') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 18.6708)
##
##flag = True
##flag = (df['City'] == 'High Point') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 19.8875)
##
##flag = True
##flag = (df['City'] == 'Safety Harbor') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 18.5818)
##    
##flag = True
##flag = (df['City'] == 'Indian Rocks Beach') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 16.4644)
##
##flag = True
##flag = (df['City'] == 'Indian Shores') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 16.5018)
##
##flag = True
##flag = (df['City'] == 'Kenneth City') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 19.3192)
##
##flag = True
##flag = (df['City'] == 'Largo') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 20.2518)
##
##
##flag = True
##flag = (df['City'] == 'Lealman') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 22.9675)
##
##
##flag = True
##flag = (df['City'] == 'Madeira Beach') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 17.3818)
##
##
##flag = True
##flag = (df['City'] == 'North Reddington Beach') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 15.6318)
##
##
##flag = True
##flag = (df['City'] == 'Olsmar') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 18.6818)
##
##
##flag = True
##flag = (df['City'] == 'Pinellas Park') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 20.1218)
##
##
##flag = True
##flag = (df['City'] == 'Redington Beach') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 16.4467)
##
##flag = True
##flag = (df['City'] == 'NORTH REDINGTON BEACH') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 16.4467)
##
##
##flag = True
##flag = (df['City'] == 'Redington Shores') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 16.3214)
##
##flag = True
##flag = (df['City'] == 'Seminole') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 17.1111)
##
##flag = True
##flag = (df['City'] == 'ST PETERSBURG') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 23.2538)
##
##flag = True
##flag = (df['City'] == 'SEMINOLE') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 17.2175)
##
##flag = True
##flag = (df['City'] == 'ST PETE BEACH') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 17.0318)
##
##flag = True
##flag = (df['City'] == 'TREASURE ISLAND') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 17.4947)
##    
##flag = True
##flag = (df['City'] == 'TARPON SPRINGS') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 20.0018)
##
##flag = True
##flag = (df['City'] == 'TIERRA VERDE') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 18.3793)
##    
##flag = True
##flag = (df['City'] == 'SOUTH PASADENA') 
##print(flag)
##if (flag.any() == True):
##    df.loc['TaxAnnualAmount'] = ((df['CurrentPrice'] / 1000) * 18.4124)


##zip_33701_1 = 2500
##zip_33732_1 = 1000
##zip_33712_1 = 1000
##zip_33705_1 = 2000
##
##
##
##zip_33784_2 = 2200
##zip_33728_2 = 2200
##zip_33702_2 = 2200 
##zip_33747_2 = 2200
##zip_33734_2 = 2200
##zip_33733_2 = 2200
##zip_33714_2 = 1800
##zip_33713_2 = 2500
##zip_33703_2 = 2500
##zip_33701_2 = 3000
##zip_33732_2 = 1450
##zip_33712_2 = 1450
##zip_33705_2 = 3000
##
##
##
##zip_33784_3 = 2500
##zip_33728_3 = 2500
##zip_33702_3 = 2500 
##zip_33747_3 = 2500
##zip_33734_3 = 2500
##zip_33733_3 = 2500
##zip_33784_3 = 2500
##zip_33714_3 = 2000
##zip_33713_3 = 2700
##zip_33703_3 = 2700
##zip_33701_3 = 3800
##zip_33732_3 = 2200
##zip_33712_3 = 2200
##zip_33705_3 = 2500
##
##
##
##
##zip_33784_4 = 3000
##zip_33728_4 = 3000
##zip_33702_4 = 3000 
##zip_33747_4 = 3000
##zip_33734_4 = 3000
##zip_33733_4 = 3000
##zip_33784_4 = 3000
##zip_33714_4 = 2200
##zip_33713_4 = 3500
##zip_33703_4 = 3500
##zip_33701_4 = 4000
##zip_33732_4 = 2500
##zip_33712_4 = 2500
##zip_33705_4 = 3500
