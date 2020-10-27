import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import time
import logging
from tqdm import tqdm
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

logging.basicConfig(level= logging.DEBUG, filename="clean.log", filemode="w")

print("\n")
print("#"*5, end = '')
print("CLEANING DATA", end='')
print("#"*5)
print("\n")

listPosition = ['free_roamers', 'full_backs', 'midfielders', 'strikers', 'wingers', 'centre_backs']
for pos in (range(len(listPosition))):
    print("\nFor position: ", listPosition[pos])
    position = listPosition[pos]
    DATA_CSV = f"../../datasets/Positionwise/{position}.csv" # Make positionwise
    logging.debug(f'\nNow cleaning {position}.csv\n')
    data = pd.read_csv(DATA_CSV)
    try:
        data.drop('Unnamed: 0', axis=1, inplace=True)
    except:
        pass
    try:
        data.drop('level_0', axis=1, inplace=True)
    except:
        pass
    data.reset_index(inplace=True)
    try:
        data.drop('level_0', axis=1, inplace=True)
    except:
        pass
    try:
        data.drop('Unnamed: 0', axis=1, inplace=True)
    except:
        pass
    labels = list(data.columns)

    data.drop(data[data['age'] <= 0].index, inplace=True)
    data.dropna()

    data.drop(data[(data['height_cm'] <= 0) & (data['weight_kg'] <= 0)].index, inplace=True)
    data.drop(data[(data['ethnicity'] == np.nan)].index,  inplace=True)
    nationalities = list(data['nationality'])

    nation_heights = {nation: [] for nation in nationalities}
    nation_weights = {nation: [] for nation in nationalities}

    for nation_index in range(len(nationalities)):
        nation_heights[nationalities[nation_index]].append(data['height_cm'][nation_index])
        nation_weights[nationalities[nation_index]].append(data['weight_kg'][nation_index])

    for nation in nationalities:
        nation_heights[nation].sort()
        nation_weights[nation].sort()

    dataset_size = len(data.index)

    heights_changed = 0
    weights_changed = 0
    height_changes_simple = 0
    weight_changes_simple = 0
    for row in tqdm(range(dataset_size), desc = "Height-Weight", ncols = 100 ):
        
        if data['height_cm'][row] < 0:
            old_height = data['height_cm'][row]
            all_heights = nation_heights[nationalities[row]]
            all_weights = nation_weights[nationalities[row]]

            weight = data['weight_kg'][row]
            possible_heights = [all_heights[index] for index, possible_weight in enumerate(all_weights) if possible_weight == weight]
            new_height = -1

            if (len(possible_heights)):
                new_height = round(sum(possible_heights)/len(possible_heights), 1)
            else:
                for possible_weight_index in all_weights:
                    if all_weights[possible_weight_index] < weight and all_weights[possible_weight_index+1] > weight:
                        new_height = round((all_heights[possible_weight_index] + all_heights[possible_weight_index+1])/2, 1)
            if new_height < 0:
                data.loc[row, 'height_cm'] = -data['height_cm'][row]
                logging.debug(f"Failed in changing {data['short_name'][row]}'s height; Changed instead to negative of itself.")
                height_changes_simple += 1
            else:
                data.loc[row, 'height_cm'] = new_height
                logging.debug(f"Converted {data['short_name'][row]}'s height from {old_height} to {data['height_cm'][row]}.")
                heights_changed += 1

        elif data['weight_kg'][row] < 0:
            old_weight = data['weight_kg'][row]
            all_weights = nation_weights[nationalities[row]]
            all_heights = nation_heights[nationalities[row]]

            height = data['height_cm'][row]
            possible_weights = [all_weights[index] for index, possible_height in enumerate(all_heights) if possible_height == height]
            new_weight = -1

            if (len(possible_weights)):
                new_weight = round(sum(possible_weights)/len(possible_weights), 1)
            else:
                for possible_height_index in all_heights:
                    if all_heights[possible_height_index] < height and all_heights[possible_height_index+1] > height:
                        new_weight = round((all_weights[possible_height_index] + all_weights[possible_height_index+1])/2, 1)
            if new_weight < 0:
                data.drop([row])
                logging.debug(f"Failed in changing {data['short_name'][row]}'s weight; It was still {old_weight}")
                weight_changes_simple += 1
            else:
                data.loc[row, 'weight_kg'] = new_weight
                logging.debug(f"Converted {data['short_name'][row]}'s weight from {old_weight} to {data['weight_kg'][row]}.")
                weights_changed += 1

    logging.debug(f"Heights changed: {heights_changed}\nHeight changes with sign inversion: {height_changes_simple}")
    logging.debug(f"Weights changed: {weights_changed}\nWeight changes with sign inversion: {weight_changes_simple}")

    data.to_csv(f"../../datasets/Positionwise/{position}.csv" ) # Save height and weight corrections
    




    def find_player(player_data, attribute_index):
        only_numeric_attributes = data
        for label in labels:
            if only_numeric_attributes[label].dtype not in [int, float]:
                only_numeric_attributes = only_numeric_attributes.drop(label, axis=1)
        only_numeric_attributes = only_numeric_attributes.drop('height_cm', axis=1)
        only_numeric_attributes = only_numeric_attributes.drop('weight_kg', axis=1)
        only_numeric_attributes = only_numeric_attributes.drop('overall', axis=1)
        only_numeric_attributes = only_numeric_attributes.drop('age', axis=1)

        name = player_data['short_name']
        attrs = (list(player_data.index))
        for attr in attrs:
            if type(player_data[attr]) not in [int, float]:
                player_data = player_data.drop(attr)
        str_Attrs = ['short_name',
                    'nationality',
                    'ethnicity',
                    'preferred_foot',
                    'weak_foot',
                    'skill_moves',
                    'work_rate',
                    'team_position',
                    'height_cm',
                    'weight_kg',
                    'overall',
                    'age']
        for str_attr in str_Attrs:
            try:
                player_data = player_data.drop(str_attr)
            except:
                pass
        try:
            players = only_numeric_attributes.drop(labels[attribute_index], axis=1).transpose()
        except:
            logging.debug("Only Numeric Attrs:", only_numeric_attributes)
        try:
            player_data = player_data.drop(labels[attribute_index])
        except:
            logging.debug("Player Data:", player_data)
        BEST_COSINE_DISTANCE = 0.75
        best_match = None
        for index in players:
            similar_player = players[index]
            check_negative = transposed_data[index]
            if check_negative[list(check_negative.keys())[attribute_index]] < 0:
                continue
            try:
                cosine_distance = (player_data @ similar_player.transpose()) / (norm(player_data)*norm(similar_player.transpose()))
                #logging.debug(cosine_distance)
                if cosine_distance > BEST_COSINE_DISTANCE and round(cosine_distance, 4) != 1.0000:
                    best_match = data.transpose()[index]['index']
                    best_match_name = data.transpose()[index]['short_name']
                    BEST_COSINE_DISTANCE = cosine_distance
            except Exception as E:
                logging.debug(E)
                logging.debug(f"Shapes:\nCol: {player_data.shape}, simplayer: {similar_player.shape}")
                logging.debug(list(player_data.keys()))
                logging.debug('AND')
                logging.debug(list(similar_player.keys()))
        if best_match:
            logging.debug(f'Best match for {name} was {best_match_name}, with similarity: {BEST_COSINE_DISTANCE}')
        else:
            logging.debug(f'No best match for {name}.')
        return best_match, BEST_COSINE_DISTANCE
        
    transposed_data = data.transpose()
    dataset_t_size = len(transposed_data.index)
    indices = list(transposed_data.columns)


    for player_idx in tqdm(range(len(indices)),desc = "Other Attributes",ncols = 100):
        player_index = indices[player_idx]
        similar_player = None  
        for attribute_index in range(labels.index('team_position')+1, dataset_t_size):
            if type(transposed_data[player_index][attribute_index]) in [int, float]:
                if transposed_data[player_index][attribute_index] < 0:
                    logging.debug(f"{player_index+1}.")
                    x, cosine_distance = find_player(transposed_data[player_index], attribute_index)
                    if cosine_distance > 0.75 and x:
                        write_val = data[x:x+1].values[0][attribute_index]
                        if write_val > 0:
                            transposed_data.loc[labels[attribute_index], player_index] = write_val
                            data.loc[player_index, labels[attribute_index]] = write_val
                        else:
                            transposed_data.loc[labels[attribute_index], player_index] = -transposed_data[player_index][attribute_index]
                            data.loc[player_index, labels[attribute_index]] = -transposed_data[player_index][attribute_index]
                    else:
                        transposed_data.loc[labels[attribute_index], player_index] = -transposed_data[player_index][attribute_index]
                        data.loc[player_index, labels[attribute_index]] = -transposed_data[player_index][attribute_index]
        
    data = transposed_data.transpose()

    data.to_csv(f"../../datasets/Positionwise/{position}.csv" )
    