import io
import numpy as np
from PIL import Image
import keras.models
from keras_preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input


MODEL_PATH="model/model.h5"
MODEL = keras.models.load_model(MODEL_PATH)


def preprocess_image(data):
    image = Image.open(io.BytesIO(data))
    image = image.resize((250, 250))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    return preprocess_input(image)


def model_predict(image) -> str:
    pred = MODEL.predict(image)
    pred = np.argmax(pred, axis=1)[0]
    labels = {0: 'fire', 1: 'no-fire'}
    pred = labels[pred]
    return pred
