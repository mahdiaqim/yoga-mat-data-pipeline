#%%
from numpy import numarray
from selenium import webdriver
from datetime import date
from time import sleep
driver = webdriver.Chrome()
import urllib.request
#to make it go faster
# options = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images": 2}
# options.add_experimental_option("prefs", prefs)


# %%
class Mat_Yoga:
    def __init__(self, provider='Lululemon', name='', price='', material=[], number_of_reviews='', rating = '', colours = ''):
        self.provider = provider
        self.name = name
        self.price = price
        self.material = material
        self.rating = rating
        self.number_of_reviews = number_of_reviews
        self.colours = colours

    def __repr__(self):
        return (f'{self.provider}, {self.name}, {self.price}, {self.material}, {self.colours}, {self.rating},{self.number_of_reviews}\n')
    # How to return in repro in different lines???
    
        
def get_all_links_to_each_mat():
        #N_items = 28    
    driver.get('https://www.lululemon.co.uk/en-gb/c/accessories?prefn1=styleNumber&prefv1=Yoga+Mats&sz=34')
    sleep(10)
    all_links = []
    for i in range(2,33):
        try:
            path_each = f'//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[{i}]/div/div/div[2]/div[2]/a'
            product_link = driver.find_element_by_xpath(path_each)
            #print (product_link.text)
            link = product_link.get_attribute('href')
            print(link)
            all_links.append(link)
        except Exception as e:
            print('meassage',e)
            continue
    return(all_links)
    #print (len(all_links))
    #return all_links
    
def get_materials():
    try:
        material_link = driver.find_element_by_xpath('//*[@id="collapseThree"]/ul/li')
        material_text = material_link.get_attribute("innerHTML")
    except Exception as e:
        material_text = 'error'
                
    #print (material_text)
    return (material_text.replace(',',' -'))


def get_price ():
    try:
        price_link = driver.find_element_by_class_name('markdown-prices')
        price = price_link.get_attribute('innerHTML')
    except Exception as e:
            price = 'error'

    return (price)


def get_name():
    try:
        name_link = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[3]/h1')
        name =  name_link.text
    except Exception as e:
        name = 'error'
    
    return (name)


def get_number_of_reviews ():
    try:
       number_of_reviews_xpath = driver.find_element_by_xpath('//*[@id="BVRRSearchContainer"]/div/div/div/div/div/div[1]/div/dl/dd[2]/a')
       number_of_reviews = number_of_reviews_xpath.text.split()[0]
    except Exception as e:
        number_of_reviews = 'error'
    
    return number_of_reviews
 
def get_rating():
    try:
        #price_link = driver.find_element_by_class_name('class="bv-rating-label bv-text-link bv-focusable')
        rating_link = driver.find_element_by_class_name('bv-rating')
        rating = rating_link.text.split()[0]
        #print(price_link.get_attribute('innerHTML'))
    except Exception as e:
            rating = 'error'
    return rating

def get_colours():
    try:
        colour_link = driver.find_element_by_class_name('selected-swatch-name')
        colour = colour_link.get_attribute("innerHTML")
    
    except Exception as e:
            colour = 'error'
    
    return colour

    
def fetch_all_data_for_one_mat(mat_url):
        driver.get(mat_url)
        sleep(5)
        mat_yoga = Mat_Yoga(
            material = get_materials(),
            price = get_price(),
            name = get_name (),
            rating = get_rating (),
            number_of_reviews = get_number_of_reviews(),
            colours = get_colours()

        )
        return(mat_yoga)

list_of_all_links = get_all_links_to_each_mat()
all_mats = []
for url in list_of_all_links:
    try:
        single_mat = fetch_all_data_for_one_mat(url)
        all_mats.append(single_mat) 
    except Exception as e:
                print('meassage',e)
                continue


#%%
print(all_mats)
#print(all_mats)

  
#%%
import pandas as pd
import csv
df = pd.DataFrame(list_of_all_links)
today = str(date.today())
df.to_csv(today+'_all_links_lululemon.csv')

df = pd.DataFrame(all_mats)
today = str(date.today())
df.to_csv(today+'_all_mats_lululemon.csv')
#%%
print (all_mats)

#%%
#To json
import json
json_file= []
for i in all_mats:
    a = {
    'Provider' : i.provider ,
    'name' : i.name ,
    'price' : i.price, 
    'material' :i.material ,
    'rating' : i.rating,
    'number_reviews' : i.number_of_reviews,
    'colours' : i.colours 

    }
    json_file.append(a)
