from numpy.lib.function_base import percentile
import pandas as pd
import numpy as np
import random


DATA_CSV = "../datasets/Full/players_20.csv"
percentage = 7

df = pd.read_csv(DATA_CSV, encoding='cp1252', index_col=0)
for i in df.columns:
    print(i, df[i].dtype)
    if (df[i].dtype == object):
        num = random.randrange(0, percentage)
        for j in range(num, df[i].size, percentage):
            try:
                df[i][j] = np.nan
            except:
                print(df[i][j])
        for j in range(num + 4, df[i].size, 4):
            if (df[i][j] != np.nan and df[i].dtype == str):
                id = random.randrange(0, len(df[i][j]))
                try:
                    df[i][j][id] = df[i][j][id].upper()
                except:
                    print(df[i][j], id)
    else:
        num = random.randrange(0, percentage)
        for j in range(num, df[i].size, percentage):
            try:
                df[i][j] *= -1
            except:
                print(df[i][j])
df.to_csv("../datasets/Full/players_20_soiled.csv")
