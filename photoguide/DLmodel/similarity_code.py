#!/usr/bin/env python
# coding: utf-8

from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model
from keras.models import load_model
import numpy as np
import pandas as pd
from PIL import Image


class FeatureExtractor:
    def __init__(self):
        # Use VGG-16 as the architecture and ImageNet for the weight
        # Customize the model to return features from fully-connected layer
        model = load_model('./photoguide/DLmodel/autoencoder_model.h5')
        self.model = Model(inputs=model.input, outputs=model.get_layer('dense').output)
        
        


    def extract(self, img):
        # Resize the image
        img = img.resize((299, 299))
        # Convert the image color space
        img = img.convert('RGB')
        # Reformat the image
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Extract Features
        feature = self.model.predict(x)[0]
        return feature / np.linalg.norm(feature)



  

