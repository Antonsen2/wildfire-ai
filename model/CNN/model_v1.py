"""Initial CNN model used in research phase of the project"""


import os

import cv2
import keras
import pickle

import numpy as np
import tensorflow as tf

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split


def load_images_from_folder(folder: str) -> list:
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None:
            images.append(img)
    return images


def cnn(fire_path: str, forest_path: str) -> None:
    fire_images = load_images_from_folder(fire_path)
    forest_images = load_images_from_folder(forest_path)

    images = fire_images + forest_images

    x_list = np.array(images)
    y_list = [0] * 500
    forest = [1] * 500
    y_list.extend(forest)
    y_list = np.array(y_list)


    x_train, x_test, y_train, y_test = train_test_split(
        x_list, y_list, random_state=104, test_size=0.25, shuffle=True
    )
    x_train, x_val, y_train, y_val = train_test_split(
        x_train, y_train, random_state=104, test_size=0.1, shuffle=True
    )

    # Create the model
    model = Sequential()

    # Add convolutional layers
    model.add(Conv2D(64, (3, 3), activation='relu', input_shape=(250, 250, 3)))
    model.add(Conv2D(128, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # Add a flattening layer
    model.add(Flatten())

    # Add dense layers
    model.add(Dense(128, activation='relu'))
    model.add(Dense(1, activation='softmax'))

    # Compile the model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(x_train, y_train, batch_size=25, epochs=5, validation_data=(x_val, y_val))

    # Evaluate the model
    model.evaluate(x_test, y_test)

    filename = 'CNN50accuracy.sav'
    pickle.dump(model, open(filename, 'wb'))


if __name__ == '__main__':
    cnn(
        fire_path="c:/code/applied-ai/data/root/datasets/50-50/fire",
        forest_path="c:/code/applied-ai/data/root/datasets/50-50/no-fire"
    )