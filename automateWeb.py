"""
Author: Brian Rafferty
Date: 8/15/20
Summary: My program automates the process of 
            accessing amazon.com and searching 
            for all the products related to an
            entered term. The program will record
            all of the data retrieved from the
            search, regardless of pagination. 
            Once all data is collected, it is
            packaged into JSON format.
"""
# System library imports
import json
import os
import time

# External library imports
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Start script by asking user for a product to search
searchTerm = input('Enter item to search on Amazon: ')

# Set web driver and website to access
PATH = '/Applications/chromedriver'
URL = 'https://www.amazon.com'

# Connect to the Google Chrome and open Amazon.com
driver = webdriver.Chrome(PATH)
driver.implicitly_wait(30)
driver.get(URL)

# Access search bar and enter product written by User
search = driver.find_element_by_id('twotabsearchtextbox')
search.send_keys(searchTerm)
search.send_keys(Keys.RETURN)

# Determine total number of pages displaying results
findLastPage = driver.find_elements_by_xpath("//li[@class='a-disabled']")
lastPage = int(findLastPage[-1].text)
print('Found {} pages of results by searching: {}... beginning web scraping...'.format(lastPage, searchTerm))

# Instantiate temporary list to hold all scraped data
dataStorage = []
pageCount = 1
nextButton = True

# Loop through pages while next button exists at bottom of webpage
while nextButton:
    
    print('Loading results from page: {}'.format(pageCount))

    # Allow webpage time to load
    time.sleep(5)

    # Create soup object that contains all HTML on current webpage
    soup = BeautifulSoup(driver.page_source, 'lxml')

    # Loop through the HTML to find products
    for item in soup.find_all('span', attrs={'cel_widget_id': 'MAIN-SEARCH_RESULTS'}):
        
        # Grab all product data (use try/catch blocks for data that is potentially missing)
        product = item.h2.a.span.text

        try:
            brand = item.h5.span.text
        except Exception:
            brand = None

        itemURL = 'https://www.amazon.com{}'.format(item.h2.a.get('href'))

        try:
            price = item.find('span', class_='a-price').span.text
        except Exception:
            price = None

        try:
            rating = item.find('span', class_='a-icon-alt').text
        except Exception:
            rating = None

        image = item.img.get('src')

        # Add all product data as a list, making dataStorage a 2D list
        dataStorage.append([product, brand, price, rating, itemURL, image])

    # End scraping process once last webpage of results is scraped
    if pageCount == lastPage:
        nextButton = False
    
    else:
        # Access next button at bottom of webpage and click it
        nextButton = driver.find_elements_by_xpath("//li[@class='a-last']/a")[0]
        nextButton.click()
        pageCount += 1
    
print('------------------\nCompleted scraping!\n------------------')

# Close Google Chrome
driver.quit()

# Convert 2D list of product data into Pandas DataFrame
df = pd.DataFrame(dataStorage, columns=['Product Name', 'Brand', 'Price', 'Rating', 'Product URL', 'Image Link'])

# Convert Pandas DataFrame into a dictionary with JSON format
json = json.dumps(df.to_dict('records'))

# Find current working directory and create output JSON file in it
path = os.getcwd()
outputFile = open(path + '/amazon_search_data.json', 'w')
outputFile.write(json)
outputFile.close()

print('Created file: amazon_search_data.json\nIn directory: {}'.format(path))