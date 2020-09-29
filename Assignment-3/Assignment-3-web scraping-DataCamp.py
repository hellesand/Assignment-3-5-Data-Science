""" 
Create a long data frame by scraping the names of all DataCamps courses in R & Python:

https://www.datacamp.com/courses/tech:r
https://learn.datacamp.com/courses/tech:python

Your final data frame should have two variables, one for “tech” and one for “language”.
"""

import requests
import urllib.request
import time
from bs4 import BeautifulSoup   
import json
from selenium import webdriver
import pandas as pd

from pandas.io.json import json_normalize

# Set the URL you want to webscrape from
url = 'https://learn.datacamp.com/courses/tech:r'

page  = requests.get(url).content
data = json.loads(page.decode('utf-8'))
print(data)

# data = json_normalize(data)
# df = pd.DataFrame(data)
# soup = BeautifulSoup(page, 'html.parser')
# books = soup.find_all('div',attrs={"class":"courses__explore-list js-async-bookmarking row"})
# print(books)





