#%%
import pandas as pd
import numpy as np
from pandas.core.indexes.base import Index
# %%
columns = ['mat_url','name','saleprice', 'ourprice', 'price_buybox','number_reviews','rating',
'reviews_text', 'table_features_color_care_material', 'other_colors_and_prices','other_prices']
#reading data from the 26/06/2021
df1 = pd.read_csv('..\data_amazon\Amazon_webscraped_data_not_clean\Amazon_output_features_20210626_1.csv',header=None)
df2 = pd.read_csv('..\data_amazon\Amazon_webscraped_data_not_clean\Amazon_output_features_20210626_2.csv',header=None)

#concatenate  the two dataframes
df = pd.concat([df1,df2])
df.columns = columns
df.head(100)
# %%
df[['mat_url']]
df.columns
df.shape

# %%
#nulls not because an error 
df.isnull().sum()
#%%
df.info()
# %%
df.head()
# %%
#%%
import re
regex = re.compile(r'alt=(.*?)style')
df['other_colors'] = df['other_colors_and_prices'].str.findall(regex).apply('-'.join)

# %%
for i in columns:
   df[i] = df[i].apply(lambda y:np.nan  if y=='[]' else y)
   df[i] = df[i].apply(lambda y:np.nan  if y=="['error']" else y)
df = df.replace(r'', np.NaN)
#%%
df.isnull().sum()
#%%
#price
def replace_1(x):
    if x:
        for k,v in [('$',""),("-"," ")]:
           x = x.replace(k,v)
        try:
            return x.split()[1]
        except:
            return np.nan

def replace_2(x):
    if x:
        for k,v in [('$',""),("-"," ")]:
           x = x.replace(k,v)
        return x.split()[0]
    else:
        return np.nan
         

df['saleprice'] = df['saleprice'].str.replace('$',"").astype('float')
df['other_ourprice'] =df['ourprice'].apply(lambda x: replace_1(x)).astype('float')
df['ourprice'] = df['ourprice'].apply(lambda x: replace_2(x)).astype('float')
df['price_buybox'] = df['price_buybox'].str.replace('$',"").astype('float')
df['other_ourprice'].unique()



 # %%
df.isna().sum()
# %%
df['saleprice'].unique()

# %%
df.head(300)
#other prices and table features

# %%

# %%

# %%

# %%

# %%
