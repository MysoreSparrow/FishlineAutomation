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
from medpy.io import load
from skimage import io, exposure

start = time.time()
source_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/1/'
dest_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/1/ref'
dest_path1 = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/1/sig'
data_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/'


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


def set_voxel_depth(f):
    im = sitk.ReadImage(f)
    print('Current voxel size:', im.GetSpacing())
    print("********Fixing Voxel Size********")
    im.SetSpacing([V_x, V_y, 1.0 * 10 ** -6])
    # Need depth to be in microns. The basic units in sitk is set in (mm) by default.
    print('New voxel size:', im.GetSpacing())
    print(im.GetPixelIDTypeAsString())
    im = sitk.GetArrayFromImage(im)
    return im


def ce(f):
    # i = img_as_float(io.imread(f)).astype(np.float64)
    logarithmic_corrected = exposure.adjust_log(f, 1)
    return logarithmic_corrected


def set_VD1(f):
    image_data, image_header = load(f)
    print(image_data.shape, image_data.dtype, image_header)
    print('voxel spacing:', image_header.get_voxel_spacing())
    # image_header.set_voxel_spacing((V_x, V_y, 1.0 * 10 ** -6))
    # print('new voxel spacing:', image_header.get_voxel_spacing())
    return image_data, image_header


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
tiff.imwrite(os.path.join(data_path, 'ref_stack.tif'), ref_image_stack)

sig_image_stack = io.concatenate_images(sig_image_collection)
# print(f"The sig_image has dimensions : {sig_image_stack.shape}")
tiff.imwrite(os.path.join(data_path, 'sig_stack.tif'), sig_image_stack)


#***********Contrast Enhancement, 8bit conversion, fixing voxel Depth*********************************#
for item in os.listdir(data_path):
    if item.endswith(".tif"):
        g = tiff.imread(os.path.join(data_path, item))
        print(f"The file {item} has dimensions : {g.shape} and is of type: {g.dtype} ")
        CE_image = ce(g)
        print(f'Creating file {item} ...')
        with tiff.TiffWriter(os.path.join(data_path, item), imagej=True) as tifw:
            tifw.write(CE_image.astype('uint8'), resolution=(1/V_x, 1/V_y), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})
        print('*********************************************************')

end = time.time()
print('total Execution Time:', end - start, 's')
