"""
Create a data frame by scraping our calendar in BED-2056:

http://timeplan.uit.no/emne_timeplan.php?sem=20h&module%5B%5D=BED-2056-1&View=list

This is the link to the “Vis” list. If you would like to scrape another “Vis”, that is ok.
In the final data frame, each date should be one row, and make sure you format the dates correctly. 
"""
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url = 'http://timeplan.uit.no/emne_timeplan.php?sem=20h&module%5B%5D=BED-2056-1&View=list'
respnse = requests.get(url)

soup = BeautifulSoup(respnse.text, 'html.parser')
title = soup.find(id="maincontent").text
table_row = soup.findAll("tbody")
coulumns = soup.find('tr', {'class': 'table-active'}).text
text = coulumns.split('\n')
print(text)
l = []
for tr in table_row:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    l.append(row)
print(l)


# liste = []


""" l = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    l.append(row)
pd.DataFrame(l, columns=["A", "B", ...]) """

""" for i in range (34,37):
    diction = {}
    ids = "Timeplan for BED-2056-1 i uke " + str(i)
    print(soup.find(title=ids)) """