# -*- coding: utf-8 -*-

import os
from nilearn import image, masking, plotting
from skimage import io, morphology, color, measure, filters, util, transform, segmentation
import numpy as np
import matplotlib.pyplot as plt

def nii2png(niiPath=None, imgPath=None, axis='z', cut=(0,), blackBg='auto', mask=1, maskThresh=0.5, maskConnected=True, maskOpening=3, verbose=0):
    """
    Takes a .nii file and converts it to a .png file containing one or multiple slices of the brain arranged horizontally
    Arguments:
    niiPath -> the .nii filepath (relative or absolute)
    imgPath -> the filepath of the output image (must end in .png)
    axis (optional, default='z') -> 'xyz' 'xy' 'xz' 'yz' 'x' 'y' 'z' - determines the axis along which the cuts are made
    cut (optional, default=(0,)) -> list of tuples of 1, 2 or 3 integers - determines the x, y, z position along which the cuts are made
    blackBg (optional, default='auto')
    mask (optional, default=1) -> int between 0 and 3 - determines the ammount of times a gray matter mask will be applied
    maskThresh (optional, default=0.8) -> float between 0 and 1 - determines the threshold used for the gray matter mask
    maskConnected (optional, default=True) -> bool - determines if the mask will keep only the largest connected components
    maskOpening (optional, default=3)
    verbose (optional, default=0) -> int - the higher it is, the more messages will be outputted to the console
    """
    # Checks if the input filepath exists and has a .nii extension
    if (os.path.isfile(niiPath) and os.path.splitext(niiPath)[1] == '.nii'):
        # Checks if the output filepath's directory is valid, if it is not a directory itself and if it has a .png extension
        if (os.path.isdir(os.path.dirname(imgPath)) and not os.path.isdir(imgPath) and os.path.splitext(imgPath)[1] == '.png'):
            imgMask = None
            brainImg = image.load_img(niiPath)
            # Clamps mask between 0 and 3
            mask = min(3, max(0, mask))
            # Applies the mask
            for i in range(0, mask):
                imgMask = masking.compute_gray_matter_mask(brainImg, threshold=maskThresh, connected=maskConnected, opening=maskOpening, verbose=verbose)
                brainImg = image.math_img('img1 * img2', img1=brainImg, img2=imgMask)
            if (verbose > 0):
                print('Outputing image at {}...'.format(imgPath))
            plotting.plot_anat(anat_img=brainImg, display_mode=axis, output_file=imgPath.format(dataDir), cut_coords=cut, annotate=False, draw_cross=False, black_bg=blackBg)
        elif (not os.path.isdir(os.path.dirname(imgPath))):
            print('{} is an invalid directory!!!'.format(os.path.dirname(imgPath)))
        elif (os.path.isdir(imgPath)):
            print('{} is a directory, not a valid file path!!!'.format(imgPath))
        elif (not os.path.splitext(imgPath)[1] == '.png'):
            print('{} is not a .png file!!!'.format(os.path.split(imgPath)[1]))
    elif (not os.path.isfile(niiPath)):
        print('{} is not a valid path!!!'.format(niiPath))
    elif (not os.path.splitext(niiPath)[1] == '.nii'):
        print('{} is not a .nii file!!!'.format(os.path.split(niiPath)[1]))
            
def plotComparison(original, filtered, filterName):
    """
    Plots 2 images side by side in the console
    """
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 4), sharex=True,
                                   sharey=True)
    ax1.imshow(original, cmap=plt.cm.gray)
    ax1.set_title('Original')
    ax1.axis('off')
    ax2.imshow(filtered, cmap=plt.cm.gray)
    ax2.set_title(filterName)
    ax2.axis('off')

def getLargestCC(segment):
    """
    Gets the largest connected component of an image
    Used to filter out the skull after thinning
    """
    labels = measure.label(segment, 8, connectivity=3)
    largestCC = labels == (np.argmax(np.bincount(labels.flatten())[1:]) + 1)
    return largestCC

def fractalDimension(img, threshold=0.9):
    """
    Gets the fractal dimension of an image
    """
    # Only for 2d image
    assert(len(img.shape) == 2)
    # From https://github.com/rougier/numpy-100 (#87)
    def boxcount(img, k):
        S = np.add.reduceat(
            np.add.reduceat(img, np.arange(0, img.shape[0], k), axis=0),
                               np.arange(0, img.shape[1], k), axis=1)

        # We count non-empty (0) and non-full boxes (k*k)
        return len(np.where((S > 0) & (S < k*k))[0])
    # Transform img into a binary array
    img = (img > threshold)
    # Minimal dimension of img
    p = min(img.shape)
    # Greatest power of 2 less than or equal to p
    n = 2**np.floor(np.log(p)/np.log(2))
    # Extract the exponent
    n = int(np.log(n)/np.log(2))
    # Build successive box sizes (from 2**n down to 2**1)
    sizes = 2**np.arange(n, 1, -1)
    # Actual box counting with decreasing size
    counts = []
    for size in sizes:
        counts.append(boxcount(img, size))
    # Fit the successive log(sizes) with log(counts)
    coeffs = np.polyfit(np.log(sizes), np.log(counts), 1)
    return -coeffs[0]

