import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def parse_data(filename):
   male = 0
   female = 0
   sex_dict = {"F":{},"M":{}}
   with open(filename, "rb") as f:
      data = f.readline()
      while data:
         month = data[12:14].decode("UTF-8")
         gender = data[474:475].decode("UTF-8")
         weight = data[503:507].decode("UTF-8")
         day = data[22:23].decode("UTF-8")

         if month not in sex_dict[gender]:
            sex_dict[gender][month] = {}
         if day not in sex_dict[gender][month]:
            sex_dict[gender][month][day] = {"amount": 0, "weight": 0}

         sex_dict[gender][month][day]["amount"] += 1
         sex_dict[gender][month][day]["weight"] += int(weight)

         data = f.readline()   

   return sex_dict   

def get_ratio_percentage(dataset, months, days):
   female = dataset["F"]
   male = dataset["M"]

   females = 0
   males = 0
 
   for month in months:
      for day in days:
         females += female[month][day]['amount']
         males += male[month][day]['amount']

   
   ratio_men = males/(females+males) * 100
   ratio_women = females/(females+males) * 100

   return males, females, ratio_men, ratio_women

def calculate_average_weight(dataset, months,days, total_males, total_females):
   female = dataset["F"]
   male = dataset["M"]

   females_weight = 0
   males_weight = 0
 
   for month in months:
      for day in days:
         females_weight += female[month][day]['weight']
         males_weight += male[month][day]['weight']
      
   average_female_weight = females_weight/total_females
   average_male_weight = males_weight/total_males

   return average_female_weight,average_male_weight

def calculate_by_day_ratio(dataset, months, days):
   female = dataset["F"]
   male = dataset["M"]

   female_days = [-1,-1,-1,-1,-1,-1,-1]
   male_days = [-1,-1,-1,-1,-1,-1,-1]

   female_num = []
   male_num = []

   for month in months:
      for day in days:
         female_num = female[month][day]['amount']
         male_num = male[month][day]['amount']

         female_days[int(day)-1] += female_num
         male_days[int(day)-1] += male_num

   ratio_male_list = []
   ratio_female_list = []

   for i in range(0,len(days)):
      ratio_male = male_days[i] / (male_days[i] + female_days[i]) * 100
      ratio_female = female_days[i]/ (male_days[i] + female_days[i]) * 100
      ratio_female_list.append(ratio_female)
      ratio_male_list.append(ratio_male)

   return ratio_male_list, ratio_female_list


def plot_days(male_2018,male_19,female_18,female_19):
   days = ["Sun", "Mon", "Tue", "Wed", "Thi", "Fri", "Sat"]
   barWidth = 0.15

   r1 = np.arange(len(male_2018))
   r2 = [x + barWidth for x in r1]
   r3 = [x + barWidth for x in r2]
   r4 = [x + barWidth for x in r3]

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

def plot(males,females, title, figname):
   x = ["2018","2019"]
   barWidth = 0.20

   r1 = np.arange(len(males))
   r2 = [x + barWidth for x in r1]

   plt.bar(r1, males, width = barWidth, color = 'lightskyblue', edgecolor = 'black', capsize=7, label='Males')
   plt.bar(r2, females, width = barWidth, color = 'pink', edgecolor = 'black', capsize=7, label='Females')

   plt.xticks([r + barWidth for r in range(len(males))], x)
   plt.ylabel('Ratio in percent')
   plt.title(title)
   plt.legend()
   plt.savefig(figname)
   plt.close()    


def main():
   months = ['01','02','03','04','05','06','07','08','09','10','11','12']
   days = ['1','2','3','4','5','6','7']

   result_2018 = parse_data("2018.txt")
   result_2019 = parse_data("2019.txt")
   total_males_2018, total_females_2018, men_ratio_2018, women_ratio_2018 = get_ratio_percentage(result_2018, months, days)
   total_males_2019, total_females_2019, men_ratio_2019, women_ratio_2019 = get_ratio_percentage(result_2019, months, days)
   females = [women_ratio_2018, women_ratio_2019]
   males = [men_ratio_2018, men_ratio_2019]
   plot(males, females, "Ratio in percentage female vs male", "ratiogender")


   average_female_weight_2018, average_male_weight_2018 = calculate_average_weight(result_2018, months, days, total_males_2018, total_females_2018)
   average_female_weight_2019, average_male_weight_2019 = calculate_average_weight(result_2019, months, days, total_males_2019, total_females_2019)

   female_average_weight = [average_female_weight_2018, average_female_weight_2019]
   male_average_weig = [average_male_weight_2018, average_male_weight_2019]

   plot(male_average_weig, female_average_weight, "Average weight of children by gender", "averageweight")

   ratio_male_day_2018, ratio_female_day_2018 = calculate_by_day_ratio(result_2018, months, days)
   ratio_male_day_2019, ratio_female_day_2019 = calculate_by_day_ratio(result_2019, months, days)

   plot_days(ratio_male_day_2018, ratio_male_day_2018, ratio_female_day_2018, ratio_female_day_2019)



if __name__ == "__main__":
   main()