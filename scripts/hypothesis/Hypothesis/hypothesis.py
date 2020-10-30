# -*- coding: utf-8 -*-
"""Hypothesis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fZ2Ze3drvF6LRu9DX_wh6JoYVJxz79Yi
"""

import pandas as pd
import scipy.stats
import numpy as np

strikers = pd.read_csv('/content/drive/My Drive/Colab Notebooks/Nihal/Hypothesis/strikers.csv')

strikers['ethnicity'].replace('', np.nan, inplace=True)
strikers.dropna(subset=['ethnicity'], inplace=True)

"""**Hypothesis 1**<br>
H0: Asians are just as good as Caucasians when it comes to mental attributes. <br>
H1: Caucasians are better than Asians when it comes to mental attributes. <br>
"""

eth_list = list(strikers['ethnicity'])

freq = dict()
for i in eth_list:
    if i not in freq.keys():
        freq[i] = 0
    freq[i] += 1

strikers['mentality_composure']

print(freq)

asn = strikers[strikers['ethnicity'] == 'Asian']
csn = strikers[strikers['ethnicity'] == 'Caucasian']

asn

csn

ma = np.array((asn['mentality_composure']))
maMean = ma.mean()
maStd = ma.std()

mc = np.array((csn['mentality_composure']))
mcMean = mc.mean()
mcStd = mc.std()

print(maMean, maStd)

print(mcMean, mcStd)

len(mc)

len(ma)

z_score = (maMean - mcMean)/(maMean/len(ma))

print(z_score)

p_values = scipy.stats.norm.sf(abs(z_score))

p_values

"""As you can see the probability value is very low, hence we disproved H0.

**Hypothesis 2**<br>
H0: Blacks are better than Asians when it comes to physical attributes. <br>
H1: Asians are just as good as Blacks when it comes to physical attributes.
"""

blc = strikers[strikers['ethnicity'] == 'Black']

blc

ma1 = np.array((asn['attacking_finishing']))
ma1Mean = ma1.mean()
ma1Std = ma1.std()

bl = np.array((blc['attacking_finishing']))
blMean = bl.mean()
blStd = bl.std()

print(ma1Mean, ma1Std)

print(blMean, blStd)

len(ma1)

len(bl)

z_score1 = (ma1Mean - blMean)/(ma1Mean/len(ma1))

p_values = scipy.stats.norm.sf(abs(z_score1))

p_values

"""As you can see the probability value is very low, hence we disproved H0."""