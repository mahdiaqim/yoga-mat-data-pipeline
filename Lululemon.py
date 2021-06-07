#%%
from selenium import webdriver
driver = webdriver.Chrome()
baseURL = 'https://www.lululemon.co.uk/en-gb/c/accessories?prefn1=styleNumber&prefv1=Yoga+Mats&sz=34'     
driver.get (baseURL)

# %%
# class Mat_Yoga:
#     def __init__(self, baseURL, N_items):
#         self.baseURL = baseURL
#         self.N_items = N_items
#         self.driver =  webdriver.Chrome()
#%%
# class ='col-6 col-md-4' class on the main page of 26 different types of product
# Xpath for eah one of the products on base:    
            #' //*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[2]/div/div'
            # '//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[3]/div/div'
            # '//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[4]/div/div'
            # //*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[29]
            # '//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[2]'
# Xpath for price of price on base
        #/'/*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[2]/div/div/div[2]/div[3]/div/span'
# Xpath for name and href on base:
            #'//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[3]/div/div/div[2]/div[2]/a'
            #'//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[5]/div/div/div[2]/div[2]/a'

# Price once I am on the website of a specific Mat:
        #'/html/body/div[1]/div[3]/div[3]/div[3]/div[3]/div/div[1]/label/span/span[1]'
        #'/html/body/div[1]/div[3]/div[3]/div[3]/div[3]/div/div[1]/label/span/span[1]'
        #'/html/body/div[1]/div[3]/div[3]/div[3]/div[3]/div/div[1]/label/span/span[1]'
#%%
#Product_name_price = driver.find_element_by_xpath('//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[2]/div/div')
#print(Product_name_price.text)
#%%
#Product_link = driver.find_element_by_xpath('//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[3]/div/div/div[2]/div[2]/a')
#href = Product_link.get_attribute('href')
# %%
#%%
#Find link to each product
#try by while it exist to cut the number of loops
#Try by class
all_links = []
for i in range(2,8):
    path_each = f'//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[{i}]/div/div/div[2]/div[2]/a'
    product_link = driver.find_element_by_xpath(path_each)
     #print (product_link.text)
    link = product_link.get_attribute('href')
    print(link)
    all_links.append(link)

for i in range(9,13):
    path_each = f'//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[{i}]/div/div/div[2]/div[2]/a'
    product_link = driver.find_element_by_xpath(path_each)
     #print (product_link.text)
    link = product_link.get_attribute('href')
    print(link)
    all_links.append(link)
for i in range(14,30):
    path_each = f'//*[@id="product-search-results"]/div[2]/div[2]/div[4]/div[{i}]/div/div/div[2]/div[2]/a'
    product_link = driver.find_element_by_xpath(path_each)
    #print (product_link.text)
    link = product_link.get_attribute('href')
    print(link)
    all_links.append(link)
# %%
print (len(all_links))
driver.quit()
#%%
#take material
driver = webdriver.Chrome()
all_material= []
for i in range (0,13):
    driver.get (all_links[i])
    material = driver.find_element_by_xpath('//*[@id="collapseThree"]/ul/li')
    text_1 = material.get_attribute("innerHTML")
    print(text_1)
    all_material.append(text_1)
for i in range (14,20):
    driver.get (all_links[i])
    material = driver.find_element_by_xpath('//*[@id="collapseThree"]/ul/li')
    text_1 = material.get_attribute("innerHTML")
    print(text_1)
    all_material.append(text_1) 
for i in range (20,26):
    driver.get (all_links[i])
    material = driver.find_element_by_xpath('//*[@id="collapseThree"]/ul/li')
    text_1 = material.get_attribute("innerHTML")
    print(text_1)
    all_material.append(text_1) 

#%%
#from 26 element I could retrieve 25 as Number 13 in All links has an error
print (len(all_material))
    
#%%
#price and reviews 

# %%
