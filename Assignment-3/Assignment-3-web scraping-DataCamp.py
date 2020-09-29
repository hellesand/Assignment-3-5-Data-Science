""" 
Create a long data frame by scraping the names of all DataCamps courses in R & Python:

https://www.datacamp.com/courses/tech:r
https://learn.datacamp.com/courses/tech:python

Your final data frame should have two variables, one for “tech” and one for “language”.
"""

import requests
from bs4 import BeautifulSoup   
import json
import pandas as pd
from tabulate import tabulate

R_courses = []
Python_courses = []

R_url = 'https://www.datacamp.com/courses/tech:r'
Python_url = 'https://www.datacamp.com/courses/tech:python'

page = requests.get(R_url)
soup = BeautifulSoup(page.content, 'html.parser')

for body in soup.findAll('div',{'class':'course-block__body'}):
    title = body.find('h4', {'class':'course-block__title'}).text
    R_courses.append(title)


python_page = requests.get(Python_url)
python_soup = BeautifulSoup(python_page.content, 'html.parser')

for body in python_soup.findAll('div',{'class':'course-block__body'}):
    title = body.find('h4', {'class':'course-block__title'}).text
    Python_courses.append(title)

R_DataFrame = pd.DataFrame(R_courses, columns=['Tech'])
R_DataFrame['Language'] = 'R'

Python_DataFrame = pd.DataFrame(Python_courses,columns=['Tech'])
Python_DataFrame['Language'] = 'Python'

frames = [R_DataFrame, Python_DataFrame]
combined = pd.concat(frames)

neatTable = tabulate(combined, showindex=False, headers=combined.columns)

text_file = open("CourseTable.txt", "w")
n = text_file.write(neatTable)
text_file.close()







