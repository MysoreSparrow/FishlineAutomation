# Author: Keshava Prasad Gubbi
# For any questions: Contact keshav.prasad.gubbi@gmail.com

# Script to perform Lines- transformation Image processing on both nrrd and tiff files
# after downloadng from cluster


# DONE: Check which file is it and then pass it onto respective read function that processes it.
# DONE: Basic functions ---> convert to 8 bit, enhance contrast, save file into respective format.
# DONE: Preserve and rewrite the processed nrrd files with rest of the metadata same as the original file.
# DONE: Rewrite the file also as a tiff file with same metadata.

import os
import nrrd
import cv2 as cv
import tifffile as tiff

inpath = r'C:/Users/keshavgubbi/Desktop/nifti/transform_individual'
outpath = inpath + '/Output/'


def read_nrrd_file(f):
    nrrd_image, head = nrrd.read(os.path.join(inpath, f), index_order='F')
    width, height, depth = nrrd_image.shape
    print(f' The image {file} has dimensions :({width}, {height}) with {depth} '
          f'slices')
    datatype = head['type']
    voxel_x, voxel_y = head['space directions'][0][0], head['space directions'][1][1]
    voxel_size_list = [voxel_x, voxel_y]
    # print(voxel_size_list)
    print(f'The Image has dtype: {datatype}. Converting into a int8 (8 bit) image!')
    ce_image = contrast_enhancement(nrrd_image)
    return ce_image.astype('uint8'), head, voxel_size_list


def image_to_nrrd(image, header):
    return nrrd.write(os.path.join(outpath, f"{name}.nrrd"), image, header=header)


def image_to_tiff(image):
    print(f'Creating file {name}.tif')
    return tiff.imwrite(os.path.join(outpath, f"{name}.tif"), image,
                        metadata={'spacing': ['1./VoxelSizeList[0]', '1./VoxelSizeList[0]', '1'], 'unit': 'um',
                                  'axes ': 'ZYX', 'imagej': 'True'})


def contrast_enhancement(f):
    alpha = 3.0  # Contrast control (1.0-3.0) but 3 is required for my purposes here
    beta = 1  # Brightness control (0-100). Not to be added beyond 5, to not hamper the signal with salt and pepper
    # noise.
    contrast_enhanced_image = cv.convertScaleAbs(f, alpha=alpha, beta=beta)
    return contrast_enhanced_image


for file in os.listdir(inpath):
    if file.endswith('.nrrd'):
        print(f'Working with Image: {file}')
        # Read the nrrd file and convert it into a 8-bit numpy array after contrast enhancement
        nrrd_image_array, Header, VoxelSizeList = read_nrrd_file(file)
        # print(Header)
        name, ext = file.split('.', 1)
        processed_nrrd_image = image_to_nrrd(nrrd_image_array, Header)
        processed_tiff_image = image_to_tiff(nrrd_image_array.transpose(2, 1, 0))
        print(f'####End of processing {file}!##################')
