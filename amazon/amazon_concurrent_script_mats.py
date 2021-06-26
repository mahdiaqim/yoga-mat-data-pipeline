#%%
import datetime
import json
import pandas as pd
import sys
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path

from selenium import webdriver

from scraper_amazon import get_driver_headless, get_driver, write_to_file_Link ,write_to_csv_mat, write_to_json_mat, connect_to_base_mat# put_all_features_together_in_list
from scraper_amazon import Mat_Yoga , upload_file  , upload_images

#%%
# main block
# set variables
def put_all_features_together_in_list(mat_url,other_features_one_mat,reviews_text_dict,table_features_dict,other_colors):
    list_of_dict = [other_features_one_mat,reviews_text_dict,table_features_dict,other_colors]
    all_features_keys = []
    all_features_values = []
    all_features_keys.append('url')
    all_features_values.append(mat_url)
    for i in list_of_dict:
        for k, v in i.items():
            all_features_keys.append(k)
            all_features_values.append(v)

    return(all_features_keys, all_features_values)

def run_process_features_each_mat(mat_url, filename_csv, filename_json):
   # mat_yoga = Mat_Yoga()
    browser = get_driver_headless()
    if connect_to_base_mat(browser, mat_url):
        sleep(10) 
        ## : Provider
        # 0: name
        #1,2,3 price
        # table Features contains: color, brand, Material,Product care, Dimentions

        #table
        try:
            table_features = []
            table = browser.find_elements_by_xpath('//*[@id="productOverview_feature_div"]/div/table/tbody')
            for i in table:
                    table_features.append(i.text.replace('\n', ''))
            separator = '_'
            table_features_dict = {'table': separator.join(table_features) }  
        except  Exception as e :
            print('error table features', e)
            table_features_dict = {'table': 'error' } 
        
        print('table_feature', table_features_dict.keys())
     
        #prie, name, reviews
        other_features_one_mat = {} 
        keys_other_paths = ['name', 'saleprice', 'ourprice', 'price_buybox','number_reviews','rating']
        other_xpath = ['//*[@id="title"]',
        '//*[@id="priceblock_saleprice"]','//*[@id="priceblock_ourprice"]','//*[@id="price_inside_buybox"]',
        '//*[@id="acrCustomerReviewText"]','//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span']
        
        for k,v in zip(keys_other_paths,other_xpath):
            try:
                feature= browser.find_element_by_xpath(v)
                feature_text= feature.text.replace('\n', '')
                other_features_one_mat[k] = feature_text
                #print(feature)
            except Exception as e:
                feature_text = 'Nan'
                print('Error other  features', e)
                other_features_one_mat[k] = feature_text
            
            print('other_features', other_features_one_mat.keys())
        

        #Reviews_text
        try:
            reviews_text =[]
            path_reviews = browser.find_elements_by_xpath('//*[@id="reviewsMedley"]/div/div[2]/div/div[2]/span[3]/div/div/div[4]/div[3]')
            for i in path_reviews:
                reviews_text.append(i.text.replace('\n', ('|')))
            reviews_text_dict = {'reviews_text_dict': separator.join(reviews_text)}

        except Exception as e:
            print('error reviews_text_dict',e)
            reviews_text_dict = {'reviews_text_dict': 'error' } 
            
        print('reviews_text_dict', reviews_text_dict.keys())

        # other colors
        other_colors ={}
        text_other_colors = []
        price_colors = []
        try:
            #Getting block for price and color for same mat
            other_colors_block = browser.find_elements_by_xpath('//*[contains(@id,"color_name_")]')
            for i in other_colors_block: 
                text_other_colors.append( i.get_attribute('innerHTML').replace('\n',''))
                
        except Exception as e:
                text_other_colors = ['error']
                print('Error other colors', e)

        try:
            #Getting block for price and color for same mat
            other_colors_block = browser.find_elements_by_xpath('//*[contains(@id,"color_name_")]')
            for i in other_colors_block: 
                price_colors.append(i.find_element_by_xpath('//*[contains(@id,"price")]/p').get_attribute('innerHTML'))
        except Exception as e:
                price_colors = ['error']
                print('Error other price colors', e)

        other_colors['text_other_colors']= text_other_colors
        other_colors['price_colors']= price_colors
            
        print('other colors',other_colors.keys())

        all_keys, all_values= put_all_features_together_in_list(mat_url,other_features_one_mat,
        reviews_text_dict,table_features_dict,other_colors)
        sleep(5)
        print('---------------------------------------------')
        print(all_keys)
       #Writing to csv is not working for now
        write_to_csv_mat(filename_csv,all_keys, all_values)
        print('written to csv')
        write_to_json_mat(filename_json, all_keys, all_values )
        print('written to json mat instance')      
        browser.quit()
    else:
        print("Error connecting to mat url")
        browser.quit()

