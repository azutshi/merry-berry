import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from numpy import nan

'''
Import all library for numpy and pandas operations

'''   

pd.options.mode.chained_assignment = None 

fname = 'OrderData.csv'
df = pd.read_csv(fname)   

'''
read converted csv to a dataframe
'''

#df.fillna("Missing data",inplace=True)
s1=df["order_id:date"].str.split(":").apply(Series,1)

'''
Split the combined field int app. Order ID and Date Values

'''
s2 =df.user_id

'''
Get User ID

'''

df['Order_id'] = s1[0]
#print order_id

date= s1[1]
'''
remove bad data

'''
date2 = s1[2].replace('replacement','')

#print date2
df['Order_date'] = date.fillna('') + date2.fillna('')
x = df['Order_date'].str
date_final = x[:4]+'-'+x[4:6]+'-'+x[6:8]

df['Order_date'] = date_final.replace('--','Missing input data')

'''
Format data as per reqd. output

'''

df1 = df[['item_price_1','item_price_2','item_price_3','item_price_4']]

df1.replace(0.00,np.nan,inplace=True)

'''
Treat 0 values as Na and don't count them for avg (as per sample data provided)
'''

df['Avg_item_price'] = df1.sum(axis=1)/df1.count(axis=1)

'''
Calculate average price for items

'''

u = df.start_page_url.str
y = df.start_page_url.to_dict()

'''
Converted to dicitonary and used string variable for easy manipulations

'''

#print y
#df['Start_page_url']= df['start_page_url'].str.contains("http://www.insacart.com", na=False)

for (k,v) in y.iteritems():
    url = u[:23]
#   print y[k]
    if url[k] != "http://www.insacart.com": 
        y[k] =''
    df2 = pd.DataFrame.from_dict([y])
df['Start_page_url'] = df2.transpose() 

'''
Transpose to get final output as requested(not showing invalid urls)

'''
t = df['Start_page_url'].to_dict()
for (k,v) in t.iteritems():
    #print t[k]
    if t[k]!= '':
        t[k] =''
    else:                
        t[k] ='Invalid URL'
    df3 = pd.DataFrame.from_dict([t])
df['Error_msg'] = df3.transpose()

'''
Same procedure followed to show bad url message for non-instacart pages

'''

df.fillna('Missing input data',inplace=True)   

'''
Show error for any remaining unparsed data

'''

df.drop(df.columns[[0, 2, 3, 4, 5, 6]], axis=1,inplace=True)

'''
Rearrange columns to prettify the output file

'''

cols=list(df.columns.values)
#print cols
cols =cols[1:3]+cols[:1]+cols[3:]
df=df.ix[:,cols]

'''
Export our fully cooked output dataset to csv file (without indexes)

'''

df.to_csv('Order_Output.csv',index=False)
