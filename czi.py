import os
import tifffile as tiff
import numpy as np
from aicspylibczi import CziFile
import time

c_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1/data/czidata/'
original_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1/data/czidata/original/'


# DONE: Read CZI file from a given folder.
# DONE: Read metadata for each file and based on channel number split into separate channels.
# TODO: Save each channel as a separate tif/tiff file with correct channel name without permission errors


def czi_splitchannel(f):
    czi = CziFile(f)
    #print(czi.dims)  # get which dimensions are present
    #print(czi.dims_shape())  # shape of the data over those dims
    # with tiff.TiffFile(czi, mode='w+b') as czi:
    for ch_num in range(*czi.dims_shape()[0]['C']):
        print('ch_num:',ch_num)
        imgarray, shp1 = czi.read_image(B=0, S=0, C=ch_num, T=0)
        # this will give a 3d array when squeezed, ZYX
        #print(imgarray.shape)
        image_list = []
        # if you wanted to iterate over each Z:
        for z_plane in range(*czi.dims_shape()[0]['Z']):
            #print('z_plane:',z_plane)
            imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)
            # print(imgarray.shape)
            image = np.squeeze(imgarray)
            # print(image.shape)
            image_list.append(image)
            # print(len(image_list))
            channel_image_stack = np.stack(image_list)
            print(channel_image_stack.shape)
            return channel_image_stack.astype('uint8')


if not os.path.exists(original_path):
    print(f'Creating {original_path}')
    os.makedirs(original_path, exist_ok=True)

#start = time.time()
for file in os.listdir(c_path):
    if file.endswith('.czi'):
        print(file)
        name, ext = file.split('.')
        #print(name, ext)
        #czi_split_image = czi_splitchannel(os.path.join(c_path, file))

        czi = CziFile(os.path.join(c_path, file))
        for ch_num in range(*czi.dims_shape()[0]['C']):
            print('ch_num:', ch_num)
            imgarray, shp1 = czi.read_image(B=0, S=0, C=ch_num, T=0)
            # this will give a 3d array when squeezed, ZYX
            # print(imgarray.shape)
            image_list = []
            # if you wanted to iterate over each Z:
            for z_plane in range(*czi.dims_shape()[0]['Z']):
                # print('z_plane:',z_plane)
                imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)
                # print(imgarray.shape)
                image = np.squeeze(imgarray)
                # print(image.shape)
                image_list.append(image)
                # print(len(image_list))
                channel_image_stack = np.stack(image_list)
                print(channel_image_stack.shape)

                #tiff.imwrite(os.path.join(original_path, f'{name}_ch{ch_num}.tif'), channel_image_stack)
                # with tiff.TiffWriter(os.path.join(original_path, f'{name}_ch{ch_num}.tif')) as tifw:
                #     tifw.write(czi_split_image.astype('uint8'), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})
                with tiff.TiffWriter(os.path.join(original_path, f'{name}_ch{ch_num}.tif')) as tifw:
                    tifw.save(channel_image_stack.astype('uint8'), metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})

#, imagej=True, bigtiff=True
# end = time.time()
# print('total Execution Time:', end - start, 's')