# test = json.dumps(json_file, indent = 4) 
# from pprint import pprint
# pprint(test)
today = str(date.today())
with open(today + '_all_mats_lululemon_10_06_21.json', 'w') as f:
      json.dump(json_file,f, indent=4)


#%%
#Test for Materials
driver = webdriver.Chrome()
# baseURL = 'https://www.lululemon.co.uk/en-gb/c/accessories?prefn1=styleNumber&prefv1=Yoga+Mats&sz=34'     
# driver.get (baseURL)
for i in list_of_all_links[2:5]:
    try:
      driver.get(i)
      material_link = driver.find_element_by_xpath('//*[@id="collapseThree"]/ul/li')
      material_text = material_link.get_attribute("innerHTML")
      print(material_text)
    except Exception as e:
        print('meassage',e)
        continue
#%%
#Test for prices
driver = webdriver.Chrome()
# baseURL = 'https://www.lululemon.co.uk/en-gb/c/accessories?prefn1=styleNumber&prefv1=Yoga+Mats&sz=34'     
# driver.get (baseURL)
for i in list_of_all_links[2:5]:
    try:
       driver.get(i)
       price_link = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[3]/h1')
       print(price_link.text)
    except Exception as e:
        print('meassage',e)
        continue

#%%
#Test for number of reviews
driver = webdriver.Chrome()
# baseURL = 'https://www.lululemon.co.uk/en-gb/c/accessories?prefn1=styleNumber&prefv1=Yoga+Mats&sz=34'     
# driver.get (baseURL)
for i in list_of_all_links[2:5]:
    try:
       driver.get(i)
       #N_reviews_link = driver.find_element_by_class_name('bv-rating-label bv-text-link bv-focusable')
       N_reviews_link = driver.find_element_by_xpath('//*[@id="BVRRSearchContainer"]/div/div/div/div/div/div[1]/div/dl/dd[2]/a')
       #print(N_reviews_link.get_attribute('innerHTML'))
       print (N_reviews_link.text.split()[0])
    except Exception as e:
        print('meassage',e)
        continue


#%%
#Test for rating
driver = webdriver.Chrome()
# baseURL = 'https://www.lululemon.co.uk/en-gb/c/accessories?prefn1=styleNumber&prefv1=Yoga+Mats&sz=34'     
# driver.get (baseURL)
for i in list_of_all_links[2:5]:
    try:
       driver.get(i)
       #price_link = driver.find_element_by_class_name('class="bv-rating-label bv-text-link bv-focusable')
       rating_link = driver.find_element_by_class_name('bv-rating')
       print (rating_link.text.split()[0])
       #print(price_link.get_attribute('innerHTML'))
    except Exception as e:
        print('meassage',e)
        continue

#%%
#Test for images, store them and then save them with unique Id
driver = webdriver.Chrome()
m = 0
for i in list_of_all_links[3:6]:
    m+=1
    try:
       driver.get(i)
       #price_link = driver.find_element_by_class_name('class="bv-rating-label bv-text-link bv-focusable')
       img_url = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[3]/div[1]/div[1]/div[1]/div[1]/a/img').get_attribute('src')
      
       print (img_url)
       urllib.request.urlretrieve(img_url, f'{m}.png')

    #    with open(f'{i}.png', 'wb') as file:
    #        file.write(driver.driver.find_element_by_xpath('.//img').screenshot_as_png)
       #print(price_link.get_attribute('innerHTML'))
    except Exception as e:
        print('meassage',e)
        continue

#%%
#Get Colors
driver = webdriver.Chrome()
# baseURL = 'https://www.lululemon.co.uk/en-gb/c/accessories?prefn1=styleNumber&prefv1=Yoga+Mats&sz=34'     
# driver.get (baseURL)
for i in list_of_all_links[2:5]:
    try:
       driver.get(i)
       #price_link = driver.find_element_by_class_name('class="bv-rating-label bv-text-link bv-focusable')
       rating_link = driver.find_element_by_class_name('selected-swatch-name')
       print (rating_link.get_attribute("innerHTML"))
       #print(price_link.get_attribute('innerHTML'))
    except Exception as e:
        print('meassage',e)
        continue


#%%




    
