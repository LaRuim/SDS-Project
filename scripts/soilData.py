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
        try:
            #df[i] = df.astype("float64")
            for j in range(df[i].size):
                try:
                    ran_num = random.random()
                    if (ran_num < 0.5):
                        sign = random.random()
                        if (sign < 0.5):
                            sign = -1
                        else:
                            sign = 1
                        df[i][j] = round(df[i][j] + sign * ran_num, 2)
                except:
                    print(df[i][j])
            num = random.randrange(0, percentage)
            for j in range(num, df[i].size, percentage):
                try:
                    df[i][j] *= -1
                except:
                    print(df[i][j])
        except:
            print(df[i].dtype)
df.to_csv("../datasets/Full/players_20_soiled.csv")
