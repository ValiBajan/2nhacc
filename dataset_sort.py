# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 09:54:33 2018

@author: Sony
"""

import os
import csv
import numpy as np
from nilearn import plotting, image
from skimage import data, io, filters, util, color
dirPath = os.path.dirname(os.path.realpath(__file__))
os.chdir(dirPath)
xCrop = [30, 122, 175, 285, 345, 440]
yCrop = [50, 138, 50, 140, 45, 155]
niiFile = r'sub-01_func_sub-01_task-letter0backtask_bold.nii'
jpgFile = r'out.jpg'
participantsFile = r'participants.tsv'

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
        
def processDataset(healthyDir='Healthy', schizoDir='Schizo'):
    healthySubjects = []
    schizoSubjects = []
    with open(participantsFile) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter="\t")
        for line in tsvreader:
            if (line[1] == 'SCZ'):
                schizoSubjects.append(line[0])
            elif (line[1] == 'CON' or line[1] == 'CON-SIB'):
                healthySubjects.append(line[0])
    for subject in healthySubjects:
        #funcFile = r'{}_func_{}_task-letter0backtask_bold.nii'.format(subject, subject, subject)
        funcFile = '{}_func_{}_task-letter0backtask_bold.nii'.format(subject, subject)
        #print(str(os.getcwd())+ '\\' + '{}\\'.format(healthyDir))
        nii2jpg(inFile = funcFile, outFile = '{}\\{}.jpg'.format(healthyDir, subject))
        splitAndConvert(inFile='{}\\{}.jpg'.format(healthyDir, subject), outDir='{}\\'.format(healthyDir), fileNumber=subject[4:], gray=True, xCrop=xCrop, yCrop=yCrop)
    for subject in schizoSubjects:
        #funcFile = r'{}\\func\\{}_func_{}_task-letter0backtask_bold.nii'.format(subject, subject, subject)
        funcFile = '{}_func_{}_task-letter0backtask_bold.nii'.format(subject, subject)
        #print(str(os.getcwd())+ '\\' + '{}\\'.format(schizoDir))
        nii2jpg(inFile = funcFile, outFile = '{}\{}.jpg'.format(schizoDir, subject))
        splitAndConvert(inFile='{}\\{}.jpg'.format(schizoDir, subject), outDir='{}\\'.format(schizoDir), fileNumber=subject[4:], gray=True, xCrop=xCrop, yCrop=yCrop)       
    
processDataset()    
