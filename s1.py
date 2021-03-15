#############################################################
# * Image Processing Script to process fish lines @ Baier Lab *
# Author: Keshav Prasad Gubbi

# DONE: Read the image as a series of slices for all formats : .czi, .nrrd, .tif, .svs and display all details
# DONE: Split channels and save each f independently.
# DONE: create a folder for saving the respective images into separate folders
# DONE: save the respective images into the folders
# DONE: Read the images from each directory using pims
# DONE: or just load an image sequence with the regex expression for loading the image
# DONE: check voxel depth and set voxel depth to 1 while retaining the other two numbers to be the same.
# DONE: check Image type or PixelIDType and set it to 8 bit integer type
# DONE: Enhance Contrast of the image
# DONE: Save Image after processing
# DONE: Rotate image
# DONE: Save after processing as both .nrrd and .tiff in respective folders along with original


import os
import re
import shutil
import time
import SimpleITK as sitk
import tifffile as tiff
from skimage import io, exposure
import numpy as np
from scipy import ndimage
import nrrd

start = time.time()
source_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/1/'
dest_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/1/ref'
dest_path1 = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/1/sig'
data_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/'
line_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/'


def image_details(f):
    print("********Image Details**************")
    img = io.imread(f)
    print(type(img))
    print('Dtype:', img.dtype)
    print("Shape:", img.shape)
    return img


def convert_to_8bit(f):
    print("********Checking Image Type********")
    # img = io.imread(f)
    dtype = f.dtype
    print(dtype)
    if dtype != 'uint8':
        f.astype('uint8', copy=False)
        print(dtype)
    return f.astype('uint8')


def read_voxel_size(f):
    # print("********Reading Voxel Size********")
    im = sitk.ReadImage(f)
    width, height = im.GetSpacing()
    # print('Current voxel size:', width, height)
    return width, height


def ce(f):
    # i = img_as_float(io.imread(f)).astype(np.float64)
    logarithmic_corrected = exposure.adjust_log(f, 1)
    return logarithmic_corrected


def _rotate(src, angle):
    # angle in degrees
    rotated_matrix = ndimage.rotate(src, angle=angle, reshape=False)
    return rotated_matrix


def tiff_unstackAndrestack(f):
    '''
    :param f: tiff file
    :return: rotated_image_stack
    #1. Iterate through each file as a tiff file.
    #2. split into individual pages //Unstacking
    #3. rotate each page and save the rotated_page into a new list
    #4. restack each array from the list
    '''
    with tiff.TiffFile(f, mode='r+b') as tif:
        print(f' Processing {tif} for rotation...')
        for page in tif.pages:
            rotated_page = _rotate(page.asarray(), theta)
            rotated_page_list.append(rotated_page)
            rotated_image_stack = np.stack(rotated_page_list)
    return rotated_image_stack.astype('uint8')


def split_and_rename(f):
    filename, exte = f.split('.')
    _first, _last = filename.split('_', 1)
    #print(_first, _last, ext)
    return _first


line_name = input("enter line_name:")
tag_name = input("Enter tag name or name of the stain used:")
# Check if each f belongs to Ch00 or Ch01 and split Channels( move files to respective folders)
ref_counter = sig_counter = V_x = V_y = 0
print("#*********************Iterating in Source path**************************#")
for file in os.listdir(source_path):
    if file.endswith(".tif"):
        # print(file)
        # Read Voxel_x (V_x), Voxel_y (V_y) from individual slices, which shall be used later for setting voxel depth
        V_x, V_y = read_voxel_size(os.path.join(source_path, file))
        # print(V_x, V_y)
        if re.search("_ch0{2}", str(file)):
            ref_counter += 1
            # print(f"ref_counter= {ref_counter}")
            # print("ref f:", f)
            shutil.copy(f"{source_path}/{file}", dest_path)
        elif re.search("_ch01{1}", str(file)):
            sig_counter += 1
            # print(f"sig_counter = {sig_counter}")
            # print(f"sig f:{f}")
            shutil.copy(f"{source_path}/{file}", dest_path1)
        else:
            print("Its a Folder. Unwanted/Unrecognized file format.")

