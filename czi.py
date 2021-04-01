# * Image Processing Script to process fish lines @ Baier Lab *
# Author: Keshav Prasad Gubbi
# DONE: Read CZI file from a given folder.
# DONE: Read metadata for each file and based on channel number split into separate channels.
# DONE: Save each channel as a separate tif/tiff file with correct channel name without permission errors.
import os
import tifffile as tiff
import numpy as np
from aicspylibczi import CziFile
import time
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
        image_list = []
        #for ch_num, z_plane in zip(max_channels, max_slices):
        for ch_num in max_channels:
            for z_plane in max_slices:
                print('file:', file, 'ch_num:', ch_num, 'z_plane:', z_plane)
                imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)
                image = np.squeeze(imgarray)
                image_list.append(image)
                channel_image_stack = np.stack(image_list)

                if ref_ch_num == ch_num:
                    with tiff.TiffWriter(os.path.join(original_path, f'{name}_ref.tif')) as tifw:
                        tifw.write(channel_image_stack.astype('uint8'))
                else:
                    with tiff.TiffWriter(os.path.join(original_path, f'{name}_sig.tif')) as tifw:
                        tifw.write(channel_image_stack.astype('uint8'))