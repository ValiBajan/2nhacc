# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 22:55:27 2018

@author: alin.manolache
"""
#import pywt
#import pywt.data
import keras

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
#import os
##
##dirPath = os.path.dirname(os.path.realpath(__file__))
#dirPath = 'C:\\Users\\alin.manolache\\Desktop\\Date'
##print(dirPath)
#os.chdir(dirPath)
##
### First col - Schizo
### Second col - Healthy
#trainLabel = np.zeros((115+203, 2))
#validateLabel = np.zeros((115+203, 2))
#trainData = np.zeros((123+65,108,94,1))
#validateData = np.zeros((,108,94,1))
#trainDataIndex = 0
#validateDataIndex = 0

#for file in os.listdir('Schizo'):
#    if (file.endswith('.csv')):
#        img = pd.read_csv('Schizo\\{}'.format(file))
#        img = img.values;
#        img=img[0:108,0:94]
#        img_r = img.reshape((108,94,1))
#        data[curDataIndex] = img_r
#        label[curDataIndex,0] = 1
#        curDataIndex += 1
#        
#for file in os.listdir('Healthy'):
#    if (file.endswith('.csv')):
#        img = pd.read_csv('Healthy\\{}'.format(file))
#        img = img.values;
#        img=img[0:108,0:94]
#        img_r = img.reshape((108,94,1))
#        data[curDataIndex] = img_r
#        label[curDataIndex,1] = 1
#        curDataIndex += 1
        
#for file in os.listdir('Schizo\\Train'):
#    if (file.endswith('.csv')):
#        img = pd.read_csv('Schizo\\{}'.format(file))
#        img = img.values;
#        img=img[0:108,0:94]
#        img_r = img.reshape((108,94,1))
#        dataTrain[curDataIndex] = img_r
#        trainLabel[curDataIndex] = 1
#        trainDataIndex += 1
#        
#for file in os.listdir('Healthy'):
#    if (file.endswith('.csv')):
#        img = pd.read_csv('Healthy\\{}'.format(file))
#        img = img.values;
#        img=img[0:108,0:94]
#        img_r = img.reshape((108,94,1))
#        data[curDataIndex] = img_r
#        label[curDataIndex,1] = 1
#        curDataIndex += 1



# (1) Importing dependency
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten,\
 Conv2D, MaxPooling2D
from keras.layers.normalization import BatchNormalization

#np.random.seed(1000)

# (2) Get Data
#import tflearn.datasets.oxflower17 as oxflower17
#x, y = oxflower17.load_data(one_hot=True)
#XX=data
#YY=label
#DATA=np.load(str(os.getcwd()) + '\\DATA.npy')
# (3) Create a sequential model
model = Sequential()

# 1st Convolutional Layer
model.add(Conv2D(filters=96, input_shape=(108,94,1), kernel_size=(3,3),\
  padding='same'))
model.add(Activation('relu'))
# Pooling
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='same'))
# Batch Normalisation before passing it to the next layer
model.add(BatchNormalization())

# 2nd Convolutional Layer
model.add(Conv2D(filters=256, kernel_size=(3,3), padding='same'))
model.add(Activation('relu'))
# Pooling
model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='same'))
# Batch Normalisation
model.add(BatchNormalization())

# 3rd Convolutional Layer
#model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='valid'))
#model.add(Activation('relu'))
# Batch Normalisation
#model.add(BatchNormalization())

# 4th Convolutional Layer
#model.add(Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), padding='valid'))
#model.add(Activation('relu'))
# Batch Normalisation
#model.add(BatchNormalization())

# 5th Convolutional Layer
#model.add(Conv2D(filters=256, kernel_size=(3,3), strides=(1,1), padding='valid'))
#model.add(Activation('relu'))
# Pooling
#model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2), padding='valid'))
# Batch Normalisation
#model.add(BatchNormalization())

# Passing it to a dense layer
model.add(Flatten())
# 1st Dense Layer
#model.add(Dense(4096, input_shape=(224*224*3,)))
#model.add(Activation('relu'))
# Add Dropout to prevent overfitting
#model.add(Dropout(0.4))
# Batch Normalisation
#model.add(BatchNormalization())

# 2nd Dense Layer
#model.add(Dense(256))
#model.add(Activation('relu'))
# Add Dropout
#model.add(Dropout(0.4))
# Batch Normalisation
#model.add(BatchNormalization())

# 3rd Dense Layer
model.add(Dense(64))
model.add(Activation('relu'))
# Add Dropout
model.add(Dropout(0.4))
# Batch Normalisation
model.add(BatchNormalization())

# Output Layer
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.summary()

# (4) Compile
model.compile(loss='binary_crossentropy', optimizer='adam',\
 metrics=['accuracy'])

# (5) Train
model.fit(data, label[:,0], batch_size=6, epochs=50, verbose=1, \
validation_split=0.2, shuffle=True)


#model.save('new_model')

#y_predictt=model.predict(data)
