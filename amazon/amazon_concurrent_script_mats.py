#%%
import datetime
import json
import pandas as pd
import sys
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path

from urllib3.packages.six import u

from scraper_amazon import get_driver_headless, write_to_file_Link ,write_to_csv_mat, write_to_json_mat, connect_to_base_mat
from scraper_amazon import Mat_Yoga , upload_file  , upload_images

#%%
# main block
# set variables


def run_process_features_each_mat(mat_url, filename_csv, filename_json):
   # mat_yoga = Mat_Yoga()
    browser = get_driver_headless()
    if connect_to_base_mat(browser, mat_url):
        sleep(5) 
        ## : Provider
        # 0: name
        #1,2,3 price
        # Table Features contains: color, brand, Material,Product care, Dimentions


        #table
        table_features = {}
        for i in range(1,7):
            try:
                    feature_name = browser.find_element_by_xpath('//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i)+']/td[1]')
                    feature_value = browser.find_element_by_xpath('//*[@id="productOverview_feature_div"]/div/table/tbody/tr['+str(i)+']/td[2]')
                    feature_name= feature_name.text.replace('\n', '')
                    feature_value= feature_value.text.replace('\n', '')
                    table_features[feature_name] = feature_value
                    #print(feature_name, feature_value)
            except Exception as e:
                    feature_name = f'xpath_table{i}'
                    feature_value = 'Nan'
                    #print('Error P1', e)
                    table_features[feature_name] = feature_value
            
        
            print('table_feature', table_features)
     
            #prie, name, reviews
            all_xpath = ['//*[@id="title"]',
            '//*[@id="priceblock_saleprice"]','//*[@id="priceblock_ourprice"]','//*[@id="price_inside_buybox"]','//*[@id="acrCustomerReviewText"]','//*[@id="acrPopover"]/span[1]/a/i[1]/span']
            all_features_one_mat = []
            for i in all_xpath:
                try:
                    feature = browser.find_element_by_xpath(i)
                    feature_text= feature.text.replace('\n', '')
                    all_features_one_mat.append(feature_text)
                    #print(feature)
                except Exception as e:
                    feature_text = 'Nan'
                    #print('Error P1', e)
                    all_features_one_mat.append(feature_text)
        
            # other colors
            other_colors ={}
            try:
                price_s = browser.find_elements_by_xpath('//*[contains(@id,"_price")]/p')
                colors= browser.find_elements_by_xpath('//*[contains(@id,"color_name_")]') 
                #price_2 = price_1.get_attribute("innerHTML")
                #print (len(price_1))
            except Exception as e:
                    price = 'Nan'
                    #print('Error P1', e)

            for i, j in zip(colors, price_s):
                k = i.get_attribute('title').replace('\n', '')
                v = j.get_attribute('innerHTML').replace('\n', '')
                other_colors[k] =v
                    
        
                
            

            # Clean price from \n
            #all_features_one_mat= [i.replace('\n', '') for i in all_features_one_mat]
            print('all_features_one_mat')
            #print(all_features_one_mat)
            write_to_csv_mat(all_features_one_mat, filename_csv, table_features, mat_url,other_colors)
            #print('Number mat', mat_url)
            write_to_json_mat(all_features_one_mat, filename_json,table_features, mat_url,other_colors)
            print('writing to json mat instance')      
            browser.quit()
    else:
        print("Error connecting to hacker news")
        browser.quit()

#%%

# #%%
# price_xpath = ["priceblock_saleprice","priceblock_ourprice","price_inside_buybox" ]
# for i in price_xpath:
# #     print(i)

# browser = get_driver_headless()
# mat_url = 'https://www.amazon.com/Unbeatable-Thickness-Alignment-Carrying-Exercise/dp/B08FZNTJSZ/ref=sr_1_5113_sspa?dchild=1&keywords=yoga+mats&qid=1624456322&s=sports-and-fitness&sr=1-5113-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFGSU8wUUxaWEdCUEgmZW5jcnlwdGVkSWQ9QTA1NjY5NjUyR1RZNUdGU0FFQktMJmVuY3J5cHRlZEFkSWQ9QTAxNjY4OTMxR0tSVlhRTEFYTzZLJndpZGdldE5hbWU9c3BfYXRmX25leHQmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl'
# if connect_to_base_mat(browser, mat_url):
#         sleep(10) 
   
#         try:
#             price_s = browser.find_elements_by_xpath('//*[contains(@id,"_price")]/p')
#             colors= browser.find_elements_by_xpath('//*[contains(@id,"color_name_")]') 
#             #price_2 = price_1.get_attribute("innerHTML")
#             #print (len(price_1))
#         except Exception as e:
#             price = 'Nan'
#             print('Error P1', e)

#         for i, j in zip(colors, price_s):
#             k = i.get_attribute('title').replace('\n', '')
            # v = j.get_attribute('innerHTML').replace('\n', '')
                    
#%%
#%%
#s= price_1.find_elements_by_xpath('//*[contains(@id,"color_name_")]') 
#//div[contains(@id,'test')]
#//*[@id="color_name_1_price"]/p
#//*[@id="color_name_0"]
#//*[@id="color_name_0"]
# //*[@id="color_name_0"]
# //*[@id="a-autoid-11-announce"]/div/div[1]/img




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
        for number in (0,2):
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
# %%
