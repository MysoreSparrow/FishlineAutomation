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
import imageio
import time
c_path = r"C:\Users\keshavgubbi\Desktop\LinesReg\new1020"
original_path = c_path + r'\original'
if not os.path.exists(original_path):
    print(f'Creating {original_path}')
    os.makedirs(original_path, exist_ok=True)

ref_ch_num = int(input('Enter Reference Channel Number:'))
start = time.time()

def czi_split(c):
    max_channels = range(*czi.dims_shape()[0]['C'])
    max_slices = range(*czi.dims_shape()[0]['Z'])
    for ch_num in max_channels:
        image_list = []
        for z_plane in max_slices:
            print('file:', file, ', ch_num:', ch_num, ', z_plane:', z_plane)
            imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)
            image_list.append(np.squeeze(imgarray))
            return ch_num, image_list

for file in os.listdir(c_path):
    if file.endswith('.czi'):
        print(file)
        name, ext = file.split('.')

        czi = CziFile(os.path.join(c_path, file))
        ch, image_stack = czi_split(czi)

        if ref_ch_num == ch:
            # with tiff.FileHandle(file, mode="rb") as fh:
            with tiff.TiffWriter(os.path.join(original_path, f'{name}_ref.tif'), imagej=True) as tifw:
                # print(f'Adding slice {z_plane} to {name}_ref.tif')
                tifw.write(np.stack(image_stack).astype('uint8'))
        else:
            # with tiff.FileHandle( file, mode="rb") as fh1:
            with tiff.TiffWriter(os.path.join(original_path, f'{name}_sig.tif'), imagej=True) as tifw:
                # print(f'Adding slice {z_plane} to {name}_sig.tif')
                tifw.write(np.stack(image_stack).astype('uint8') )

##################################################################################################
end = time.time()
t = end - start
print(f'Totally took {t}s')