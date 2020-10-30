import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

centre_backs = pd.read_csv("../../datasets/Positionwise/centre_backs.csv") 
free_roamers = pd.read_csv("../../datasets/Positionwise/free_roamers.csv")
full_backs = pd.read_csv("../../datasets/Positionwise/full_backs.csv")
midfielders = pd.read_csv("../../datasets/Positionwise/midfielders.csv")
strikers = pd.read_csv("../../datasets/Positionwise/strikers.csv")
wingers = pd.read_csv("../../datasets/Positionwise/wingers.csv")

centre_backs.hist(column='overall')
plt.xlabel(" CentrebacksOverall Value")
plt.ylabel("Number of players")
plt.show()
free_roamers.hist(column='overall')
plt.xlabel("Free Roamers Overall Value")
plt.ylabel("Number of players")
plt.show()
full_backs.hist(column='overall')
plt.xlabel("Full Backs Overall Value")
plt.ylabel("Number of players")
plt.show()
midfielders.hist(column='overall')
plt.xlabel("Mid-Fielders Overall Value")
plt.ylabel("Number of players")
plt.show()
strikers.hist(column='overall')
plt.xlabel("Strikers Overall Value")
plt.ylabel("Number of players")
plt.show()
wingers.hist(column='overall')
plt.xlabel("Wingers Overall Value")
plt.ylabel("Number of players")
plt.show()

fig, ax = plt.subplots(figsize = (10, 5))


plt.boxplot(centre_backs.height_cm, positions = [1], widths= 0.6)
plt.boxplot(free_roamers.height_cm, positions = [2.3], widths = 0.6)
plt.boxplot(full_backs.height_cm, positions = [3.5], widths = 0.6)
plt.boxplot(midfielders.height_cm, positions = [4.6], widths = 0.6)
plt.boxplot(strikers.height_cm, positions = [5.6], widths = 0.6)
plt.boxplot(wingers.height_cm, positions = [6.6], widths = 0.6)
ax.set_xticklabels(['Centre_backs', 'Free_roamers', 'Full_backs', 'Midfielders', 'Strikers', 'Wingers'])
ax.set_xticks([1, 2.3, 3.5, 4.6, 5.6, 6.6])
plt.show()

