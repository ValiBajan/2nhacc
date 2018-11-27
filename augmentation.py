# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 18:41:53 2018

@author: alin.manolache
"""
import os
import numpy as np
from imgaug import augmenters as iaa
import pandas as pd
import random

dirPath = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirPath)

for file in os.listdir('Healthy'):
    if (file.endswith('.csv') and len(file) <= 18):
        img = pd.read_csv('Healthy\\{}'.format(file))
        img=img.values;
        seq1 = iaa.Sequential([
        iaa.Crop(px=(0, 1)), # crop images from each side by 0 to 16px (randomly chosen)
        #iaa.Fliplr(0.1), # horizontally flip 50% of the images
        #iaa.GaussianBlur(sigma=(0, 1.0)), # blur images with a sigma of 0 to 3.0
        #iaa.Affine(translate_px={"x":-40}),
        #iaa.AdditiveGaussianNoise(scale=0.1*255)   
        ],random_order=True)
        seq2 = iaa.Sequential([
        #iaa.Crop(px=(0, 1)), # crop images from each side by 0 to 16px (randomly chosen)
        #iaa.Fliplr(0.1), # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 1.0)), # blur images with a sigma of 0 to 3.0
        #iaa.Affine(translate_px={"x":-40}),
        #iaa.AdditiveGaussianNoise(scale=0.1*255)   
        ],random_order=True)
        seq3 = iaa.Sequential([
        #iaa.Crop(px=(0, 1)), # crop images from each side by 0 to 16px (randomly chosen)
        #iaa.Fliplr(0.1), # horizontally flip 50% of the images
        #iaa.GaussianBlur(sigma=(0, 1.0)), # blur images with a sigma of 0 to 3.0
        iaa.Affine(translate_px={"x":int(random.uniform(-3, 3))}),
        #iaa.AdditiveGaussianNoise(scale=0.1*255)   
        ],random_order=True)
        seq4 = iaa.Sequential([
        iaa.Crop(px=(0, 1)), # crop images from each side by 0 to 16px (randomly chosen)
        #iaa.Fliplr(0.1), # horizontally flip 50% of the images
        iaa.GaussianBlur(sigma=(0, 1.0)), # blur images with a sigma of 0 to 3.0
        iaa.Affine(translate_px={"x":int(random.uniform(-3, 3))}),
        #iaa.AdditiveGaussianNoise(scale=0.1*255)   
        ],random_order=True)
        img1 = img.reshape((109,95,1))
        img2 = img.reshape((109,95,1))
        img3 = img.reshape((109,95,1))
        img4 = img.reshape((109,95,1))
        img_aug1 = seq1.augment_image(img1)  # done by the library
        img_aug2 = seq2.augment_image(img2)
        img_aug3 = seq3.augment_image(img3)
        img_aug4 = seq3.augment_image(img4)
        img1 = img_aug1.reshape((109,95))
        img2 = img_aug2.reshape((109,95))
        img3 = img_aug3.reshape((109,95))
        img4 = img_aug4.reshape((109,95))
        # train_on_images(images_aug)  # you have to implement this function
        np.savetxt('Healthy\\{}_crop.csv'.format(file[0:-4]), img1, delimiter=",")
        np.savetxt('Healthy\\{}_blur.csv'.format(file[0:-4]), img2, delimiter=",")
        np.savetxt('Healthy\\{}_noise.csv'.format(file[0:-4]), img3, delimiter=",")
        np.savetxt('Healthy\\{}_all.csv'.format(file[0:-4]), img4, delimiter=",")
        
#seq=iaa.SomeOf(2,[
        #iaa.Affine(rotate=1.2),
        #iaa.AdditiveGaussianNoise(scale=0.1*255),
        #iaa.Add(20, per_channel=True),
 #       iaa.Sharpen(alpha=0.1)
  #      ])


#for batch_idx in range(1000):
    # 'images' should be either a 4D numpy array of shape (N, height, width, channels)
    # or a list of 3D numpy arrays, each having shape (height, width, channels).
    # Grayscale images must have shape (height, width, 1) each.
    # All images must have numpy's dtype uint8. Values are expected to be in
    # range 0-255.
#images = load_batch(batch_idx)  # you have to implement this function
#img1 = np.expand_dims(img, axis=2)
#img1 = img.reshape((109,95,1))
#images_aug = seq.augment_images(img1)  # done by the library
   # train_on_images(images_aug)  # you have to implement this function
#img2 = images_aug.reshape((109,95))

  
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
#img=mpimg.imread('your_image.png')
#imgplot = plt.imshow(img2)

plt.show()