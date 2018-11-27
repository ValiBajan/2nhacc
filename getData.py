# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 10:30:52 2018

@author: alin.manolache
"""

import numpy as np
import pandas as pd
import os

dirPath = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirPath)

img1 = pd.read_csv('Healthy\\topImageGray10_crop.csv')
img2 = pd.read_csv('Healthy\\topImageGray10_blur.csv')
img3 = pd.read_csv('Healthy\\topImageGray15_all.csv')

# First col - Schizo
# Second col - Healthy
label = np.zeros((115+203, 2))
data = np.zeros((115+203,108,95,1))
curDataIndex = 0

for file in os.listdir('Schizo'):
    if (file.endswith('.csv')):
        img = pd.read_csv('Schizo\\{}'.format(file))
        img = img.values;
        img=img[0:108,:]
        img_r = img.reshape((108,95,1))
        data[curDataIndex] = img_r
        label[curDataIndex,0] = 1
        curDataIndex += 1
        
for file in os.listdir('Healthy'):
    if (file.endswith('.csv')):
        img = pd.read_csv('Healthy\\{}'.format(file))
        img = img.values;
        img=img[0:108,:]
        img_r = img.reshape((108,95,1))
        data[curDataIndex] = img_r
        label[curDataIndex,1] = 1
        curDataIndex += 1
        
#for file in os.listdir('Schizo'):
    #if (file.endswith('.csv') ):
    #    img = pd.read_csv('Schizo\\{}'.format(file))
#img1=img1.values
#img1=img1[0:108, :]
#img1_r = img1.reshape((1,108,95,1))

#img1=img1.values
#img1=img1[0:108, :]
#img2=img2.values
#img2=img2[0:108, :]
#img3=img3.values
#img3=img3[0:108, :]
#img2_r = img2.reshape((1,108,95,1))

#imgRes = np.concatenate((img1_r, img2_r), 0)

#img222 = data[1][:][:][:].reshape((108,95))

  
import matplotlib.pyplot as plt
#import random
#from imgaug import augmenters as iaa
#import matplotlib.image as mpimg
#img=mpimg.imread('your_image.png')
#seq3 = iaa.Sequential([
#iaa.Crop(px=(0, 1)), # crop images from each side by 0 to 16px (randomly chosen)
#iaa.Fliplr(0.1), # horizontally flip 50% of the images
#iaa.GaussianBlur(sigma=(0, 1.0)), # blur images with a sigma of 0 to 3.0
#iaa.Affine(translate_px={"x":int(random.uniform(-3, 3))}),
#iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5)   
#],random_order=True)
#img3 = img3.reshape((108,95,1))
#img_aug3 = seq3.augment_image(img3)
#img3 = img_aug3.reshape((108,95))
img = data[316].reshape(108,95)
imgplot = plt.imshow(img)

plt.show()
