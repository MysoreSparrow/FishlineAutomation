import os
import re
import nrrd
import tifffile as tiff
import numpy as np
from aicspylibczi import CziFile
from pathlib import Path
import matplotlib.pyplot as plt

c_path = r'C:\Users\joe\Downloads\czidata'
saving_path = r'./export/'

# TODO: Read CZI file from a given folder.
# TODO: Read metadata for each file and based on channel number split into separate channels.
# TODO: Save each channel as a separate tif/tiff file with correct channel name.


for file in os.listdir(c_path):
    czi = CziFile(os.path.join(c_path, file))
    print(czi.dims)  # get which dimensions are present
    print(czi.dims_shape())  # shape of the data over those dims
    l = [md[0] for md in czi.read_subblock_metadata(B=0, S=0, C=0, T=0)]
    # print(l)

    for ch_num in range(*czi.dims_shape()[0]['C']):
        print(ch_num)
        imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0)
        # this will give a 3d array when squeezed, ZYX

        # if you wanted to iterate over each Z:
        # for z_plane in range(*czi.dims_shape()[0]['Z']):
        #     print(z_plane)
        #     imgarray, shp = czi.read_image(B=0, S=0, C=ch_num, T=0, Z=z_plane)
        #     print(imgarray.shape)

    for index in range(len(l)):
        # for z in _z
        # print(l[index]['C'])## Gives the actual value of channel number here.
        print(l[index])  # Gives all of the dict values
        if l[index]['C'] == 0:
            imgarray, shp = czi.read_image(B=0, S=0, C=0, T=0, Z=0)
            print('image array shape', imgarray.shape)
            # (1, 1, 1, 370, 1521, 801)
            a1 = np.transpose(np.squeeze(imgarray))
            print('transpose shape:', a1.shape)
            # (801, 1521, 370)
            # Q: Why does the third dimension still have 370..isnt this is each slice?
            a2 = np.stack(a1, axis=0)
            print(a2.shape)
            print('############################')

            # a1 = a1.transpose((3,2,1,0))
            # tiff.imwrite(os.path.join(saving_path, file), a1)
            # a1_reshape = a1_transpose.reshape(np.prod(a1.shape[2:]), -1)
            # print('reshape shape:', a1_reshape.shape)

            # .reshape(np.prod(a1.shape[:2]), -1)
            # a2 = a1
            # print(a2.shape)

            # tiff.imwrite(os.path.join(c_path, file), a1)
            # with tiff.TiffWriter(os.path.join(line_path, f"{item}"), imagej=True) as tifw:
            #    tifw.write(rotated_image.astype('uint8'), resolution=(1 / V_x, 1 / V_y),
            #               metadata={'spacing': 1.0, 'unit': 'um', 'axes': 'ZYX'})

            # for key in l[index]:
            #    print(l[index][key])
            # B, C, T, Z = l[index][key]

            # img, shp = czi.read_image(B=0, S=0)
            # print(img.shape)
            # print(shp)
