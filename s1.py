#TODO: Read the image as a series of slices for all formats : .czi, .nrrd, .tif, .svs and display all details
#DONE: Split channels and save each file independently.
#DONE: create a folder for saving the respective images into separate folders
#DONE: save the respective images into the folders
#DONE: Read the images from each directory using pims
#DONE: or just load an image sequence with the regex expression for loading the image
#TODO: check voxel depth and set voxel depth to 1
#DONE: check Image type or PixelIDType and set it to 8 bit integer type
#TODO: Rotate image
#TODO: Save after processing as both .nrrd and .tiff in respective folders along with original


import os
import re
import shutil
from pims import ImageSequence
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
#import SimpleITK as sitk

source_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/'
dest_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/ref'
dest_path1 = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/sig'

def imread_convert(f):
    return plt.imread(f).astype(np.uint8)

#Check if each file belongs to Ch00 or Ch01 and split Channels( move files to respective location
ref_counter = sig_counter = 0
for file in os.listdir(source_path):
    #print(file)
    if re.search("_ch0{2}", str(file)):
        ref_counter += 1
        #print(f"ref_counter= {ref_counter}")
        #print("ref file:", file)
        shutil.copy(f"{source_path}/{file}", dest_path)
    elif re.search("_ch01{1}", str(file)):
        sig_counter +=1
        #print(f"sig_counter = {sig_counter}")
        #print(f"sig file:{file}")
        shutil.copy(f"{source_path}/{file}", dest_path1)
    else:
        print("Its a Folder. Unwanted/Unrecognized file format.")

#Load images sequentially as per respective channels using pims ImageSequence
#ref_image = ImageSequence(dest_path + '/*.tif')
#print(f'The ref_image details: {len(ref_image)} frames with dimensions of {ref_image.frame_shape}')
#sig_image = ImageSequence(dest_path1 + '/*.tif')
#print(f'The sig_image details: {len(sig_image)} frames with dimensions of {sig_image.frame_shape}')

#Load images sequentially as per respective channels using skimage imageCollection
#ref_image = io.ImageCollection(dest_path + '/*.tif', load_func=imread_convert)
ref_image = io.ImageCollection(dest_path + '/*.tif')
print(f'The ref_image details: {len(ref_image)} frames')
sig_image = io.ImageCollection(dest_path1 + '/*.tif')
print(f'The sig_image details: {len(sig_image)} frames')

#Convert these image collection object (sequential images) into a single image
rimage = io.concatenate_images(ref_image)# rimage is a np.array
print(f"The rimage has dimensions : {rimage.shape}")
simage = io.concatenate_images(sig_image)
print(f"The simage has dimensions : {simage.shape}")