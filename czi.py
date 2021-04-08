# * Image Processing Script to process fish lines @ Baier Lab *
# Author: Keshav Prasad Gubbi
# DONE: Read CZI file from a given folder.
# DONE: Read metadata for each file and based on channel number split into separate channels.
# DONE: Save each channel as a separate tif/tiff file with correct channel name without permission errors.
import os
import tifffile as tiff
import numpy as np
from aicspylibczi import CziFile
import SimpleITK as sitk
from skimage import io, exposure
from scipy import ndimage
import nrrd
import glob

c_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1/data/czidata/'
original_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1/data/czidata/original/'
if not os.path.exists(original_path):
    print(f'Creating {original_path}')
    os.makedirs(original_path, exist_ok=True)

ref_ch_num = int(input('Enter Reference Channel Number:'))
#start = time.time()
for file in os.listdir(c_path):
    if file.endswith('.czi'):
        print(file)
        name, ext = file.split('.')

        czi = CziFile(os.path.join(c_path, file))
        max_channels = range(*czi.dims_shape()[0]['C'])
        max_slices = range(*czi.dims_shape()[0]['Z'])
        for ch_num in max_channels:
            image_list = []
            for z_plane in max_slices:
                print('file:', file, ', ch_num:', ch_num, ', z_plane:', z_plane)
                imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)
                image_list.append(np.squeeze(imgarray))

                if ref_ch_num == ch_num:
                    with tiff.TiffWriter(os.path.join(original_path, f'{name}_ref.tif')) as tifw:
                        print(f'Adding slice {z_plane} to {name}_ref.tif')
                        tifw.write(np.stack(image_list).astype('uint8'))
                else:
                    with tiff.TiffWriter(os.path.join(original_path, f'{name}_sig.tif')) as tifw:
                        print(f'Adding slice {z_plane} {name}_sig.tif')
                        tifw.write(np.stack(image_list).astype('uint8'))
##################################################################################################3

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


V_x, V_y = 0
for item in os.listdir(line_path):
    if item.endswith(".tif"):
        # print(file)
        # Read Voxel_x (V_x), Voxel_y (V_y) from individual slices, which shall be used later for setting voxel depth
        V_x, V_y = read_voxel_size(os.path.join(source_path, item))

        # ****Contrast Enhancement, 8bit conversion, fixing voxel Depth******#
        g = tiff.imread(os.path.join(line_path, item))
        print(f"The file {item} has dimensions : {g.shape} and is of type: {g.dtype} ")
        CE_image = ce(g)
        print(f'Creating file {item} ...')
        with tiff.TiffWriter(os.path.join(line_path, item), imagej=True) as tifw:
            tifw.write(CE_image.astype('uint8'), resolution=(1/V_x, 1/V_y), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})

        #***********Rotation*********************************#
        print(f'Image stack to be rotated: {item}')
        theta = float(input('Enter the angle by which image to be rotated:'))
        rotated_page_list = []
        rotated_image = tiff_unstackAndrestack(os.path.join(line_path, item))
        print(f'Creating Rotated Image: rotated_{item}')
        with tiff.TiffWriter(os.path.join(line_path, f"{item}"), imagej=True) as tifw:
            tifw.write(rotated_image.astype('uint8'), resolution=(1/V_x, 1/V_y), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})
        print('*********************************************************')


#**********Final Saving of Images to respective folders********
print('Final Saving of Images to respective folders!')
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
