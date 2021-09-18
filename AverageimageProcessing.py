## Script to perform Image procesing on averaged Image files after downloadng from cluster
# The folder for storing these nifti-zipped (.nii.gz) files is to store them fr easy access
# DONE: import nifti file
# DONE: Read the nifti file and also convert it to a np array
# DONE: convert to 8 bit, perform contrast enhancement
# DONE: correct the name and also save it as an nrrd file

import nibabel as nib
import os
import nrrd
import re
filepath = r'C:/Users/keshavgubbi/Desktop/nifti/'


def read_nifti_file(f):
    averaged_image = nib.load(os.path.join(filepath, f))
    print(averaged_image.shape)
    width, height, depth = averaged_image.shape
    header = averaged_image.header
    datatype = header.get_data_dtype()
    print(f'Working with Image: {file} with dtype:{datatype}, with dimensions :({width}, {height}) and has {depth} '
          f'slices')
    print(f'Converting the nifti file from {datatype} into a int8(8 bit) numpy array!')
    avg_image_array = averaged_image.get_fdata()
    print(avg_image_array.shape)
    return avg_image_array.astype('uint8')


def image_to_nrrd(image, img_name):
    # Header = {'units': ['m', 'm', 'm'], 'spacings': [voxel_width, voxel_height, 1e-6]}
    print(f'Creating nrrd image with name : {img_name}.nrrd')
    return nrrd.write(os.path.join(filepath, f"{img_name}.nrrd"), image)


tag = input('Enter reference channel name:')
signal = input('Enter signal channel name:')
ref_image_name = f'{signal}_AVG_{tag}'
sig_image_name = f'{signal}_AVG_GFP'
# Ref_channel = True


for file in os.listdir(filepath):
    if file.endswith('.nii.gz'):
        # Read the nifti file and convert it into a 8-bit numpy array
        averaged_image_array = read_nifti_file(file)

        # Based on name, check if the respective file in Reference/Signal and then write it into .nrrd format into
        # same folder
        if re.search("template0", str(file)):  # all T_template0.nii.gz files are always the reference channel files
            print(f'Creating Reference channel image: {ref_image_name}.nrrd')
            Reference_nrrd_image = image_to_nrrd(averaged_image_array, ref_image_name)
        elif re.search("template1", str(file)):  # all T_template1.nii.gz files are always the signal channel files
            print(f'Creating Signal channel image: {sig_image_name}.nrrd')
            Signal_image_name = image_to_nrrd(averaged_image_array, sig_image_name)
        else:
            print('Unknown channel in the image. Check total number of channels in the image!')

