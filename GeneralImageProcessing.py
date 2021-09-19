# Author: Keshava Prasad Gubbi
# For any questions: Contact keshav.prasad.gubbi@gmail.com

# Script to perform General Image processing on General Image processing on both nrrd and tiff files after downloadng
# from cluster


# DONE: Check which file is it and then pass it onto respective read function that processes it.
# DONE: Basic functions ---> convert to 8 bit, enhance contrast, save file into respective format.
# TODO: Need original reformatted files and most likely an alternative way to enhance contrast for these files


import os
import nrrd
import cv2 as cv

outpath = r'C:/Users/keshavgubbi/Desktop/nifti/reformatted'
inpath = r'C:/Users/keshavgubbi/Desktop/LinesReg/210719_rspo1_GCaMP6s_new/reformatted/'


def read_nrrd_file(f):
    nrrd_image, head = nrrd.read(os.path.join(inpath, f), index_order='F')
    width, height, depth = nrrd_image.shape
    print(f'Working with Image: {file} with dimensions :({width}, {height}) and has {depth} '
          f'slices')
    print(f'Converting the nrrd file into a int8 (8 bit) numpy array!')
    ce_image = contrast_enhancement(nrrd_image)
    return ce_image.astype('uint8'), head


def image_to_nrrd(image):
    # Header = {'units': ['m', 'm', 'm'], 'space units': ['microns', 'microns', 'microns']} #'spacings': [voxel_width,
    # voxel_height, 1e-6]}
    return nrrd.write(os.path.join(outpath, f"{name}.nrrd"), image)


def contrast_enhancement(f):
    alpha = 3.0  # Contrast control (1.0-3.0) but 5 is required for my purposes here
    beta = 1  # Brightness control (0-100). Not to be added beyond 5, to not hamper the signal with salt and peper
    # noise.
    # contrast_enhanced_image = exposure.adjust_log(f, 50)
    contrast_enhanced_image = cv.convertScaleAbs(f, alpha=alpha, beta=beta)
    return contrast_enhanced_image


for file in os.listdir(inpath):
    if file.endswith('.nrrd'):
        print(file)
        # Read the nrrd file and convert it into a 8-bit numpy array after contrast enhancement
        nrrd_image_array, header = read_nrrd_file(file)
        name, ext = file.split('.', 1)
        print(name)
        processed_image = image_to_nrrd(nrrd_image_array)
        print(f'####End of processing {file}!##################')