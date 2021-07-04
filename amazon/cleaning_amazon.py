#%%
import pandas as pd
# %%
columns = ['mat_url','name','saleprice', 'ourprice', 'price_buybox','number_reviews','rating',
'reviews_text', 'table_features_color_care_material', 'other_colors_and_prices','other_prices']
#reading data from the 26/06/2021
df1 = pd.read_csv('..\data_amazon\Amazon_webscraped_data_not_clean\Amazon_output_features_20210626_1.csv',header=None)
df2 = pd.read_csv('..\data_amazon\Amazon_webscraped_data_not_clean\Amazon_output_features_20210626_2.csv',header=None)
df2.shape
df = pd.concat([df1,df2])
df.columns = columns
df.head(100)
# %%
df[['mat_url']]
#%%
df.columns
#%%
import re
regex = re.compile(r'\b(alt="\w+)\b')
#df['other_colors_and_prices_cleaned'] = df['other_colors_and_prices'].str.extract(regex)

# %%
df['other_colors_and_prices'].str.extract(regex)
# %%
#nulls not because an error 
df2.isnull().sum()
# %%
df2.isnull().sum()
#%%
df.info()

# %%
df.head()
# %%
