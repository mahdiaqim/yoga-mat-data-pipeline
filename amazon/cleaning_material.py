#%%
import pandas as pd
import numpy as np
from pandas.core.indexes.base import Index
import matplotlib.pyplot as plt
pd.options.display.max_colwidth
# %%
columns = ['mat_url','name','saleprice', 'ourprice', 'price_buybox','number_reviews','rating',
'reviews_text', 'table_features_color_care_material', 'other_colors_and_prices','other_prices']
#reading data from the 26/06/2021
#df1 = pd.read_csv('..\data_amazon\Amazon_webscraped_data_not_clean\Amazon_output_features_20210626_1.csv',header=None)
#df2 = pd.read_csv('..\data_amazon\Amazon_webscraped_data_not_clean\Amazon_output_features_20210626_2.csv',header=None)
df1 = pd.read_csv('C:\\Users\\kautar\\Documents\\Aicore\\Projects\\Webscraping\\data_amazon\\Amazon_webscraped_data_not_clean\\Amazon_output_features_20210626_1.csv',header=None)
df2 = pd.read_csv('C:\\Users\\kautar\\Documents\\Aicore\\Projects\\Webscraping\\data_amazon\\Amazon_webscraped_data_not_clean\\Amazon_output_features_20210626_2.csv',header=None)


#concatenate  the two dataframes
df = pd.concat([df1,df2])
df.columns = columns
df.head(1)
# %%
df[['mat_url']]
df.columns
df.shape

# %%
#nulls not because an error 
df.isnull().sum()
#%%
df.isna().sum()
#%%
df.info()
# %%
df.head()
# %%
import re
regex_color = re.compile(r'alt=(.*?)style')
df['other_colors'] = df['other_colors_and_prices'].str.findall(regex_color).apply('-'.join)
#%%
regex_price = re.compile(r'Price(.*?)<')
df['other_prices']=df['other_colors_and_prices'].str.findall(regex_price).apply('-'.join)
df.drop(['other_colors_and_prices'],axis=1, inplace=True)


# %%
for i in columns:
    try:
        df[i] = df[i].apply(lambda y:np.nan  if len(y)==0 else y)
        df[i] = df[i].apply(lambda y:np.nan  if y=="['error']" else y)
    except Exception as e:
        print(e)
df = df.replace(r'', np.NaN)

#%%
df['other_prices']
#%%
df.isnull().sum()#%%
df.isna().sum()
df.info()

#%%
#cleaning all prices and putting all in one single column, converting to float
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

def replace_3(x):
   
    if x:
        x = str(x)
        x = x.split('-')[0] 
        x = x.replace('$',"").replace(">","").replace('"', "")
        return x

    else:
        return np.nan

#%%        
#cleaning saleprice
df['saleprice'] = df['saleprice'].str.replace('$',"").astype('float')
#dividing our price in two cclumns ourprice_1 and ourprice_2
df['ourprice_2'] =df['ourprice'].apply(lambda x: replace_1(x)).astype('float')
df['ourprice_1'] = df['ourprice'].apply(lambda x: replace_2(x)).astype('float')
df.drop(['ourprice'],axis=1, inplace=True)
#cleaning buybox
df['price_buybox'] = df['price_buybox'].str.replace('$',"").astype('float')
#Cleaning prices from other colors
df['other_prices_to fill_ourprice'] = df['other_prices'].apply(lambda x: replace_3(x)).astype('float') 
#%%
plt.plot(df['saleprice'], label='saleprice')
plt.plot(df['ourprice_2'], label='ourprice_2')
plt.plot(df['ourprice_1'], label='ourprice_1')
plt.plot(df['price_buybox'], label='price_buybox')
#%%
#find outliers 
df[df['ourprice_1']>200]
 # %%
#pd.options.display.max_colwidth
#Droping outlier: price over 700
df.loc[525, 'mat_url']
df.drop(525,axis=0, inplace=True)
#%%
#only mat costing more than 200, 
df.loc[951, 'mat_url']

# %%
plt.plot(df['saleprice'], label=f"saleprice-nulls={df['saleprice'].isna().sum()}")
plt.plot(df['ourprice_2'], label=f"ourprice_2-nulls={df['ourprice_2'].isna().sum()}")
plt.plot(df['ourprice_1'], label=f"ourprice_1-nulls={df['ourprice_1'].isna().sum()}")
plt.plot(df['price_buybox'], label=f"price_buybox-nulls={df['price_buybox'].isna().sum()}")
plt.plot(df['other_prices_to fill_ourprice'], label=f"other_prices_to fill_ourprice-nulls={df['other_prices_to fill_ourprice'].isna().sum()}")
plt.legend()

