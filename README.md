Automated Amazon Scraping

This program automates the web scraping process of connecting 
to amazon.com, searching for a product entered by the user,
scraping the results, and writing the product data found in
a JSON file. The script will run automatically and collect all
of the search results, regardless of the number of pages.

Sample amazon_search_data.json file is included from the latest
time I ran the script to demonstrate what the output looks like.

To run this program:

    - Open your terminal, and cd to project directory

    - Type: python automateWeb.py

    - A file named: amazon_search_data.json will appear
        in the project directory once the web scraping
        is complete.

Dependencies:

    - Python 3.8
    - json
    - os
    - time
    - BeautifulSoup
    - Pandas
    - Selenium
    
