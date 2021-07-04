#%%
import pandas as pd

# %%
columns = ['mat_url','name','saleprice', 'ourprice', 'price_buybox','number_reviews','rating',
'reviews_text', 'table_features_color_care_material', 'other_colors_and_prices','other_prices']
df = pd.read_csv('data_amazon\Amazon_webscraped_data_not_clean\Amazon_output_features_20210626014219.csv')
df.columns=columns
df.head()
# %%
import re
regex = re.compile(r'\b(alt="\w+)\b')
df['other_colors_and_prices_cleaned'] = df['other_colors_and_prices'].str.extract(regex)

# %%
