

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
# Link to all pages with scraping using click scraping. #in range  400 or while more,
# it only takes 7 pages when I access by find_element_by_id('twotabsearchtextbox'),
# I have to select department and then yoga mats to load more pages
driver = webdriver.Chrome()
driver.get('https://www.amazon.com')

driver.implicitly_wait(5) #time.sleep(5)
try:
    num_page = driver.find_element_by_xpath('//*[@class="a-pagination"]/li[6]')
except NoSuchElementException:
    num_page = driver.find_element_by_class_name('a-last').click()
driver.implicitly_wait(3)
url_list = []
print(num_page.text)
for i in range(5):
        page_ = i + 1
        url_list.append(driver.current_url)
        driver.implicitly_wait(4)
        click_next = driver.find_element_by_xpath('//*[@class="a-last"]/a').click()                        
        print("Page " + str(page_) + " grabbed")
driver.quit()

def get_all_links_to_each_mat_in_each_page(driver, current_page):   
    all_links = []    
    try:
        print('sleeping 5 sec, page',current_page)
        links = driver.find_elements_by_xpath('//*[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a')
        sleep(5)
        for i in links:
            all_links.append(i.get_attribute("href"))
    except Exception as e:
        print('Error getting URLs for each mat', e)
    return(all_links)