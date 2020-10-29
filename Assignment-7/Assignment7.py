import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parse_data(filename):
   ''' 
      Read the text files and extract the necessary information.
      The information is gathered by byte position and these 
      byte positions can be found in the user guide to the datasets.
   '''
   male = 0
   female = 0

   # Make a dictionary for females and males.
   sex_dict = {"F":{},"M":{}}

   # Open the file and read bytes
   with open(filename, "rb") as f:

      # Read one line at the time
      data = f.readline()
      while data:

         # Extract month, gender, weight and day by byte position.
         month = data[12:14].decode("UTF-8")
         gender = data[474:475].decode("UTF-8")
         weight = data[503:507].decode("UTF-8")
         day = data[22:23].decode("UTF-8")

         # Check if the month is located inside the dictionary for the gender
         if month not in sex_dict[gender]:
            sex_dict[gender][month] = {}
         
         # Check if the day is located inside the gender and inside the month
         if day not in sex_dict[gender][month]:
            sex_dict[gender][month][day] = {"amount": 0, "weight": 0}

         # Add another to the amount of gender to the day
         sex_dict[gender][month][day]["amount"] += 1

         # Sum the weight of the day
         sex_dict[gender][month][day]["weight"] += int(weight)

         data = f.readline()   

   return sex_dict   

def get_ratio_percentage(dataset, months, days):
   """ Method to calculate ratio of men and womens"""
   female = dataset["F"]
   male = dataset["M"]

   females = 0
   males = 0
   
   # Iterate through the dictionary - each month and each dat of month
   for month in months:
      for day in days:
         females += female[month][day]['amount']
         males += male[month][day]['amount']

   # Calculate the ratio of males and females
   ratio_men = males/(females+males) * 100
   ratio_women = females/(females+males) * 100

   return males, females, ratio_men, ratio_women

def calculate_average_weight(dataset, months,days, total_males, total_females):
   """ Calculate the average weight of males and females of the year """ 
   female = dataset["F"]
   male = dataset["M"]

   females_weight = 0
   males_weight = 0
 
   # Iterate through the dictionary and add to total weight
   for month in months:
      for day in days:
         females_weight += female[month][day]['weight']
         males_weight += male[month][day]['weight']
   
   # Calculate the average weight of females and males
   average_female_weight = females_weight/total_females
   average_male_weight = males_weight/total_males

   return average_female_weight,average_male_weight

def calculate_by_day_ratio(dataset, months, days):
   """ Calculate the ratio of females/males for each day throughout the year"""
   female = dataset["F"]
   male = dataset["M"]

   # Make list to hold each day of the week for both gender
   female_days = [-1,-1,-1,-1,-1,-1,-1]
   male_days = [-1,-1,-1,-1,-1,-1,-1]

   female_num = []
   male_num = []

   # Iterate through the dictionary
   for month in months:
      for day in days:
         female_num = female[month][day]['amount']
         male_num = male[month][day]['amount']

         # Add the current day into the total amount for that day
         female_days[int(day)-1] += female_num
         male_days[int(day)-1] += male_num

   ratio_male_list = []
   ratio_female_list = []

   # Calculate the ratio for each day of the week for both genders
   for i in range(0,len(days)):
      ratio_male = male_days[i] / (male_days[i] + female_days[i]) * 100
      ratio_female = female_days[i]/ (male_days[i] + female_days[i]) * 100
      ratio_female_list.append(ratio_female)
      ratio_male_list.append(ratio_male)

   return ratio_male_list, ratio_female_list


def plot_days(male_2018,male_19,female_18,female_19):
   """ Method to plot bars of ratio """
   days = ["Sun", "Mon", "Tue", "Wed", "Thi", "Fri", "Sat"]
   barWidth = 0.15

   # Make a group of 4 bars 
   r1 = np.arange(len(male_2018))
   r2 = [x + barWidth for x in r1]
   r3 = [x + barWidth for x in r2]
   r4 = [x + barWidth for x in r3]

   # Plot 4 bars, one bar for each gender and one for each year
   plt.bar(r1, male_2018, width = barWidth, color = 'lightskyblue', edgecolor = 'black', capsize=7, label='Males 2018')
   plt.bar(r2, male_19, width = barWidth, color = 'steelblue', edgecolor = 'black', capsize=7, label='Males 2019')
   plt.bar(r3, female_18, width = barWidth, color = 'hotpink', edgecolor = 'black', capsize=7, label='Females 2018')
   plt.bar(r4, female_19, width = barWidth, color = 'lightpink', edgecolor = 'black', capsize=7, label='Females 2019')

   plt.ylim(0,70)
   plt.xticks([r + barWidth for r in range(len(male_2018))], days)
   plt.ylabel('Porportion in percent of day of birth')
   plt.title("Ratio of gender born per day")
   plt.legend()
   plt.savefig("days")
   plt.close()

def plot(males,females, title, figname, labelen):
   """ Method to bar plot"""
   x = ["2018","2019"]
   barWidth = 0.20

   # Arrange group of two 
   r1 = np.arange(len(males))
   r2 = [x + barWidth for x in r1]

   # Plot two bars, one for femles and one for males
   plt.bar(r1, males, width = barWidth, color = 'lightskyblue', edgecolor = 'black', capsize=7, label='Males')
   plt.bar(r2, females, width = barWidth, color = 'pink', edgecolor = 'black', capsize=7, label='Females')

   plt.xticks([r + barWidth for r in range(len(males))], x)
   plt.ylabel(labelen)
   plt.title(title)
   plt.legend()
   plt.savefig(figname)
   plt.close()    


def main():
   months = ['01','02','03','04','05','06','07','08','09','10','11','12']
   days = ['1','2','3','4','5','6','7']

   # Parse the datafiles for 2018 and 2019
   result_2018 = parse_data("2018.txt")
   result_2019 = parse_data("2019.txt")

   # Get the ratio and total number for each gender for both years
   total_males_2018, total_females_2018, men_ratio_2018, women_ratio_2018 = get_ratio_percentage(result_2018, months, days)
   total_males_2019, total_females_2019, men_ratio_2019, women_ratio_2019 = get_ratio_percentage(result_2019, months, days)
   
   # Plot the ratio of females and males on gender
   females = [women_ratio_2018, women_ratio_2019]
   males = [men_ratio_2018, men_ratio_2019]
   plot(males, females, "Ratio in percentage female vs male", "ratiogender", 'Ratio in percent')

   # Calculate the average weight for females and males for both years
   average_female_weight_2018, average_male_weight_2018 = calculate_average_weight(result_2018, months, days, total_males_2018, total_females_2018)
   average_female_weight_2019, average_male_weight_2019 = calculate_average_weight(result_2019, months, days, total_males_2019, total_females_2019)

   # Plot the average weight for both years
   female_average_weight = [average_female_weight_2018, average_female_weight_2019]
   male_average_weig = [average_male_weight_2018, average_male_weight_2019]
   plot(male_average_weig, female_average_weight, "Average weight of children by gender", "averageweight", "Weight in grams")

   # Calculate the ratio of men and women for each day of the week for both years
   ratio_male_day_2018, ratio_female_day_2018 = calculate_by_day_ratio(result_2018, months, days)
   ratio_male_day_2019, ratio_female_day_2019 = calculate_by_day_ratio(result_2019, months, days)

   # Plot the ratio for each day of the week 
   plot_days(ratio_male_day_2018, ratio_male_day_2018, ratio_female_day_2018, ratio_female_day_2019)



if __name__ == "__main__":
   main()