# %%
prices =df.fillna(0)['other_prices_to fill_ourprice'] + df.fillna(0)['saleprice'] + df.fillna(0)['ourprice_2'] + df.fillna(0)['ourprice_1'] + df.fillna(0)['price_buybox']
bool= prices==0
bool.sum()
#184 missing values for the price, 161 missing if I use the price from other colors
#%%
#Combined price is completed with the ones with less missing values

df['combined_price'] =df['price_buybox'].fillna(0)
print((df['combined_price']==0).sum())
df['combined_price']=np.where(df['combined_price']==0 ,df['other_prices_to fill_ourprice'],df['combined_price'])
print((df['combined_price']==0).sum())
df['combined_price']=np.where(df['combined_price']==0 ,df['saleprice'],df['combined_price'])
print((df['combined_price']==0).sum())
#%%
#drop where price is 0
df = df.drop(df[df.combined_price.isnull()].index)
df.shape
#%%
#drop columns with other prices
columns_to_drop = ['saleprice','ourprice_2','ourprice_1','price_buybox','other_prices_to fill_ourprice']
df.drop(columns_to_drop,axis=1, inplace=True)
df.shape
#%%
#other prices and table features
df['table_features_color_care_material'].isna().sum()
df['table_features_color_care_material'] = df['table_features_color_care_material'].apply(lambda y:np.nan  if type(y)==list and len(y)==0 else y)
# %%
def split_feature(x, feature):
    if type(x)==float:
        return np.nan
    elif feature in x :
        return x.split(feature)[-1]
    else:
        return np.nan
def after_split(x, feature):
    if type(x)==float:
        return np.nan
    elif feature in x :
        return x.split(feature)[0]
    else:
        return x
#Color Cherry Pink & Navy BlueBrand BEAUTYOVOMaterial Thermoplastic ElastomersProduct Care Instructions 
#Hand Wash OnlyItem Dimensions LxWxH 72 x 24 x 0.31 inchesItem Weight 2 Pounds
df['weight']=df['table_features_color_care_material'].apply(lambda x: split_feature(x, 'Weight'))
df['table_features_color_care_material']=df['table_features_color_care_material'].apply(lambda x: after_split(x, 'Weight'))

df['dimentions']=df['table_features_color_care_material'].apply(lambda x: split_feature(x, 'Item Dimensions LxWxH'))
df['table_features_color_care_material']=df['table_features_color_care_material'].apply(lambda x: after_split(x, 'Item Dimensions LxWxH'))

df['care']=df['table_features_color_care_material'].apply(lambda x: split_feature(x, 'Product Care Instructions'))
df['table_features_color_care_material']=df['table_features_color_care_material'].apply(lambda x: after_split(x, 'Product Care Instructions'))

df['thickness']=df['table_features_color_care_material'].apply(lambda x: split_feature(x, 'Item Thickness'))
df['table_features_color_care_material']=df['table_features_color_care_material'].apply(lambda x: after_split(x, 'Item Thickness'))

df['material']=df['table_features_color_care_material'].apply(lambda x: split_feature(x, 'Material'))
df['table_features_color_care_material']=df['table_features_color_care_material'].apply(lambda x: after_split(x, 'Material'))

df['brand']=df['table_features_color_care_material'].apply(lambda x: split_feature(x, 'Brand'))
df['color']=df['table_features_color_care_material'].apply(lambda x: after_split(x, 'Brand'))



#%%

# %%
#color: Fabric Type 90% Polyester/10% NylonCare Instructions Machine WashOrigin ImportedSize 24.5" x 69"Color Blue Curacao'
#material: PU, EVAItem 
#care : Machine WashItem Thickness 6 Millimeters // BPA free: our products are free of Phthalate
#rinted yoga mats release a very strong but harmless odor when fir… See more'
#只能手洗',//⭐Get a free carry strap by claiming the promotion code., ⭐Th… See more',
#dimentions: 23.62 x 9.84 x 0.59 inchesItem Thickness 1.5 Centimeters
df['weight'].unique()
# %%
df.isna().sum()
# %%
pd.set_option('display.max_colwidth', None)
<<<<<<< HEAD
df['material']
df.loc[501, 'material']
=======

>>>>>>> ec56a2b15fc290bdb99a4d43aa016b34ac97179b

# %%
st = 'as c a m'
st.split('c')
# %%
