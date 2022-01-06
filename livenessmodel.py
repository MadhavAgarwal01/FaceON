import numpy as np 
import keras
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling3D
from keras import backend as K

def get_liveness_model():

    model = Sequential()
    model.add(Conv3D(32, kernel_size=(3, 3, 3),
                    activation='relu',
                    input_shape=(24,100,100,1))) # takes as input a 3D volume or a sequence of 2D frames
    model.add(Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))# halve the size of the 3D input in each dimension
    model.add(Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))# halve the size of the 3D input in each dimension
    model.add(Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))# halve the size of the 3D input in each dimension

    model.add(Dropout(0.25)) # Dropout layer randomly sets input units to 0 which helps prevent overfitting
    model.add(Flatten()) # converting the data into a 1-dimensional array for inputting it to the next layer
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    return model
