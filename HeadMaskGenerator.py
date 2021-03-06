

# # import Dependencies
import sys
import os
from os import path

import matplotlib.pyplot as plt
import numpy as np
import warnings

sys.path.append(path.abspath('./util'))

from AnDiffusion import *
from MaskGenAlgo import *
from tqdm import tqdm
from hysteresisThresholding import apply_hysteresis_threshold
from time import sleep
from skimage.morphology import erosion, dilation, opening, closing, white_tophat
from skimage.morphology import disk
from ImageFinder import *
from scipy.stats import norm
from scipy.ndimage.morphology import binary_fill_holes


#print("Enter image folder path: ")
#Ipath = input()
#print("Enter path where to save the results: ")
#Spath = input()

#Dicom location
Ipath  = "./sample_mri_image(DICOM)/"
Spath  = "./OutputImg/"

print("Loading images .......... ")
l = filelocation(Ipath)
[orgImge,nofimage] =  LoadOrginalImage(l)
print("Done! no of images: " + str(nofimage))


print("Apply pipeline for generate masks.....")

mask   = np.zeros((512,512,nofimage))
fgnd   = np.zeros((512,512,nofimage))
actImg = np.zeros((512,512,nofimage))
selem  = disk(4)
for i in tqdm(range(nofimage)):
    img             = orgImge[:,:,i]
    diff            = anisodiff(img,20,50,0.1)
    mu,sigma        = norm.fit(diff)
    htr             = apply_hysteresis_threshold(diff,mu,sigma).astype(int)
    pmask           = binary_fill_holes(htr)
    eroded          = erosion(pmask, selem)
    [fg,bg]         = foregroundBackground(eroded,img)
    mask[:,:,i]     = eroded
    fgnd[:,:,i]     = fg
    actImg[:,:,i]   = img
    sleep(0.1)


print("save all generate image in a folder.... ")

dictr = Spath
for i in tqdm(range(nofimage)):
    x=l[i].split("/")
    loc1=dictr+x[-1]+'.png'
    loc2=dictr+x[-1]+'fg'+'.png'
    loc3=dictr+x[-1]+'actImg'+'.png'
    plt.imsave(loc1,mask[:,:,i],cmap = plt.cm.gray) # save psudo mask
    plt.imsave(loc2,fgnd[:,:,i],cmap = plt.cm.gray)
    plt.imsave(loc3,actImg[:,:,i],cmap = plt.cm.gray)


print("Done! ")

