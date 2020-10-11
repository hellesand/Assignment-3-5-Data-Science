import numpy as np
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import re
import pandas as pd
import re
import calendar

# List of conties in Norway and Svalbard
county = ["Troms og Finnmark", "Nordland", "Trøndelag", "Møre og Romsdal", "Vestland", "Rogaland", "Agder", "Vestfold og Telemark", "Viken", "Oslo", "Innlandet","Svalbard","Utenlands"]

# Months in a year in numeric
months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

def daysInEachMonth(year):
    ''' Method to find out number of days in each month in a specific year '''
    days = []
    for i in range(1,13):
        days.append(calendar.monthrange(year, i)[1])

    return days

def scrapeWeb(days, month, counties, year):
    '''
        Method that scrapes each month in the year. 
        A new url is generate for all months in the year. 
    '''

    # Set empty dictionary
    result = {year:{}}

    # Go through all months in the months list
    for i in range(len(month)):

        # Format a new url based on which month, number of days in the month and year
        url = ("https://w2.brreg.no/kunngjoring/kombisok.jsp?datoFra=01.{}.{}&datoTil={}.{}.{}&id_region=0&id_niva1=51&id_niva2=56&id_bransje1=0").format(month[i], year,days[i], month[i], year) 
        
        # Send get request to the formatted url
        response = requests.get(url)

        # Parse the response text
        soup = BeautifulSoup(response.text, 'html.parser')
        curent_county = None
        counter = 0

        # Locate all tr elements in the response
        for tr in soup.findAll('tr'):

            # Check if the value one of the countes
            if tr.text.strip() in counties:
                curr_month = None

                # If a county is set - update the value in the dictionary
                if curent_county != None:
                    curr_month = {i+1:counter}
                    result[year][curent_county].update(curr_month)

                counter = 0
                # If the county is not located in the result dictionary - add key to dictionary
                curent_county = tr.text.strip()
                if curent_county not in result[year]:
                    result[year][curent_county] = {}
            else:
                # If the value is not a county
                text = tr.text.strip()

                # Check if the value is "Konkuråpning" if it is - add another to the counter 
                if "Konkursåpning" in text:
                    counter += 1

    return result

def calculateCumulative(liste, year):
    ''' Calculate cumulative '''
    for index,i in enumerate(liste):

        # If first element in list - do nothing
        if(index == 0):
            continue
        else:
            # Add the sum of the previous element
            liste[index] = i + liste[index - 1]
    
    return liste

def makeDataFrameAndPlotFigure(resultat_2019, resultat_2020):
    ''' Method to make the two data frames and plot the results for all conties '''

    # All months in 2019
    monts = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun','Jul','Aug', 'Sep', 'Oct','Nov', 'Dec']

    # Only the nine first months in 2020
    monts_2020 = ['Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun','Jul','Aug', 'Sep']

    # Dataframe for 2019 with result of 12 months
    df_2019 = pd.DataFrame(columns=['2019'])
    df_2019['Months'] = monts

    # Dataframe for 2020 - only nine first months
    df_2020 = pd.DataFrame(columns=['2020'])
    df_2020['Months'] = monts[:9] #.dt.strftime('%b')

    # Go through all names in the county list
    for i in county:
        counter = 1
        liste = []
        liste_2020 = []

        # Append the result for all 12 monts
        while counter < 13:

            # Check if the month has any bankruptcies
            try:
                liste.append(resultat_2019[2019][i][counter])
            except:
                # If the month had no bankruptcies add a zero to the list
                liste.append(0)
            try:
                liste_2020.append(resultat_2020[2020][i][counter])
            except:
                liste_2020.append(0)
            counter += 1

        # Calculate cumulative number for both years
        liste = calculateCumulative(liste, 2019)
        liste_2020 = calculateCumulative(liste_2020, 2020)
        
        # Append the cumulative result into the dataframes
        df_2019['2019'] = liste
        df_2020['2020'] = liste_2020[:9]

        # Plot the line of 2020
        ax = df_2020.plot(x = 'Months', y = '2020')

        # Plot the line for 2019 i same plot
        df_2019.plot(x = 'Months', y = '2019',ax=ax)

        # Set limit for x and y
        plt.xticks(list(range(0,12)), monts)
        plt.ylim([0,1100])
        plt.show()

        # Set title of figure
        plt.title(i)

        # Save figure
        plt.savefig(i)
        

def run():
    days = daysInEachMonth(2019)
    days_2020 = daysInEachMonth(2020)
    resultat_2019 = scrapeWeb(days, months, county, 2019)
    resultat_2020 = scrapeWeb(days_2020, months, county, 2020)
    makeDataFrameAndPlotFigure(resultat_2019, resultat_2020)

if __name__ == "__main__":
    run()