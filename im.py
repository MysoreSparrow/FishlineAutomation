import os
import re
import skimage.io as io
import glob
import matplotlib.pyplot as plt
import numpy as np
path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/1/'
outpath = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/'
#path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/d/'
#tiffiles = os.listdir(path) # this reads the image name as string type.

#print(tiffiles[0])

#ref_image_list = [tiffiles[0] for tiffiles[0] in tiffiles if re.search("_ch0{2}", tiffiles[0])]
#sig_image_list = [tiffiles[0] for tiffiles[0] in tiffiles if not re.search("_ch0{2}", tiffiles[0])]


ref_counter = sig_counter = 0
ref_image_list = sig_image_list = combined_image_list = []
for img in glob.glob(os.path.join(path, "*.tif")):
    #print(img)
    image_name = str(img)# this is the name of the image file of type string
    image = io.imread(img)# this is reading the actual image itself
    print("##################################")
    print("name of the file", img)

    if re.search("_ch0{2}", str(image_name)):
        ref_counter += 1
        print(f" ref_counter= {ref_counter}.Adding {image_name} to ref_image_list")
        #converting to arrays
        ref_image_array = np.array(image)
        ref_image_list.append(ref_image_array)
        #saving the image
        refpath = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22' \
                  '/1/ref_image_dir/'
        if not os.path.exists(refpath):
            os.makedirs(refpath)
        for k in range(len(ref_image_list)):
            plt.imsave(os.path.join(refpath, str(image_name)+".tiff"), ref_image_list[k], cmap='gray')

    elif re.search("_ch01{1}", str(image_name)):
        sig_counter += 1
        print(f"sig_counter= {sig_counter}.Adding {image_name} to sig_image_list")
        # converting to arrays
        sig_image_array = np.array(image)
        sig_image_list.append(sig_image_array)
        #saving
        sigpath = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22' \
                  '/1/sig_image_dir/'
        if not os.path.exists(sigpath):
            os.makedirs(sigpath)
        for j in range(len(sig_image_list)):
            plt.imsave(os.path.join(sigpath, str(image_name)+".tiff"), sig_image_list[j], cmap='gray')

    else:
        print("cant recognize")

#TODO: create a folder for saving the respective images into separate folders
#TODO: save the respective images into the folders
#TODO: Read the images from each directory using pims
#TODO: or just load an image sequence with the regex expression for loading the image


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
#print(image)
    # Selection/Splitting of channels
    #ref_image_list = [img for img in os.listdir(path) if re.search("_ch0{2}", img)]
    #sig_image_list = [img for img in os.listdir(path) if re.search("_ch01{1}", img)]
#print(ref_image_list)
#print(sig_image_list)

# print("ref_image_list", ref_image_list)
# print("sig_image_list", sig_image_list)
# print(len(ref_image_list))
# print(len(sig_image_list))
# print("ref_image_list", ref_image_list)