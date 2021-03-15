#DONE: Ask for input of angle from user input
#DONE: Rotate object correctly, without cropping the image or changing dimensions
#TODO: Save files in respective folders in both .nrrd and .tif format in correct name and location


import os
import re
import time
import tifffile as tiff
import numpy as np
from scipy import ndimage
import nrrd
start = time.time()
line_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/'


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
        print(f' Processing file {tif}...')
        #tag_XR = tif.pages[0].tags['XResolution'].overwrite(tif, (V_x,V_y))
        #print(tag_XR)
        for page in tif.pages:
            rotated_page = _rotate(page.asarray(), theta)
            rotated_page_list.append(rotated_page)
            rotated_image_stack = np.stack(rotated_page_list)
    return rotated_image_stack.astype('uint8')


def _t(f):
    with tiff.TiffFile(f, mode='r+b') as tif:
        print(f' Processing file {tif}...')
        for page in tif.pages:
            tag = tif.pages[0].tags['ImageDescription']
            print(f'{tag.name}, {tag.value}')
        # tif_tags = {}
        # for tag in tif.pages[0].tags.values():
        #    name, value = tag.name, tag.value
        #    print(name, value)
        #    tif_tags[name] = value
        # print(tif_tags)
    return tif


line_name = input("enter line_name:")
for item in os.listdir(line_path):
    if item.endswith(".tif"):
        print(f'Image stack to be rotated: {item}')
        theta = float(input('Enter the angle by which image to be rotated:'))
        rotated_page_list = []
        rotated_image = tiff_unstackAndrestack(os.path.join(line_path, item))
        print(f'Creating Rotated Image: rotated_{item}')
        tiff.imwrite(os.path.join(line_path, f"{line_name}_rotated_{item}"), rotated_image)

        #file = _t(os.path.join(data_path, item))

#**********Final Saving of Images to respective folders********
line_name = input("enter line_name:")


print('Final Saving of Images to respective folders!')
processed_path = f'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/processed/'
processed_for_average_path = f'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22' \
                      f'/processed_for_average/'

tag_name = input("Enter tag name or name of the stain used:")
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
        print(readdata.shape, readdata.dtype)
        stackname = os.path.splitext(item)[0]
       #print(stackname)
        nrrd.write(os.path.join(processed_path, f"{stackname}_{tag_name}.nrrd"), readdata,  index_order='C')
    if item.endswith('.tif') and re.search("sig", str(item)):
        # Read the data back from file
        readdata = tiff.imread(os.path.join(line_path, item))
        print(readdata.shape, readdata.dtype)
        stackname = os.path.splitext(item)[0]
        #print(stackname)
        nrrd.write(os.path.join(processed_path, f"{stackname}_GFP.nrrd"), readdata, index_order='C')


end = time.time()
print(end - start, 'secs')
