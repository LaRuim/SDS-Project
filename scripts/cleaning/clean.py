import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm


DATA_CSV = "../../datasets/Full/players_20.csv" # Make positionwise

df = pd.read_csv(DATA_CSV)

labels = list(df.columns)

# dropping negative ages
df.drop(df[df['age'] <= 0].index, inplace=True)
df.dropna()
# fixing weight and height

# case 1: height and weight negative
df.drop(df[(df[labels[2]] <= 0) & (df[labels[3]] <= 0)].index, inplace=True)

nationalities = list(df['nationality'])
df['ethnicity'] = np.nan
df = df[[col for col in labels[:5]] + ['ethnicity'] + [col for col in labels[5:]]]

nation_heights = {nation: [] for nation in nationalities}
nation_weights = {nation: [] for nation in nationalities}

for nation_index in range(len(nationalities)):
    nation_heights[nationalities[nation_index]].append(df['height_cm'][nation_index])
    nation_weights[nationalities[nation_index]].append(df['weight_kg'][nation_index])
    nation_weights[nationalities[nation_index]].append(df['weight_kg'][nation_index])

for nation in nationalities:
    nation_heights[nation].sort()
    nation_weights[nation].sort()

dataset_size = len(df.index)

heights_changed = 0
weights_changed = 0
height_changes_failed = 0
weight_changes_failed = 0

for i in range(dataset_size):
    if df['height_cm'][i] < 0:
        old_height = df['height_cm'][i]
        all_heights = nation_heights[nationalities[i]]
        all_weights = nation_weights[nationalities[i]]

        weight = df['weight_kg'][i]
        possible_heights = [all_heights[index] for index, possible_weight in enumerate(all_weights) if possible_weight == weight]
        new_height = -1

        if (len(possible_heights)):
            new_height = round(sum(possible_heights)/len(possible_heights), 1)
        else:
            for possible_weight_index in all_weights:
                if all_weights[possible_weight_index] < weight and all_weights[possible_weight_index+1] > weight:
                    new_height = round((all_heights[possible_weight_index] + all_heights[possible_weight_index+1])/2, 1)
        if new_height < 0:
            df.drop([i])
            print(f"Failed in changing {df['short_name'][i]}'s height; It was still {old_height}")
            height_changes_failed += 1
        else:
            df.loc[i, 'height_cm'] = new_height
            print(f"Converted {df['short_name'][i]}'s height from {old_height} to {df['height_cm'][i]}.")
            heights_changed += 1

    elif df['weight_kg'][i] < 0:
        old_weight = df['weight_kg'][i]
        all_weights = nation_weights[nationalities[i]]
        all_heights = nation_heights[nationalities[i]]

        height = df['height_cm'][i]
        possible_weights = [all_weights[index] for index, possible_height in enumerate(all_heights) if possible_height == height]
        new_weight = -1

        if (len(possible_weights)):
            new_weight = round(sum(possible_weights)/len(possible_weights), 1)
        else:
            for possible_height_index in all_heights:
                if all_heights[possible_height_index] < height and all_heights[possible_height_index+1] > height:
                    new_weight = round((all_weights[possible_height_index] + all_weights[possible_height_index+1])/2, 1)
        if new_weight < 0:
            df.drop([i])
            print(f"Failed in changing {df['short_name'][i]}'s weight; It was still {old_weight}")
            weight_changes_failed += 1
        else:
            df.loc[i, 'weight_kg'] = new_weight
            print(f"Converted {df['short_name'][i]}'s weight from {old_weight} to {df['weight_kg'][i]}.")
            weights_changed += 1



print(f"Heights changed: {heights_changed}\nHeight changes failed: {height_changes_failed}")
print(f"Weights changed: {weights_changed}\nWeight changes failed: {weight_changes_failed}")

#df.to_csv('../datasets/Full/players_20_cleaned.csv')


"""def getIndex(hw, val, col):
    if (col == 'w'):
        if (hw[0][0] > val):
            return [0, ]
        for i in range(len(hw)-1):
            if (hw[i][0] == val):
                return [i, ]
            if (hw[i][0] < val and hw[i+1][0] > val):
                return [i, i+1]
        return ([len(hw)-1, ])
    else:
        if (hw[0][1] > val):
            return [0, ]
        for i in range(len(hw)-1):
            if (hw[i][1] == val):
                return [i, ]
            if (hw[i][1] < val and hw[i+1][1] > val):
                return [i, i+1]

        return ([len(hw)-1, ])


# case 2: height positive and weight negative
hw.sort(key=lambda x: x[1])

index = []
for i in range(len(hw)):
    if (heights[i] < 0):
        index = getIndex(hw, heights[i]*-1, 'h')
        if (len(index) == 1):
            heights[i] = heights[index[0]]
        else:
            heights[i] = (heights[index[0]] +
                        heights[index[1]])/2
# case 3: height negative and weight postive
index = []
hw.sort(key=lambda x: x[0])
for i in range(len(hw)):
    if (weights[i] < 0):
        index = getIndex(hw, weights[i]*-1, 'h')
        if (len(index) == 1):
            weights[i] = weights[index[0]]
        else:
            weights[i] = (weights[index[0]] +
                        weights[index[1]])/2
df[labels[2]] = heights
df[labels[3]] = weights
# df.to_csv('../datasets/Full/temp.csv')


def getIndex2(hw, val):
    if (hw[0][0] > val):
        return [0, ]
    for i in range(len(hw)-1):
        if (hw[i][0] == val):
            return [i, ]
        if (hw[i][0] < val and hw[i+1][0] > val):
            return [i, i+1]
    return ([len(hw)-1, ])


# bmi
new_height_list = list(df[labels[2]])
new_weight_list = list(df[labels[3]])
bmi = [new_weight_list[i]/(new_height_list[i]**2)
       for i in range(len(new_height_list))]

# replacing rest of the integer values based on bmi
for i in range(len(labels)):
    if (df[labels[i]].dtype != object):
        idx = []
        temp = list(df[labels[i]])
        tempList = list(zip(bmi, temp))
        tempList.sort(key=lambda x: x[1])
        for j in range(len(temp)):
            if (temp[j] < 0):
                temp_bmi = df[labels[3]]/(df[labels[2]]**2)
                idx = getIndex2(tempList, temp[j]*-1)
                if (len(idx) == 1):
                    temp[j] = tempList[idx[0]][1]
                else:
                    temp[j] = (tempList[idx[0]][1] + tempList[idx[1]][1])/2
        df[labels[i]] = temp
pref_foot = list(df["preferred_foot"])

for i in range(len(pref_foot)):
    if(pref_foot[i] != "Right" and pref_foot != "Left"):
        pref_foot[i] = "Both"

df["preferred"] = pref_foot"""
