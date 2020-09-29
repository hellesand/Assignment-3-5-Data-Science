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
import plotly.figure_factory as ff
from tabulate import tabulate



url = 'http://timeplan.uit.no/emne_timeplan.php?sem=20h&module%5B%5D=BED-2056-1&View=list'
respnse = requests.get(url)

soup = BeautifulSoup(respnse.text, 'html.parser')
title = soup.find(id="maincontent").text
table_row = soup.findAll("tbody")
column = soup.find('tr', {'class': 'table-active'}).text
column.strip()
column.strip("\n")
column = column.split('\n')

while("" in column) : 
    column.remove("") 

rows = []
for tr in table_row:
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    print(row)
    rows.append(row)

df2 = pd.DataFrame(rows, columns=column)
print(df2)
print(tabulate(df2, showindex=False, headers=df2.columns))
neatTable = tabulate(df2, showindex=False, headers=df2.columns)

text_file = open("TimeTable.txt", "w")
n = text_file.write(neatTable)
text_file.close()

# with open('TimeTable.txt','w+') as outfile:

#     df2.to_string(outfile,columns=column)
    