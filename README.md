# Webscraping yoga mats
## Summary:
### The project has the scripts for webscraping yoga mats from Lululemon and Amazon. it uses multithreading for Amazon. in both cases it has two parts, the first one 
### collects urls for each product and the second collects the targeted features: price, color, reviews, rating , material and images. 
## Motivation:
### Finding the relation between price, material, provider, color, ratings and reviews and predict the price using ML.
## Elements necessary:
### Libraries for webscraping : selenium, urlib.request, pathlib, tempfile
### Libraries to upload images to S3 bucket  : boto3
### Libraries to upload to database created in RDS : psycopg, sqlachemy , pandas and json
### Libraries for multuthreading : ThreadPoolExecutor and wait from concurrent.futures  
## Results:
### In the case of amazon the scraper file contains all functions that are used in the script files. Amazon contains multithreading and it appends continuosly any data scraped to a csv and a json file simultaneously. It collected data for 1000 yoga mats in 5221 seconds.
### In the case of Lululemon multithreading there is only one file that contains all functions, it  uploads continuosly the images to a bucket in s3. At the end it saves all scraped data to a csv file, to a json file and a database in Amazon RDS  
