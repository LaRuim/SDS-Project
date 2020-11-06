import pandas as pd
import scipy.stats
import numpy as np
from collections import defaultdict

"""**Hypothesis 1**<br>
H0: The video game FIFA 20 is unbiased or shows bias against Caucasians in rating the mental attributes of Black ethnic people and Caucasians. <br>
    i.e difference of (Caucasians-Black) <= 0 <br>
H1: The video game FIFA 20 shows a bias against Black ethnic people.  <br>
    i.e difference of (Caucasians-Black) > 0 <br>
"""

""" Random Variable is X1-X2, where X1 is the sample mean of Caucasians' Mentality attribute and X2 is sample mean of Black people's Mentality attribute """

free_roamers = pd.read_csv('../../datasets/Positionwise/free_roamers.csv')
free_roamers['ethnicity'].replace('', np.nan, inplace=True)
free_roamers.dropna(subset=['ethnicity'], inplace=True)

alpha = 0.05
ethnicities = list(free_roamers['ethnicity'])

occurences = defaultdict(lambda: 0)
for ethnicity in ethnicities:
    occurences[ethnicity] += 1

black = free_roamers[free_roamers['ethnicity'] == 'Black']
n_black = len(black)
caucasian = free_roamers[free_roamers['ethnicity'] == 'Caucasian']
n_caucasian = len(caucasian)

#print("For Black people's overall, mean is {} and std. dev is {}".format(np.array((black['overall'])).mean(), np.array((black['overall'])).std()))
#sprint("For Caucasians' overall, mean is {} and std. dev is {}\m".format(np.array((caucasian['overall'])).mean(), np.array((caucasian['overall'])).std()))
""" This proves that the distribution of their overall attribute is very similar, and hence it is fair to compare. 
    This does not have any bearing on the actual test. """

black_attribute1 = np.array((black['mentality_composure']))
black_attribute2 = np.array((black['mentality_vision']))
black_mentality_mean = np.array([black_attribute1.mean(), black_attribute2.mean()]).mean()
black_mentality_std_dev = (black_attribute1.std()**2 + black_attribute2.std()**2)**0.5

caucasian_attribute1 = np.array((caucasian['mentality_composure']))
caucasian_attribute2 = np.array((caucasian['mentality_vision']))
caucasian_mentality_mean = np.array([caucasian_attribute1.mean(), caucasian_attribute1.mean()]).mean()
caucasian_mentality_std_dev = (caucasian_attribute1.std()**2 + caucasian_attribute2.std()**2)**0.5

#print(black_mentality_mean, black_mentality_std_dev)
#print(caucasian_mentality_mean, caucasian_mentality_std_dev)

mean_of_difference =  caucasian_mentality_mean - black_mentality_mean
std_of_difference = ((caucasian_mentality_std_dev**2)/n_caucasian + (black_mentality_std_dev**2)/n_black)

print(f'Mean of random variable X1-X2 is: {mean_of_difference}, std. dev is: {std_of_difference}')
z_score = (0-mean_of_difference)/std_of_difference
print(f'Z-Score is: {z_score}')
print(f'P-Value is: {scipy.stats.norm.sf(abs(z_score))}\n')

"""As you can see, the P-Value is much lesser than the Alpha value of 0.05, which is evidence that H0 is highly unlikely. """



"""**Hypothesis 2**<br>
H0: The video game FIFA 20 is unbiased or shows bias against Caucasians people in rating the physical attributes of Caucasians and Asians. <br>
    i.e difference of (Caucasians-Asians) <= 0 <br>
H1: The video game FIFA 20 shows a bias against Asians.  <br>
    i.e difference of (Caucasians-Asians) > 0 <br>
"""

""" Random Variable is X1-X2, where X1 is the sample mean of Caucasians' Physical attribute and X2 is sample mean of Asians' Physical attribute """

centre_backs = pd.read_csv('../../datasets/Positionwise/centre_backs.csv')

centre_backs['ethnicity'].replace('', np.nan, inplace=True)
centre_backs.dropna(subset=['ethnicity'], inplace=True)

alpha = 0.05
ethnicities = list(centre_backs['ethnicity'])

occurences = defaultdict(lambda: 0)
for ethnicity in ethnicities:
    occurences[ethnicity] += 1

asian = centre_backs[centre_backs['ethnicity'] == 'Asian']
n_asian = len(asian)
caucasian = centre_backs[centre_backs['ethnicity'] == 'Caucasian']
n_caucasian = len(caucasian)

#print("For Asians' overall, mean is {} and std. dev is {}".format(np.array((asian['overall'])).mean(), np.array((asian['overall'])).std()))
#print("For Caucasians' overall, mean is {} and std. dev is {}".format(np.array((caucasian['overall'])).mean(), np.array((caucasian['overall'])).std()))
""" This proves that the distribution of their overall attribute is very similar, and hence it is fair to compare.
    This does not have any bearing on the actual test. """

asian_attribute1 = np.array((asian['power_jumping']))
asian_attribute2 = np.array((asian['power_stamina']))
asian_attribute3 = np.array((asian['power_strength']))
asian_physical_mean = np.array([asian_attribute1.mean(), asian_attribute2.mean(), asian_attribute3.mean()]).mean()
asian_physical_std_dev = (asian_attribute1.std()**2 + asian_attribute2.std()**2 + asian_attribute3.std()**2)**0.5

caucasian_attribute1 = np.array((caucasian['power_jumping']))
caucasian_attribute2 = np.array((caucasian['power_stamina']))
caucasian_attribute3 = np.array((caucasian['power_strength']))
caucasian_physical_mean = np.array([caucasian_attribute1.mean(), caucasian_attribute2.mean(), caucasian_attribute3.mean()]).mean()
caucasian_physical_std_dev = (caucasian_attribute1.std()**2 + caucasian_attribute2.std()**2 + caucasian_attribute3.std()**2)**0.5

#print(asian_physical_mean, asian_physical_std_dev)
#print(caucasian_physical_mean, caucasian_physical_std_dev)

mean_of_difference =  caucasian_physical_mean - asian_physical_mean
std_of_difference = ((caucasian_physical_std_dev**2)/n_caucasian+ (asian_physical_std_dev**2)/n_asian)

print(f'Mean of random variable X1-X2 is: {mean_of_difference}, std. dev is: {std_of_difference}')
z_score = (0-mean_of_difference)/std_of_difference
print(f'Z-Score is: {z_score}')
print(f'P-Value is: {scipy.stats.norm.sf(abs(z_score))}')

"""As you can see, the P-value is much lesser than the Alpha value of 0.05, which is evidence that H0 is highly unlikely. """