#%%


# M ='https://www.amazon.com/Friendly-Fitness-Exercise-Carrying-Exercises/dp/B08R55YR6J/ref=sr_1_217_sspa?dchild=1&keywords=yoga+mats&qid=1624447198&s=sports-and-fitness&sr=1-217-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyTE9RNTJUTDlaTERQJmVuY3J5cHRlZElkPUEwMzczODk3Mk8yNFYyT09CQTYyNCZlbmNyeXB0ZWRBZElkPUEwNzA2Njc1RDlZWTNLMzVCQjBJJndpZGdldE5hbWU9c3BfYXRmX25leHQmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl'
# G ='https://www.google.com/'
# C ='https://www.amazon.com/Unbeatable-Thickness-Alignment-Carrying-Exercise/dp/B08FZNTJSZ/ref=sr_1_5113_sspa?dchild=1&keywords=yoga+mats&qid=1624456322&s=sports-and-fitness&sr=1-5113-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFGSU8wUUxaWEdCUEgmZW5jcnlwdGVkSWQ9QTA1NjY5NjUyR1RZNUdGU0FFQktMJmVuY3J5cHRlZEFkSWQ9QTAxNjY4OTMxR0tSVlhRTEFYTzZLJndpZGdldE5hbWU9c3BfYXRmX25leHQmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl'
# A ='https://www.amazon.com/Yoga-Direct-Deluxe-Sticky-4-Inch/dp/B007MTZFUW/ref=sr_1_222?dchild=1&keywords=yoga+mats&qid=1624447198&s=sports-and-fitness&sr=1-222'
# B ='https://www.amazon.com/YuniMuse-Anti-Tear-Cushioning-Extra-Thick-Pink-purple/dp/B08GG7WRX9/ref=sr_1_221?dchild=1&keywords=yoga+mats&qid=1624447198&s=sports-and-fitness&sr=1-221'
# testo =[A,B]
# browser = get_driver_headless()
# browser.get(A)
































#%%
if __name__ == "__main__":

#     # headless mode?
#     headless = False
#     if len(sys.argv) > 1:
#         if sys.argv[1] == "headless":
#             print("Running in headless mode")
#             headless = True

    # set variables
    #n=0
    start_time =  time()
    output_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename_csv = f"Amazon_output_features_{output_timestamp}.csv"
    output_filename_json = f"Amazon_output_features_{output_timestamp}.json"
    futures = []

    A ='https://www.amazon.com/Yoga-Direct-Deluxe-Sticky-4-Inch/dp/B007MTZFUW/ref=sr_1_222?dchild=1&keywords=yoga+mats&qid=1624447198&s=sports-and-fitness&sr=1-222'
    B ='https://www.amazon.com/YuniMuse-Anti-Tear-Cushioning-Extra-Thick-Pink-purple/dp/B08GG7WRX9/ref=sr_1_221?dchild=1&keywords=yoga+mats&qid=1624447198&s=sports-and-fitness&sr=1-221'
    testo =[A,B]
        #read urls for each mat form csv file
    header_urls = ['index', 'url']
    BASE_DIR = Path(__file__).resolve(strict=True).parent
    urls = pd.read_csv(Path(BASE_DIR).joinpath('Amazon_output_Urls20210623121907.csv'), names=header_urls)


    # crawl
    with ThreadPoolExecutor() as executor:
        for number in range (0,2):
            futures.append(
                #executor.submit(run_process_features_each_mat, urls['url'][number], output_filename_csv, output_filename_json)
                executor.submit(run_process_features_each_mat, testo[number], output_filename_csv, output_filename_json)
            )

    wait(futures)
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Elapsed run time: {elapsed_time} seconds")
 

# %%
# browser = get_driver_headless()
# browser.get('https://www.amazon.co.uk/Exercise-Non-Slip-gymnastics-stretching-Turquoise/dp/B082L1YS9F/ref=asc_df_B082L1YS9F/?tag=googshopuk-21&linkCode=df0&hvadid=399635169056&hvpos=&hvnetw=g&hvrand=3049200703902801442&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9045928&hvtargid=pla-849766291679&psc=1&tag=&ref=&adgrpid=88836927767&hvpone=&hvptwo=&hvadid=399635169056&hvpos=&hvnetw=g&hvrand=3049200703902801442&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9045928&hvtargid=pla-849766291679')
# ## : Provider
# # 0: name
# #1,2,3 price
# # Table Features contains: color, brand, Material,Product care, Dimentions