# Load images sequentially as per respective channels using skimage imageCollection
ref_image_collection = io.ImageCollection(dest_path + '/*.tif')
print(f'The ref_image_collection details: {len(ref_image_collection)} frames')
sig_image_collection = io.ImageCollection(dest_path1 + '/*.tif')
print(f'The sig_image_collection details: {len(sig_image_collection)} frames')


# Convert these image collection object (sequential images) into a single image
ref_image_stack = io.concatenate_images(ref_image_collection)
tiff.imwrite(os.path.join(data_path, f'{line_name}_refstack.tif'), ref_image_stack)

sig_image_stack = io.concatenate_images(sig_image_collection)
tiff.imwrite(os.path.join(data_path, f'{line_name}_sigstack.tif'), sig_image_stack)


for item in os.listdir(data_path):
    if item.endswith(".tif"):

        # ****Contrast Enhancement, 8bit conversion, fixing voxel Depth******#
        g = tiff.imread(os.path.join(data_path, item))
        print(f"The file {item} has dimensions : {g.shape} and is of type: {g.dtype} ")
        CE_image = ce(g)
        print(f'Creating file {item} ...')
        with tiff.TiffWriter(os.path.join(data_path, item), imagej=True) as tifw:
            tifw.write(CE_image.astype('uint8'), resolution=(1/V_x, 1/V_y), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})

        #***********Rotation*********************************#
        print(f'Image stack to be rotated: {item}')
        theta = float(input('Enter the angle by which image to be rotated:'))
        rotated_page_list = []
        rotated_image = tiff_unstackAndrestack(os.path.join(line_path, item))
        print(f'Creating Rotated Image: rotated_{item}')
        with tiff.TiffWriter(os.path.join(line_path, f"{item}"), imagej=True) as tifw:
            tifw.write(rotated_image.astype('uint8'), resolution=(1/V_x, 1/V_y), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})
        #tiff.imwrite(os.path.join(line_path, f"{item}"), rotated_image)
        print('*********************************************************')


#**********Final Saving of Images to respective folders********
print('Final Saving of Images to respective folders!')
processed_path = f'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/processed/'
processed_for_average_path = f'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22' \
                      f'/processed_for_average/'


if not os.path.exists(processed_path):
    print(f'Creating {processed_path}')
    os.makedirs(processed_path, exist_ok=True)

if not os.path.exists(processed_for_average_path):
    print(f'Creating {processed_for_average_path}')
    os.makedirs(processed_for_average_path, exist_ok=True)

for item in os.listdir(line_path):
    if item.endswith(".tif") and re.search("ref", str(item)):
        print(f'Image stack to be saved: {item}')
        # Read the data back from file
        readdata = tiff.imread(os.path.join(line_path, item))
        name = split_and_rename(item)
        nrrd.write(os.path.join(processed_path, f"{name}_{tag_name}.nrrd"), readdata,  index_order='C')
        #tiff.imwrite(os.path.join(processed_for_average_path, f"{name}_{tag_name}.tif"), readdata)
        with tiff.TiffWriter(os.path.join(processed_for_average_path, f"{name}_{tag_name}.tif"), imagej=True) as tifw:
            tifw.write(readdata.astype('uint8'), resolution=(1/V_x, 1/V_y), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})
    if item.endswith('.tif') and re.search("sig", str(item)):
        # Read the data back from file
        readdata = tiff.imread(os.path.join(line_path, item))
        name = split_and_rename(item)
        nrrd.write(os.path.join(processed_path, f"{name}_GFP.nrrd"), readdata, index_order='C')
        with tiff.TiffWriter(os.path.join(processed_for_average_path, f"{name}_GFP.tif"), imagej=True) as tifw:
            tifw.write(readdata.astype('uint8'), resolution=(1 / V_x, 1 / V_y), metadata={'spacing': 1.0,
                                                                                          'unit': 'um', 'axes': 'ZYX'})

end = time.time()
print('total Execution Time:', end - start, 's')

#with tiff.TiffWriter(os.path.join(data_path, item), imagej=True) as tifw:
#    tifw.write(CE_image.astype('uint8'), resolution=(1 / V_x, 1 / V_y), metadata={'spacing': 1.0, 'unit': 'um',
 #                                                                                 'axes': 'ZYX'})
