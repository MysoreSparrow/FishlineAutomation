#TODO: Ask for input of angle from user input
#TODO: Rotate object correctly, without cropping the image or changing dimensions
#TODO: Save files in respective folders in both .nrrd and .tif format in correct name and location


import os
import time
import tifffile as tiff
import numpy as np
from scipy import ndimage

start = time.time()
data_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/'


# angle in degrees

def _r(src, angle):
    rotated_matrix = ndimage.rotate(src, angle=angle, reshape=False)
    #rotated_matrix = imutils.rotate_bound(src, angle=angle)
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
    with tiff.TiffFile(f) as tif:
        print(f' Processing file {tif}...')
        for page in tif.pages:
            rotated_page = _r(page.asarray(), theta)
            rotated_page_list.append(rotated_page)
        #rotated_image_stack = np.dstack(rotated_page_list)
        rotated_image_stack = np.stack(rotated_page_list)
    return rotated_image_stack.astype('uint8')


theta = float(input('Enter the angle by which image to be rotated:'))
for item in os.listdir(data_path):
    if item.endswith(".tif"):
        print(item)
        rotated_page_list = []
        rotated_image = tiff_unstackAndrestack(os.path.join(data_path, item))
        print(f'Creating Rotated Image: rotated_{item}')
        tiff.imwrite(os.path.join(data_path, f"rotated_{item}"), rotated_image)


#with SKIMAGE
#rotated_image = _rotate(image, theta)
#with IMUTILS
#rotated_image = imutils.rotate_bound(image, theta)
end = time.time()
print(end - start, 'secs')

#image = io.imread(os.path.join(data_path, item))
#rotated = ndimage.rotate(image, angle=theta, mode='nearest')