#table
# table_features = {}
# for i in range(1,7):
#     try:
#             feature_name = browser.find_element_by_xpath('//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i)+']/td[1]')
#             feature_value = browser.find_element_by_xpath('//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i)+']/td[2]')
#             feature_name= feature_name.text
#             feature_value= feature_value.text
#             table_features[feature_name] = feature_value
#             print(feature_name, feature_value)
#     except Exception as e:
#             feature_name = i
#             feature_value = 'Nan'
#             print('Error P1', e)
#             table_features[feature_name] = feature_value

# all_xpath = ['//*[@id="title"]',
# '//*[@id="priceblock_saleprice"]','//*[@id="priceblock_ourprice"]','//*[@id="price_inside_buybox"]',

# ]


# all_features_one_mat = []
# for i in all_xpath:
#     try:
#         feature = browser.find_element_by_xpath(i)
#         feature= feature.text
#         all_features_one_mat.append(feature)
#         print(feature)
#     except Exception as e:
#         feature = 'Nan'
#         print('Error P1', e)
#         all_features_one_mat.append(feature)

# separator='-'
# print('price', separator.join(all_features_one_mat[1:4]))
# print (table_features)           

# # %%
# dict_ = {
#     'Provider' : ['$37.99''-' 'Nan''-' '$37.99'] ,
#     'name' : ['$37.99', 'Nan', '\n$37.99\n'] ,
#     'price' : ['$37.99', 'Nan', '\n$37.99\n'], 
#     'material' : ['$37.99', 'Nan', '\n$37.99\n'],
#     'rating' : ['$37.99', 'Nan', '\n$37.99\n'] ,
#     'number_reviews' :['$37.99', 'Nan', '\n$37.99\n'] ,
#     'colours' : ['$37.99', 'Nan', '\n$37.99\n']

#     }
# dict_1 = {
#     'osama' : ['$37.99', 'Nan', '$37.99'] ,
#     'rida' : ['$37.99', 'Nan', '$37.99'] 

#     }
# dict_.update(dict_1)
# #%%
# df = pd.DataFrame.from_dict(dict_,orient='index').T
# df.to_csv('name.csv', mode='a',columns=dict_.keys())
# # %%
# df = pd.DataFrame.from_dict(dict_1,orient='index' ).T
# df.to_csv('name.csv',mode='a')
# #%%

# nme = ["aparna", "pankaj", "sudhir", "Geeku"]
# deg = ["MBA", "BCA", "M.Tech", "MBA"]
# scr = [90, 40, 80, 98]
# dict = {'name': nme, 'degree': deg, 'score': scr} 
    
# df = pd.DataFrame(dict)
    
# df 
# # %%
# header_urls = ['index', 'url']
# urls = pd.read_csv('Amazon_output_Urls20210623153408.csv', names=header_urls)
# print (urls['url'][5])

# # %%
# def write_to_json_mat(output_list, filename):
#     separator = '-'
#     a = {
#     'Provider' :separator.join(output_list) ,
#     'name' :separator.join(output_list)  ,
#     'price' : separator.join(output_list), 
#     'material' : separator.join(output_list),
#     'rating' : separator.join(output_list) ,
#     'number_reviews' : separator.join(output_list) ,
#     'colours' : separator.join(output_list)

#     }
#     print('in function write_to_json_mat')
#     with open(filename, 'w') as file:
#         # First we load existing data into a dict.
#         file_data = a
#         # Join new_dat3a with file_data
#         #file_data.append(a)
#         # Sets file's current position at offset.
#         #file.seek(0)
#         # convert back to json.
#         json.dump(file_data, file, indent = 4)

# l= ['1','1','1','1','1']
# l2=['2','2','2','2','2']

# write_to_json_mat(l, 'test.json')
# write_to_json_mat(l2, 'test.json')
# 
# #%%
# dict_1 = {
#      'osama' : ['$37.99', 'Nan', '$37.99'] ,
#      'rida' : ['$37.99', 'Nan', '$37.99'] 

#     }
# def put_all_features_together_in_list(mat_url,other_features_one_mat,reviews_text_dict,table_features_dict,other_colors):
#     list_of_dict = [other_features_one_mat,reviews_text_dict,table_features_dict,other_colors]
#     all_features_keys = []
#     all_features_values = []
#     all_features_keys.append('url')
#     all_features_values.append(mat_url)
#     for i in list_of_dict:
#         for k, v in i.items():
#             all_features_keys.append(k)
#             all_features_values.append(v)

#     return(all_features_keys, all_features_values)

# a , b = put_all_features_together_in_list('a', dict_1,dict_1,dict_1,dict_1)

# # %%
# a
# # %%
# b
# # %%
