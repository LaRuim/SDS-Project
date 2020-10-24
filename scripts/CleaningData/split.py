import pandas as pd
import os

class Dataset:
    RAW_FILE_PATH = "../datasets/Full/players_20.csv"
    DATA_FILE_PATH = "../datasets/Full/players_20_filtered.csv"
    OUTPUT_DIRECTORY = "../datasets/Positionwise"

    USELESS_ATTRIBUTES = {
        'all': ['ls', 'st', 'rs', 'lw', 'lf', 'cf', 'rf', 'rw', 'lam', 'cam', 'ram', 'lm', 'lcm', 'cm',
                'rcm', 'rm', 'lwb', 'ldm', 'cdm', 'rdm', 'rwb', 'lb', 'lcb', 'cb', 'rcb', 'rb',
                'pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'player_traits'],

        'centre_backs': ['attacking_crossing', 'attacking_finishing', 'attacking_volleys', 'skill_dribbling',
                        'skill_curve', 'skill_fk_accuracy', 'skill_ball_control', 'power_shot_power',
                        'power_long_shots', 'mentality_penalties'],

        'full_backs': ['attacking_heading_accuracy', 'attacking_volleys', 'skill_curve', 'skill_fk_accuracy',
                    'power_shot_power', 'power_jumping', 'power_long_shots', 'mentality_aggression', 
                    'mentality_composure'],

        'midfielders': ['attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy', 'attacking_volleys',
                    'skill_curve', 'skill_fk_accuracy', 'mentality_penalties'],

        'wingers': ['attacking_heading_accuracy', 'attacking_volleys', 'power_shot_power', 'power_jumping', 
                    'defending_marking', 'defending_standing_tackle', 'defending_sliding_tackle'],

        'free_roamers': ['attacking_heading_accuracy', 'attacking_volleys', 'power_shot_power', 'power_jumping', 
                        'power_long_shots', 'mentality_aggression', 'mentality_interceptions', 'mentality_positioning', 
                        'defending_marking', 'defending_standing_tackle', 'defending_sliding_tackle'],                                  

        'strikers': ['attacking_crossing', 'skill_long_passing', 'mentality_aggression', 'mentality_interceptions',
                    'mentality_positioning', 'mentality_vision', 'defending_marking', 'defending_standing_tackle',
                    'defending_sliding_tackle'],
    }                                                          
                        
    def filter_data(self, RAW_FILE_PATH, DATA_FILE_PATH):
        df = pd.read_csv(RAW_FILE_PATH, encoding='cp1252', index_col=0)
        list(map(lambda useless_attribute: df.drop(useless_attribute, axis=1, inplace=True), self.USELESS_ATTRIBUTES['all']))
        df.to_csv(DATA_FILE_PATH, index=True)

    def __read_filtered_data(self, DATA_FILE_PATH):
        self.data = pd.read_csv(DATA_FILE_PATH)

    def __split_by_position(self):
        positionwise_data = dict()
        positionwise_data['centre_backs'] = self.data.loc[self.data['team_position'].isin(['LCB', 'RCB', 'SW', 'CB'])]
        positionwise_data['full_backs'] = self.data.loc[self.data['team_position'].isin(['LB', 'RB', 'LWB', 'RWB'])]
        positionwise_data['midfielders'] = self.data.loc[self.data['team_position'].isin(['CDM', 'RDM', 'LDM', 'CM', 'RCM', 'LCM'])]
        positionwise_data['wingers'] = self.data.loc[self.data['team_position'].isin(['LW', 'LM', 'RW', 'RM'])]
        positionwise_data['free_roamers'] = self.data.loc[self.data['team_position'].isin(['RAM', 'LAM', 'CAM'])]
        positionwise_data['strikers'] = self.data.loc[self.data['team_position'].isin(['ST', 'RS', 'LS', 'CF', 'LF', 'RF'])]
        self.positionwise_data = positionwise_data

    def __filter_split_data(self):
        for position in self.positionwise_data:
            for useless_attribute in self.USELESS_ATTRIBUTES[position]:
                self.positionwise_data[position].drop(useless_attribute, axis=1, inplace=True)
        #list(map(lambda position: map(lambda useless_attribute: self.positionwise_data[position].drop(useless_attribute, axis=1, inplace=True), self.USELESS_ATTRIBUTES[position]), self.positionwise_data.keys()))

    def __write_to_csv(self, OUTPUT_DIRECTORY):
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.mkdir(OUTPUT_DIRECTORY)
        list(map(lambda position: self.positionwise_data[position].to_csv(f'{OUTPUT_DIRECTORY}/{position}.csv', index=True), self.positionwise_data.keys()))

    def create_datasets(self, RAW_FILE_PATH=None, DATA_FILE_PATH=None, OUTPUT_DIRECTORY=None):
        if not RAW_FILE_PATH:
            RAW_FILE_PATH = self.RAW_FILE_PATH
        if not DATA_FILE_PATH:
            DATA_FILE_PATH = self.DATA_FILE_PATH
        if not OUTPUT_DIRECTORY:
            OUTPUT_DIRECTORY = self.OUTPUT_DIRECTORY

        self.filter_data(RAW_FILE_PATH=RAW_FILE_PATH, DATA_FILE_PATH=DATA_FILE_PATH)
        self.__read_filtered_data(DATA_FILE_PATH=DATA_FILE_PATH)
        self.__split_by_position()
        self.__filter_split_data()
        self.__write_to_csv(OUTPUT_DIRECTORY)

    def print_data(self):
        '''for position in self.positionwise_data:
            print(self.positionwise_data[position].to_markdown())'''
        list(map(lambda position: print(self.positionwise_data[position].to_markdown()), self.positionwise_data.keys()))
        print("\n\n\n\n")

#dataset = Dataset()
#dataset.create_datasets()
#myData.filter_data()
#myData.print_data()
Dataset().create_datasets()