# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 09:54:33 2018

@author: Sony
"""

import os
import numpy as np
from nilearn import plotting, image
from skimage import data, io, filters, util, color
os.chdir(str(os.getcwd()))
xCrop = [30, 122, 175, 285, 345, 440]
yCrop = [50, 138, 50, 140, 45, 155]

def convertFile(inFile=None, outFile=None, cutCoords = (3, 3, 3), displayMode = 'ortho'):
    epiImage = image.mean_img(inFile)
    epiImage = image.smooth_img(epiImage, 'fast');
    plotting.plot_epi(epi_img=epiImage, cut_coords=cutCoords, output_file=outFile, display_mode=displayMode, annotate=False, draw_cross=False)



#inFile = r'C:\Users\Sony\Desktop\Programming\Test\sub-01_func_sub-01_task-letter0backtask_bold.nii'
#outFile = r'C:\Users\Sony\Desktop\Programming\Test\out1.jpg'
inFile = r'sub-01_func_sub-01_task-letter0backtask_bold.nii'
outFile = r'out3.jpg'   
convertFile (inFile, outFile, (3, 3, 3), displayMode = 'ortho')

brainImage = io.imread(outFile)
#brainImage = color.rgb2gray(brainImage)
frontalImage = brainImage[yCrop[0]:yCrop[1], xCrop[0]:xCrop[1]]
sideImage = brainImage[yCrop[2]:yCrop[3], xCrop[2]:xCrop[3]]
topImage = brainImage[yCrop[4]:yCrop[5], xCrop[4]:xCrop[5]]

np.savetxt("topImageR.csv", topImage[:,:,0], delimiter=',')
np.savetxt("topImageG.csv", topImage[:,:,1], delimiter=',')
np.savetxt("topImageB.csv", topImage[:,:,2], delimiter=',')
#30, 440px - crop x
#45, 155px - crop y
