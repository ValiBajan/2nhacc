# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 16:20:53 2018

@author: Sony
"""

import argparse
import os
import numpy as np
from nilearn import plotting, image
from skimage import data, io, filters, util, color
curDir = str(os.getcwd()) + '\\'

parser = argparse.ArgumentParser()
parser.add_argument('convert', type=str)
args = parser.parse_args()
niiFile = args.convert

xCrop = [30, 122, 175, 285, 345, 440]
yCrop = [50, 138, 50, 140, 45, 155]

def nii2jpg(inFile=None, outFile=None, cutCoords = (3, 3, 3), displayMode = 'ortho'):
    epiImage = image.mean_img(inFile)
    epiImage = image.smooth_img(epiImage, 'fast');
    plotting.plot_epi(epi_img=epiImage, cut_coords=cutCoords, output_file=outFile, display_mode=displayMode, annotate=False, draw_cross=False)

def splitAndConvert(inFile=None, outDir='', fileNumber='0', gray=True, xCrop=None, yCrop=None):
    brainImage = io.imread(inFile)
    if (gray):  
        brainImage = color.rgb2gray(brainImage)
        frontalImage = brainImage[yCrop[0]:yCrop[1], xCrop[0]:xCrop[1]]
        sideImage = brainImage[yCrop[2]:yCrop[3], xCrop[2]:xCrop[3]]
        topImage = brainImage[yCrop[4]:yCrop[5], xCrop[4]:xCrop[5]]
        np.savetxt(outDir + 'topImageGray' + fileNumber + '.csv', topImage, delimiter=',')
        np.savetxt(outDir + 'sideImageGray' + fileNumber + '.csv', sideImage, delimiter=',')
        np.savetxt(outDir + 'frontalImageGray' + fileNumber + '.csv', frontalImage, delimiter=',')
    else:
        frontalImage = brainImage[yCrop[0]:yCrop[1], xCrop[0]:xCrop[1]]
        sideImage = brainImage[yCrop[2]:yCrop[3], xCrop[2]:xCrop[3]]
        topImage = brainImage[yCrop[4]:yCrop[5], xCrop[4]:xCrop[5]]
        np.savetxt(outDir + 'topImageR' + fileNumber + '.csv', topImage[:,:,0], delimiter=',')
        np.savetxt(outDir + 'topImageG' + fileNumber + '.csv', topImage[:,:,1], delimiter=',')
        np.savetxt(outDir + 'topImageB' + fileNumber + '.csv', topImage[:,:,2], delimiter=',')
        np.savetxt(outDir + 'sideImageR' + fileNumber + '.csv', sideImage[:,:,0], delimiter=',')
        np.savetxt(outDir + 'sideImageG' + fileNumber + '.csv', sideImage[:,:,1], delimiter=',')
        np.savetxt(outDir + 'sideImageB' + fileNumber + '.csv', sideImage[:,:,2], delimiter=',')
        np.savetxt(outDir + 'frontalImageR' + fileNumber + '.csv', frontalImage[:,:,0], delimiter=',')
        np.savetxt(outDir + 'frontalImageG' + fileNumber + '.csv', frontalImage[:,:,1], delimiter=',')
        np.savetxt(outDir + 'frontalImageB' + fileNumber + '.csv', frontalImage[:,:,2], delimiter=',')
       

if __name__ == '__main__':
    if (os.path.isfile(niiFile)):
        nii2jpg(inFile=niiFile, outFile='{}brain.jpg'.format(curDir))
        splitAndConvert(inFile='{}brain.jpg'.format(curDir), outDir=curDir, fileNumber='', gray=True, xCrop=xCrop, yCrop=yCrop)
    else:
        print ('Incorrect file path')
    
    
#xCrop = [30, 122, 175, 285, 345, 440]
#yCrop = [50, 138, 50, 140, 45, 155]