# -*- coding: utf-8 -*-

import os
from nilearn import image, masking, plotting
from skimage import io, morphology, color, measure, segmentation, filters, util
import numpy as np

def nii2png(niiPath=None, imgPath=None, axis='z', cut=(0,), blackBg='auto', mask=True, maskThresh=0.8, maskConnected=True, maskOpening=3, verbose=0):
    if (os.path.isfile(niiPath) and os.path.splitext[1] == '.nii'):
        if (os.path.isdir(os.path.dirname(imgPath)) and not os.path.isdir(imgPath) and os.path.splitext[1] == '.png'):
            imgMask = None
            brainImg = image.load_img(niiPath)
            if (mask):
                imgMask = masking.compute_gray_matter_mask(brainImg, threshold=maskThresh, connected=maskConnected, opening=maskOpening, verbose=verbose)
                brainImg = image.math_img('img1 * img2', img1=brainImg, img2=imgMask)
            if (verbose > 0):
                print('Outputing image at {}...'.format(imgPath))
            plotting.plot_anat(anat_img=niiPath, display_mode=axis, output_file=imgPath.format(dataDir), cut_coords=cut, annotate=False, draw_cross=False, black_bg=blackBg)
        elif (not os.path.isdir(os.path.dirname(imgPath))):
            print('{} is an invalid directory!!!'.format(os.path.dirname(imgPath)))
        elif (os.path.isdir(imgPath)):
            print('{} is a directory, not a valid file path!!!'.format(imgPath))
        elif (not os.path.splitext[1] == '.png'):
            print('{} is not a .png file!!!'.format(os.path.split(imgPath)[1]))
    elif (not os.path.isfile(niiPath)):
        print('{} is not a valid path!!!'.format(niiPath))
    elif (not os.path.splitext(niiPath)[1] == '.nii'):
        print('{} is not a .nii file!!!'.format(os.path.split(niiPath)[1]))
            

def hysteresis(imgPath=None, lowThresh=0.2, highThresh=0.24, verbose=0):
    if (os.path.isfile(imgPath) and os.path.splitext(imgPath)[1] == '.png'):
        img = io.imread(imgPath)
        img = color.rgb2gray
        if (verbose > 0):
            print('Applying hysterisis filter...\n')
        res = filters.apply_hysteresis_threshold(img, lowThresh, highThresh)
        if (verbose > 1):
            print('Filtered image:')
            io.imshow(res)
        return res
    elif (not os.path.isfile(imgPath)):
        print('{} is not a valid path!!!'.format(imgPath))
    elif (not os.path.splitext(imgPath)[1] == '.png'):
        print('{} is not a .png file!!!'.format(os.path.split(imgPath)[1]))
    return None

if __name__ == '__main__':
    scriptsDir = os.path.dirname(os.path.realpath(__file__))
    mainDir = os.path.dirname(scriptsDir)
    datasetDir = '{}\\Dataset'.format(mainDir)
    dataDir = '{}\\Data'.format(mainDir)
    plotting.plot_anat()

    funcPath = '{}\\sub-01_func_sub-01_task-letter0backtask_bold.nii'.format(datasetDir)
    anatPath = '{}\\sub-01_anat_sub-01_T1w.nii'.format(datasetDir)
    #maskImg = masking.compute_gray_matter_mask(anatPath, threshold=0.8, connected=True, opening=3, verbose=1)
    #maskImg = masking.compute_background_mask(anatPath, verbose=2)
    #maskImg = masking.compute_epi_mask(funcPath)
    #brainImg = image.clean_img(funcPath, high_pass=0.009, standardize=True, t_r=2.5, mask_img=maskImg)
    #brainImg = image.mean_img(funcPath, verbose=2, n_jobs=-1)
    #brainImg = image.smooth_img(brainImg, fwhm='fast')
    #brainImg = image.math_img('img1 * img2', img1=brainImg, img2=maskImg)
    #brainImg = image.math_img('img1 * img2', img1=anatPath, img2=maskImg)

    #view = plotting.view_img(stat_map_img=brainImg, bg_img=None, threshold=None)
    #view.open_in_browser()
    #brainImg = image.load_img(anatPath)
    #cutSlices = plotting.find_cut_slices(brainImg, n_cuts=1)
    #plotting.plot_anat(brainImg, display_mode='z', output_file='{}\\test.png'.format(dataDir), cut_coords=(5,), annotate=False, draw_cross=False)
    testImg = r'{}\\test.png'.format(dataDir)
    img = io.imread(testImg)
    img = color.rgb2gray(img)
    #img = util.invert(img)
    #io.imshow(img)
    #res = morphology.thin(img, 1000)
    startPos = np.array([img.shape[0]/2.0, img.shape[1]/2.0, img.shape[0]/3.0, img.shape[1]/2.0, img.shape[0]*(2.0/3.0), img.shape[1]/2.0])
    startPos = np.reshape(startPos, (3, 2))
    #res = segmentation.active_contour(image=img, snake=startPos)
    #res = filters.frangi(img, scale_range=(1, 2), scale_step=0.25, beta1=1, beta2=15)
    res = filters.apply_hysteresis_threshold(img, 0.2, 0.24)
    io.imshow(res)
    
    
    
