# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 13:17:52 2018

@author: alin.manolache
"""
from keras.models import load_model
import numpy as np
import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

def readCSV(csv_loc):
    csv = pd.read_csv(csv_loc)
    csv = csv.values
    csv = csv[0:108,0:94]
    csv_r = csv.reshape((1,108,94,1))
    return csv_r

def analyze(csv_loc):
    img_r=readCSV(csv_loc)
    model = load_model('model_test')
    y_predict=model.predict(img_r)
    return y_predict[0][0] * 100
