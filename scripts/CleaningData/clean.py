import pandas as pd
import numpy as np

DATA_CSV = "../datasets/Full/players_20_soiled.csv"

df = pd.read_csv(DATA_CSV)

labels = list(df.columns)

# dropping negative ages
df.drop(df[df['age'] <= 0].index, inplace=True)
df.dropna()
# fixing weight and height

# case 1: height and weight negative
df.drop(df[(df[labels[2]] <= 0) & (df[labels[3]] <= 0)].index, inplace=True)

list1 = list(df[labels[2]])
list2 = list(df[labels[3]])
hw = list(zip(list1, list2))


def getIndex(hw, val, col):
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
    if (list1[i] < 0):
        index = getIndex(hw, list1[i]*-1, 'h')
        if (len(index) == 1):
            list1[i] = list1[index[0]]
        else:
            list1[i] = (list1[index[0]] +
                        list1[index[1]])/2
# case 3: height negative and weight postive
index = []
hw.sort(key=lambda x: x[0])
for i in range(len(hw)):
    if (list2[i] < 0):
        index = getIndex(hw, list2[i]*-1, 'h')
        if (len(index) == 1):
            list2[i] = list2[index[0]]
        else:
            list2[i] = (list2[index[0]] +
                        list2[index[1]])/2
df[labels[2]] = list1
df[labels[3]] = list2
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

df["preferred"] = pref_foot

df.to_csv('../datasets/Full/players_20_cleaned.csv')
