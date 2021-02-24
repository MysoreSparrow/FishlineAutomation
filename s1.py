#############################################################
# * Image Processing Script to process fish lines @ Baier Lab
# Author: Keshav Prasad Gubbi

#DONE: Read the image as a series of slices for all formats : .czi, .nrrd, .tif, .svs and display all details
#DONE: Split channels and save each f independently.
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
from skimage import io, img_as_ubyte, util, exposure, img_as_float
#import matplotlib.pyplot as plt
import imageio
import cv2
import time
import numpy as np
from medpy.io import load
import SimpleITK as sitk
start = time.time()
source_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/'
dest_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/ref'
dest_path1 = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/sig'
data_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/'
CE_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/2/CE'


def image_details(f):
    print("********Image Details**************")
    img = io.imread(f)
    print(img.dtype)
    print("Shape:", img.shape)


def convert_to_8bit(f):
    print("********Checking Image Type********")
    img = io.imread(f)
    img_as_ubyte(img)
    print(img.dtype)
    return img


def set_voxel_size(f):
    print("********Fixing Voxel Size********")
    image_data, image_header = load(f)
    print(image_header.get_voxel_spacing())
    print(image_header.get_offset())
    #image_header.set_voxel_spacing([1.0, 1.0])
    #print(image_header.get_voxel_spacing())

    image = sitk.ReadImage(f)
    print(image.GetSpacing())

    return f


def ce(f):
    i = img_as_float(io.imread(f)).astype(np.float64)
    gamma_corrected = exposure.adjust_gamma(i, gamma=0.4, gain=1)
    sigmoid_corrected = exposure.adjust_sigmoid(i)
    log_corrected = exposure.adjust_log(i)

    return gamma_corrected

def enhance_contrast(f):
    """
Brightness and contrast can be adjusted using alpha (α) and beta (β), respectively.
NOTE: (α) --> contrast control (1.0-3.0);  (β) --> Brightness control (0-100).
The expression can be written as: g(i,j) = (α) * f(i,j) + (β).
OpenCV already implements this as cv2.convertScaleAbs(), just provide user defined alpha and beta values.
    :param f: alpha (α) and beta (β), f
    :return: contrast enhanced image
    """
    print(f"Enhancing contrast for {f}:")
    alpha = 1.5
    beta = 50
    im = cv2.imread(f, cv2.COLOR_BGR2GRAY)
    ce_image = cv2.convertScaleAbs(im, alpha=alpha, beta=beta)
    print("ce image shape:", ce_image.shape)
    # converting array to image object
    #ce_image = Image.fromarray(ce_image)
    return ce_image


#Check if each f belongs to Ch00 or Ch01 and split Channels( move files to respective folders)
ref_counter = sig_counter = 0
for file in os.listdir(source_path):
    if file.endswith(".tif"):
        print(file)
        image_details(os.path.join(source_path, file))
        convert_to_8bit(os.path.join(source_path, file))
        #set_voxel_size(os.path.join(source_path, file))
        ce(os.path.join(source_path, file))
        if re.search("_ch0{2}", str(file)):
            ref_counter += 1
            #print(f"ref_counter= {ref_counter}")
            #print("ref f:", f)
            shutil.copy(f"{source_path}/{file}", dest_path)
        elif re.search("_ch01{1}", str(file)):
            sig_counter += 1
            #print(f"sig_counter = {sig_counter}")
            #print(f"sig f:{f}")
            shutil.copy(f"{source_path}/{file}", dest_path1)
        else:
            print("Its a Folder. Unwanted/Unrecognized f format.")

#TODO: iterate through all files in data_path, apply all 3 functions to it and save it there itself
# and  then stacked together.


for item in os.listdir(dest_path):
    if item.endswith(".tif"):
        pass
        #print("FILENAME:", os.path.join(dest_path, item))
        # Contrast Enhancement (CE)
        #image = enhance_contrast(os.path.join(dest_path, item))
        #Saving the Ce images in a separate folder for sanity check
        #print("Saving f:", item)
        #plt.imsave(os.path.join(dest_path, f"{item}.tiff"), image, cmap="gray")


for item in os.listdir(dest_path):
    if item.endswith(".tif"):
        print("#*************************************************#")
        print("FILENAME:", os.path.join(dest_path, item))

        # Getting image Details
        image_details(os.path.join(dest_path, item))
        # converting to 8bit image
        #image = convert_to_8bit(image)
        # Setting Voxel Size
        #image = set_voxel_size(image)
        #plt.imsave(os.path.join(dest_path, f"{item}.tiff"), image, cmap="gray")
        print("#*************************************************#")

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


end = time.time()
print(end - start)
