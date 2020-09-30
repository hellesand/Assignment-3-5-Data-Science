import requests
from bs4 import BeautifulSoup   
import pandas as pd
from tabulate import tabulate

''' Lists for storing the course titles '''
R_courses = []
Python_courses = []

def extract_data():
    ''' Method for scraping the web page '''
    R_url = 'https://www.datacamp.com/courses/tech:r'
    Python_url = 'https://www.datacamp.com/courses/tech:python'
    page = requests.get(R_url)
    python_page = requests.get(Python_url)

    return page, python_page

def parse_data(page, liste):
    ''' Method that locate course title '''
    soup = BeautifulSoup(page.content, 'html.parser')
    for body in soup.findAll('div',{'class':'course-block__body'}):
        title = body.find('h4', {'class':'course-block__title'}).text
        liste.append(title)

def make_frame(liste, language):
    ''' Method that creates dataframe and appends language '''
    DataFrame = pd.DataFrame(liste, columns=['Tech'])
    DataFrame['Language'] = language
    return DataFrame


def concatenate_and_store_dataframes(R_Frame, Python_Frame):
    ''' Method that concatinates R courses and python corses and stores it in file '''
    frames = [R_DataFrame, Python_DataFrame]
    combined = pd.concat(frames)
    frames = [R_DataFrame, Python_DataFrame]
    combined = pd.concat(frames)

    neatTable = tabulate(combined, showindex=False, headers=combined.columns)

    text_file = open("CourseTable.txt", "w")
    n = text_file.write(neatTable)
    text_file.close()

    combined.to_csv("CourseTable.csv", sep='\t', index=False, header=True)


if __name__ == "__main__":
    R_Page, Python_Page = extract_data()

    parse_data(R_Page, R_courses)
    parse_data(Python_Page, Python_courses)

    R_DataFrame = make_frame(R_courses, 'R')
    Python_DataFrame = make_frame(Python_courses, 'Python')
    concatenate_and_store_dataframes(R_DataFrame, Python_DataFrame)




