from numpy.linalg.linalg import norm
import pandas as pd
import numpy as np
from helper import NormStd
import os

Path_to_csv = ['../../datasets/Positionwise/centre_backs.csv', ]
# Add all the paths to CSV here
# Make sure it is in the same format
OUTPUT_DIRECTORY = f'./Values'
if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(OUTPUT_DIRECTORY)

for csv in Path_to_csv:
    OUTPUT_DIRECTORY_FILE = f'./Values/{csv[28:-3]}txt'

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
