#%%

import datetime
import json
import pandas as pd
import sys
from time import sleep, time
from concurrent.futures import ThreadPoolExecutor, wait
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from scraper_amazon import get_driver_headless, get_driver, write_to_file_Link ,write_to_csv_mat, write_to_json_mat, connect_to_base_mat# put_all_features_together_in_list
from scraper_amazon import Mat_Yoga , upload_file  , upload_images
#get all links for mats in one page
def get_all_links_to_each_mat_in_each_page(current_page): 
    '''
    we are in the page where all products are listed and this function get all urls to each
    one or those products and appends into the list all_links
    '''
   
    all_links = []    
    try:
        print('sleeping 5 sec, page',current_page)
        links = driver.find_elements_by_xpath('//*[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a')
        sleep(5)
        for i in links:
            all_links.append(i.get_attribute("href"))
    except Exception as e:
        print('Error getting URLs for each mat', e)
    print(f'{len(all_links)} urls obtained')
    return(all_links)

# Link to all pages with scraping using click scraping. #in range  400 or while more,
# it only takes 7 pages when I access by find_element_by_id('twotabsearchtextbox'),
# I have to select department and then yoga mats to load more pages

driver = webdriver.Chrome()
driver.get('https://www.amazon.com')
driver.implicitly_wait(5) #time.sleep(5)

page_url_list = []
product_url_list = []

#Find search box and send keys
search_box = driver.find_element_by_id('twotabsearchtextbox').send_keys('yoga mats')

#insert text to search box and click and wait 5 seconds
search_button = driver.find_element_by_id("nav-search-submit-text").click()

# sleeping 5 until the page is uploaded
driver.implicitly_wait(5) #time.sleep(5)

#appending page 0
page_url_list.append(driver.current_url)  
product_url_list.extend(get_all_links_to_each_mat_in_each_page ('0'))
page_ = 0
for i in range(3):
        page_ = i + 1
        #find and click on next page 
        class_pagination = driver.find_element_by_class_name('a-pagination')
        click_next = class_pagination.find_element_by_xpath('//*[@class="a-last"]/a').click()  
        driver.implicitly_wait(20)  
        #append all urls for each page   
        page_url_list.append(driver.current_url)
        print("Page " + str(page_) + " grabbed")
        #find all urls per each product
        product_url_list.extend(get_all_links_to_each_mat_in_each_page (page_))
        print(f'all urls in page {page_} have been appended')


driver.quit()

# it does't collect all urls


# %%
