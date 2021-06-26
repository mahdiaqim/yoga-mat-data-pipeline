
import sys
import csv
import json
from datetime import date
from time import sleep, time
from pathlib import Path
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#Libraries for downloding images
import urllib.request
import tempfile
from tqdm import tqdm

#Libraries for uploading images to aws
from botocore.exceptions import ClientError
import logging
import boto3
import botocore

class Mat_Yoga:
    def __init__(self, provider='Amazon', name='', price='', material=[], number_of_reviews='', rating = '', colours = ''):
        self.provider = provider # provider and distributor (amazon has more than one provider)
        self.name = name
        self.price = price
        self.material = material
        self.rating = rating
        self.number_of_reviews = number_of_reviews
        self.colours = colours

    def __repr__(self):
        return (f'{self.provider}, {self.name}, {self.price}, {self.material}, {self.colours}, {self.rating},{self.number_of_reviews}\n')
    # How to return in repro in different lines??? 

BASE_DIR = Path(__file__).resolve(strict=True).parent

def get_driver_headless():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors-spki-list')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--headless")
    # initialize driver
    driver = webdriver.Chrome(chrome_options=options)
    return driver

def get_driver():
    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors-spki-list')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-ssl-errors')
    # options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome()#chrome_options=options)
    return driver

def connect_to_base(browser, page_number):
    base_url = f"https://www.amazon.com/s?k=yoga+mats&i=sports-and-fitness&rh=n%3A3422251%2Cn%3A3422301&dc&page={page_number}"
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(base_url)
            # wait for the page to be loaded
            # before returning True
            print('he estado en la pagina,', page_number)
            sleep(5)
            return True
        except Exception as e:
            print(e)
            connection_attempts += 1
            print(f"Error connecting to {base_url}.")
            print(f"Attempt #{connection_attempts}.")
    return False

def connect_to_base_mat(browser, mat_url):
    base_url = mat_url
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(base_url)
            # wait for the page to be loaded
            # before returning True
            print('he estado en la pagina de una mat' )
            return True
        except Exception as e:
            print(e)
            connection_attempts += 1
            print(f"Error connecting to {base_url}.")
            print(f"Attempt #{connection_attempts}.")
    return False
#Link to all pages with scraping using click scraping. #in range  400 or while more,
#it only takes 7 when I access by find_element_by_id('twotabsearchtextbox'),
#I have to select department and then yoga mats to load more pages
# driver = webdriver.Chrome()
# driver.get('https://www.amazon.com')
# search_box = driver.find_element_by_id('twotabsearchtextbox').send_keys('yoga mats')
# search_button = driver.find_element_by_id("nav-search-submit-text").click()
# driver.implicitly_wait(5) #time.sleep(5)
# try:
#     num_page = driver.find_element_by_xpath('//*[@class="a-pagination"]/li[6]')
# except NoSuchElementException:
#     num_page = driver.find_element_by_class_name('a-last').click()
# driver.implicitly_wait(3)
# url_list = []
# print(num_page.text)
# for i in range(10):
#         page_ = i + 1
#         url_list.append(driver.current_url)
#         driver.implicitly_wait(4)
#         click_next = driver.find_element_by_xpath('//*[@class="a-last"]/a').click()                        
#         print("Page " + str(page_) + " grabbed")
# driver.quit()

# def get_all_links_to_each_mat_in_each_page(driver, current_page):   
#     all_links = []    
#     try:
#         print('sleeping 5 sec, page',current_page)
#         links = driver.find_elements_by_xpath('//*[@class="a-size-mini a-spacing-none a-color-base s-line-clamp-4"]/a')
#         sleep(5)
#         for i in links:
#             all_links.append(i.get_attribute("href"))
#     except Exception as e:
#         print('Error getting URLs for each mat', e)
#     return(all_links)


def write_to_file_Link(output_list, filename):
    df = pd.DataFrame(output_list)
    df.to_csv(Path(BASE_DIR).joinpath(filename), mode='a', header=False)

def write_to_csv_mat(filename_csv, keys, values):
    name =Path(BASE_DIR).joinpath(filename_csv)
    #desordenado con solo las siguientes dos lineas
    df = pd.DataFrame(values, index=keys).T
    df.to_csv(name, mode='a', header=False)
    #vertical con las siguientes lineas
    # df = pd.DataFrame(values)
    # df.to_csv(Path(BASE_DIR).joinpath(filename_csv), mode='a', index=keys)
  
    #fieldnames=list(mat.keys())
    #with open(name, "a") as fp:
    #      writer = csv.DictWriter(fp)
    #      writer.writerow(fieldnames)
    #      writer.writerows(mat)

   

# with open(today+'_Amazon_link_to__each_page.txt', 'w') as f:
#         for url in link_to_all_pages:
#             f.write('%s\n' % url)
# print("---DONE---")



def write_to_json_mat(filename_json, keys, values ):
    mat ={}
    for k,v in zip(keys,values):
        mat[k] = v
    name =Path(BASE_DIR).joinpath(filename_json)
    with open(name, 'a') as file:
        #json_ = json.dump(file_data)
        #file.write(str(mat)+'\n')
        json.dump(str(mat),file) # it works but too much inf so indent dont work

# today = str(date.today())
# with open(today + '_all_mats_lululemon_10_06_21.json', 'w') as f:
#       json.dump(json_file,f, indent=4)

def upload_images(src_list, src_name):
    """
    Get the list of cat images from excel with all features as src_list      
    Create a temporary directory, so you don't store images in your local machine
    """
    # with tempfile.TemporaryDirectory() as temp_dir:
    #     for name, scr in src_list, src_name: 
    #         print('uploading to aws', name, scr)
    #         urllib.request.urlretrieve(scr, f'{temp_dir}/{name}.png')
    #         upload_file(f'{temp_dir}/{name}.png', 'webscraping-project-amazon-mats-pictures', f'pictures/{name}')
    return True

def upload_file(file_name, bucket, object_name=None):
    """
    Upload a file to an S3 bucket
    
    Parameters
    ----------
    file_name : str
        Name of the file we want to upload
    bucket: str
        Name of the bucket
    object_name:
        Name of the object as we want it to appear in the bucket

    Returns
    -------
    bool
        False if the upload caused an error. True if the upload was successful
    """
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


