import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import keras
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping

print("\n")
print("#"*5, end = '')
print("TRAINING MODEL", end='')
print("#"*5)
print("\n")

def getModel(inputShape):
    #Defining model
    model = Sequential()
    model.add(Dense(32, input_shape = [inputShape,], activation = 'relu'))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(1, activation = 'relu'))
    model.summary()
    return model
#Defining callbacks
callbacks = [
    EarlyStopping(monitor='loss', patience=3, verbose = 0)]

#Function reference for standardizing
scaler = StandardScaler()

PATH_LIST = ['../../datasets/Positionwise/centre_backs.csv', '../../datasets/Positionwise/free_roamers.csv',
               '../../datasets/Positionwise/full_backs.csv', '../../datasets/Positionwise/midfielders.csv',
               '../../datasets/Positionwise/strikers.csv', '../../datasets/Positionwise/wingers.csv']

for i in tqdm(range(len(PATH_LIST)), desc = "Training Model", ncols = 100):

    #Reading PATH
    dataset = pd.read_csv(PATH)

    #Cleaning Dataset
    dataset.isna().sum()
    dataset = dataset.dropna()

    #Getting all attributes
    attributeList = list(dataset.columns)[14:]

    #Filtering dataframe
    dataset = dataset[attributeList+['overall']]

    #Obtaining model's input and output
    X = np.array(dataset[attributeList])
    y = np.array(dataset[['overall']])

    X = scaler.fit_transform(X)

    #Splitting into test and train
    X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)

    #Obtaining model
    model = getModel(len(X[0]))

    #Compiling model
    model.compile(Adam(),loss = 'mse' )

    #Training model
    history = model.fit(X_train,y_train,batch_size = 20,shuffle=True,verbose=0,epochs = 5000, callbacks=callbacks)

    #Saving weights
    model.save_weights(f"./Weights/{PATH[28:-4]}.h5")

    # #Evaluating model
    print("Evaluate on test data")
    results = model.evaluate(X_test, y_test, batch_size=20)
    print("test loss, test acc:", results)

    fileName = f"./Output/{PATH[28:-4]}.txt"
    with open(fileName, 'w') as file:
        modelOutput = model.predict(X_test)
        for i in range(len(y_test)):
            file.write(f"Expected Output: {y_test[i][0]}\tModel's Output: {modelOutput[i][0]}\n")
    #model.predict([[88, 95, 70, 92, 88]])
    #X_test[-1]
    #y_test[-1]

