## Script to perform Image procesing on averaged Image files after downloadng from cluster
# The folder for storing these nifti-zipped (.nii.gz) files is to store them fr easy access
# DONE: import nifti file
# DONE: Read the nifti file and also convert it to a np array
# DONE: convert to 8 bit, perform contrast enhancement
# DONE: correct the name and also save it as an nrrd file

import nibabel as nib
import os
import nrrd

filepath = r'C:/Users/keshavgubbi/Desktop/nifti/'


def read_nifti_file(f):
    averaged_image = nib.load(os.path.join(filepath, f))
    print(averaged_image.shape)
    width, height, depth = averaged_image.shape
    header = averaged_image.header
    datatype = header.get_data_dtype()
    print(f'Working with Image: {file} with dtype:{datatype}, with dimensions :({width}, {height}) and has {depth} '
          f'slices')
    print('Converting the nifti file into a 8 bit numpy array!')
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
Ref_channel = True


for file in os.listdir(filepath):
    if file.endswith('.nii.gz'):
        pass
        averaged_image_array = read_nifti_file(file)
        Ref_channel = input(f'Is the {file} Reference Channel?')
        #Enter True or False for the question.

        if Ref_channel is True:
            print(f'Creating image: {ref_image_name}.nrrd')
            Reference_nrrd_image = image_to_nrrd(averaged_image_array, ref_image_name)
        elif Ref_channel is False:
            print(f'Creating image: {sig_image_name}.nrrd')
            Signal_image_name = image_to_nrrd(averaged_image_array, sig_image_name)
        else:
            print('Check total number of channels in the image!')