def preprocess(imgPath=None, lowThresh=0.21, highThresh=0.27, verbose=0, rotations=4, crop=(15, 143, 30, 158)):
    if (os.path.isfile(imgPath) and os.path.splitext(imgPath)[1] == '.png'):
        img = io.imread(imgPath)
        img = color.rgb2gray(img)
        img = img[crop[2]:crop[3], crop[0]:crop[1]]
        if (verbose > 0):
            print('Applying hysterisis filter...\n')
        #res = segmentation.chan_vese(img)
        res = filters.apply_hysteresis_threshold(img, lowThresh, highThresh)
        
        #res = res > 2
        #res = segmentation.find_boundaries(res, mode='inner')
        res = morphology.skeletonize(res)
        res = getLargestCC(res)
        #res = measure.label(res, 8, connectivity=3)
        #res = res.flat
        #print(np.argmax(np.bincount(res.flat)) + 1)
        #res = res == 1
        angle = 360.0 / rotations
        dimension = 0
        for i in range(0, rotations):
            res = transform.rotate(res, angle, order=0, preserve_range=True)
            dimension += fractalDimension(res, 0.5)
        dimension /= rotations
        res = res.astype(int)
        #print("Minkowski–Bouligand dimension: ", dimension)
        if (verbose > 1):
            print('Filtered image:')
            plotComparison(img, res, 'M-B dimension: {0:.5f}'.format(dimension))
        return res
    elif (not os.path.isfile(imgPath)):
        print('{} is not a valid path!!!'.format(imgPath))
    elif (not os.path.splitext(imgPath)[1] == '.png'):
        print('{} is not a .png file!!!'.format(os.path.split(imgPath)[1]))
    return None

def preprocess3d(imgPaths=None, lowThresh=0.19, highThresh=0.26, verbose=0, keepLargest=True, crop=(15, 143, 30, 158)):
    xSize = crop[3] - crop[2]
    ySize = crop[1] - crop[0]
    results = np.empty((len(imgPaths), xSize, ySize), dtype=np.int8)
    i = 0
    for imgPath in imgPaths:
        if (os.path.isfile(imgPath) and os.path.splitext(imgPath)[1] == '.png'):
            img = io.imread(imgPath)
            img = color.rgb2gray(img)
            img = img[crop[2]:crop[3], crop[0]:crop[1]]
            if (verbose > 0):
                print('Applying hysterisis filter...\n')
            img = filters.apply_hysteresis_threshold(img, lowThresh, highThresh)
            results[i] = img
            i += 1
        elif (not os.path.isfile(imgPath)):
            print('{} is not a valid path!!!'.format(imgPath))
            return None
        elif (not os.path.splitext(imgPath)[1] == '.png'):
            print('{} is not a .png file!!!'.format(os.path.split(imgPath)[1]))
            return None
    results = morphology.skeletonize_3d(results)
    if (keepLargest):
        i = 0
        for img in results:
            img = getLargestCC(img)
            results[i] = img
            i += 1
    return results

if __name__ == '__main__':
    scriptsDir = os.path.dirname(os.path.realpath(__file__))
    mainDir = os.path.dirname(scriptsDir)
    datasetDir = '{}\\Dataset'.format(mainDir)
    dataDir = '{}\\Data'.format(mainDir)
    funcPath = '{}\\sub-01_func_sub-01_task-letter0backtask_bold.nii'.format(datasetDir)
    anatPath = '{}\\sub-01_anat_sub-01_T1w.nii'.format(datasetDir)
    
    #nii2png(anatPath, '{}\\test.png'.format(dataDir), cut=(0,), verbose=2, mask=1, maskThresh=0.1, maskConnected=True, maskOpening=3)
#    for x in range(12, 27):
#        for y in range(12, 27):
#            if (x < y):
#                preprocess('{}\\test.png'.format(dataDir), lowThresh=x/100.0, highThresh=y/100.0, verbose=2)
    #res = preprocess('{}\\test.png'.format(dataDir), lowThresh=0.21, highThresh=0.27, verbose=2)
#    imgPaths = []
    for i in range(-5, 6):
#        imgPath = '{}\\test{}.png'.format(dataDir, i)
#        imgPaths.append(imgPath)
        #nii2png(anatPath, '{}\\test{}.png'.format(dataDir, i), cut=(i,), verbose=2, mask=1, maskThresh=0.1, maskConnected=True, maskOpening=3)
        preprocess('{}\\test{}.png'.format(dataDir, i), lowThresh=0.19, highThresh=0.26, verbose=2)
    #res = preprocess('{}\\test{}.png'.format(dataDir, -5), lowThresh=0.19, highThresh=0.26, verbose=2)
#    res = preprocess3d(imgPaths, keepLargest=False)
#    crop=(15, 143, 30, 158)
#
#    for i in range(-5, 6):
#        img = io.imread('{}\\test{}.png'.format(dataDir, i))
#        img = color.rgb2gray(img)
#        img = img[crop[2]:crop[3], crop[0]:crop[1]]
#        plotComparison(img, res[i+5], 'Slice ' + str(i))
    
    