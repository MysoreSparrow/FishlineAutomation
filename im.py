import os
import sys
import re
import numpy as np
import skimage.io as io
import glob

#path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/1/'
outpath = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/'
path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/d/'
#tiffiles = os.listdir(path) # this reads the image name as string type.

#print(tiffiles[0])

#ref_image_list = [tiffiles[0] for tiffiles[0] in tiffiles if re.search("_ch0{2}", tiffiles[0])]
#sig_image_list = [tiffiles[0] for tiffiles[0] in tiffiles if not re.search("_ch0{2}", tiffiles[0])]


#combined_image_list = \
ref_image_list = sig_image_list = combined_image_list = []
for img in glob.glob(os.path.join(path, "*.tif")):
    #print(img)
    image_name = str(img)# this is the name of the image file of type string
    image = io.imread(img)# this is reading the actual image itself
    print("##################################")
    print("name of the file", img)
    #print(image)
    # Selection/Splitting of channels
    #ref_image_list = [img for img in os.listdir(path) if re.search("_ch0{2}", img)]
    #sig_image_list = [img for img in os.listdir(path) if re.search("_ch01{1}", img)]
#print(ref_image_list)
#print(sig_image_list)

    if re.search("_ch0{2}", str(image_name)):
        print(f"Adding {image_name} to ref_image_list")
        ref_image_list.append(image)
        #r1.append(image_name)
    elif re.search("_ch01{1}", str(image_name)):
        print(f"Adding {image_name} to sig_image_list")
        sig_image_list.append(image)
        #s1.append(image_name)
    else:
        print("cant recognize")

#print(len(ref_image_list))
    #print("In R1", r1)
print("ref_image_list", ref_image_list)
print("sig_image_list", sig_image_list)
#print("In S1", s1)

# why is if condition not working that for each iteration same
# image is getting added to both ref_image_list and sig_image_list?

    #combined_image_list.append([img, image])
    #combined_image_list = [[image_name, image]]

    #print(combined_image_list)
    #print(combined_image_list[0])# this will give the img or names of files
    #print(combined_image_list[1]) #gives the values of the image


"""
#stack_tiff_image = io.MultiImage(tiff_image)
combined_image = io.imread_collection(combined_image_list)
#print(combined_image)# is the stacked image of both channels combined
#io.imsave(os.path.join(outpath, combined_image)) #needs to be fixed
# Selection/Splitting of channels
#ref_image_list = [img for img in os.listdir(path) if re.search("_ch0{2}", img)]
#sig_image_list = [img for img in os.listdir(path) if re.search("_ch01{1}", img)]


# check for the item in tiff_image to be also present in ref_image_list.
#if yes, then add into reference_image.
# this probably just adds strings(names)
#reference_image = io.imread_collection(ref_image_list)
#signal_image = io.imread_collection(sig_image_list)

#print(reference_image)
#print(signal_image)

#for frame in stack_tiff_image:
#    print(frame)

#reference_image = io.MultiImage(ref_image_list)
#signal_image = io.MultiImage(sig_image_list)

print(len(combined_image_list))
print(len(ref_image_list))
print(ref_image_list)
print(len(sig_image_list))
print(sig_image_list)
"""
