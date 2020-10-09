import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from tabulate import tabulate


def get_data():
    ''' Method that scrape the data '''
    url = 'http://timeplan.uit.no/emne_timeplan.php?sem=20h&module%5B%5D=BED-2056-1&View=list'
    response = requests.get(url)
    return response

def parse_data(response):
    ''' Method that parse the page content and put it into data table'''
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find(id="maincontent").text
    table_row = soup.findAll("tbody")
    column = soup.find('tr', {'class': 'table-active'}).text
    column = column.split('\n')
    while("" in column) : 
        column.remove("") 

    ''' Get all rows with lectures '''
    rows = []
    for tr in table_row:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        rows.append(row)


    ''' Split date variable into day and date '''
    days = []
    for row in rows:
        days.append(row[0][0:6])
        date = row[0][6:]
        row[0] = date
    df = pd.DataFrame(rows, columns=column)
    df.insert(0, 'Dag', days)

    return df 

def store_table(df):
    ''' Method that stores the data frame '''
    neatTable = tabulate(df, showindex=False, headers=df.columns)
    text_file = open("TimeTable.txt", "w")
    n = text_file.write(neatTable)
    text_file.close()

    df.to_csv("TimeTable.csv", index=False, header=True)


if __name__ == "__main__":    
    page = get_data()
    dataframe = parse_data(page)
    store_table(dataframe)