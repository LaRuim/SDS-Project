from numpy.linalg.linalg import norm
import pandas as pd
import numpy as np
from helper import NormStd
import os


print("\n")
print("#"*5, end='')
print("NORMALIZING AND STANDARDIZING DATA", end='')
print("#"*5)
print("\n")

Path_to_csv = ['../../datasets/Positionwise/centre_backs.csv', '../../datasets/Positionwise/free_roamers.csv',
               '../../datasets/Positionwise/full_backs.csv', '../../datasets/Positionwise/midfielders.csv',
               '../../datasets/Positionwise/strikers.csv', '../../datasets/Positionwise/wingers.csv']

OUTPUT_DIRECTORY = f'./logs'
if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)

for csv in Path_to_csv:
    OUTPUT_DIRECTORY_FILE = f'./logs/{csv[28:-3]}txt'

    file = open(OUTPUT_DIRECTORY_FILE, 'w')
    df = pd.read_csv(csv)
    for playerColumnHeading in df.columns:
        if df[playerColumnHeading].dtype in [int, float] and playerColumnHeading:
            playerColumn = np.array(df[playerColumnHeading])
            normStdObj = NormStd(playerColumn)
            values = normStdObj.NormalizeAndStandardize()
            file.write(f"Column Name: {playerColumnHeading}\n")
            for val in values.keys():
                file.write(f"\t{val}\n")
                file.write(f"\t\t{values[val]}\n")
