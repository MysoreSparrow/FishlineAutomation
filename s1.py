#############################################################
# * Image Processing Script to process fish lines @ Baier Lab
# Author: Keshav Prasad Gubbi

#DONE: Read the image as a series of slices for all formats : .czi, .nrrd, .tif, .svs and display all details
#DONE: Split channels and save each file independently.
#DONE: create a folder for saving the respective images into separate folders
#DONE: save the respective images into the folders
#DONE: Read the images from each directory using pims
#DONE: or just load an image sequence with the regex expression for loading the image
#DONE: check voxel depth and set voxel depth to 1
#DONE: check Image type or PixelIDType and set it to 8 bit integer type
#TODO: Enhance Contrast of the image
#TODO: Rotate image
#TODO: Save after processing as both .nrrd and .tiff in respective folders along with original


import os
import re
import shutil
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import imageio
import SimpleITK as sitk
import cv2
import time

start = time.time()
source_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/'
dest_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/ref'
dest_path1 = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/sig'
data_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/'


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
        sig_counter += 1
        #print(f"sig_counter = {sig_counter}")
        #print(f"sig file:{file}")
        shutil.copy(f"{source_path}/{file}", dest_path1)
    else:
        print("Its a Folder. Unwanted/Unrecognized file format.")

#Load images sequentially as per respective channels using skimage imageCollection
#ref_image = io.ImageCollection(dest_path + '/*.tif', load_func=imread_convert)
ref_image_collection = io.ImageCollection(dest_path + '/*.tif')
print(f'The ref_image_collection details: {len(ref_image_collection)} frames')
sig_image_collection = io.ImageCollection(dest_path1 + '/*.tif')
print(f'The sig_image_collection details: {len(sig_image_collection)} frames')

#Convert these image collection object (sequential images) into a single image
ref_image = io.concatenate_images(ref_image_collection)
print(f"The ref_image has dimensions : {ref_image.shape}")
sig_image = io.concatenate_images(sig_image_collection)
print(f"The sig_image has dimensions : {sig_image.shape}")


#Saving these images via mimwrite from imageio
imageio.mimwrite(os.path.join(data_path, "ref_image" + ".tif"), ref_image)
imageio.mimwrite(os.path.join(data_path, "sig_image" + ".tif"), sig_image)

#*************************************************#
#Reading the respective saved images
image_r = sitk.ReadImage(os.path.join(data_path, "ref_image.tif"))
image_s = sitk.ReadImage(os.path.join(data_path, "sig_image.tif"))


def image_details(file):
    print("********Image Details**************")
    print("Size:", file.GetSize())
    print("PixelIDType:", file.GetPixelIDTypeAsString())
    print("Voxel Size:", file.GetSpacing())


def convert_to_8bit(file):
    print("********Checking Image Type********")
    print("PixelIDType:", file.GetPixelIDTypeAsString())
    if file.GetPixelID() != 1:
        file.SetPixelID = 1
        print("New PixelIDType:", file.GetPixelIDTypeAsString())
    #return plt.imread(file).astype(np.uint8)
    return file


def set_voxel_size(file):
    print("********Checking Voxel Size********")
    print("Voxel Size:", file.GetSpacing())
    file.SetSpacing([1.0, 1.0, 1.0])
    print("Voxel Size:", file.GetSpacing())


def enhance_contrast(file):
    """
Brightness and contrast can be adjusted using alpha (α) and beta (β), respectively.
NOTE: (α) --> contrast control (1.0-3.0);  (β) --> Brightness control (0-100).
The expression can be written as: g(i,j) = (α) * f(i,j) + (β).
OpenCV already implements this as cv2.convertScaleAbs(), just provide user defined alpha and beta values.
    :param file: alpha (α) and beta (β), file
    :return: contrast enhanced image
    """
    alpha = 1.5
    beta = 0
    CE_image = cv2.imread(file)
    CE_image = cv2.convertScaleAbs(file, alpha=alpha, beta=beta)
    return CE_image


#obtaining basic image details
image_details(image_r)
image_details(image_s)


#converting to 8bit image
convert_to_8bit(image_r)
convert_to_8bit(image_s)


#Setting Voxel Size
set_voxel_size(image_r)
set_voxel_size(image_s)

#Contrast Enhancement
#enhance_contrast(np.float32(image_r))
#enhance_contrast(np.float32(image_s))

end = time.time()
t = end - start
print(t)


#converting to 8bit image
#convert_to_8bit(image_r)
#convert_to_8bit(image_s)

#Saving CE images
#plt.imsave(os.path.join(data_path, "CE_imager" + ".tif"), image_r)