import SimpleITK as sitk
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import nrrd

#TODO: Read the image as a series of slices.
#TODO: check voxel depth and set voxel depth to 1
#TODO: check Image type or PixelIDType and set it to 8 bit integer type
#TODO: Split channels and save each file independently.
#TODO: Rotate image
#TODO: Save after processing as both .nrrd and .tiff in respective folders along with original


sample_path = 'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/data/201126_bhlhe22/original/201126_bhlhe22/'
# *********************
line_name = input("enter line_name:")

def set_voxel_depth():
    pass



for filename in os.listdir(sample_path):
    if filename.endswith(".nrrd"): #or filename.endswith(".tif"):
        outpath = f'C:/Users/keshavgubbi/Desktop/ATLAS/S1-ImageProcessing/S1_Output/{line_name}/'
        if not os.path.exists(outpath):
            os.makedirs(outpath)

        print("**********************")
        print("File:", os.path.join(sample_path, filename))
        reader = sitk.ImageSeriesReader()
        image = sitk.ReadImage(os.path.join(sample_path, filename))
        # image_details(image)
        #w, h, d = image.GetSize()
        #for key in image.GetMetaDataKeys():
        #    print(f"\"{key}\":\"{image.GetMetaData(key)}\"")
        w, h, d = image.GetSize()
        print("Width:", w, "Height:", h, "Number of images:", d)
        PixelIDType = image.GetPixelIDTypeAsString()
        print("PixelIDType:", PixelIDType)
        voxel_depth = image.GetSpacing()
        print("Voxel Size:", voxel_depth)


















        #print("NumberOfComponentsPerPixel", image.GetNumberOfComponentsPerPixel())
        #data, header = nrrd.read(os.path.join(sample_path, filename))
        #print(data)
        #print(header)